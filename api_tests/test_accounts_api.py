import pytest


class TestAccountsAPI:
    """Tests for ParaBank REST API account endpoints."""

    def test_get_accounts_returns_list(self, api_client, authenticated_session):
        """Accounts endpoint returns a non-empty list for a valid customer."""
        response = api_client.get_accounts(authenticated_session["customer_id"])
        assert isinstance(response, list), \
            f"Expected list, got {type(response)}: {response}"
        assert len(response) > 0, \
            f"Account list is empty for customer {authenticated_session['customer_id']}"

    def test_account_has_required_fields(self, api_client, authenticated_session):
        """Each account object contains the required schema fields."""
        response = api_client.get_accounts(authenticated_session["customer_id"])
        assert all(k in response[0] for k in ["id", "customerId", "balance", "type"]), \
            f"Missing required field in account object: {response[0]}"

    def test_get_account_details_returns_correct_id(self, api_client, account_ids):
        """Account details endpoint returns the account with the requested ID."""
        response = api_client.get_account(account_ids[0])
        assert response["id"] == account_ids[0], \
            f"Expected account ID {account_ids[0]}, got {response['id']}"

    def test_invalid_account_id_returns_error(self, api_client):
        """Non-existent account ID returns 400 Bad Request."""
        response = api_client.get_account_raw(999999999)
        assert response.status_code == 400, \
            f"Expected 400, got {response.status_code}"