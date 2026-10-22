from server import findClubByEmail


def test_returns_club_when_email_is_known(clubs):
    club = findClubByEmail("john@simplylift.co", clubs)

    assert club["name"] == "Simply Lift"


def test_returns_none_when_email_is_unknown(clubs):
    assert findClubByEmail("unknown@example.com", clubs) is None


def test_returns_none_when_email_is_empty(clubs):
    assert findClubByEmail("", clubs) is None


def test_returns_none_when_there_are_no_clubs():
    assert findClubByEmail("john@simplylift.co", []) is None


def test_email_must_match_exactly(clubs):
    assert findClubByEmail("JOHN@SIMPLYLIFT.CO", clubs) is None


def test_returns_none_when_email_is_missing(clubs):
    assert findClubByEmail(None, clubs) is None
