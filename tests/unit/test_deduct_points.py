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
