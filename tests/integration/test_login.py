UNKNOWN_EMAIL_MESSAGE = "Sorry, that email wasn&#39;t found."


def test_known_email_shows_summary(client):
    response = client.post(
        "/showSummary", data={"email": "john@simplylift.co"}
    )

    assert response.status_code == 200
    page = response.get_data(as_text=True)
    assert "Welcome, john@simplylift.co" in page
    assert "Points available: 13" in page


def test_unknown_email_redirects_to_index(client):
    response = client.post(
        "/showSummary", data={"email": "unknown@example.com"}
    )

    assert response.status_code == 302
    assert response.headers["Location"] == "/"


def test_unknown_email_displays_error_message(client):
    response = client.post(
        "/showSummary",
        data={"email": "unknown@example.com"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert UNKNOWN_EMAIL_MESSAGE in response.get_data(as_text=True)


def test_empty_email_displays_error_message(client):
    response = client.post(
        "/showSummary", data={"email": ""}, follow_redirects=True
    )

    assert response.status_code == 200
    assert UNKNOWN_EMAIL_MESSAGE in response.get_data(as_text=True)


def test_missing_email_field_displays_error_message(client):
    response = client.post("/showSummary", data={}, follow_redirects=True)

    assert response.status_code == 200
    assert UNKNOWN_EMAIL_MESSAGE in response.get_data(as_text=True)
