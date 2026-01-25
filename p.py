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


def subsample(
    image: Image,
    x1: float, y1: float,
    x2: float, y2: float,
    threshold: float,
    inverted: bool = False,
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


def sample(
    image: Image,
    inverted: bool = False,
    crop_y: bool = False,
    rchw_func: Callable[
        [], tuple[int, int, int, int]
    ] = terminal_rcwh,
) -> list[str]:
    image = image.convert('L')
    threshold = sum(image.getextrema()) / 2
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
                subsample(
                    image, pixel[0], pixel[1], pixel[0] + sx, pixel[1] + sy,
                    threshold,
                    inverted=inverted,
                )
            )
    return [''.join(row) for row in result if row]


if __name__ == '__main__':
    im = Image.open('shelly.jpg')
    cc = sample(im, inverted=False, crop_y=True)
    print('\n'.join(cc))
