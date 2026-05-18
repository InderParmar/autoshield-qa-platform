from playwright.sync_api import Page
from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class LoginPage(BasePage):
    """Page object for the ParaBank login page (index.htm)."""

    def __init__(self, page: Page):
        super().__init__(page)
        # Locators defined once here — never hardcoded inside methods
        self._username_input        = "input[name='username']"
        self._password_input        = "input[name='password']"
        self._login_button          = "input[value='Log In']"
        self._error_message_element = ".error"

    def navigate_to_login(self, baseurl: str) -> None:
        logger.info("Navigating to login page")
        self.navigate(baseurl)
        self.wait_for_selector(self._username_input)


    def login(self, username: str, password: str) -> None:
        logger.info(f"Attempting login with username: {username}")
        self.page.locator(self._username_input).fill(username)
        self.page.locator(self._password_input).fill(password)
        self.page.locator(self._login_button).click()
        logger.info(f"Login form submitted for username: {username}")

    def get_error_message(self) -> str:
        self.wait_for_selector(self._error_message_element)
        error = self.page.locator(self._error_message_element).text_content()
        logger.debug(f"Login error message received: '{error}'")
        return error

    def is_login_page(self) -> bool:
        return "index" in self.get_current_url()