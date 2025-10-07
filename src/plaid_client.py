import os
from dotenv import load_dotenv
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api_client import ApiClient

load_dotenv()

PLAID_CLIENT_ID = os.getenv("PLAID_CLIENT_ID")
PLAID_SECRET = os.getenv("PLAID_SECRET")
PLAID_ENV = os.getenv("PLAID_ENV", "sandbox")

# Centralized Plaid client factory
def get_plaid_client():
    host = "https://sandbox.plaid.com"
    if PLAID_ENV == "development":
        host = "https://development.plaid.com"
    elif PLAID_ENV == "production":
        host = "https://production.plaid.com"

    configuration = Configuration(
        host=host,
        api_key={
            "clientId": PLAID_CLIENT_ID,
            "secret": PLAID_SECRET
        }
    )
    return plaid_api.PlaidApi(ApiClient(configuration))
