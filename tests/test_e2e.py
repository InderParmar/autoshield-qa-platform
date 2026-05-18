import pytest
import json
from pages.accounts_page import AccountsPage
from pages.transfer_page import TransferPage
from pages.bill_payment_page import BillPaymentPage
from config.config_reader import BASE_URL
from utils.logger import get_logger

logger = get_logger(__name__)


@pytest.fixture(scope="session")
def test_data_bill_payment():
    with open("test_data/bill_payment_data.json") as f:
        return json.load(f)


class TestE2E:
    @pytest.fixture(autouse=True)
    def initialise_pages(self, page):
        self.accounts_page     = AccountsPage(page)
        self.transfer_page     = TransferPage(page)
        self.bill_payment_page = BillPaymentPage(page)

    def test_transfer_updates_account_balance(self, logged_in_page):
        """Verifies that a fund transfer changes the first account's displayed balance."""
        self.accounts_page.navigate_to_accounts(BASE_URL)
        initial_balance = self.accounts_page.get_initial_account_balance()

        self.transfer_page.navigate_to_transfer_funds(BASE_URL)
        self.transfer_page.transfer_funds(amount="10", from_account_index=0, to_account_index=1)
        assert "transferred" in self.transfer_page.get_success_message()

        self.accounts_page.navigate_to_accounts(BASE_URL)
        updated_balance = self.accounts_page.get_initial_account_balance()
        assert float(initial_balance) != float(updated_balance)

    def test_full_user_journey(self, logged_in_page, test_data_bill_payment):
        """
        Full user journey: login → verify accounts page → transfer funds → pay a bill.
        This is the showcase test that chains all major features in one flow.
        """
        assert self.accounts_page.is_accounts_page()

        self.transfer_page.navigate_to_transfer_funds(BASE_URL)
        self.transfer_page.transfer_funds(amount="25", from_account_index=0, to_account_index=1)
        assert "transferred" in self.transfer_page.get_success_message()

        self.bill_payment_page.navigate_to_bill_payment(BASE_URL)
        assert self.bill_payment_page.is_bill_payment_page()
        self.bill_payment_page.pay_bill(
            test_data_bill_payment["valid_payment"], from_account_index=0
        )
        assert "bill payment complete" in self.bill_payment_page.get_success_message().lower()

        logger.info("Full user journey completed successfully")