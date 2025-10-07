# fetch_balances.py
from plaid_client import client
from plaid.model.accounts_balance_get_request import AccountsBalanceGetRequest
from plaid.model.sandbox_public_token_create_request import SandboxPublicTokenCreateRequest
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest

def get_balances():
    # 1. Create sandbox account
    sandbox_request = SandboxPublicTokenCreateRequest(
        institution_id="ins_109508",
        initial_products=["balance"]
    )
    sandbox_response = client.sandbox_public_token_create(sandbox_request)
    public_token = sandbox_response.public_token

    # 2. Exchange for access token
    exchange_request = ItemPublicTokenExchangeRequest(public_token=public_token)
    exchange_response = client.item_public_token_exchange(exchange_request)
    access_token = exchange_response.access_token

    # 3. Get balances
    request = AccountsBalanceGetRequest(access_token=access_token)
    response = client.accounts_balance_get(request)

    balances = {}
    for acct in response.accounts:
        balances[acct.name] = acct.balances.current

    return balances

if __name__ == "__main__":
    print(get_balances())
