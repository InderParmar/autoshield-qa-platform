import pytest
from api_tests.api_utils.api_helper import ParaBankClient
from utils.logger import get_logger

logger = get_logger(__name__)


# ── API client fixture ─────────────────────────────────────────────────────────
# Scope: session — one HTTP session for the entire API test run
# Pre-configured with Accept and Content-Type headers for ParaBank's REST API
@pytest.fixture(scope="session")
def api_client():
    logger.info("Initialising ParaBankClient for API test session")
    return ParaBankClient()


# ── Authenticated session fixture ──────────────────────────────────────────────
# Scope: session — logs in once using the UI-registered user from root conftest
# Returns a dict with customer_id for use in account and transaction tests
# Reuses registered_user so UI and API tests always operate on the same account
@pytest.fixture(scope="session")
def authenticated_session(api_client, registered_user):
    logger.info(f"Authenticating API session for: {registered_user['username']}")
    response = api_client.login(registered_user["username"], registered_user["password"])
    assert "id" in response, f"Login failed — no 'id' field in response: {response}"
    customer_id = response["id"]
    logger.info(f"API authentication successful — customer ID: {customer_id}")
    return {"customer_id": customer_id}


# ── Account IDs fixture ────────────────────────────────────────────────────────
# Scope: session — fetches account list once and extracts IDs for all tests
# Depends on authenticated_session so login always runs first
@pytest.fixture(scope="session")
def account_ids(api_client, authenticated_session):
    accounts = api_client.get_accounts(authenticated_session["customer_id"])
    ids = [item["id"] for item in accounts]
    logger.debug(f"Account IDs available for testing: {ids}")
    return ids