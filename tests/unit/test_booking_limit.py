import pytest

from server import (
    isWithinBookingLimit,
    maxPlacesBookable,
    placesBookedBy,
    recordBooking,
)


SIMPLY_LIFT = {"name": "Simply Lift", "points": "13"}


def test_within_limit_when_booking_12_places():
    assert isWithinBookingLimit(SIMPLY_LIFT, {}, 12) is True


def test_exceeds_limit_when_booking_13_places():
    assert isWithinBookingLimit(SIMPLY_LIFT, {}, 13) is False


def test_exceeds_limit_when_previous_bookings_add_up_to_more_than_12():
    competition = {"bookings": {"Simply Lift": 10}}

    assert isWithinBookingLimit(SIMPLY_LIFT, competition, 3) is False


def test_within_limit_when_previous_bookings_leave_room():
    competition = {"bookings": {"Simply Lift": 10}}

    assert isWithinBookingLimit(SIMPLY_LIFT, competition, 2) is True


def test_limit_applies_to_each_club_separately():
    competition = {"bookings": {"Iron Temple": 12}}

    assert isWithinBookingLimit(SIMPLY_LIFT, competition, 12) is True


def test_records_first_booking_of_a_club():
    competition = {}

    recordBooking(SIMPLY_LIFT, competition, 5)

    assert competition["bookings"] == {"Simply Lift": 5}


def test_adds_new_booking_to_previous_ones():
    competition = {"bookings": {"Simply Lift": 5}}

    recordBooking(SIMPLY_LIFT, competition, 3)

    assert competition["bookings"] == {"Simply Lift": 8}


def test_max_places_is_limited_by_club_points():
    club = {"name": "Iron Temple", "points": "4"}

    assert maxPlacesBookable(club, {"numberOfPlaces": "25"}) == 4


def test_max_places_is_limited_to_12():
    assert maxPlacesBookable(SIMPLY_LIFT, {"numberOfPlaces": "25"}) == 12


def test_max_places_accounts_for_previous_bookings():
    competition = {"numberOfPlaces": "25", "bookings": {"Simply Lift": 10}}

    assert maxPlacesBookable(SIMPLY_LIFT, competition) == 2


@pytest.mark.parametrize(
    "alreadyBooked, places, expected",
    [
        (0, 1, True),
        (0, 11, True),
        (11, 1, True),
        (11, 2, False),
        (12, 1, False),
        (6, 6, True),
        (6, 7, False),
    ],
)
def test_booking_limit_cases(alreadyBooked, places, expected):
    competition = {"bookings": {"Simply Lift": alreadyBooked}}

    assert isWithinBookingLimit(SIMPLY_LIFT, competition, places) is expected


def test_no_places_booked_when_competition_has_no_bookings():
    assert placesBookedBy(SIMPLY_LIFT, {}) == 0


def test_no_places_booked_when_only_other_clubs_booked():
    competition = {"bookings": {"Iron Temple": 4}}

    assert placesBookedBy(SIMPLY_LIFT, competition) == 0


def test_places_booked_by_the_club_are_returned():
    competition = {"bookings": {"Iron Temple": 4, "Simply Lift": 7}}

    assert placesBookedBy(SIMPLY_LIFT, competition) == 7


def test_bookings_of_other_clubs_are_kept():
    competition = {"bookings": {"Iron Temple": 4}}

    recordBooking(SIMPLY_LIFT, competition, 2)

    assert competition["bookings"] == {"Iron Temple": 4, "Simply Lift": 2}


def test_several_bookings_add_up():
    competition = {}

    for places in (1, 2, 3):
        recordBooking(SIMPLY_LIFT, competition, places)

    assert competition["bookings"] == {"Simply Lift": 6}


@pytest.mark.parametrize(
    "points, alreadyBooked, placesLeft, expected",
    [
        ("20", 0, "25", 12),
        ("5", 0, "25", 5),
        ("20", 10, "25", 2),
        ("20", 0, "3", 3),
        ("0", 0, "25", 0),
        ("20", 12, "25", 0),
        ("20", 0, 0, 0),
    ],
)
def test_max_places_cases(points, alreadyBooked, placesLeft, expected):
    club = {"name": "Simply Lift", "points": points}
    competition = {
        "numberOfPlaces": placesLeft,
        "bookings": {"Simply Lift": alreadyBooked},
    }

    assert maxPlacesBookable(club, competition) == expected
