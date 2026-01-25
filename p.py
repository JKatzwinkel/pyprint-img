import argparse
import fcntl
import pathlib
import struct
import sys
import termios
import textwrap
import unicodedata
from typing import Callable

from PIL import Image, ImageFilter

import pytest


def terminal_rcwh() -> tuple[int, int, int, int]:
    return struct.unpack(
        'HHHH', fcntl.ioctl(
            0, termios.TIOCGWINSZ,
            struct.pack('HHHH', 0, 0, 0, 0)
        )
    )


def chardims(
    rchw_func: Callable[
        [], tuple[int, int, int, int]
    ] = terminal_rcwh,
) -> tuple[float, float]:
    r, c, h, w = rchw_func()
    return w / c, h / r


def char_name(matrix: list[bool], inverted: bool = False) -> str:
    '''
    >>> char_name([False, True, True, False])
    'BRAILLE PATTERN DOTS-23'

    >>> char_name([False, True, True, False], inverted=True)
    'BRAILLE PATTERN DOTS-14'

    >>> char_name([])
    'En space'
    '''
    key = ''.join(
        f'{i+1}' for i, b in enumerate(matrix) if b != inverted
    )
    return f'BRAILLE PATTERN DOTS-{key}' if key else 'En space'


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
    return i


type ThresholdFunc = Callable[[tuple[float, float]], float]
type ThresholdFuncFactory = Callable[[Image.Image, int], ThresholdFunc]


def thr_percentile_factory(image: Image.Image, percent: int = 50) -> ThresholdFunc:
    threshold = percentile(image.convert('L').histogram(), percent)
    return lambda pixel: threshold


def thr_const_factory(image: Image.Image, threshold: int = 127) -> ThresholdFunc:
    return lambda pixel: threshold


def thr_btw_extr_factory(image: Image.Image, _: int | None) -> ThresholdFunc:
    threshold = sum(image.convert('L').getextrema()) / 2  # type: ignore[arg-type]
    return lambda pixel: threshold


def thr_median_factory(image: Image.Image, _: int = -1) -> ThresholdFunc:
    return thr_percentile_factory(image, 50)


def thr_local_avg_factory(image: Image.Image, _: int = -1) -> ThresholdFunc:
    blur_radius = min(image.width, image.height) // 10
    averaged = image.filter(
        ImageFilter.GaussianBlur(blur_radius)
    ).convert('L')

    def threshold(pixel: tuple[float, float]) -> int:
        assert isinstance(
            result := averaged.getpixel(pixel), int  # type: ignore[arg-type]
        )
        return result
    return threshold


def rasterize(
    image: Image.Image,
    inverted: bool = False,
    crop_y: bool = False,
    threshold_func: ThresholdFunc | None = None,
    rchw_func: Callable[
        [], tuple[int, int, int, int]
    ] = terminal_rcwh,
) -> list[str]:

    def sample(
        x1: float, y1: float,
        x2: float, y2: float,
    ) -> str:
        sx = (x2 - x1) / 2
        sy = (y2 - y1) / 4
        matrix = []
        for dx, dy in (
            (0, 0), (0, 1), (0, 2), (1, 0),
            (1, 1), (1, 2), (0, 3), (1, 3),
        ):
            pixel = x1 + dx * sx, y1 + dy * sy
            pixelvalue = image.getpixel(pixel) or 0  # type: ignore[arg-type]
            assert isinstance(pixelvalue, int), f'{pixelvalue}'
            matrix.append(pixelvalue > threshold(pixel))
        return unicodedata.lookup(char_name(matrix, inverted=inverted))

    threshold: ThresholdFunc = threshold_func or thr_btw_extr_factory(image, 0)
    r, c, w, h = terminal_rcwh()
    sx, sy = w / c, h / r
    result: list[list[str]] = [[]]
    max_row = int(image.height / sy) if not crop_y else min(
        int(image.height / sy), r
    )
    image = image.convert('L')
    for y in range(max_row):
        for x in range(c):
            pixel = x * sx, y * sy
            if pixel[0] + sx > image.width:
                result.append([])
                break
            result[-1].append(
                sample(
                    pixel[0], pixel[1], pixel[0] + sx, pixel[1] + sy,
                )
            )
    return [''.join(row) for row in result if row]


THRESHOLD_FUNC_FACTORIES: dict[str, ThresholdFuncFactory] = {
    'extremes': thr_btw_extr_factory,
    'median': thr_median_factory,
    'percentile': thr_percentile_factory,
    'const': thr_const_factory,
    'local': thr_local_avg_factory,
}
THR_MODES_REQUIRING_ARGS = ('percentile', 'const')


def get_threshold_func(
    image: Image.Image, options: argparse.Namespace
) -> ThresholdFunc:
    return THRESHOLD_FUNC_FACTORIES[options.threshold_mode](
        image, options.threshold_arg
    )


def parse_args(argv: list[str]) -> argparse.Namespace:
    argp_thr = argparse.ArgumentParser(add_help=False)
    threshold_choices = tuple(THRESHOLD_FUNC_FACTORIES.keys())
    def thr_arg_value_range_constraints(
        value_range: tuple[int, int]
    ) -> Callable[[str], int]:
        def check(value: str) -> int:
            if value_range[0] <= (sane := int(value)) <= value_range[1]:
                return sane
            raise ValueError(
                f'value must be between {" and ".join(map(str, value_range))}'
            )
        return check
    argp_thr.add_argument(
        '-m', '--threshold', dest='threshold_mode', metavar='mode',
        choices=threshold_choices, default='median',
        help=(
            f'threshold mode, allowed values: [{"|".join(threshold_choices)}] '
            '(default: %(default)s)'
        ),
    )
    thr_options, _ = argp_thr.parse_known_args(argv)

    argp = argparse.ArgumentParser(
        description=textwrap.dedent(
            '''
            rasterize an image into the terminal.
            '''
        ),
        parents=[argp_thr],
    )
    argp.add_argument(
        'filename', help='path to image file', type=pathlib.Path,
    )
    argp.add_argument(
        '-y', '--crop-y', dest='crop_y', action='store_true',
        help='crop image to terminal height',
    )
    argp.add_argument(
        '-v', '--invert', dest='invert', action='store_true',
        help='rasterize a negative of the image',
    )
    thr_arg_help = (
        'value to be passed to the threshold function. '
        'required if selected --threshold mode is '
        f'{" or ".join(THR_MODES_REQUIRING_ARGS)}. '
    )
    thr_arg_value_default = None
    if thr_options.threshold_mode in THR_MODES_REQUIRING_ARGS:
        thr_arg_value_range = (
            (0, 100) if thr_options.threshold_mode == 'percentile' else (0, 255)
        )
        thr_arg_value_default = (
            50 if thr_options.threshold_mode == 'percentile' else 127
        )
        thr_arg_help += (
            f'--threshold mode "{thr_options.threshold_mode}" '
            'allows values between '
            f'{" and ".join(map(str, thr_arg_value_range))} '
            '(default: %(default)s).'
        )
    argp.add_argument(
        '-t', '--threshold-arg', dest='threshold_arg', metavar='NUM',
        help=thr_arg_help,
        type=(
            int if thr_options.threshold_mode not in THR_MODES_REQUIRING_ARGS
            else thr_arg_value_range_constraints(thr_arg_value_range)
        ),
        default=thr_arg_value_default,
    )
    return argp.parse_args(args=argv)


@pytest.mark.parametrize(
    'argv, error', (
        ('-m median', True),
        ('-m const -t 256 f.png', True),
        ('-m const -t 128 f.png', False),
        ('-m percentile -t 128 f.pn', True),
    )
)
def test_parse_args(argv: str, error: bool) -> None:
    if not error:
        assert parse_args(argv.split())
        return
    with pytest.raises(SystemExit):
        parse_args(argv.split())


def test_file_not_found() -> None:
    with pytest.raises(FileNotFoundError):
        main('fya.jpg'.split())


def main(argv: list[str] = sys.argv[1:]) -> None:
    options = parse_args(argv)
    print(options)
    im = Image.open(options.filename)
    cc = rasterize(
        im, inverted=options.invert,
        crop_y=options.crop_y,
        threshold_func=get_threshold_func(im, options),
    )
    print('\n'.join(cc))


if __name__ == '__main__':
    main()
