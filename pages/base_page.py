from playwright.sync_api import Page
from utils.logger import get_logger
from config.config_reader import SCREENSHOT_DIR
import re

logger = get_logger(__name__)


class BasePage:
    """
    Base class inherited by all page objects.
    Wraps common Playwright interactions so page classes stay clean and consistent.
    """

    def __init__(self, page: Page):
        # page is the Playwright browser tab — all interactions go through it
        self.page = page

    def navigate(self, url: str):
        logger.info(f"Navigating to: {url}")
        self.page.goto(url)

    def get_title(self) -> str:
        return self.page.title()

    def get_current_url(self) -> str:
        return self.page.url

    def wait_for_url(self, url_pattern: str):
        # Wraps the pattern in a wildcard regex so partial URL matches work cleanly
        self.page.wait_for_url(re.compile(f".*{url_pattern}.*"))

    def wait_for_selector(self, selector: str):
        # Playwright auto-waits on most actions — use this for explicit readiness checks
        self.page.wait_for_selector(selector)

    def take_screenshot(self, name: str):
        path = f"{SCREENSHOT_DIR}/{name}.png"
        self.page.screenshot(path=path)
        logger.info(f"Screenshot saved: {path}")