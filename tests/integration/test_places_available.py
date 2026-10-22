def book(client, club, places, competition="Summer Cup"):
    return client.post(
        "/purchasePlaces",
        data={"club": club, "competition": competition, "places": places},
    )


def test_booking_more_places_than_available_is_refused(
    client, clubs, competitions
):
    competitions[1]["numberOfPlaces"] = "3"

    response = book(client, "Simply Lift", 5)

    assert response.status_code == 400
    assert (
        "Not enough places left in this competition: 3 available."
        in response.get_data(as_text=True)
    )
    assert competitions[1]["numberOfPlaces"] == "3"
    assert clubs[0]["points"] == "13"


def test_booking_all_remaining_places_is_confirmed(client, competitions):
    competitions[1]["numberOfPlaces"] = "3"

    response = book(client, "Simply Lift", 3)

    assert response.status_code == 200
    assert competitions[1]["numberOfPlaces"] == 0


def test_booking_in_full_competition_says_it_is_full(client, competitions):
    competitions[1]["numberOfPlaces"] = "0"

    response = book(client, "Simply Lift", 1)

    assert response.status_code == 400
    assert "This competition is full." in response.get_data(as_text=True)


def test_booking_form_limits_places_to_places_available(
    client, competitions
):
    competitions[1]["numberOfPlaces"] = "3"

    response = client.get("/book/Summer Cup/Simply Lift")

    assert 'max="3"' in response.get_data(as_text=True)
