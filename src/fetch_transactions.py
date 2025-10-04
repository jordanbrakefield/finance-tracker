import os
import time
import plaid
from dotenv import load_dotenv
from plaid.api import plaid_api
from plaid.model.products import Products
from plaid.model.sandbox_public_token_create_request import SandboxPublicTokenCreateRequest
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.configuration import Configuration
from plaid.api_client import ApiClient
from plaid.exceptions import ApiException
from datetime import date, timedelta

# Load .env
load_dotenv()

PLAID_CLIENT_ID = os.getenv("PLAID_CLIENT_ID")
PLAID_SECRET = os.getenv("PLAID_SECRET")
PLAID_ENV = os.getenv("PLAID_ENV", "sandbox")

# Configure Plaid client
configuration = Configuration(
    host="https://sandbox.plaid.com",
    api_key={
        "clientId": PLAID_CLIENT_ID,
        "secret": PLAID_SECRET
    }
)
client = plaid_api.PlaidApi(ApiClient(configuration))

# 1. Create a sandbox public token
sandbox_request = SandboxPublicTokenCreateRequest(
    institution_id="ins_109508",  # Sandbox bank
    initial_products=[Products("transactions")]
)
sandbox_response = client.sandbox_public_token_create(sandbox_request)
public_token = sandbox_response.public_token

# 2. Exchange for access token
exchange_request = ItemPublicTokenExchangeRequest(public_token=public_token)
exchange_response = client.item_public_token_exchange(exchange_request)
access_token = exchange_response.access_token

# 3. Get transactions
start_date = date.today() - timedelta(days=30)
end_date = date.today()

transactions_request = TransactionsGetRequest(
    access_token=access_token,
    start_date=start_date,
    end_date=end_date,
)

# Retry loop to handle sandbox PRODUCT_NOT_READY error
max_retries = 5
for attempt in range(max_retries):
    try:
        transactions_response = client.transactions_get(transactions_request)
        transactions = transactions_response['transactions']
        print(f"Transactions fetched successfully on attempt {attempt+1}")
        break
    except ApiException as e:
        if "PRODUCT_NOT_READY" in str(e):
            print(f"Transactions not ready yet, retrying... ({attempt+1}/{max_retries})")
            time.sleep(3)  # wait 3 seconds before retrying
        else:
            raise e
else:
    print("Failed to fetch transactions after multiple attempts")
    transactions = []

# 4. Simple categorization
categories = {
    "coffee": ["Starbucks", "Dunkin", "Dutch Bros"],
    "fast_food": ["McDonald's", "Burger King", "Taco Bell"],
    "amazon": ["Amazon"]
}

# 5. Summarize transactions
summary = {}
for tx in transactions:
    merchant = tx['merchant_name'] or "Other"
    amount = tx['amount']
    found = False
    for category, keywords in categories.items():
        if any(k.lower() in merchant.lower() for k in keywords):
            summary[category] = summary.get(category, 0) + amount
            found = True
            break
    if not found:
        summary["other"] = summary.get("other", 0) + amount

# 6. Print summary
print("Transaction summary for last 30 days:")
for cat, total in summary.items():
    print(f"{cat}: ${total:.2f}")

