import pytest
from flask import get_flashed_messages

import server


CLUB = {"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"}
COMPETITION = {"name": "Summer Cup", "numberOfPlaces": "13"}


@pytest.fixture
def rendered(monkeypatch):
    """Remplace render_template pour tester les fonctions sans templates."""
    monkeypatch.setattr(
        server, "render_template",
        lambda template, **context: (template, context),
    )
    with server.app.test_request_context():
        yield


def test_booking_error_shows_booking_page_with_status_400(rendered):
    (template, context), status = server.renderBookingError(
        "Some error", CLUB, COMPETITION
    )

    assert template == "booking.html"
    assert status == 400


def test_booking_error_keeps_form_limit(rendered):
    (template, context), status = server.renderBookingError(
        "Some error", CLUB, COMPETITION
    )

    assert context["maxPlaces"] == 12


def test_booking_error_flashes_its_message(rendered):
    server.renderBookingError("Some error", CLUB, COMPETITION)

    assert get_flashed_messages() == ["Some error"]


def test_summary_error_shows_summary_with_status_400_by_default(rendered):
    (template, context), status = server.renderSummaryError(
        "Some error", CLUB
    )

    assert template == "welcome.html"
    assert context["club"] == CLUB
    assert status == 400


def test_summary_error_can_use_another_status(rendered):
    (template, context), status = server.renderSummaryError(
        "Not found", CLUB, 404
    )

    assert status == 404
    assert get_flashed_messages() == ["Not found"]
