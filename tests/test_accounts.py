import pytest
from pages.accounts_page import AccountsPage
from utils.logger import get_logger

logger = get_logger(__name__)

class TestAccounts:
    @pytest.fixture(autouse=True)
    def initialise_pages(self, page):
        self.accounts_page = AccountsPage(page)
        
    def test_accounts_page_loads_after_login(self, logged_in_page):
        assert self.accounts_page.is_accounts_page()
        
    def test_account_list_is_not_empty(self, logged_in_page):
        assert len(self.accounts_page.get_account_list()) > 0
        
    def test_total_balance_is_displayed(self, logged_in_page):
        assert len(self.accounts_page.get_total_balance()) > 0