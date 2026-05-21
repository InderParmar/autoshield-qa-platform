"""
BDD step definitions for login.feature.
Covers valid login, invalid credentials, and empty credentials scenarios.
Step functions reuse LoginPage POM — no direct browser interaction here.

Note: 'I should see a login error message' is shared between two scenarios
and written once — pytest-bdd reuses it automatically.
"""
import pytest
from pytest_bdd import given, when, then, scenarios
from config.config_reader import BASE_URL, WRONG_USERNAME, WRONG_PASSWORD

# Register all scenarios from login.feature with this module
scenarios("../features/login.feature")


@given("I am on the Parabank login page")
def navigate_to_login(login_page):
    login_page.navigate_to_login(BASE_URL)


@when("I enter valid username and password")
def enter_valid_credentials(login_page, registered_user):
    # Uses the session-registered user from root conftest — same credentials across UI and BDD tests
    login_page.login(registered_user["username"], registered_user["password"])


@when("I enter invalid username and password")
def enter_invalid_credentials(login_page):
    login_page.login(WRONG_USERNAME, WRONG_PASSWORD)


@when("I submit the login form with empty credentials")
def submit_empty_credentials(login_page):
    login_page.login("", "")


@then("I should be redirected to the accounts overview page")
def verify_redirected_to_accounts(login_page):
    login_page.wait_for_url("overview")
    assert "overview" in login_page.get_current_url()


@then("I should see a login error message")
def verify_login_error(login_page):
    # Shared step — used by both invalid and empty credentials scenarios
    assert len(login_page.get_error_message()) > 0