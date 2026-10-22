from server import findClubByName, findCompetitionByName


def test_finds_club_by_its_name(clubs):
    assert findClubByName("Iron Temple", clubs)["points"] == "4"


def test_returns_none_for_unknown_club(clubs):
    assert findClubByName("Unknown Club", clubs) is None


def test_returns_none_when_club_name_is_missing(clubs):
    assert findClubByName(None, clubs) is None


def test_finds_competition_by_its_name(competitions):
    competition = findCompetitionByName("Summer Cup", competitions)

    assert competition["numberOfPlaces"] == "13"


def test_returns_none_for_unknown_competition(competitions):
    assert findCompetitionByName("Unknown Cup", competitions) is None


def test_returns_none_when_competition_name_is_missing(competitions):
    assert findCompetitionByName(None, competitions) is None
