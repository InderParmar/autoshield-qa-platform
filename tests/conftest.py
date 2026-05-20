import pytest
from config.config_reader import BASE_URL
from pages.login_page import LoginPage


# ── Logged-in page fixture ─────────────────────────────────────────────────────
# Scope: function — logs in fresh per test using the session-registered user
# UI-specific — yields a Playwright page object positioned on the accounts overview
# All tests that need an authenticated browser session use this fixture
@pytest.fixture(scope="function")
def logged_in_page(page, registered_user):
    login_page = LoginPage(page)
    login_page.navigate_to_login(BASE_URL)
    login_page.login(registered_user["username"], registered_user["password"])
    yield page