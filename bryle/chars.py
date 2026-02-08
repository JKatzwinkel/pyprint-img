from typing import Iterable, Literal


BRAILLE_DOT_MASK = [
    0x01, 0x08,
    0x02, 0x10,
    0x04, 0x20,
    0x40, 0x80,
]


def braille(pixels: Iterable[bool | int], inverted: bool = False) -> str:
    '''
    >>> braille((1, 0))
    '⠁'

    >>> braille((
    ...     1, 0,
    ...     0, 0,
    ...     0, 0,
    ...     1, 0,
    ... ))
    '⡁'

    >>> braille((
    ...     1, 0,
    ...     0, 1,
    ...     1, 0,
    ...     0, 1,
    ... ))
    '⢕'

    >>> braille((
    ...     1, 0,
    ...     0, 1,
    ...     1, 0,
    ...     0, 1), True
    ... )
    '⡪'
    '''
    codepoint = 0x2800
    for i, b in enumerate(pixels):
        if b != inverted:
            codepoint |= BRAILLE_DOT_MASK[i]
    return chr(codepoint)


def eighthblock(fraction: float) -> str:
    '''
    >>> eighthblock(0)
    ' '

    >>> eighthblock(.25)
    '▂'

    >>> eighthblock(.5)
    '▄'

    >>> eighthblock(7 / 8)
    '▇'

    >>> eighthblock(15 / 16)
    '▇'

    >>> eighthblock(1)
    '█'

    >>> eighthblock(2)
    '█'
    '''
    eighths = min(8, int(8 * fraction))
    if eighths < 1:
        return ' '
    return chr(0x2580 + eighths)


def pair2braille(left: float, right: float) -> str:
    '''
    >>> pair2braille(-1, -2)
    '\u2800'

    >>> pair2braille(.25, .5)
    '⣠'
    '''
    return chr(
        0x2800 + [0x00, 0x40, 0x44, 0x46, 0x47][
            max(0, min(4, int(left * 4)))
        ] + [0x00, 0x80, 0xa0, 0xb0, 0xb8][
            max(0, min(4, int(right * 4)))
        ]
    )


EIGHTH_PAIRS = {
    (4, 0): 0x2596,
    (8, 0): 0x258c,
    (8, 4): 0x2599,
    (0, 4): 0x2597,
    (0, 8): 0x2590,
    (4, 8): 0x259f,
}


type PairCharset = Literal['braille', 'eighths', '8ths', 'blocks']


def pair2char(
    left: float, right: float,
    charset: PairCharset = 'braille',
) -> str:
    '''
    >>> pair2char(.25, 5 / 8)
    '⣠'

    >>> pair2char(.1, 1)
    '⢸'

    >>> pair2char(2, .5)
    '⣧'

    >>> pair2char(1, 0, '8ths')  # 0x258c
    '▌'

    >>> pair2char(.1, 1, '8ths')  # 0x2590
    '▐'

    >>> pair2char(.5, 0, '8ths')  # 0x2596
    '▖'

    >>> pair2char(0, .5, '8ths')  # 0x2597
    '▗'

    >>> pair2char(1, .5, '8ths')  # 0x2599
    '▙'

    >>> pair2char(.5, 1, '8ths')  # 0x259f
    '▟'

    >>> pair2char(.75, .5, '8ths')
    '▅'

    >>> pair2char(.25, 2, '8ths')
    '▅'
    '''
    if charset == 'braille':
        return pair2braille(left, right)
    return pair2blocks(left, right)


def pair2blocks(left: float, right: float) -> str:
    '''
    >>> pair2blocks(-1, .5)
    '▗'
    '''
    if (codepoint := EIGHTH_PAIRS.get((
        min(8, max(0, int(left * 8))),
        min(8, max(0, int(right * 8))),
    ))):
        return chr(codepoint)
    return eighthblock((min(1, left) + min(1, right)) / 2)
