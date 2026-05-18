from playwright.sync_api import Page
from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class BillPaymentPage(BasePage):
    """Page object for the ParaBank bill payment page (billpay.htm)."""

    def __init__(self, page: Page):
        super().__init__(page)
        # Payee form field locators — all use name attributes on this page
        self._payee_name_input            = "input[name='payee.name']"
        self._address_input               = "input[name='payee.address.street']"
        self._city_input                  = "input[name='payee.address.city']"
        self._state_input                 = "input[name='payee.address.state']"
        self._zip_code_input              = "input[name='payee.address.zipCode']"
        self._phone_number_input          = "input[name='payee.phoneNumber']"
        self._account_number_input        = "input[name='payee.accountNumber']"
        self._verify_account_number_input = "input[name='verifyAccount']"
        self._amount_input                = "input[name='amount']"
        self._from_account_dropdown       = "select[name='fromAccountId']"
        self._send_payment_button         = "input[value='Send Payment']"
        # Result elements
        self._success_message_title_element = "div[id='billpayResult'] h1[class='title']"
        # XPath used here because the success paragraph is identified by its text content
        self._success_message_body_element  = "//p[contains(text(),'Bill Payment to')]"

    def _get_error_message_element(self, element: str) -> str:
        # Constructs the field-specific validation error selector dynamically
        return f"#validationModel-{element}"

    def navigate_to_bill_payment(self, baseurl: str) -> None:
        logger.info("Navigating to bill payment page")
        self.navigate(f"{baseurl}/billpay.htm")

    def fill_payee_details(self, data: dict) -> None:
        logger.info(f"Filling bill payment form for payee: {data.get('payee_name')}")
        self.page.locator(self._payee_name_input).fill(data.get("payee_name"))
        self.page.locator(self._address_input).fill(data.get("address"))
        self.page.locator(self._city_input).fill(data.get("city"))
        self.page.locator(self._state_input).fill(data.get("state"))
        self.page.locator(self._zip_code_input).fill(data.get("zip_code"))
        self.page.locator(self._phone_number_input).fill(data.get("phone_number"))
        self.page.locator(self._account_number_input).fill(data.get("account_number"))
        # ParaBank requires account number entered twice for confirmation
        self.page.locator(self._verify_account_number_input).fill(data.get("account_number"))
        self.page.locator(self._amount_input).fill(data.get("amount"))

    def select_from_account(self, index: int) -> None:
        self.page.locator(self._from_account_dropdown).select_option(index=index)

    def send_payment(self) -> None:
        logger.info("Submitting bill payment")
        self.page.locator(self._send_payment_button).click()

    def get_success_message(self) -> str:
        # wait_for_selector not used here — ParaBank renders result elements
        # as hidden initially; text_content() is sufficient to retrieve the value
        title = self.page.locator(self._success_message_title_element).text_content()
        body  = self.page.locator(self._success_message_body_element).text_content()
        logger.debug(f"Bill payment success — title: '{title}' | body: '{body}'")
        return title + "\n" + body

    def get_error_message(self, element: str) -> str:
        error_selector = self._get_error_message_element(element)
        self.wait_for_selector(error_selector)
        error = self.page.locator(error_selector).text_content()
        logger.debug(f"Validation error for field '{element}': '{error}'")
        return error

    def is_bill_payment_page(self) -> bool:
        return "billpay" in self.get_current_url()

    def pay_bill(self, data: dict, from_account_index: int) -> None:
        # Convenience method — fills form, selects account, and submits in one call
        self.fill_payee_details(data)
        self.select_from_account(from_account_index)
        self.send_payment()