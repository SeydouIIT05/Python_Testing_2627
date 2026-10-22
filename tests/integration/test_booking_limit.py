BOOKING_LIMIT_MESSAGE = "You cannot book more than 12 places per competition."


def book(client, club, places, competition="Summer Cup"):
    return client.post(
        "/purchasePlaces",
        data={"club": club, "competition": competition, "places": places},
    )


def test_booking_12_places_is_confirmed(client):
    response = book(client, "Simply Lift", 12)

    assert response.status_code == 200
    assert "Great-booking complete!" in response.get_data(as_text=True)


def test_booking_13_places_is_refused(client, clubs, competitions):
    response = book(client, "Simply Lift", 13)

    assert response.status_code == 400
    assert BOOKING_LIMIT_MESSAGE in response.get_data(as_text=True)
    assert competitions[1]["numberOfPlaces"] == "13"
    assert clubs[0]["points"] == "13"


def test_bookings_in_several_steps_are_limited_to_12(client):
    book(client, "Simply Lift", 10)
    response = book(client, "Simply Lift", 3)

    assert response.status_code == 400
    assert BOOKING_LIMIT_MESSAGE in response.get_data(as_text=True)


def test_booking_form_limits_places_to_12(client):
    response = client.get("/book/Summer Cup/Simply Lift")

    assert 'max="12"' in response.get_data(as_text=True)


def test_booking_form_accounts_for_previous_bookings(client):
    book(client, "Simply Lift", 10)
    response = client.get("/book/Summer Cup/Simply Lift")

    assert 'max="2"' in response.get_data(as_text=True)
