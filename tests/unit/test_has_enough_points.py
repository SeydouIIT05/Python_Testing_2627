from server import hasEnoughPoints


def test_true_when_places_are_below_points():
    assert hasEnoughPoints({"points": "13"}, 5) is True


def test_true_when_places_equal_points():
    assert hasEnoughPoints({"points": "4"}, 4) is True


def test_false_when_places_exceed_points():
    assert hasEnoughPoints({"points": "4"}, 5) is False


def test_false_when_club_has_no_points():
    assert hasEnoughPoints({"points": "0"}, 1) is False
