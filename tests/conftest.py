import pytest
from playwright.sync_api import Browser, BrowserContext, Page, expect
from config.config_reader import BASE_URL
import uuid
import json
from pages.login_page import LoginPage
from pages.registration_page import RegistrationPage


# ── Browser fixture ────────────────────────────────────────────────────────────
# Scope: session — one browser instance for the entire test run
# --browser flag controls which browser; --headed flag runs visibly (default: headless)
@pytest.fixture(scope="session")
def browser_instance(playwright, pytestconfig):
    browser_name = pytestconfig.getoption("--browser")
    browser_name = browser_name[0] if browser_name else "chromium"
    headless = not pytestconfig.getoption("--headed", default=False)
    browser = getattr(playwright, browser_name).launch(headless=headless)
    yield browser
    browser.close()


# ── Context fixture ────────────────────────────────────────────────────────────
# Scope: function — fresh isolated browser session per test
# Cookies, localStorage, and auth state are wiped between every test
@pytest.fixture(scope="function")
def context(browser_instance: Browser) -> BrowserContext:
    context = browser_instance.new_context()
    yield context
    context.close()


# ── Page fixture ───────────────────────────────────────────────────────────────
# Scope: function — fresh tab per test, created from the fresh context above
@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Page:
    page = context.new_page()
    yield page
    page.close()


# ── Registered user fixture ────────────────────────────────────────────────────
# Scope: session — registers one user once for the entire test run
# Returns a dict with username and password so logged_in_page can log in correctly
# Uses a uuid suffix to guarantee a unique username on every run
@pytest.fixture(scope="session")
def registered_user(browser_instance, base_url, test_data):
    context = browser_instance.new_context()
    page = context.new_page()
    registration_page = RegistrationPage(page)

    registration_page.navigate_to_registration(base_url)

    user_data = test_data["valid_user"].copy()
    user_data["username"] = f"{user_data.get('username')}{str(uuid.uuid4())[:6]}"
    registration_page.register(user_data)

    # Confirm registration succeeded before allowing any test to proceed
    expect(registration_page.get_success_locator()).to_contain_text(
        f"Welcome {user_data['username']}", timeout=5000
    )

    context.close()

    return {"username": user_data["username"], "password": user_data["password"]}


# ── Logged-in page fixture ─────────────────────────────────────────────────────
# Scope: function — logs in fresh per test using the session-registered user
# Yields the page so tests can interact directly with the browser after login
@pytest.fixture(scope="function")
def logged_in_page(page, registered_user):
    login_page = LoginPage(page)
    login_page.navigate_to_login(BASE_URL)
    login_page.login(registered_user["username"], registered_user["password"])
    yield page


# ── Base URL fixture ───────────────────────────────────────────────────────────
@pytest.fixture(scope="session")
def base_url() -> str:
    return BASE_URL


# ── Test data fixture ──────────────────────────────────────────────────────────
# Scope: session — loads registration_data.json once and shares it across all tests
@pytest.fixture(scope="session")
def test_data():
    with open("test_data/registration_data.json") as f:
        return json.load(f)