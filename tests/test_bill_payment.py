import pytest
import json
from pages.bill_payment_page import BillPaymentPage
from config.config_reader import BASE_URL
from utils.logger import get_logger

logger = get_logger(__name__)


@pytest.fixture(scope="session")
def test_data_bill_payment():
    with open("test_data/bill_payment_data.json") as f:
        return json.load(f)


class TestBillPayment:
    @pytest.fixture(autouse=True)
    def initialise_pages(self, page):
        self.bill_payment_page = BillPaymentPage(page)

    def test_bill_payment_page_loads(self, logged_in_page):
        self.bill_payment_page.navigate_to_bill_payment(BASE_URL)
        assert self.bill_payment_page.is_bill_payment_page()

    def test_valid_bill_payment_shows_success(self, logged_in_page, test_data_bill_payment):
        self.bill_payment_page.navigate_to_bill_payment(BASE_URL)
        self.bill_payment_page.pay_bill(
            test_data_bill_payment["valid_payment"], from_account_index=0
        )
        assert "bill payment complete" in self.bill_payment_page.get_success_message().lower()

    def test_missing_payee_name_shows_error(self, logged_in_page, test_data_bill_payment):
        self.bill_payment_page.navigate_to_bill_payment(BASE_URL)
        self.bill_payment_page.pay_bill(
            test_data_bill_payment["missing_fields_payment"], from_account_index=0
        )
        assert len(self.bill_payment_page.get_error_message("name")) > 0