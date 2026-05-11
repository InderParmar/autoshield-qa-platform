import pytest
from playwright.sync_api import Browser, BrowserContext, Page
from config.config_reader import BASE_URL


@pytest.fixture(scope="session")
def browser_instance(playwright, pytestconfig):
    browser_name = pytestconfig.getoption("--browser", default="chromium")
    browser = getattr(playwright, browser_name).launch(headless=True)
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def context(browser_instance: Browser) -> BrowserContext:
    context = browser_instance.new_context()
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Page:
    page = context.new_page()
    yield page
    page.close()


@pytest.fixture(scope="session")
def base_url() -> str:
    return BASE_URL