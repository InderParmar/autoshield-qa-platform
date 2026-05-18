import pytest
from pages.transfer_page import TransferPage
from config.config_reader import BASE_URL
from utils.logger import get_logger

logger = get_logger(__name__)

class TestTransfer:
    @pytest.fixture(autouse=True)
    def initialise_pages(self, page):
        self.transfer_page = TransferPage(page)
    
    def test_valid_transfer_shows_success(self, logged_in_page):
        self.transfer_page.navigate_to_transfer_funds(BASE_URL)
        self.transfer_page.transfer_funds(amount= "200", from_account_index= 0, to_account_index= 1)
        assert "transferred" in self.transfer_page.get_success_message()
        
    def test_transfer_zero_amount_shows_error(self, logged_in_page):
        self.transfer_page.navigate_to_transfer_funds(BASE_URL)
        self.transfer_page.transfer_funds(amount= "", from_account_index= 0, to_account_index= 1)
        assert "error" in self.transfer_page.get_error_message().lower()

    def test_transfer_page_loads(self, logged_in_page):
        self.transfer_page.navigate_to_transfer_funds(BASE_URL)
        assert "transfer" in self.transfer_page.get_current_url()

