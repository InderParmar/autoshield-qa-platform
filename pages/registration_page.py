from playwright.sync_api import Page
from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class RegistrationPage(BasePage):
    """Page object for the ParaBank new user registration page (register.htm)."""

    def __init__(self, page: Page):
        super().__init__(page)
        self._first_name_input              = "input[id='customer.firstName']"
        self._last_name_input               = "input[id='customer.lastName']"
        self._address_input                 = "input[id='customer.address.street']"
        self._city_input                    = "input[id='customer.address.city']"
        self._state_input                   = "input[id='customer.address.state']"
        self._zip_code_input                = "input[id='customer.address.zipCode']"
        self._phone_input                   = "input[id='customer.phoneNumber']"
        self._SSN_input                     = "input[id='customer.ssn']"
        self._username_input                = "input[id='customer.username']"
        self._password_input                = "input[id='customer.password']"
        self._confirm_password_input        = "input[id='repeatedPassword']"
        self._register_button               = "input[value='Register']"
        self._success_message_title_element = ".title"
        self._success_message_body_element  = "div[id='rightPanel'] p"

    def _get_error_message_element(self, element: str) -> str:
        # Constructs the field-specific validation error selector dynamically
        return f"span[id='customer.{element}.errors']"

    def navigate_to_registration(self, baseurl: str) -> None:
        logger.info("Navigating to registration page")
        self.navigate(f"{baseurl}/register.htm")
        self.wait_for_selector(self._first_name_input)

    def fill_registration_form(self, data: dict) -> None:
        logger.info(f"Filling registration form for username: {data.get('username')}")
        self.page.locator(self._first_name_input).fill(data.get("first_name"))
        self.page.locator(self._last_name_input).fill(data.get("last_name"))
        self.page.locator(self._address_input).fill(data.get("address"))
        self.page.locator(self._city_input).fill(data.get("city"))
        self.page.locator(self._state_input).fill(data.get("state"))
        self.page.locator(self._zip_code_input).fill(data.get("zip_code"))
        self.page.locator(self._phone_input).fill(data.get("phone_number"))
        self.page.locator(self._SSN_input).fill(data.get("SSN"))
        self.page.locator(self._username_input).fill(data.get("username"))
        self.page.locator(self._password_input).fill(data.get("password"))
        self.page.locator(self._confirm_password_input).fill(data.get("password"))

    def submit_form(self) -> None:
        logger.info("Submitting registration form")
        self.page.locator(self._register_button).click()

    def get_success_message(self) -> str:
        self.wait_for_selector(self._success_message_title_element)
        self.wait_for_selector(self._success_message_body_element)
        title = self.page.locator(self._success_message_title_element).text_content()
        body  = self.page.locator(self._success_message_body_element).text_content()
        logger.debug(f"Registration success — title: '{title}' | body: '{body}'")
        return title + "\n" + body

    def get_success_locator(self):
        # Returns the locator object directly — used with expect() for timeout-aware assertions
        return self.page.locator(self._success_message_title_element)

    def get_error_message(self, element: str) -> str:
        error_selector = self._get_error_message_element(element)
        self.wait_for_selector(error_selector)
        error = self.page.locator(error_selector).text_content()
        logger.debug(f"Validation error for field '{element}': '{error}'")
        return error

    def register(self, data: dict) -> None:
        # Convenience method — fills and submits the form in one call
        self.fill_registration_form(data)
        self.submit_form()