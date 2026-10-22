import threading

import pytest
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from werkzeug.serving import make_server

import server


@pytest.fixture(scope="session")
def live_server():
    """Lance l'application sur un port libre le temps des tests.

    Le serveur traite les requêtes en parallèle : sinon une connexion ouverte
    à l'avance par le navigateur peut bloquer les suivantes.
    """
    httpd = make_server("127.0.0.1", 0, server.app, threaded=True)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{httpd.server_port}"
    httpd.shutdown()


@pytest.fixture(scope="session")
def edge():
    """Navigateur Edge sans fenêtre, partagé par tous les tests."""
    options = webdriver.EdgeOptions()
    options.add_argument("--headless=new")
    try:
        driver = webdriver.Edge(options=options)
    except WebDriverException as error:
        pytest.skip(f"Edge indisponible : {error.msg}")
    driver.implicitly_wait(2)
    yield driver
    driver.quit()


@pytest.fixture
def site(live_server, monkeypatch, clubs, competitions):
    """Données de test neuves pour chaque test fonctionnel."""
    monkeypatch.setattr(server, "clubs", clubs)
    monkeypatch.setattr(server, "competitions", competitions)
    return live_server


@pytest.fixture
def browser(edge, site):
    edge.delete_all_cookies()
    return edge
