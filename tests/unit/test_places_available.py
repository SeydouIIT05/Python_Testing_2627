import pytest

from server import hasEnoughPlaces, maxPlacesBookable, placesLeftMessage


def test_enough_places_when_booking_fewer_than_available():
    assert hasEnoughPlaces({"numberOfPlaces": "13"}, 5) is True


def test_enough_places_when_booking_all_places_left():
    assert hasEnoughPlaces({"numberOfPlaces": "13"}, 13) is True


def test_not_enough_places_when_booking_more_than_available():
    assert hasEnoughPlaces({"numberOfPlaces": "13"}, 14) is False


def test_not_enough_places_when_competition_is_full():
    assert hasEnoughPlaces({"numberOfPlaces": "0"}, 1) is False


def test_enough_places_after_previous_bookings():
    assert hasEnoughPlaces({"numberOfPlaces": 3}, 3) is True


def test_message_says_competition_is_full_when_no_places_left():
    message = placesLeftMessage({"numberOfPlaces": 0})

    assert message == "This competition is full."


def test_message_gives_number_of_places_left():
    message = placesLeftMessage({"numberOfPlaces": "3"})

    assert message == (
        "Not enough places left in this competition: 3 available."
    )


def test_max_places_is_limited_by_places_available():
    club = {"name": "Simply Lift", "points": "13"}

    assert maxPlacesBookable(club, {"numberOfPlaces": "5"}) == 5


@pytest.mark.parametrize(
    "placesLeft, places, expected",
    [(0, 1, False), ("25", 25, True), ("25", 26, False), (1, 1, True)],
)
def test_places_available_cases(placesLeft, places, expected):
    competition = {"numberOfPlaces": placesLeft}

    assert hasEnoughPlaces(competition, places) is expected


def test_message_says_full_when_places_left_is_text_zero():
    assert placesLeftMessage({"numberOfPlaces": "0"}) == (
        "This competition is full."
    )


@pytest.mark.parametrize("placesLeft", [1, "12", 25])
def test_message_gives_any_number_of_places_left(placesLeft):
    message = placesLeftMessage({"numberOfPlaces": placesLeft})

    assert message.endswith(f": {placesLeft} available.")
