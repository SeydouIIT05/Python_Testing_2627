import pytest


INVALID_PLACES_MESSAGE = "Please enter a valid number of places (at least 1)."


@pytest.mark.parametrize("places", ["0", "-5", "abc", "", "2.5"])
def test_invalid_number_of_places_is_refused(
    client, clubs, competitions, places
):
    response = client.post(
        "/purchasePlaces",
        data={"club": "Simply Lift", "competition": "Summer Cup",
              "places": places},
    )

    assert response.status_code == 400
    assert INVALID_PLACES_MESSAGE in response.get_data(as_text=True)
    assert competitions[1]["numberOfPlaces"] == "13"
    assert clubs[0]["points"] == "13"


def test_missing_number_of_places_is_refused(client):
    response = client.post(
        "/purchasePlaces",
        data={"club": "Simply Lift", "competition": "Summer Cup"},
    )

    assert response.status_code == 400
    assert INVALID_PLACES_MESSAGE in response.get_data(as_text=True)


def test_booking_form_requires_at_least_one_place(client):
    page = client.get("/book/Summer Cup/Simply Lift").get_data(as_text=True)

    assert 'min="1"' in page
    assert "required" in page
