import argparse
import pathlib
import textwrap
from typing import Callable

from .p import DITHER_ERROR_RECIPIENTS, THRESHOLD_FUNC_FACTORIES


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
        epilog=(
            '%(prog)s reads the environment variable TERM_RCWH which when set '
            'bypasses any attempt at determining actual terminal && xterm '
            'window sizes from tty and ioctl and forces fixed terminal and '
            'optionally window size to be used for image processing. '
            'TERM_RCWH accepts values in the forms `RxC` and `RxCxWxH` '
            'where `RxC` is terminal size in rows '
            'and columns and `WxH` is window width and hieght in pixels.'
        ),
    )
    argp.add_argument(
        'inputfile', type=str, metavar='FILE',
        help='path to input image file, or "-" to read from stdin.',
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
        help="invert 'pixel' values of output.",
    )
    argp.add_argument(
        '-a', '--sharpen', dest='sharpen', action='count', default=0,
        help=(
            'enhance input image by emphasizing edges a little '
            '(the more often the option gets repeated, the more).'
        ),
    )
    argp.add_argument(
        '-A', '--aliasing', dest='disable_antialiasing', action='store_true',
        help='disable antialiasing.',
    )
    argp.add_argument(
        '-b', '--brightness', dest='brightness', type=int,
        default=100, metavar='LEVEL', choices=range(200),
        help='adjust brightness in percent (default: %(default)d).',
    )
    argp_dither = argp.add_argument_group('dithering options')
    argp_dither.add_argument(
        '-e', '--dither', dest='error_preservation_factor', type=float,
        nargs='?', const=1., default=0., metavar='FACTOR',
        help=(
            'error preservation factor/dithering ratio. '
            'accepts an optional %(type)s value and assumes %(const)s '
            'if omitted. (default: %(default)s).'
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
