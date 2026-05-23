from locust import HttpUser, task, between
from config.config_reader import USERNAME, PASSWORD

class ParaBankUser(HttpUser):
    host = "https://parabank.parasoft.com"
    wait_time = between(1,3)
    def on_start(self):
        self.client.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })
        response = self.client.get(f"/parabank/services/bank/login/{USERNAME}/{PASSWORD}")
        self.customer_id = response.json()["id"]
        response_accounts = self.client.get(f"/parabank/services/bank/customers/{self.customer_id}/accounts")
        self.account_id = response_accounts.json()[0]["id"]

    @task(3)
    def view_accounts(self):
        self.client.get(f"/parabank/services/bank/customers/{self.customer_id}/accounts")
        
    @task(2)
    def get_account_details(self):
        self.client.get(f"/parabank/services/bank/accounts/{self.account_id}")
    
    @task(1)
    def get_transactions(self):
        self.client.get(f"/parabank/services/bank/accounts/{self.account_id}/transactions")