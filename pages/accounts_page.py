from playwright.sync_api import Page
from pages.base_page import BasePage
from utils.logger import get_logger
from utils import wait_helper

logger = get_logger(__name__)


class AccountsPage(BasePage):
    """Page object for the ParaBank accounts overview page (overview.htm)."""

    def __init__(self, page: Page):
        super().__init__(page)
        # Balance of the first account row — used in E2E balance change assertions
        self._initial_account_balance = "tbody tr:nth-child(1) td:nth-child(2)"
        # Total balance row at the bottom of the accounts table
        self._total_account_balance   = "tbody tr td:nth-child(2) b:nth-child(1)"
        self._welcome_message_element = ".smallText"

    def _get_account_list_locator(self, count: int) -> str:
        # Builds a row-specific selector for the account number column
        return f"tbody tr:nth-child({count}) td:nth-child(1)"

    def _get_accounts_list_elements(self) -> list:
        """
        Scans table rows one by one until a row is not found or not numeric.
        Uses wait_helper to detect row existence without hardcoding the row count.
        Returns a list of CSS selectors — one per valid account row.
        """
        element_visible = True
        count = 0
        element_list = []

        while element_visible:
            count += 1
            selector = self._get_account_list_locator(count)
            element_visible = wait_helper.check_with_timeout(self.page, selector, timeout=1000)

        # count stopped at the first missing row — range(1, count) covers all valid rows
        for i in range(1, count):
            element_list.append(self._get_account_list_locator(i))

        logger.debug(f"Found {len(element_list)} account row(s)")
        return element_list

    def navigate_to_accounts(self, baseurl: str) -> None:
        logger.info("Navigating to accounts overview page")
        self.navigate(f"{baseurl}/overview.htm")

    def get_account_list(self) -> list:
        """Returns a list of account number text values from the accounts table."""
        accounts_elements_list = self._get_accounts_list_elements()
        account_list = []
        for account_element in accounts_elements_list:
            account_list.append(self.page.locator(account_element).text_content())
        logger.debug(f"Account list retrieved: {account_list}")
        return account_list

    def get_total_balance(self) -> str:
        """Returns total balance as a plain numeric string — strips $ and commas."""
        balance = self.page.locator(self._total_account_balance).text_content()
        logger.debug(f"Total balance text: '{balance}'")
        return balance[1:].replace(",", "")

    def get_initial_account_balance(self) -> str:
        """Returns the first account's balance as a plain numeric string — strips $ and commas."""
        balance = self.page.locator(self._initial_account_balance).text_content()
        logger.debug(f"First account balance text: '{balance}'")
        return balance[1:].replace(",", "")

    def is_accounts_page(self) -> bool:
        return "overview" in self.get_current_url()

    def get_welcome_message(self) -> str:
        return self.page.locator(self._welcome_message_element).text_content()