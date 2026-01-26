import argparse
import fcntl
import os
import pathlib
import struct
import sys
import tempfile
import termios
import textwrap
import unicodedata
from typing import Callable

from PIL import Image, ImageFilter

from unittest import mock

import pytest


def terminal_rcwh() -> tuple[int, int, int, int]:
    return struct.unpack(
        'HHHH', fcntl.ioctl(
            0, termios.TIOCGWINSZ,
            struct.pack('HHHH', 0, 0, 0, 0)
        )
    )


def get_terminal_rcwh_func() -> Callable[[], tuple[int, int, int, int]]:
    if sys.stdout.isatty() and os.environ.get('DISPLAY'):
        return terminal_rcwh
    return lambda: (44, 174, 1914, 1012)


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
        image.convert('L').getextrema()  # type: ignore[arg-type]
    ) / 2
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
    blur_radius = blur_radius or min(image.width, image.height) // 10
    averaged = image.filter(
        ImageFilter.GaussianBlur(blur_radius)
    ).convert('L')
    return threshold


def rasterize(
    image: Image.Image,
    inverted: bool = False,
    crop_y: bool = False,
    antialias: int = 0,
    threshold_func: ThresholdFunc | None = None,
    rchw_func: Callable[
        [], tuple[int, int, int, int]
    ] = terminal_rcwh,
) -> list[str]:

    def sample(x1: float, y1: float) -> str:
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
    r, c, w, h = rchw_func()
    cw, ch = w / c, h / r
    sx, sy = cw / 2, ch / 4
    result: list[list[str]] = [[]]
    max_row = int(image.height / ch) if not crop_y else min(
        int(image.height / ch), r
    )
    max_col = int(min(image.width / cw, c))
    image = image.convert('L')
    while antialias:
        antialias -= 1
        image = image.filter(
            ImageFilter.MedianFilter(size=int(min(sx, sy) / 2) * 2 + 1)
        )
    for y in range(max_row):
        py = y * ch
        for x in range(max_col):
            px = x * cw
            result[-1].append(sample(px, py))
        result.append([])
    return [''.join(row) for row in result if row]


def scale_image(image: Image.Image, zoom_factor: float = -1) -> Image.Image:
    if zoom_factor <= 0:
        r, c, w, h = terminal_rcwh()
        zoom_factor = w / image.width
    return image.resize(
        (
            int(image.width * zoom_factor),
            int(image.height * zoom_factor)
        ),
        resample=Image.Resampling.LANCZOS,
    )


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
        '-y', '--crop-y', dest='crop_y', action='store_true',
        help='crop image to terminal height.',
    )
    argp_scale_group = argp.add_argument_group(
        'resizing options'
    ).add_mutually_exclusive_group()
    argp_scale_group.add_argument(
        '-x', '--fit-x', dest='fit_to_width', action='store_true',
        help=(
            'scale image so it fits into the terminal window horizontally '
            '(default: %(default)s).'
        ),
    )
    argp_scale_group.add_argument(
        '-z', '--zoom', dest='zoom_factor', type=non_negative_float,
        default=0, metavar='FACTOR',
        help='factor by which input image should be scaled in size.',
    )
    argp.add_argument(
        '-v', '--invert', dest='invert', action='store_true',
        help='rasterize a negative of the image',
    )
    argp.add_argument(
        '-a', '--smooth', dest='antialias', action='count', default=0,
        help=(
            'smooth input image a little bit based on the sample rate. '
            'might be a good idea for images with a lot highly contrasted '
            'detail but is slow. Can be repeated '
            '(default: %(default)d).'
        ),
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


@pytest.mark.parametrize(
    'argv, error', (
        ('-m median', True),
        ('f.png -aaa', False),
        ('-m const -t 256 f.png', True),
        ('-m const -t 128 f.png', False),
        ('--thresh median f.png', True),
        ('--inv f.png', False),
        ('-m percentile -t 128 f.pn', True),
        ('-m local f.png', False),
        ('-m local -t fya f.png', True),
        ('--fit f.png', False),
        ('-z 2 -x f.png', True),
        ('-z -1.2 f.png', True),
        ('-z fya f.png', True),
        ('-z 1.2 f.png', False),
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
        main(['fya.jpg'])


@pytest.mark.parametrize(
    'argv, phrase, expect', (
        ('-m percentile', 'mode "percentile"', True),
        ('-m percentile', '0 and 99', True),
        ('-m percentile', 'default: 50', True),
        ('-m local', 'allows values', True),
        ('-m local', '0 and 9999', True),
        ('-m median', 'allows values', False),
        ('-o fya.txt', 'output file (default: False', True),
        ('-o /dev/stdout', 'output file (default: True', True),
        ('', 'default: /dev/stdout', True),
        ('', 'output file (default: True', True),
    )
)
def test_cli_help(
    argv: str, phrase: str, expect: bool,
    capsys: pytest.CaptureFixture[str],
) -> None:
    try:
        main(argv.split() + ['-h'])
    except SystemExit:
        ...
    collapsed = ' '.join(
        ' '.join(
            capsys.readouterr().out.split('\n')
        ).split()
    )
    if expect:
        assert phrase in capsys.readouterr().out or phrase in collapsed
    else:
        assert (
            phrase not in capsys.readouterr().out and phrase not in collapsed
        )


@mock.patch(
    f'{__name__}.terminal_rcwh',
    side_effect=lambda: (44, 174, 1914, 1012),
)
def test_cli_creates_file(terminal_rcwh_mock: mock.MagicMock) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        outfile = pathlib.Path(tmp) / 'fya.txt'
        main(f'shelly.jpg -o {outfile}'.split())
        assert outfile.exists()
        with pytest.raises(SystemExit):
            main(f'irrelevant.jpg -o {outfile}'.split())
        assert main(f'shelly.jpg -fo {outfile}'.split()) == 0


def main(argv: list[str] = sys.argv[1:]) -> int:
    options = parse_args(argv)
    if not options.output_overwrite and options.outputfile.exists():
        print(
            f'output file {options.outputfile} already exists! '
            'set option --force to overwrite.',
            file=sys.stderr
        )
        sys.exit(1)
    im = Image.open(options.inputfile).copy()
    if options.fit_to_width or options.zoom_factor:
        im = scale_image(im, options.zoom_factor)
    cc = rasterize(
        im, inverted=options.invert,
        crop_y=options.crop_y,
        antialias=options.antialias,
        threshold_func=get_threshold_func(im, options),
        rchw_func=get_terminal_rcwh_func(),
    )
    options.outputfile.touch(
        mode=0o644, exist_ok=options.output_overwrite,
    )
    with options.outputfile.open('w') as f:
        print('\n'.join(cc), file=f)
    return 0


if __name__ == '__main__':
    main()
