import argparse
import fcntl
import io
import os
import pathlib
import struct
import sys
import termios
from typing import Callable, Iterable, TextIO

from PIL import Image

from .args import DitherMethod, parse_args
from .chars import PairCharset
from .img import (
    ImgData,
    ThresholdFunc,
    get_threshold_func,
    plot_brightness_and_threshold,
    sharpen,
    thr_local_avg_factory,
)
from .util import Debug
from .pxp import rasterize as _rasterize


def get_ioctl_windowsize(dev: TextIO) -> tuple[int, int, int, int]:
    fd = dev.fileno()
    return struct.unpack(
        'HHHH', fcntl.ioctl(
            fd, termios.TIOCGWINSZ,
            struct.pack('HHHH', 0, 0, 0, 0)
        )
    )


def _terminal_rcwh(dev: TextIO) -> tuple[int, int, int, int]:
    try:
        r, c, w, h = get_ioctl_windowsize(dev)
        assert w * h > 0, f'invalid dimensions: {w}×{h} ({c}cols{r}rows)'
        Debug.log(
            f'terminal size determined via ioctl for device {dev}'
        ).log(
            f'terminal size: {c}×{r} columns×rows'
        ).log(
            f'window size: {w}×{h} px'
        )
        return r, c, w, h
    except Exception as e:
        Debug.log(f'could not determine terminal dimensions: {e}')
    if 'r' not in locals() or r * c == 0:
        r, c = termios.tcgetwinsize(dev)
    if r * c > 0:
        Debug.log(
            'terminal size determined using termios.tcgetwinsize '
            f'for device {dev}'
        ).log(
            f'terminal size: {c}×{r} columns×rows'
        ).log(
            'window size made up based on terminal size'
        )
    return (r, c, c * 9, r * 19)


def terminal_rcwh(
    stdin: TextIO = sys.stdin, stdout: TextIO = sys.stdout,
    fallback_values: tuple[int, int, int, int] = (53, 53,  477, 1007),
) -> tuple[int, int, int, int]:
    if (TERM_RCWH := os.environ.get('TERM_RCWH')):
        values = TERM_RCWH.split('x')
        Debug.log(
            f'got fixed term size from TERM_RCWH env var: {"×".join(values)}'
        )
        if len(values) == 4:
            r, c, w, h = list(map(int, values))
        elif len(values) == 2:
            r, c = list(map(int, values))
            w, h = c * 9, r * 19
        else:
            msg = f'wrong number of values in TERM_RCWH: {values}'
            Debug.log(msg)
            raise ValueError(msg)
        return (r, c, w, h)
    for dev in (stdout, stdin):
        try:
            return _terminal_rcwh(dev)
        except Exception as e:
            Debug.log(f'getting terminal size failed for device {dev}: {e}')
    return fallback_values


def get_zoom_factor(
    image: Image.Image, zoom_factor: float,
    rcwh_func: Callable[
        [], tuple[int, int, int, int]
    ] = terminal_rcwh,
) -> float:
    if zoom_factor <= 0:
        r, c, w, h = rcwh_func()
        zoom_factor = w / image.width
    Debug.log(f'resize image to {zoom_factor*100:.1f}%')
    return zoom_factor


def load_image_file(filename: str) -> Image.Image:
    if filename != '-':
        Debug.log(f'input file: {filename}')
        return Image.open(pathlib.Path(filename)).copy()
    byteinput = sys.stdin.buffer.read()
    try:
        result = Image.open(
            filename := byteinput.decode('utf8').strip()
        ).copy()
        Debug.log(f'input file: {filename}')
        return result
    except Exception:
        ...
    return Image.open(io.BytesIO(byteinput)).copy()


def plot_image_histogram(
    image: Image.Image, options: argparse.Namespace,
    charset: PairCharset = 'blocks',
) -> int:
    if image.mode != 'L':
        image = image.convert('L')
    for line in plot_brightness_and_threshold(
        image, options, charset=charset,
    ):
        print(line)
    if options.debug:
        Debug.show(sys.stderr)
    return 0


def rasterize(
    image: Image.Image,
    zoom: float = 1,
    inverted: bool = False,
    crop_y: bool = False,
    edging: int = 0,
    dither: float = 0,
    dither_method: DitherMethod = DitherMethod.atkinson,
    adjust_brightness: float = 1,
    threshold_func: ThresholdFunc | None = None,
    interpolate: bool = True,
    rcwh_func: Callable[
        [], tuple[int, int, int, int]
    ] = terminal_rcwh,
) -> Iterable[str]:
    threshold = threshold_func or thr_local_avg_factory(image, 0)
    r, c, w, h = rcwh_func()
    image = sharpen(image, edging, w / c)
    if image.mode != 'L':
        image = image.convert('L')
    yield from _rasterize(
        ImgData(image), r, c, w, h,
        threshold=threshold,
        zoom=zoom,
        interpolate=interpolate,
        crop_y=crop_y,
        dither_method=dither_method,
        adjust_brightness=adjust_brightness,
        dither=dither,
        inverted=inverted,
    )


def main(
    argv: list[str] = sys.argv[1:],
    load_image_file_func: Callable[
        [str], Image.Image
    ] = load_image_file,
) -> int:
    options = parse_args(argv)
    if not options.output_overwrite and options.outputfile.exists():
        print(
            f'output file {options.outputfile} already exists! '
            'set option --force to overwrite.',
            file=sys.stderr
        )
        sys.exit(1)
    image = load_image_file_func(options.inputfile)
    Debug.log(f'image dimensions: {"×".join(map(str, image.size))}')
    if options.histogram:
        return plot_image_histogram(
            image, options,
            charset='blocks' if os.isatty(1) else 'ascii',
        )
    rows = list(rasterize(
        image,
        zoom=get_zoom_factor(image, options.zoom_factor),
        inverted=options.invert,
        interpolate=not options.disable_antialiasing,
        crop_y=options.crop_y,
        edging=options.sharpen,
        dither=options.error_preservation_factor,
        dither_method=options.dither_method,
        threshold_func=get_threshold_func(image, options),
        adjust_brightness=options.brightness / 100,
    ))
    options.outputfile.touch(
        mode=0o644, exist_ok=options.output_overwrite,
    )
    if options.debug:
        Debug.show(sys.stderr)
    with options.outputfile.open('w') as f:
        for row in rows:
            print(f'{row}', file=f)
    return 0


if __name__ == '__main__':
    main()
