import json
from datetime import datetime
from pathlib import Path

import pytest

from server import loadClubs, loadCompetitions


PROJECT_ROOT = Path(__file__).resolve().parents[2]
REAL_CLUBS = json.loads((PROJECT_ROOT / "clubs.json").read_text())["clubs"]
REAL_COMPETITIONS = json.loads(
    (PROJECT_ROOT / "competitions.json").read_text()
)["competitions"]

TEST_CLUB = {"name": "Test Club", "email": "test@club.com", "points": "5"}
TEST_COMPETITION = {
    "name": "Test Cup",
    "date": "2099-01-01 10:00:00",
    "numberOfPlaces": "10",
}


def write_json(folder, name, content):
    (folder / name).write_text(json.dumps(content))


def test_load_clubs_reads_clubs_from_json_file(tmp_path, monkeypatch):
    write_json(tmp_path, "clubs.json", {"clubs": [TEST_CLUB]})
    monkeypatch.chdir(tmp_path)

    assert loadClubs() == [TEST_CLUB]


def test_load_clubs_returns_empty_list_when_file_has_no_club(
    tmp_path, monkeypatch
):
    write_json(tmp_path, "clubs.json", {"clubs": []})
    monkeypatch.chdir(tmp_path)

    assert loadClubs() == []


def test_load_competitions_reads_competitions_from_json_file(
    tmp_path, monkeypatch
):
    write_json(
        tmp_path, "competitions.json", {"competitions": [TEST_COMPETITION]}
    )
    monkeypatch.chdir(tmp_path)

    assert loadCompetitions() == [TEST_COMPETITION]


def test_load_competitions_returns_empty_list_when_file_has_none(
    tmp_path, monkeypatch
):
    write_json(tmp_path, "competitions.json", {"competitions": []})
    monkeypatch.chdir(tmp_path)

    assert loadCompetitions() == []


@pytest.mark.parametrize("club", REAL_CLUBS, ids=lambda club: club["name"])
def test_each_real_club_has_name_email_and_points(club):
    assert club["name"]
    assert "@" in club["email"]
    assert int(club["points"]) >= 0


def test_real_club_emails_are_unique():
    emails = [club["email"] for club in REAL_CLUBS]

    assert len(emails) == len(set(emails))


def test_real_club_names_are_unique():
    names = [club["name"] for club in REAL_CLUBS]

    assert len(names) == len(set(names))


@pytest.mark.parametrize(
    "competition", REAL_COMPETITIONS, ids=lambda comp: comp["name"]
)
def test_each_real_competition_has_valid_date_and_places(competition):
    datetime.strptime(competition["date"], "%Y-%m-%d %H:%M:%S")
    assert int(competition["numberOfPlaces"]) >= 0


def test_real_competition_names_are_unique():
    names = [competition["name"] for competition in REAL_COMPETITIONS]

    assert len(names) == len(set(names))
