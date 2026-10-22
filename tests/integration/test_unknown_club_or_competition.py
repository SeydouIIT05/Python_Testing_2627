CLUB_NOT_FOUND = "Sorry, that club was not found."
COMPETITION_NOT_FOUND = "Sorry, that competition was not found."


def purchase(client, data, follow_redirects=False):
    return client.post(
        "/purchasePlaces", data=data, follow_redirects=follow_redirects
    )


def test_booking_page_of_unknown_competition_shows_summary_with_error(
    client
):
    response = client.get("/book/Unknown Cup/Simply Lift")

    assert response.status_code == 404
    page = response.get_data(as_text=True)
    assert COMPETITION_NOT_FOUND in page
    assert "Welcome, john@simplylift.co" in page


def test_booking_page_of_unknown_club_redirects_to_login(client):
    response = client.get("/book/Summer Cup/Unknown Club")

    assert response.status_code == 302
    assert response.headers["Location"] == "/"


def test_booking_page_of_unknown_club_displays_error(client):
    response = client.get(
        "/book/Summer Cup/Unknown Club", follow_redirects=True
    )

    assert CLUB_NOT_FOUND in response.get_data(as_text=True)


def test_purchase_in_unknown_competition_is_refused(client, clubs):
    response = purchase(
        client,
        {"club": "Simply Lift", "competition": "Unknown Cup", "places": 2},
    )

    assert response.status_code == 404
    assert COMPETITION_NOT_FOUND in response.get_data(as_text=True)
    assert clubs[0]["points"] == "13"


def test_purchase_for_unknown_club_is_refused(client, competitions):
    response = purchase(
        client,
        {"club": "Unknown Club", "competition": "Summer Cup", "places": 2},
        follow_redirects=True,
    )

    assert CLUB_NOT_FOUND in response.get_data(as_text=True)
    assert competitions[1]["numberOfPlaces"] == "13"


def test_purchase_without_club_and_competition_is_refused(client):
    response = purchase(client, {"places": 2}, follow_redirects=True)

    assert response.status_code == 200
    assert CLUB_NOT_FOUND in response.get_data(as_text=True)
