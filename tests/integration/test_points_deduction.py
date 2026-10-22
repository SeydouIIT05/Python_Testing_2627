def book(client, club, places, competition="Summer Cup"):
    return client.post(
        "/purchasePlaces",
        data={"club": club, "competition": competition, "places": places},
    )


def test_booking_deducts_points_from_club(client, clubs):
    book(client, "Simply Lift", 2)

    assert clubs[0]["points"] == 11


def test_summary_shows_updated_points_after_booking(client):
    response = book(client, "Simply Lift", 2)

    assert "Points available: 11" in response.get_data(as_text=True)


def test_points_are_deducted_across_several_bookings(client, clubs):
    book(client, "Simply Lift", 2)
    book(client, "Simply Lift", 3)

    assert clubs[0]["points"] == 8


def test_refused_booking_does_not_deduct_points(client, clubs):
    book(client, "Iron Temple", 5)

    assert clubs[1]["points"] == "4"
