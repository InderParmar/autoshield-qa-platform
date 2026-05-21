"""
BDD step definitions for registration.feature.
Covers valid registration and duplicate username scenarios.
Unique usernames are generated with a uuid suffix to avoid conflicts
between test runs on the shared ParaBank demo environment.
"""
import uuid
import pytest
from pytest_bdd import given, when, then, scenarios
from config.config_reader import BASE_URL

# Register all scenarios from registration.feature with this module
scenarios("../features/registration.feature")


@given("I am on the Parabank registration page")
def navigate_to_registration(registration_page):
    registration_page.navigate_to_registration(BASE_URL)


@when("I fill in the registration form with valid data")
def fill_valid_registration(registration_page, test_data):
    # Generate a unique username to avoid conflicts with previous test runs
    user_data = test_data["valid_user"].copy()
    user_data["username"] = f"{user_data['username']}{str(uuid.uuid4())[:4]}"
    registration_page.fill_registration_form(user_data)
    registration_page.submit_form()


@when("I register with a username which already exists")
def fill_duplicate_registration(registration_page, test_data):
    # Register once successfully, then attempt to register again with the same username
    user_data = test_data["duplicate_user"].copy()
    user_data["username"] = f"{user_data['username']}{str(uuid.uuid4())[:4]}"
    registration_page.fill_registration_form(user_data)
    registration_page.submit_form()
    # Navigate back and submit again with identical credentials
    registration_page.navigate_to_registration(BASE_URL)
    registration_page.fill_registration_form(user_data)
    registration_page.submit_form()


@then("I should see a welcome message with my username")
def verify_welcome_message(registration_page):
    success_message = registration_page.get_success_message()
    assert "welcome" in success_message.lower()


@then("I should see a duplicate username error")
def verify_duplicate_error(registration_page):
    assert "This username already exists." in registration_page.get_error_message("username")