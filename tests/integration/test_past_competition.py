PAST_COMPETITION_MESSAGE = (
    "Booking is closed: this competition has already taken place."
)


def login(client, email="john@simplylift.co"):
    return client.post("/showSummary", data={"email": email})


def test_booking_page_of_past_competition_is_refused(client):
    response = client.get("/book/Spring Festival/Simply Lift")

    assert response.status_code == 400
    page = response.get_data(as_text=True)
    assert PAST_COMPETITION_MESSAGE in page
    assert "How many places?" not in page


def test_booking_page_of_future_competition_is_displayed(client):
    response = client.get("/book/Summer Cup/Simply Lift")

    assert response.status_code == 200
    assert "How many places?" in response.get_data(as_text=True)


def test_purchase_in_past_competition_is_refused(client, clubs, competitions):
    response = client.post(
        "/purchasePlaces",
        data={"club": "Simply Lift", "competition": "Spring Festival",
              "places": 2},
    )

    assert response.status_code == 400
    assert PAST_COMPETITION_MESSAGE in response.get_data(as_text=True)
    assert competitions[0]["numberOfPlaces"] == "25"
    assert clubs[0]["points"] == "13"


def test_summary_still_lists_past_competitions(client):
    page = login(client).get_data(as_text=True)

    assert "Spring Festival" in page


def test_summary_has_booking_link_only_for_future_competitions(client):
    page = login(client).get_data(as_text=True)

    assert "/book/Spring%20Festival/" not in page
    assert "/book/Summer%20Cup/" in page
