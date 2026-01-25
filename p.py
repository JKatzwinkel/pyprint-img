import fcntl
import struct
import termios
import unicodedata
from typing import Callable

from PIL import Image


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


def thr_percentile(percent: int) -> Callable[[Image], float]:
    return lambda i: percentile(i.histogram(), percent)


thr_btw_extr = lambda i: sum(i.getextrema()) / 2
thr_median = thr_percentile(50)

def rasterize(
    image: Image,
    inverted: bool = False,
    crop_y: bool = False,
    threshold_func: Callable[[Image], float] = thr_btw_extr,
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
            matrix.append(image.getpixel(pixel) > threshold)
        return unicodedata.lookup(char_name(matrix, inverted=inverted))

    image = image.convert('L')
    threshold = threshold_func(image)
    r, c, w, h = terminal_rcwh()
    sx, sy = w / c, h / r
    result: list[list[str]] = [[]]
    max_row = int(image.height / sy) if not crop_y else min(
        int(image.height / sy), r
    )
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


if __name__ == '__main__':
    im = Image.open('shelly.jpg')
    cc = rasterize(
        im, inverted=False, crop_y=False, threshold_func=thr_percentile(42),
    )
    print('\n'.join(cc))
