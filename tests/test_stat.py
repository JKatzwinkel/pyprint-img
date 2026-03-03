import pyvips  # type: ignore[import-untyped]

import pytest

from bryle.args import parse_args
from bryle.img import histogram, plot_brightness_and_threshold
from bryle.stat import BoxplotCharset, boxplot, extrema, plot


def test_extrema(image: pyvips.Image) -> None:
    assert extrema(histogram(image)) == (int(image.min()), int(image.max()))


@pytest.mark.parametrize(
    'bins, charset, expect', (
        (
            [1, 1, 1, 1],
            'utf8',
            '┾╋┽─',
        ),
        (
            [0, 1, 1, 1, 1, 1, 1, 0],
            'ascii',
            ' -[| ]- ',
        ),
        (
            [0,  0, 0, 4, 0, 0, 0, 0],
            'utf8',
            '   ╋    ',
        ),
        (
            [0,  0, 0, 4, 5, 0, 0, 0],
            'utf8',
            '   ┾╋   ',
        ),
        (
            [1,  0, 0, 2, 5, 0, 1, 0],
            'utf8',
            '───┾╋── ',
        ),
    )
)
def test_boxplots(
    bins: list[int], charset: BoxplotCharset, expect: str,
) -> None:
    assert boxplot(bins, charset=charset) == expect, '\n'.join(plot(bins))


def test_plot_histogram(image: pyvips.Image) -> None:
    lines = list(plot(histogram(image), c=64, r=8, fns='ascii'))
    result = '\n'.join([''] + lines)
    assert len(lines) == 8 + 2, result
    assert len(lines[0]) == 64, result
    assert len(lines[-1]) == 64, result


@pytest.mark.parametrize(
    'argv, thresh_plot', (
        (
            '-mlocal -t 30',
            '─────────┾━━━━━━━╋━━━┽──────'
        ),
        (
            '-mlocal -t 50',
            '──┾━━━╋━━━┽──────'
        ),
        (
            '-mlocal -t30 -b120',
            '────────┾━━━━━╋━━━┽─────'
        ),
        (
            '-mmedian', '╋'
        ),
    )
)
def test_plot_histogram_with_thresholds(
    image: pyvips.Image, argv: str, thresh_plot: str,
) -> None:
    options = parse_args(['f.png'] + argv.split())  # noqa: SIM905
    lines = list(
        plot_brightness_and_threshold(image, options, 80, 8, charset='blocks')
    )
    result = '\n'.join([''] + lines)
    assert len(lines) == 8 + 3, result
    assert len(lines[0]) == 64, result
    assert len(lines[-1]) == 64, result
    assert lines[-1].strip() == thresh_plot, result
