DOT_MASK = [
    0x01, 0x08,
    0x02, 0x10,
    0x04, 0x20,
    0x40, 0x80,
]


def braille(*pixels: bool | int) -> str:
    '''
    >>> braille(1, 0)
    '⠁'

    >>> braille(
    ...     1, 0,
    ...     0, 0,
    ...     0, 0,
    ...     1, 0,
    ... )
    '⡁'

    >>> braille(
    ...     1, 0,
    ...     0, 1,
    ...     1, 0,
    ...     0, 1,
    ... )
    '⢕'
    '''
    codepoint = 0x2800
    for i, b in enumerate(pixels):
        if b:
            codepoint |= DOT_MASK[i]
    return chr(codepoint)
