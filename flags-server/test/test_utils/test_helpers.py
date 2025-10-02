import pytest

from src.utils.helpers import is_positive_integer


@pytest.mark.parametrize(
    "value,expected",
    [
        (1, True),
        (10, True),
        (0, False),
        (-5, False),
        ("3", True),
        ("0", False),
        ("-7", False),
        ("abc", False),
        (None, False),
        (3.5, False),
        ([], False),
        ({}, False),
    ],
)
def test_is_positive_integer(value: object, expected: bool) -> None:
    assert is_positive_integer(value) == expected
