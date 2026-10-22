from server import sortClubsByPoints


def names(listOfClubs):
    return [club["name"] for club in listOfClubs]


def test_clubs_are_sorted_by_points_from_highest_to_lowest():
    listOfClubs = [
        {"name": "Iron Temple", "points": "4"},
        {"name": "Simply Lift", "points": "13"},
        {"name": "She Lifts", "points": "12"},
    ]

    assert names(sortClubsByPoints(listOfClubs)) == [
        "Simply Lift", "She Lifts", "Iron Temple"
    ]


def test_clubs_with_same_points_are_sorted_by_name():
    listOfClubs = [
        {"name": "Simply Lift", "points": "5"},
        {"name": "Iron Temple", "points": "5"},
    ]

    assert names(sortClubsByPoints(listOfClubs)) == [
        "Iron Temple", "Simply Lift"
    ]


def test_points_already_updated_are_compared_as_numbers():
    listOfClubs = [
        {"name": "Simply Lift", "points": 9},
        {"name": "She Lifts", "points": "12"},
    ]

    assert names(sortClubsByPoints(listOfClubs)) == [
        "She Lifts", "Simply Lift"
    ]


def test_original_list_is_not_modified():
    listOfClubs = [
        {"name": "Iron Temple", "points": "4"},
        {"name": "Simply Lift", "points": "13"},
    ]

    sortClubsByPoints(listOfClubs)

    assert names(listOfClubs) == ["Iron Temple", "Simply Lift"]


def test_empty_list_gives_empty_board():
    assert sortClubsByPoints([]) == []
