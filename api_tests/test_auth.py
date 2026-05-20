import pytest
from config.config_reader import WRONG_USERNAME, WRONG_PASSWORD


class TestAuth:
    """Tests for ParaBank REST API authentication endpoints."""

    def test_valid_login_returns_customer_id(self, api_client, registered_user):
        """Valid credentials return a customer object with a positive integer ID."""
        response = api_client.login(registered_user["username"], registered_user["password"])
        assert "id" in response, \
            f"No 'id' field in login response: {response}"
        assert isinstance(response["id"], int), \
            f"'id' is not an integer: {response['id']}"
        assert response["id"] > 0, \
            f"'id' is not a positive integer: {response['id']}"

    def test_invalid_login_returns_error(self, api_client):
        """Invalid credentials return 400 Bad Request — ParaBank does not use 401."""
        response = api_client.login_raw(WRONG_USERNAME, WRONG_PASSWORD)
        assert response.status_code == 400, \
            f"Expected 400, got {response.status_code}"

    def test_login_response_time_is_acceptable(self, api_client, registered_user):
        """Login endpoint responds within 3000ms under normal conditions."""
        response = api_client.login_raw(registered_user["username"], registered_user["password"])
        elapsed_ms = response.elapsed.total_seconds() * 1000
        assert elapsed_ms < 3000, \
            f"Response time {elapsed_ms:.0f}ms exceeded 3000ms limit"