import pytest


PAGES = ["/", "/pointsBoard", "/book/Summer Cup/Simply Lift"]


def summary_page(client, email="john@simplylift.co"):
    response = client.post("/showSummary", data={"email": email})
    return response.get_data(as_text=True)


def purchase(client, club, places):
    return client.post(
        "/purchasePlaces",
        data={"club": club, "competition": "Summer Cup", "places": places},
    ).get_data(as_text=True)


@pytest.mark.parametrize("url", PAGES)
def test_pages_are_html5_documents(client, url):
    page = client.get(url).get_data(as_text=True)

    assert page.lstrip().startswith("<!DOCTYPE html>")


@pytest.mark.parametrize("url", PAGES)
def test_pages_share_the_site_header(client, url):
    page = client.get(url).get_data(as_text=True)

    assert '<header class="site-header">' in page
    assert "GÜDLFT" in page


def test_summary_page_shares_the_site_header(client):
    assert '<header class="site-header">' in summary_page(client)


def test_summary_page_shows_club_name(client):
    assert '<p class="eyebrow">Simply Lift</p>' in summary_page(client)


def test_error_message_is_shown_as_an_error(client):
    response = client.post(
        "/showSummary", data={"email": "unknown@example.com"},
        follow_redirects=True,
    )

    assert 'class="flash flash-error"' in response.get_data(as_text=True)


def test_refused_booking_is_shown_as_an_error(client):
    assert 'class="flash flash-error"' in purchase(client, "Iron Temple", 5)


def test_booking_confirmation_is_shown_as_a_success(client):
    assert 'class="flash flash-success"' in purchase(client, "Simply Lift", 2)


def test_open_competition_has_open_badge_and_book_button(client):
    page = summary_page(client)

    assert '<span class="badge badge-open">Open</span>' in page
    assert (
        '<a class="button" href="/book/Summer%20Cup/Simply%20Lift">'
        'Book Places</a>'
    ) in page


def test_past_competition_has_closed_badge(client):
    page = summary_page(client)

    assert '<span class="badge badge-closed">Booking closed</span>' in page


def test_full_competition_has_full_badge_and_no_book_button(
    client, competitions
):
    competitions[1]["numberOfPlaces"] = "0"

    page = summary_page(client)

    assert '<span class="badge badge-full">Full</span>' in page
    assert "/book/Summer%20Cup/" not in page


def test_competition_dates_are_easy_to_read(client):
    assert "14 July 2099, 10:00" in summary_page(client)
