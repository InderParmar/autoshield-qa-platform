import pytest
import uuid
import json
import re
from playwright.sync_api import Browser, BrowserContext, Page, expect
from config.config_reader import BASE_URL
from pages.login_page import LoginPage
from pages.registration_page import RegistrationPage
from utils import wait_helper
from utils.logger import get_logger

logger = get_logger(__name__)


# ── Browser fixture ────────────────────────────────────────────────────────────
# Scope: session — one browser instance for the entire test run
# --browser controls which browser; --headed runs visibly (default: headless)
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

    # Generate a unique username to avoid conflicts on repeated runs
    user_data = test_data["valid_user"].copy()
    user_data["username"] = f"{user_data.get('username')}{str(uuid.uuid4())[:6]}"
    registration_page.register(user_data)

    # Confirm registration succeeded before proceeding
    expect(registration_page.get_success_locator()).to_contain_text(
        f"Welcome {user_data['username']}", timeout=5000
    )

    # ── Open a second account ──────────────────────────────────────────────────
    # Transfer tests require two distinct accounts — ParaBank creates only one on registration
    registration_page.navigate(f"{BASE_URL}/openaccount.htm")
    page.wait_for_url("**/openaccount.htm", timeout=5000)
    page.locator("select#type").select_option(index=1)

    # CRITICAL: Wait for the 'From Account' dropdown to populate via AJAX before submitting
    # Clicking before this loads causes a silent backend failure — the form sends no account ID
    page.locator("select#fromAccountId option").first.wait_for(state="attached")
    page.locator("input[value='Open New Account']").click()

    # Verify the new account was created and has a valid 5-digit ID
    expect(page.locator("div[id='openAccountResult'] p b")).to_contain_text(
        "Your new account number", timeout=5000
    )
    expect(page.locator("#newAccountId")).to_have_text(re.compile(r"\d{5}"), timeout=5000)
    new_account_id = page.locator("#newAccountId").text_content()
    logger.debug(f"Second account opened successfully — account ID: {new_account_id}")

    # ── Confirm second account is visible in overview before any test runs ─────
    # ParaBank's overview loads accounts via AJAX — poll until the second row appears
    max_retries = 10
    for _ in range(max_retries):
        page.goto(f"{BASE_URL}/overview.htm")
        if wait_helper.check_with_timeout(
            page, "tbody tr:nth-child(2) td:nth-child(1)", timeout=2000
        ):
            break
    else:
        raise RuntimeError(
            "Second account did not appear in overview after opening — "
            f"new account ID was: {new_account_id}"
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