import pytest
from pages.registration_page import RegistrationPage
from config.config_reader import BASE_URL
from utils.logger import get_logger
from playwright.sync_api import expect
import uuid
logger = get_logger(__name__)

class TestRegistration:
    @pytest.fixture(autouse=True)
    def initialise_pages(self, page):
        self.registration_page = RegistrationPage(page)
    
    def test_valid_registration_shows_welcome(self, test_data):
        self.registration_page.navigate_to_registration(BASE_URL)
        user_data = test_data["valid_user"].copy()
        user_data["username"] = f"{user_data.get("username")}{str(uuid.uuid4())[:6]}"
        self.registration_page.register(user_data)
        expect (self.registration_page.get_success_locator()).to_contain_text(f"Welcome {user_data["username"]}", timeout=5000)
        #assert is not used here because timeout was necessary because the same locators before registration has different text
        #and after registration has different expected text

    def test_duplicate_username_shows_error(self, test_data):
        self.registration_page.navigate_to_registration(BASE_URL)
        user_data = test_data["duplicate_user"].copy()
        user_data["username"] = f"{user_data.get("username")}{str(uuid.uuid4())[:6]}"
        self.registration_page.register(user_data)
        self.registration_page.navigate_to_registration(BASE_URL)
        self.registration_page.register(user_data)
        assert "This username already exists." in self.registration_page.get_error_message("username")

    def test_missing_fields_shows_error(self, test_data):
        self.registration_page.navigate_to_registration(BASE_URL)
        self.registration_page.register(test_data["missing_fields_user"])
        assert "Zip Code is required." in self.registration_page.get_error_message("address.zipCode")

