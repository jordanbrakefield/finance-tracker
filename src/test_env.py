from dotenv import load_dotenv
import os

load_dotenv()

print("Plaid Client ID:", os.getenv("PLAID_CLIENT_ID"))
print("Plaid Env:", os.getenv("PLAID_ENV"))
