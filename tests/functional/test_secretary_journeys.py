import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


pytestmark = pytest.mark.functional


def page_text(browser):
    return browser.find_element(By.TAG_NAME, "body").text


def click_and_wait(browser, element):
    """Clique puis attend que la page suivante soit chargée."""
    current_page = browser.find_element(By.TAG_NAME, "html")
    element.click()
    WebDriverWait(browser, 5).until(EC.staleness_of(current_page))


def log_in(browser, site, email):
    browser.get(site)
    browser.find_element(By.ID, "email").send_keys(email)
    click_and_wait(browser, browser.find_element(By.TAG_NAME, "button"))


def open_booking_page(browser):
    click_and_wait(browser, browser.find_element(By.LINK_TEXT, "Book Places"))


def test_secretary_logs_in_and_sees_points_and_competitions(browser, site):
    log_in(browser, site, "john@simplylift.co")

    text = page_text(browser)
    assert "Welcome, john@simplylift.co" in text
    assert "Points available: 13" in text
    assert "Summer Cup" in text


def test_unknown_email_shows_error_message(browser, site):
    log_in(browser, site, "unknown@example.com")

    assert "Sorry, that email wasn't found." in page_text(browser)


def test_secretary_books_places_and_points_are_deducted(browser, site):
    log_in(browser, site, "john@simplylift.co")
    open_booking_page(browser)

    browser.find_element(By.ID, "places").send_keys("3")
    click_and_wait(browser, browser.find_element(By.TAG_NAME, "button"))

    text = page_text(browser)
    assert "3 places booked for Summer Cup." in text
    assert "Points available: 10" in text


def test_booking_form_blocks_more_places_than_club_points(browser, site):
    log_in(browser, site, "admin@irontemple.com")
    open_booking_page(browser)
    booking_page = browser.current_url

    field = browser.find_element(By.ID, "places")
    field.send_keys("5")
    browser.find_element(By.TAG_NAME, "button").click()

    assert browser.current_url == booking_page
    assert browser.execute_script(
        "return arguments[0].validity.rangeOverflow", field
    )


def test_past_competition_cannot_be_booked(browser, site):
    log_in(browser, site, "john@simplylift.co")

    assert "BOOKING CLOSED" in page_text(browser).upper()
    assert len(browser.find_elements(By.LINK_TEXT, "Book Places")) == 1


def test_points_board_is_visible_without_logging_in(browser, site):
    browser.get(site)

    link = browser.find_element(By.LINK_TEXT, "See the clubs points board")
    click_and_wait(browser, link)

    rows = [row.text for row in browser.find_elements(By.TAG_NAME, "tr")]
    assert rows[1:] == ["Simply Lift 13", "Iron Temple 4"]


def test_secretary_can_log_out(browser, site):
    log_in(browser, site, "john@simplylift.co")

    click_and_wait(browser, browser.find_element(By.LINK_TEXT, "Logout"))

    assert "Welcome to the GUDLFT Registration Portal!" in page_text(browser)
