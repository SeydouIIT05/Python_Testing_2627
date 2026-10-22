from server import isWithinBookingLimit, maxPlacesBookable, recordBooking


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
