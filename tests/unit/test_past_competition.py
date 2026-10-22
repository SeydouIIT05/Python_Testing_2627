from datetime import datetime

import pytest

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


@pytest.mark.parametrize(
    "date, expected",
    [
        ("2026-10-22 11:59:59", True),
        ("2026-10-22 12:00:00", False),
        ("2026-10-22 12:00:01", False),
        ("2025-12-31 23:59:59", True),
        ("2027-01-01 00:00:00", False),
    ],
)
def test_boundary_dates(date, expected):
    assert isPastCompetition(competition_on(date), NOW) is expected


def test_invalid_date_format_is_rejected():
    with pytest.raises(ValueError):
        isPastCompetition(competition_on("22/10/2026"), NOW)
