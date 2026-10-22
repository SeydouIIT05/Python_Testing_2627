from datetime import datetime

from server import competitionStatus, displayDate


NOW = datetime(2026, 10, 22, 12, 0, 0)


def competition(date="2099-07-14 10:00:00", places="13"):
    return {"name": "Test Cup", "date": date, "numberOfPlaces": places}


def test_future_competition_with_places_is_open():
    assert competitionStatus(competition(), NOW) == "open"


def test_future_competition_without_places_is_full():
    assert competitionStatus(competition(places="0"), NOW) == "full"


def test_full_competition_after_bookings_is_full():
    assert competitionStatus(competition(places=0), NOW) == "full"


def test_past_competition_is_closed():
    assert competitionStatus(
        competition(date="2020-03-27 10:00:00"), NOW
    ) == "closed"


def test_past_and_full_competition_is_closed():
    assert competitionStatus(
        competition(date="2020-03-27 10:00:00", places="0"), NOW
    ) == "closed"


def test_date_is_displayed_in_words():
    assert displayDate("2099-07-14 10:00:00") == "14 July 2099, 10:00"


def test_single_digit_day_has_no_leading_zero():
    assert displayDate("2027-02-05 09:05:00") == "5 February 2027, 09:05"
