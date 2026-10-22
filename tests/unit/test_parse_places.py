import pytest

from server import parsePlacesRequired


def test_returns_number_of_places_when_valid():
    assert parsePlacesRequired("3") == 3


def test_accepts_surrounding_spaces():
    assert parsePlacesRequired(" 12 ") == 12


@pytest.mark.parametrize("value", ["0", "-2", "abc", "", "2.5", None])
def test_returns_none_when_invalid(value):
    assert parsePlacesRequired(value) is None
