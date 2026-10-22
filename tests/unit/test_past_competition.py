from datetime import datetime

from server import isPastCompetition


NOW = datetime(2026, 10, 22, 12, 0, 0)


def competition_on(date):
    return {"name": "Test Cup", "date": date}


def test_competition_in_a_previous_year_is_past():
    assert isPastCompetition(competition_on("2020-03-27 10:00:00"), NOW)


def test_competition_in_a_future_year_is_not_past():
    assert not isPastCompetition(competition_on("2099-07-14 10:00:00"), NOW)


def test_competition_earlier_today_is_past():
    assert isPastCompetition(competition_on("2026-10-22 09:00:00"), NOW)


def test_competition_later_today_is_not_past():
    assert not isPastCompetition(competition_on("2026-10-22 18:00:00"), NOW)


def test_uses_current_date_by_default_for_past_competition():
    assert isPastCompetition(competition_on("2000-01-01 10:00:00"))


def test_uses_current_date_by_default_for_future_competition():
    assert not isPastCompetition(competition_on("2999-01-01 10:00:00"))
