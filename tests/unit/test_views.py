import pytest

import server


@pytest.fixture
def rendered(monkeypatch):
    """Appelle les vues directement, sans passer par HTTP ni les templates."""
    monkeypatch.setattr(
        server, "render_template",
        lambda template, **context: (template, context),
    )
    with server.app.test_request_context():
        yield


def test_index_view_renders_login_page(rendered):
    assert server.index() == ("index.html", {})


def test_points_board_view_passes_clubs_sorted_by_points(
    rendered, monkeypatch
):
    monkeypatch.setattr(server, "clubs", [
        {"name": "Iron Temple", "points": "4"},
        {"name": "Simply Lift", "points": "13"},
    ])

    template, context = server.pointsBoard()

    assert template == "points.html"
    assert [club["name"] for club in context["clubs"]] == [
        "Simply Lift", "Iron Temple"
    ]


def test_logout_view_redirects_to_login_page(rendered):
    response = server.logout()

    assert response.status_code == 302
    assert response.headers["Location"] == "/"
