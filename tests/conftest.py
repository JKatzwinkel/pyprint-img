import pyvips  # type: ignore[import-untyped]

import pytest


@pytest.fixture(scope='session')
def image() -> pyvips.Image:
    img = pyvips.Image.new_from_file('eppels.png')
    return img.colourspace(pyvips.Interpretation.B_W)
