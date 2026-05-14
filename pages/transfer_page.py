from playwright.sync_api import Page
from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class TransferPage(BasePage):
    """Page object for the ParaBank fund transfer page (transfer.htm)."""

    def __init__(self, page: Page):
        super().__init__(page)
        self._amount_input                  = "#amount"
        self._from_account_dropdown         = "#fromAccountId"
        self._to_account_dropdown           = "#toAccountId"
        self._transfer_button               = "input[value='Transfer']"
        self._success_message_title_element = "div[id='showResult'] h1[class='title']"
        self._success_message_body_element  = "#showResult p:nth-of-type(1)"
        self._error_message_title_element   = "div[id='showError'] h1[class='title']"
        self._error_message_body_element    = "div[id='showError'] p[class='error']"

    def navigate_to_transfer_funds(self, baseurl: str) -> None:
        logger.info("Navigating to transfer funds page")
        self.navigate(f"{baseurl}/transfer.htm")

    def transfer_funds(self, amount: str, from_account_index: int, to_account_index: int) -> None:
        logger.info(f"Transferring amount: '{amount}' | from index: {from_account_index} → to index: {to_account_index}")
        self.page.locator(self._amount_input).fill(amount)
        self.page.locator(self._from_account_dropdown).select_option(index=from_account_index)
        self.page.locator(self._to_account_dropdown).select_option(index=to_account_index)
        self.page.locator(self._transfer_button).click()

    def get_success_message(self) -> str:
        self.wait_for_selector(self._success_message_title_element)
        self.wait_for_selector(self._success_message_body_element)
        title = self.page.locator(self._success_message_title_element).text_content()
        body  = self.page.locator(self._success_message_body_element).text_content()
        logger.debug(f"Transfer success — title: '{title}' | body: '{body}'")
        return title + "\n" + body

    def get_error_message(self) -> str:
        self.wait_for_selector(self._error_message_title_element)
        self.wait_for_selector(self._error_message_body_element)
        title = self.page.locator(self._error_message_title_element).text_content()
        body  = self.page.locator(self._error_message_body_element).text_content()
        logger.debug(f"Transfer error — title: '{title}' | body: '{body}'")
        return title + "\n" + body