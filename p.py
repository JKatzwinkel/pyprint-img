import argparse
import fcntl
import io
import pathlib
import struct
import sys
import termios
import textwrap
import unicodedata
from typing import Any, Callable, Iterable, Self

from PIL import Image, ImageChops, ImageFilter


class Debug:
    msgs: list[str] = []

    @classmethod
    def log(cls, msg: str) -> type[Self]:
        cls.msgs.append(msg)
        return cls

    @classmethod
    def show(cls, out: io.TextIOBase | Any) -> None:
        print('\n'.join(cls.msgs), file=out)


def terminal_rcwh() -> tuple[int, int, int, int]:
    try:
        return struct.unpack(
            'HHHH', fcntl.ioctl(
                0, termios.TIOCGWINSZ,
                struct.pack('HHHH', 0, 0, 0, 0)
            )
        )
    except Exception as e:
        Debug.log(f'could not determine terminal dimensions: {e}')
    return (44, 174, 1723, 911)


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


def percentile(histogram: list[int], percent: int = 50) -> int:
    '''
    >>> percentile([0, 3, 2, 1], 50)
    1

    >>> percentile([0, 3, 2, 1], 66)
    2
    '''
    target = sum(histogram) * percent / 100
    acc = 0
    for i, count in enumerate(histogram):
        if (acc := acc + count) >= target:
            break
    Debug.log(f'{percent}th percentile at brightness level {i}')
    return i


type ThresholdFunc = Callable[[tuple[float, float]], float]
type ThresholdFuncFactory = Callable[[Image.Image, int], ThresholdFunc]


def thr_percentile_factory(
    image: Image.Image, percent: int = 50,
) -> ThresholdFunc:
    threshold = percentile(image.convert('L').histogram(), percent)
    return lambda pixel: threshold


def thr_const_factory(
    image: Image.Image, threshold: int = 127,
) -> ThresholdFunc:
    return lambda pixel: threshold


def thr_btw_extr_factory(image: Image.Image, _: int | None) -> ThresholdFunc:
    threshold = sum(
        (extrema := image.convert('L').getextrema())  # type: ignore[arg-type]
    ) / 2
    Debug.log(f'min/max brightness {extrema} -> threshold={threshold}')
    return lambda pixel: threshold


def thr_median_factory(image: Image.Image, _: int | None) -> ThresholdFunc:
    return thr_percentile_factory(image, 50)


def thr_local_avg_factory(
    image: Image.Image, blur_radius: int = 0
) -> ThresholdFunc:
    def threshold(pixel: tuple[float, float]) -> int:
        assert isinstance(
            result := averaged.getpixel(pixel), int  # type: ignore[arg-type]
        )
        return result
    blur_radius = blur_radius or max(
        25, min(image.width, image.height) // 20
    )
    averaged = image.filter(
        ImageFilter.GaussianBlur(blur_radius)
    ).convert('L')
    Debug.log(f'gaussian blur radius for `local` mode: {blur_radius}')
    Debug.log(
        'min/max threshold values used in `local` mode: '
        f'{averaged.getextrema()}'
    )
    return threshold


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


DITHER_ERROR_RECIPIENTS = {
    'atkinson': [
        (1, 0, 2), (2, 0, 2), (-1, 1, 2), (0, 1, 2), (1, 1, 2), (0, 2, 2),
    ],
    'floyd-steinberg': [
        (1, 0, 7), (-1, 1, 3), (0, 1, 5), (1, 1, 1),
    ],
}


def rasterize(
    image: Image.Image,
    zoom: float = 1,
    inverted: bool = False,
    crop_y: bool = False,
    edging: int = 0,
    dither: float = 0,
    dither_method: str = 'atkinson',
    adjust_brightness: float = 1,
    threshold_func: ThresholdFunc | None = None,
    rcwh_func: Callable[
        [], tuple[int, int, int, int]
    ] = terminal_rcwh,
) -> Iterable[str]:

    def sample(x: float, y: float) -> int:
        pixel = x * sx, y * sy
        pixelvalue = image.getpixel(pixel) or 0  # type: ignore[arg-type]
        assert isinstance(pixelvalue, int), f'{pixelvalue}'
        return pixelvalue

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
    max_row = int(image.height * zoom / ch) if not crop_y else min(
        int(image.height * zoom / ch), r
    )
    max_col = int(min(image.width * zoom / cw, c))
    Debug.log(f'using {max_col} columns × {max_row} rows')
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


THRESHOLD_FUNC_FACTORIES: dict[
    str, tuple[ThresholdFuncFactory, tuple[int, int] | None, int | None]
] = {
    'extremes': (thr_btw_extr_factory, None, None),
    'median': (thr_median_factory, None, None),
    'percentile': (thr_percentile_factory, (0, 99), 50),
    'const': (thr_const_factory, (0, 255), 127),
    'local': (thr_local_avg_factory, (0, 9999), None),
}


def get_threshold_func(
    image: Image.Image, options: argparse.Namespace
) -> ThresholdFunc:
    return THRESHOLD_FUNC_FACTORIES[options.threshold_mode][0](
        image, options.threshold_arg
    )


def thr_arg_value_range_constraints(
    value_range: tuple[int, int] | None
) -> Callable[[str], int]:
    def check(value: str) -> int:
        if not value_range:
            return int(value)
        if value_range[0] <= (sane := int(value)) <= value_range[1]:
            return sane
        raise ValueError(
            f'value must be between {" and ".join(map(str, value_range))}'
        )
    return check


def non_negative_float(src: str) -> float:
    if (value := float(src)) > 0:
        return value
    raise ValueError(f'{value} must be positive')


def parse_args(argv: list[str]) -> argparse.Namespace:
    argp_thr = argparse.ArgumentParser(add_help=False)
    threshold_choices = tuple(THRESHOLD_FUNC_FACTORIES.keys())
    thr_modes_requiring_args = tuple(
        mode for mode, properties in THRESHOLD_FUNC_FACTORIES.items()
        if properties[2]
    )
    thr_mode_arg_name = 'threshold'
    argp_thr.add_argument(
        '-m', f'--{thr_mode_arg_name}', dest='threshold_mode', metavar='MODE',
        choices=threshold_choices, default='local',
        help=(
            f'threshold mode, allowed values: [{"|".join(threshold_choices)}] '
            '(default: %(default)s)'
        ),
    )
    thr_options, _ = argp_thr.parse_known_args(argv)

    argp_out = argparse.ArgumentParser(add_help=False)
    stdout_path = pathlib.Path('/dev/stdout')
    argp_out.add_argument(
        '-o', '--output', dest='outputfile', type=pathlib.Path,
        metavar='FILE', default=stdout_path,
        help='output file (default: %(default)s).',
    )
    out_options, _ = argp_out.parse_known_args(argv)

    argp = argparse.ArgumentParser(
        description=textwrap.dedent(
            '''
            rasterize an image into the terminal.
            '''
        ),
        parents=[argp_thr, argp_out],
    )
    argp.add_argument(
        'inputfile', type=pathlib.Path, metavar='FILE',
        help='path to input image file.',
    )
    argp.add_argument(
        '-f', '--force', dest='output_overwrite', action='store_true',
        default=(
            out_options.outputfile.resolve() == stdout_path.resolve()
        ),
        help=(
            'overwrite existing output file '
            f'(default: %(default)s for {out_options.outputfile}).'
        ),
    )
    argp.add_argument(
        '-d', '--debug', action='store_true', dest='debug',
        help='preceed normal output with debug log printed to /dev/stderr.',
    )
    argp.add_argument(
        '-y', '--crop-y', dest='crop_y', action='store_true',
        help='crop image to terminal height.',
    )
    argp_scale_group = argp.add_argument_group(
        'resizing options'
    ).add_mutually_exclusive_group()
    argp_scale_group.add_argument(
        '-z', '--zoom', dest='zoom_factor', type=non_negative_float,
        default=1, metavar='FACTOR',
        help='factor by which input image should be scaled in size.',
    )
    argp_scale_group.add_argument(
        '-x', '--fit-x', dest='zoom_factor', action='store_const', const=0,
        help=(
            'scale image so it fits into the terminal window horizontally.'
        ),
    )
    argp.add_argument(
        '-v', '--invert', dest='invert', action='store_true',
        help="use the input image's negative.",
    )
    argp.add_argument(
        '-a', '--sharpen', dest='sharpen', action='count', default=0,
        help=(
            'enhance input image by emphasizing edges a little '
            '(the more often the option gets repeated, the more).'
        ),
    )
    argp.add_argument(
        '-b', '--brightness', dest='brightness', type=int,
        default=100, metavar='LEVEL', choices=range(200),
        help='adjust brightness in percent (default: %(default)d).',
    )
    argp_dither = argp.add_argument_group('dithering options')
    argp_dither.add_argument(
        '-e', '--dither', dest='error_preservation_factor', type=float,
        default=0, metavar='FACTOR',
        help=(
            'error preservation factor/dithering ratio (default: %(default)s).'
        ),
    )
    argp_dither_method = argp_dither.add_mutually_exclusive_group()
    argp_dither_method.add_argument(
        '-D', '--dmethod', dest='dither_method', metavar='METH',
        choices=('atkinson', 'floyd-steinberg'), default='atkinson',
        help=(
            'dither method to use ('
            f'one of {"|".join(DITHER_ERROR_RECIPIENTS.keys())}, '
            'default: %(default)s).'
        ),
    )
    argp_dither_method.add_argument(
        '--floyd', dest='dither_method', action='store_const',
        const='floyd-steinberg', help='shortcut for -Dfloyd-steinberg',
    )
    thr_arg_help = (
        'value to be passed to the threshold function '
        f'(see the --{thr_mode_arg_name} option). '
        'required if selected threshold mode is '
        f'{" or ".join(f'"{mode}"' for mode in thr_modes_requiring_args)}. '
    )
    _, thr_arg_value_range, thr_arg_value_default = THRESHOLD_FUNC_FACTORIES[
        thr_options.threshold_mode
    ]
    if thr_arg_value_range:
        thr_arg_help += (
            f'threshold mode "{thr_options.threshold_mode}" '
            'allows values between '
            f'{" and ".join(map(str, thr_arg_value_range))}'
        )
    if thr_arg_value_default:
        thr_arg_help += ' (default: %(default)s).'
    else:
        thr_arg_help += '.'
    argp.add_argument(
        '-t', '--threshold-arg', dest='threshold_arg', metavar='NUM',
        help=thr_arg_help,
        type=(
            int if thr_options.threshold_mode not in thr_modes_requiring_args
            else thr_arg_value_range_constraints(thr_arg_value_range)
        ),
        default=thr_arg_value_default,
    )
    return argp.parse_args(args=argv)


def main(argv: list[str] = sys.argv[1:]) -> int:
    options = parse_args(argv)
    if not options.output_overwrite and options.outputfile.exists():
        print(
            f'output file {options.outputfile} already exists! '
            'set option --force to overwrite.',
            file=sys.stderr
        )
        sys.exit(1)
    image = Image.open(options.inputfile).copy()
    Debug.log(f'image dimensions: {"×".join(map(str, image.size))}')
    rows = rasterize(
        image,
        zoom=scale_image(image, options.zoom_factor),
        inverted=options.invert,
        crop_y=options.crop_y,
        edging=options.sharpen,
        dither=options.error_preservation_factor,
        dither_method=options.dither_method,
        threshold_func=get_threshold_func(image, options),
        adjust_brightness=options.brightness / 100,
    )
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
