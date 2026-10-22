import pytest


BOOKING_PAGE = "/book/Summer Cup/Simply Lift"


def test_confirmation_shows_number_of_places_booked(client):
    response = client.post(
        "/purchasePlaces",
        data={"club": "Simply Lift", "competition": "Summer Cup",
              "places": 3},
    )

    assert "3 places booked for Summer Cup." in response.get_data(
        as_text=True
    )


def test_booking_page_shows_club_points(client):
    page = client.get(BOOKING_PAGE).get_data(as_text=True)

    assert "Points available: 13" in page


def test_booking_page_says_how_many_places_can_be_booked(client):
    page = client.get(BOOKING_PAGE).get_data(as_text=True)

    assert "You can book up to 12 places." in page


def test_booking_page_uses_singular_for_one_place(client, competitions):
    competitions[1]["numberOfPlaces"] = "1"

    page = client.get(BOOKING_PAGE).get_data(as_text=True)

    assert "You can book up to 1 place." in page


def test_booking_page_says_when_no_more_places_can_be_booked(
    client, competitions
):
    competitions[1]["bookings"] = {"Simply Lift": 12}

    page = client.get(BOOKING_PAGE).get_data(as_text=True)

    assert "No more places can be booked" in page
    assert "<form" not in page


def test_places_label_is_linked_to_its_field(client):
    page = client.get(BOOKING_PAGE).get_data(as_text=True)

    assert '<label for="places">' in page
    assert 'id="places"' in page


def test_email_label_is_linked_to_its_field(client):
    page = client.get("/").get_data(as_text=True)

    assert '<label for="email">' in page
    assert 'id="email"' in page


@pytest.mark.parametrize("url", ["/", "/pointsBoard", BOOKING_PAGE])
def test_pages_use_the_shared_stylesheet(client, url):
    page = client.get(url).get_data(as_text=True)

    assert 'href="/static/style.css"' in page


def test_summary_page_shows_points_on_their_own_line(client):
    response = client.post(
        "/showSummary", data={"email": "john@simplylift.co"}
    )

    assert "<p>Points available: 13</p>" in response.get_data(as_text=True)


def test_summary_page_uses_the_shared_stylesheet(client):
    response = client.post(
        "/showSummary", data={"email": "john@simplylift.co"}
    )

    assert 'href="/static/style.css"' in response.get_data(as_text=True)


def test_shared_stylesheet_is_served(client):
    response = client.get("/static/style.css")

    assert response.status_code == 200
    response.close()
