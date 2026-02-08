from PIL import Image

import pytest


@pytest.fixture(scope='session')
def image() -> Image.Image:
    return Image.open('eppels.png').convert('L')
