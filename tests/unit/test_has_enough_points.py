import pytest

from server import hasEnoughPoints


def test_true_when_places_are_below_points():
    assert hasEnoughPoints({"points": "13"}, 5) is True


def test_true_when_places_equal_points():
    assert hasEnoughPoints({"points": "4"}, 4) is True


def test_false_when_places_exceed_points():
    assert hasEnoughPoints({"points": "4"}, 5) is False


def test_false_when_club_has_no_points():
    assert hasEnoughPoints({"points": "0"}, 1) is False


@pytest.mark.parametrize(
    "points, places, expected",
    [
        ("13", 1, True),
        ("13", 12, True),
        ("13", 14, False),
        ("1", 2, False),
        (5, 5, True),
        (5, 6, False),
        (0, 1, False),
    ],
)
def test_points_limit_cases(points, places, expected):
    assert hasEnoughPoints({"points": points}, places) is expected
