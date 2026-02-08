import pytest

from bryle.stat import extrema


@pytest.mark.parametrize(
    'bins, expect', (
        (
            [0, 0, 1, 0], (2, 2)
        ),
    )
)
def test_extrema(bins: list[int], expect: tuple[int, int]) -> None:
    assert extrema(bins) == expect
