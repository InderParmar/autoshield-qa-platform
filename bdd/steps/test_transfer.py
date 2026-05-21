"""
BDD step definitions for transfer.feature.
Covers valid fund transfer and transfer page load scenarios.
Login is handled inline in the Given step — the transfer page
fixtures operate on the same browser tab after login completes.
"""
import pytest
from pytest_bdd import given, when, then, scenarios
from config.config_reader import BASE_URL

# Register all scenarios from transfer.feature with this module
scenarios("bdd/features/transfer.feature")


@given("I am logged into Parabank")
def logged_into_parabank(login_page, registered_user):
    # Logs in with the session-registered user and waits for accounts overview
    login_page.navigate_to_login(BASE_URL)
    login_page.login(registered_user["username"], registered_user["password"])
    login_page.wait_for_url("overview")


@when("I navigate to transfer funds page")
def navigate_to_transfer_page(transfer_page):
    # Shared step — used by both transfer scenarios
    transfer_page.navigate_to_transfer_funds(BASE_URL)


@when("I transfer funds between two accounts")
def transfer_between_accounts(transfer_page):
    # Transfers between account index 0 and 1 — both exist after registered_user fixture runs
    transfer_page.transfer_funds("10", 0, 1)


@then("I should see a transfer success message")
def verify_transfer_success(transfer_page):
    assert "transferred" in transfer_page.get_success_message()


@then("the transfer page should be displayed")
def verify_transfer_page_displayed(transfer_page):
    assert "transfer" in transfer_page.get_current_url()