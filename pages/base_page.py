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
        # domcontentloaded is faster than networkidle and sufficient for ParaBank
        # Individual page objects call wait_for_selector for their key element after navigation
        self.page.goto(url, wait_until="domcontentloaded")

    def get_title(self) -> str:
        return self.page.title()

    def get_current_url(self) -> str:
        return self.page.url

    def wait_for_url(self, url_pattern: str):
        # Wraps the pattern in a wildcard regex so partial URL matches work cleanly
        self.page.wait_for_url(re.compile(f".*{url_pattern}.*"))

    def wait_for_selector(self, selector: str):
        # state="attached" means in DOM — does not require visibility
        # Use this after navigation to confirm the page is ready before interacting
        self.page.wait_for_selector(selector, state="attached")

    def take_screenshot(self, name: str):
        path = f"{SCREENSHOT_DIR}/{name}.png"
        self.page.screenshot(path=path)
        logger.info(f"Screenshot saved: {path}")