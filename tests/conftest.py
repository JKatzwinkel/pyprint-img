import pytest
from PIL import Image


@pytest.fixture(scope='session')
def image() -> Image.Image:
    return Image.open('eppels.png').convert('L')
