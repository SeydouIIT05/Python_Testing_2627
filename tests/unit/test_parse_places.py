import pytest

from server import parsePlacesRequired


def test_returns_number_of_places_when_valid():
    assert parsePlacesRequired("3") == 3


def test_accepts_surrounding_spaces():
    assert parsePlacesRequired(" 12 ") == 12


@pytest.mark.parametrize(
    "value, expected", [("1", 1), ("+3", 3), ("007", 7), (" 5\n", 5)]
)
def test_valid_values(value, expected):
    assert parsePlacesRequired(value) == expected


@pytest.mark.parametrize(
    "value",
    ["0", "-0", "-2", "--1", "abc", "three", "", "  ", "2.5", "1,5", "1e3",
     None],
)
def test_returns_none_when_invalid(value):
    assert parsePlacesRequired(value) is None
