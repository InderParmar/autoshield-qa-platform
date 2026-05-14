import pytest
from pages.login_page import LoginPage
from config.config_reader import BASE_URL, WRONG_USERNAME, WRONG_PASSWORD
from utils.logger import get_logger

logger = get_logger(__name__)

class TestLogin:

    @pytest.fixture(autouse=True)
    def initialise_pages(self, page):
        self.login_page = LoginPage(page)
        
    def test_valid_login_redirects_to_account(self, registered_user):
        self.login_page.navigate(BASE_URL)
        self.login_page.login(registered_user["username"], registered_user["password"])
        self.login_page.wait_for_url("overview")
        assert "overview" in self.login_page.get_current_url()

    def test_invalid_login_shows_error(self):
        self.login_page.navigate(BASE_URL)
        self.login_page.login(WRONG_USERNAME, WRONG_PASSWORD)
        assert len(self.login_page.get_error_message()) > 0

    def test_empty_credentials_shows_error(self):
        self.login_page.navigate(BASE_URL)
        self.login_page.login("", "")
        assert len(self.login_page.get_error_message()) > 0

        