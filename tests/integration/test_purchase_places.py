NOT_ENOUGH_POINTS_MESSAGE = "Not enough points to book that many places."


def book(client, club, places, competition="Summer Cup"):
    return client.post(
        "/purchasePlaces",
        data={"club": club, "competition": competition, "places": places},
    )


def test_booking_within_points_is_confirmed(client):
    response = book(client, "Simply Lift", 2)

    assert response.status_code == 200
    assert "Great-booking complete!" in response.get_data(as_text=True)


def test_booking_more_places_than_points_is_refused(client):
    response = book(client, "Iron Temple", 5)

    assert response.status_code == 400
    page = response.get_data(as_text=True)
    assert NOT_ENOUGH_POINTS_MESSAGE in page
    assert "Great-booking complete!" not in page


def test_refused_booking_does_not_change_competition_places(
    client, competitions
):
    book(client, "Iron Temple", 5)

    assert competitions[1]["numberOfPlaces"] == "13"


def test_booking_form_limits_places_to_club_points(client):
    response = client.get("/book/Summer Cup/Iron Temple")

    assert response.status_code == 200
    assert 'max="4"' in response.get_data(as_text=True)
