from PIL import Image

import pytest

from bryle.img import ImgData
from bryle.pxp import sample_func


@pytest.mark.parametrize(
    'x, y, value', (
        (0, 0, 0),
        (2, 0, 64),
        (0, 2, 128),
        (2, 2, 255),
        (1, 0, 32),
        (0, 1, 64),
        (1, 2, 192),
        (1, 1, 112),
    )
)
def test_sampling(x: int, y: int, value: int) -> None:
    imdat = ImgData(
        Image.frombytes('L', (2, 2), b'\x00\x40\x80\xff')
    )
    sample = sample_func(imdat, .5, .5)
    assert sample(x, y) == value
