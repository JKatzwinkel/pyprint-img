from typing import Iterable

from .chars import braille
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


def plot(histogram: list[int], c: int = 80, r: int = 10) -> Iterable[str]:
    '''
    >>> bins = [0, 0, 0, 2, 1, 4, 6, 5, 4, 3, 2, 1, 0, 1, 0, 0]
    >>> for line in plot(bins, r=3):
    ...     print(line)
    ⠀⠀⠀⣆⠀⠀⠀⠀
    ⠀⠀⢰⣿⣆⠀⠀⠀
    ⠀⢰⣸⣿⣿⣆⢀⠀
    ▔▔🭽▔🭽▔▔🭽

    '''
    histogram = shrink(histogram, c * 2)
    max_frequency = max(histogram)
    bin_height = [
        r * b / max_frequency * 4 for b in histogram
    ]
    line = []
    for j in range(r):
        y = (r - j) * 4
        for i in range(0, len(histogram) - 1, 2):
            dots = [
                bin_height[i + dx] > y - dy
                for dx, dy in (
                    (0, 0), (1, 0),
                    (0, 1), (1, 1),
                    (0, 2), (1, 2),
                    (0, 3), (1, 3),
                )
            ]
            line.append(braille(dots))
        yield ''.join(line)
        line.clear()
    markers = minmedmax(histogram)
    for i in range(len(histogram) // 2):
        if not markers or i * 2 < markers[0]:
            line.append('▔')
            continue
        if i * 2 + 1 == markers[0]:
            line.append('🭾')
        elif i * 2 >= markers[0]:
            line.append('🭽')
        markers.pop(0)
    yield ''.join(line)


def errbar(histogram: list[int], c: int = 80) -> str:
    '''
    >>> bins = [0, 0, 0, 2, 1, 4, 6, 5, 4, 3, 2, 1, 0, 1, 0, 0]
    >>> errbar(bins)
    '   ┝━━━╋━━━━━┥'

    >>> errbar([0, 0, 0, 0, 10, 0, 0, 0])
    '    ╋'

    >>> errbar([0, 0, 0, 5, 5, 0, 0, 0])
    '   ┝┥'
    '''
    histogram = shrink(histogram, c * 2)
    markers = minmedmax(histogram)
    line = [' '] * len(histogram)
    for i in range(markers[0], markers[2]):
        line[i] = '━'
    line[markers[1]] = '╋'
    if len(set(markers)) > 1:
        line[markers[0]] = '┝'
        line[markers[2]] = '┥'
    return ''.join(line).rstrip()
