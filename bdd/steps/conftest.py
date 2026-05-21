"""
BDD step conftest — page object fixtures for all step definition modules.
Each fixture wraps a page object class around the shared Playwright `page` fixture
so step functions can interact with ParaBank through the existing POM layer.
"""
import pytest
from pages.login_page import LoginPage
from pages.registration_page import RegistrationPage
from pages.transfer_page import TransferPage
from pages.accounts_page import AccountsPage


@pytest.fixture(scope="function")
def login_page(page):
    """LoginPage instance bound to the current test's browser tab."""
    return LoginPage(page)


@pytest.fixture(scope="function")
def registration_page(page):
    """RegistrationPage instance bound to the current test's browser tab."""
    return RegistrationPage(page)


@pytest.fixture(scope="function")
def transfer_page(page):
    """TransferPage instance bound to the current test's browser tab."""
    return TransferPage(page)


@pytest.fixture(scope="function")
def accounts_page(page):
    """AccountsPage instance bound to the current test's browser tab."""
    return AccountsPage(page)