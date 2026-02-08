from PIL import Image

import pytest

from bryle.stat import boxplot, extrema, plot


def test_extrema(image: Image.Image) -> None:
    assert extrema(image.histogram()) == image.getextrema()


@pytest.mark.parametrize(
    'bins, bar', (
        (
            [1,  1, 1, 1],
            '┾╋┽─',
        ),
        (
            [0,  0, 0, 4, 0, 0, 0, 0],
            '   ╋',
        ),
        (
            [0,  0, 0, 4, 5, 0, 0, 0],
            '   ┾╋',
        ),
        (
            [1,  0, 0, 2, 5, 0, 1, 0],
            '───┾╋──',
        ),
    )
)
def test_boxplots(bins: list[int], bar: str) -> None:
    assert boxplot(bins) == bar, '\n'.join(plot(bins))
