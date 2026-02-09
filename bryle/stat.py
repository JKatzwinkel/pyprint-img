from typing import Iterable, Literal

from .chars import PairCharset, pair2char
from .util import Debug


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


def extrema(histogram: list[int]) -> tuple[int, int]:
    '''
    >>> extrema([0, 0, 3, 5, 7, 6, 0, 0, 1, 0])
    (2, 8)

    >>> extrema([0, 0, 1, 0])
    (2, 2)
    '''
    for i in range(len(histogram)):
        if histogram[i]:
            break
    for j in range(len(histogram) - 1, i - 1, -1):
        if histogram[j]:
            break
    return (i, j)


def minmedmax(histogram: list[int]) -> list[int]:
    return sorted(
        list(extrema(histogram)) + [percentile(histogram, 50)]
    )


def five_number_summary(histogram: list[int]) -> list[int]:
    return sorted(
        minmedmax(histogram) + [
            percentile(histogram, p) for p in (25, 75)
        ]
    )


def shrink(
    histogram: list[int],
    max_width: int,
) -> list[int]:
    '''
    squeeze histogram by merging bins until their number
    gets lower than required.

    >>> shrink([0, 1, 1, 3, 5, 6, 2, 0], 4)
    [1, 4, 11, 2]
    '''
    def _squeeze() -> list[int]:
        return [
            histogram[i] + histogram[i + 1]
            for i in range(0, len(histogram) - 1, 2)
        ]

    while len(histogram) > max_width:
        histogram = _squeeze()
    return histogram


type BoxplotCharset = Literal['utf8', 'ascii']


BOXPLOT_CHARS = {
    'utf8': '─┾━╋┽',
    'ascii': '-[ |]',
}


def plot(
     histogram: list[int], c: int = 80, r: int = 10,
     fns: BoxplotCharset | None = None,
     charset: PairCharset = 'braille',
) -> Iterable[str]:
    '''
    >>> for line in plot([0, 1, 2, 3, 4, 3], r=2):
    ...     print(line)
    ⠀⢠⣧
    ⢠⣿⣿
    <=|

    >>> bins = [0, 0, 0, 2, 1, 4, 6, 5, 4, 3, 2, 1, 0, 1, 0, 0]
    >>> for line in plot(bins, r=3):
    ...     print(line)
    ⠀⠀⠀⣧⠀⠀⠀⠀
    ⠀⠀⢸⣿⣧⠀⠀⠀
    ⠀⢸⣼⣿⣿⣧⢠⠀
    =<=|==>=

    >>> for line in plot(bins, r=3, charset='8ths'):
    ...     print(line)  # doctest: +NORMALIZE_WHITESPACE
       ▙
      ▐█▙
     ▐▟██▙▗
    =<=|==>=

    >>> for line in plot(bins, r=3, charset='ascii'):
    ...     print(line)  # doctest: +NORMALIZE_WHITESPACE
       \\
      /|\\
     //||\\/
    =<=|==>=
    '''
    histogram = shrink(histogram, c * 2)
    if fns:
        yield boxplot(histogram, c, charset=fns)
    max_frequency = max(histogram)
    bin_height = [
        r * b / max_frequency for b in histogram
    ]
    line = []
    for j in range(r):
        y = (r - j)
        for i in range(0, len(histogram) - 1, 2):
            left, right = (
                bin_height[i + dx] - y + 1 for dx in range(2)
            )
            line.append(pair2char(left, right, charset=charset))
        yield ''.join(line)
        line.clear()
    markers = minmedmax(histogram)
    line = ['='] * (len(histogram) // 2)
    line[markers[0] // 2] = '<'
    line[markers[2] // 2] = '>'
    line[markers[1] // 2] = '|'
    yield ''.join(line)


def boxplot(
    histogram: list[int], c: int = 80, charset: BoxplotCharset = 'utf8',
) -> str:
    '''
    >>> bins = [0, 0, 0, 2, 1, 4, 6, 5, 4, 3, 2, 1, 0, 1, 0, 0]
    >>> boxplot(bins)
    '   ───┾╋┽─────  '

    >>> boxplot([0, 0, 0, 0, 10, 0, 0, 0])
    '    ╋   '

    >>> boxplot([0, 0, 0, 5, 5, 0, 0, 0])
    '   ╋┽   '
    '''
    histogram = shrink(histogram, c)
    markers = five_number_summary(histogram)
    line = [' '] * len(histogram)
    CHARS = tuple(BOXPLOT_CHARS[charset])
    for i in range(markers[0], markers[4] + 1):
        line[i] = CHARS[0]
    for i in range(markers[1], markers[3] + 1):
        line[i] = CHARS[2]
    line[markers[1]] = CHARS[1]
    line[markers[3]] = CHARS[4]
    line[markers[2]] = CHARS[3]
    return ''.join(line)
