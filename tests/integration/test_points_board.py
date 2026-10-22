def test_points_board_is_public(client):
    response = client.get("/pointsBoard")

    assert response.status_code == 200


def test_points_board_shows_points_of_every_club(client):
    page = client.get("/pointsBoard").get_data(as_text=True)

    assert "<td>Simply Lift</td><td>13</td>" in page
    assert "<td>Iron Temple</td><td>4</td>" in page


def test_points_board_lists_highest_points_first(client):
    page = client.get("/pointsBoard").get_data(as_text=True)

    assert page.index("Simply Lift") < page.index("Iron Temple")


def test_points_board_shows_points_after_a_booking(client):
    client.post(
        "/purchasePlaces",
        data={"club": "Simply Lift", "competition": "Summer Cup",
              "places": 2},
    )

    page = client.get("/pointsBoard").get_data(as_text=True)

    assert "<td>Simply Lift</td><td>11</td>" in page


def test_points_board_is_read_only(client):
    page = client.get("/pointsBoard").get_data(as_text=True)

    assert "<form" not in page
    assert client.post("/pointsBoard").status_code == 405


def test_login_page_links_to_points_board(client):
    page = client.get("/").get_data(as_text=True)

    assert 'href="/pointsBoard"' in page


def test_summary_page_links_to_points_board(client):
    response = client.post(
        "/showSummary", data={"email": "john@simplylift.co"}
    )

    assert 'href="/pointsBoard"' in response.get_data(as_text=True)
