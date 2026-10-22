import pytest

from server import deductPoints


def test_deducts_points_used_for_places():
    club = {"points": "13"}

    deductPoints(club, 5)

    assert club["points"] == 8


def test_can_use_all_remaining_points():
    club = {"points": "4"}

    deductPoints(club, 4)

    assert club["points"] == 0


def test_deducts_from_points_already_updated():
    club = {"points": 8}

    deductPoints(club, 3)

    assert club["points"] == 5


@pytest.mark.parametrize(
    "points, places, remaining",
    [("13", 1, 12), ("13", 12, 1), (12, 12, 0), ("1", 1, 0)],
)
def test_remaining_points_cases(points, places, remaining):
    club = {"points": points}

    deductPoints(club, places)

    assert club["points"] == remaining


def test_only_points_are_changed():
    club = {"name": "Simply Lift", "email": "john@simplylift.co",
            "points": "13"}

    deductPoints(club, 2)

    assert club == {"name": "Simply Lift", "email": "john@simplylift.co",
                    "points": 11}
