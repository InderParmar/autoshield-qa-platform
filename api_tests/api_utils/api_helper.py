import requests
from config.config_reader import API_BASE_URL
from utils.logger import get_logger

logger = get_logger(__name__)


class ParaBankClient:
    """
    HTTP client for the ParaBank REST API.
    Wraps requests.Session with default headers and one method per endpoint.
    Happy-path methods assert status 200 and return parsed JSON.
    Raw methods return the Response object for negative/error case testing.
    """

    def __init__(self):
        self.api_base_url = API_BASE_URL
        self.session = requests.Session()
        # Set default headers on the session — applied to every request automatically
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })
        logger.info("ParaBankClient initialised")

    # ── Auth ───────────────────────────────────────────────────────────────────

    def login(self, username: str, password: str) -> dict:
        """Authenticates and returns the customer object dict. Asserts 200."""
        logger.info(f"Logging in as: {username}")
        response = self.session.get(f"{self.api_base_url}/login/{username}/{password}")
        assert response.status_code == 200, \
            f"Login failed — status: {response.status_code}, body: {response.text}"
        logger.debug(f"Login successful — status: {response.status_code}")
        return response.json()

    def login_raw(self, username: str, password: str) -> requests.Response:
        """Returns raw Response — used in negative tests expecting non-200."""
        logger.debug(f"Raw login request for username: {username}")
        return self.session.get(f"{self.api_base_url}/login/{username}/{password}")

    # ── Accounts ───────────────────────────────────────────────────────────────

    def get_accounts(self, customer_id: int) -> list:
        """Returns list of account dicts for a customer. Asserts 200."""
        logger.info(f"Fetching accounts for customer ID: {customer_id}")
        response = self.session.get(f"{self.api_base_url}/customers/{customer_id}/accounts")
        assert response.status_code == 200, \
            f"get_accounts failed — status: {response.status_code}, body: {response.text}"
        accounts = response.json()
        logger.debug(f"Retrieved {len(accounts)} account(s) for customer {customer_id}")
        return accounts

    def get_account(self, account_id: int) -> dict:
        """Returns account details dict. Asserts 200."""
        logger.debug(f"Fetching details for account ID: {account_id}")
        response = self.session.get(f"{self.api_base_url}/accounts/{account_id}")
        assert response.status_code == 200, \
            f"get_account failed — status: {response.status_code}, body: {response.text}"
        return response.json()

    def get_account_raw(self, account_id: int) -> requests.Response:
        """Returns raw Response — used in negative tests expecting non-200."""
        logger.debug(f"Raw account request for ID: {account_id}")
        return self.session.get(f"{self.api_base_url}/accounts/{account_id}")

    def create_account(self, customer_id: int, account_type: int, from_account_id: int) -> dict:
        """
        Creates a new account and returns the account dict. Asserts 200.
        account_type: 0 = CHECKING, 1 = SAVINGS
        """
        logger.info(f"Creating account — customer: {customer_id}, type: {account_type}, from: {from_account_id}")
        response = self.session.post(
            f"{self.api_base_url}/createAccount",
            params={"customerId": customer_id, "newAccountType": account_type, "fromAccountId": from_account_id}
        )
        assert response.status_code == 200, \
            f"create_account failed — status: {response.status_code}, body: {response.text}"
        new_account = response.json()
        logger.debug(f"New account created — ID: {new_account.get('id')}")
        return new_account

    # ── Transactions ───────────────────────────────────────────────────────────

    def get_transactions(self, account_id: int) -> list:
        """Returns list of transaction dicts for an account. Asserts 200."""
        logger.debug(f"Fetching transactions for account ID: {account_id}")
        response = self.session.get(f"{self.api_base_url}/accounts/{account_id}/transactions")
        assert response.status_code == 200, \
            f"get_transactions failed — status: {response.status_code}, body: {response.text}"
        transactions = response.json()
        logger.debug(f"Retrieved {len(transactions)} transaction(s) for account {account_id}")
        return transactions

    # ── Transfer ───────────────────────────────────────────────────────────────

    def transfer(self, from_account_id: int, to_account_id: int, amount: float) -> str:
        """Transfers funds between accounts. Returns response text (plain string, not JSON)."""
        logger.info(f"Transferring {amount} from account {from_account_id} to {to_account_id}")
        response = self.session.post(
            f"{self.api_base_url}/transfer",
            params={"fromAccountId": from_account_id, "toAccountId": to_account_id, "amount": amount}
        )
        logger.debug(f"Transfer response — status: {response.status_code}, body: {response.text}")
        return response.text