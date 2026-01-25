import fcntl
import struct
import termios
import unicodedata
from typing import Callable

from PIL import Image


def terminal_rchw() -> tuple[int, int, int, int]:
    return struct.unpack(
        'HHHH', fcntl.ioctl(
            0, termios.TIOCGWINSZ,
            struct.pack('HHHH', 0, 0, 0, 0)
        )
    )


def chardims(
    rchw_func: Callable[
        [], tuple[int, int, int, int]
    ] = terminal_rchw
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
        matrix.append(sum(image.getpixel(pixel)) > 384)
    return unicodedata.lookup(char_name(matrix, inverted=inverted))


def sample(
    image: Image,
    inverted: bool = False,
    rchw_func: Callable[
        [], tuple[int, int, int, int]
    ] = terminal_rchw,
) -> list[str]:
    r, c, h, w = terminal_rchw()
    sx, sy = w / c, h / r
    result: list[list[str]] = [[]]
    for y in range(r):
        if (y + 1) * sy > image.height:
            break
        for x in range(c):
            pixel = x * sx, y * sy
            if pixel[0] + sx > image.width:
                result.append([])
                break
            result[-1].append(
                subsample(
                    image, pixel[0], pixel[1], pixel[0] + sx, pixel[1] + sy,
                    inverted=inverted,
                )
            )
    return [''.join(row) for row in result if row]


if __name__ == '__main__':
    im = Image.open('shelly.jpg')
    cc = sample(im, inverted=False)
    print('\n'.join(cc))
