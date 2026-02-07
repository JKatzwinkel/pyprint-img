import fcntl
import os
import pathlib
import struct
import sys
import termios
import unicodedata
from typing import Callable, Iterable, Literal, TextIO

from PIL import Image, ImageChops, ImageFilter

from .args import parse_args
from .p import (
    DITHER_ERROR_RECIPIENTS, ThresholdFunc, get_threshold_func,
    thr_local_avg_factory,
)
from .util import Debug


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


def char_name(matrix: list[bool], inverted: bool = False) -> str:
    '''
    >>> char_name([False, True, True, False])
    'BRAILLE PATTERN DOTS-23'

    >>> char_name([False, True, True, False], inverted=True)
    'BRAILLE PATTERN DOTS-14'

    >>> char_name([])
    'BRAILLE PATTERN BLANK'
    '''
    key = ''.join(
        f'{i+1}' for i, b in enumerate(matrix) if b != inverted
    )
    return f'BRAILLE PATTERN DOTS-{key}' if key else (
        'BRAILLE PATTERN BLANK'
    )


def sharpen(
    image: Image.Image, factor: int, blur_radius: float
) -> Image.Image:
    if factor < 1:
        return image
    smot = image.filter(ImageFilter.GaussianBlur(blur_radius))
    for chops, images in (
        (ImageChops.add, (image, smot)), (ImageChops.subtract, (smot, image))
    ):
        image = chops(
            image, ImageChops.subtract(*images).point(
                lambda p: p * factor
            )
        )
    Debug.log(f'edge emphasis by factor {factor}')
    return image


type DitherMethod = Literal['atkinson', 'floyd-steinberg']


def sample_func(
    image: Image.Image, sx: float, sy: float,
    interpolate: bool = True,
) -> Callable[[int, int], int]:

    def getpixel(px: int, py: int) -> int:
        pixelvalue = image.getpixel((px, py)) or 0
        assert isinstance(pixelvalue, int), f'{pixelvalue}'
        return pixelvalue

    def getvalues(px: float, py: float) -> tuple[int, int, int, int]:
        x1, y1 = int(px), int(py)
        V = [getpixel(x1, y1)] * 4
        if x1 + 1 < image.width:
            V[1] = getpixel(x1 + 1, y1)
            if y1 + 1 < image.height:
                V[3] = getpixel(x1 + 1, y1 + 1)
        if y1 + 1 < image.height:
            V[2] = getpixel(x1, y1 + 1)
        return (
            V[0], V[1],
            V[2], V[3],
        )

    def sample(x: int, y: int) -> int:
        px, py = sx * x, sy * y
        if px > image.width or py > image.height:
            return 0
        if not interpolate:
            return getpixel(int(px), int(py))
        v1, v2, v3, v4 = getvalues(px, py)
        dx = px - int(px)
        wx1 = v1 + (v2 - v1) * dx
        wx2 = v3 + (v4 - v3) * dx
        dy = py - int(py)
        result = wx1 + (wx2 - wx1) * dy
        return round(result)

    return sample


def rasterize(
    image: Image.Image,
    zoom: float = 1,
    inverted: bool = False,
    crop_y: bool = False,
    edging: int = 0,
    dither: float = 0,
    dither_method: DitherMethod = 'atkinson',
    adjust_brightness: float = 1,
    threshold_func: ThresholdFunc | None = None,
    interpolate: bool = True,
    rcwh_func: Callable[
        [], tuple[int, int, int, int]
    ] = terminal_rcwh,
) -> Iterable[str]:

    error_recipients = DITHER_ERROR_RECIPIENTS[dither_method]

    def dither_victims(x: int, y: int, error: float) -> Iterable[
        tuple[int, int, float]
    ]:
        for dx, dy, weight in error_recipients:
            if not 0 <= (rx := x + dx) < max_col * 2:
                continue
            if (ry := y + dy) >= max_row * 4:
                continue
            yield rx, ry, weight

    threshold = threshold_func or thr_local_avg_factory(image, 0)
    r, c, w, h = rcwh_func()
    cw, ch = w / c, h / r
    sx, sy = cw / zoom / 2, ch / zoom / 4
    Debug.log(
        f'xterm window dimensions: {w}×{h} pixels, {c}×{r} characters'
    ).log(
        f'character size in pixels: {cw:.2f}×{ch:.2f}'
    ).log(
        f'sample rate in pixels: {sx:.2f} horizontal, {sy:.2f} vertical'
    )
    image = sharpen(image.convert('L'), edging, cw)
    max_row = round(image.height * zoom / ch) if not crop_y else min(
        round(image.height * zoom / ch), r
    )
    max_col = min(round(image.width * zoom / cw), c)
    Debug.log(f'using {max_col} columns × {max_row} rows')
    sample = sample_func(image, sx, sy, interpolate=interpolate)
    grid: list[list[float]] = [
        [sample(x, y) for x in range(max_col * 2)]
        for y in range(max_row * 4)
    ]
    mono = []
    for y in range(max_row * 4):
        for x in range(max_col * 2):
            approx = (value := grid[y][x]) * adjust_brightness >= threshold(
                (sx * x, sy * y)
            )
            mono.append(approx)
            error = (value - (247 * approx)) * dither / 16
            for dx, dy, weight in dither_victims(x, y, error):
                grid[dy][dx] += error * weight
    for cy in range(max_row):
        row: list[str] = []
        for cx in range(max_col):
            registers = [
                mono[
                    max_col * 2 * (cy * 4 + dy) + cx * 2 + dx
                ]
                for dx, dy in (
                    (0, 0), (0, 1), (0, 2), (1, 0),
                    (1, 1), (1, 2), (0, 3), (1, 3),
                )
            ]
            row.append(
                unicodedata.lookup(char_name(registers, inverted=inverted))
            )
        yield ''.join(row)


def scale_image(
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
    if filename == '-':
        return Image.open(sys.stdin.buffer).copy()
    return Image.open(pathlib.Path(filename)).copy()


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
    rows = list(rasterize(
        image,
        zoom=scale_image(image, options.zoom_factor),
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
