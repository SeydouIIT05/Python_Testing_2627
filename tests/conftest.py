import pytest

import server


@pytest.fixture
def clubs():
    return [
        {
            "name": "Simply Lift",
            "email": "john@simplylift.co",
            "points": "13",
        },
        {
            "name": "Iron Temple",
            "email": "admin@irontemple.com",
            "points": "4",
        },
    ]


@pytest.fixture
def competitions():
    return [
        {
            "name": "Spring Festival",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "25",
        },
        {
            "name": "Summer Cup",
            "date": "2099-07-14 10:00:00",
            "numberOfPlaces": "13",
        },
    ]


@pytest.fixture
def client(monkeypatch, clubs, competitions):
    """Client de test Flask, isolé des fichiers JSON réels."""
    monkeypatch.setattr(server, "clubs", clubs)
    monkeypatch.setattr(server, "competitions", competitions)
    server.app.config["TESTING"] = True
    with server.app.test_client() as client:
        yield client
