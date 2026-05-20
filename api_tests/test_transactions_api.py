import pytest


class TestTransactionsAPI:
    """
    Tests for ParaBank REST API transaction and transfer endpoints.
    Each test creates a fresh account via API to transfer into — this ensures
    a known transaction exists without depending on prior test state.
    """

    def test_get_transactions_returns_list(self, api_client, authenticated_session, account_ids):
        """Transactions endpoint returns a non-empty list after a transfer."""
        new_account = api_client.create_account(
            authenticated_session["customer_id"], 1, account_ids[0]
        )
        api_client.transfer(account_ids[0], new_account["id"], amount=10)
        response = api_client.get_transactions(account_ids[0])
        assert isinstance(response, list), \
            f"Expected list, got {type(response)}: {response}"
        assert len(response) > 0, \
            f"Transaction list is empty for account {account_ids[0]}"

    def test_transaction_has_required_fields(self, api_client, authenticated_session, account_ids):
        """Each transaction object contains the required schema fields."""
        new_account = api_client.create_account(
            authenticated_session["customer_id"], 1, account_ids[0]
        )
        api_client.transfer(account_ids[0], new_account["id"], amount=10)
        response = api_client.get_transactions(account_ids[0])
        assert len(response) > 0, \
            f"No transactions found for account {account_ids[0]}"
        assert all(k in response[0] for k in ["id", "amount", "date", "description"]), \
            f"Missing required field in transaction object: {response[0]}"

    def test_transfer_and_verify_transaction_appears(self, api_client, authenticated_session, account_ids):
        """A completed transfer creates a transaction record on the source account."""
        new_account = api_client.create_account(
            authenticated_session["customer_id"], 1, account_ids[0]
        )
        transfer_result = api_client.transfer(account_ids[0], new_account["id"], amount=10)
        assert "transferred" in transfer_result, \
            f"Transfer response did not confirm completion: {transfer_result}"
        transactions = api_client.get_transactions(account_ids[0])
        assert len(transactions) > 0, \
            f"No transactions found after transfer on account {account_ids[0]}"