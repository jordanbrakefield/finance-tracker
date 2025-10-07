# compute_balance_diff.py
from fetch_balances import get_balances

def compute_net_balance(main_acct, subtract_accts):
    balances = get_balances()
    main = balances.get(main_acct, 0)
    minus_total = sum(balances.get(a, 0) for a in subtract_accts)
    return main - minus_total

if __name__ == "__main__":
    net = compute_net_balance("Checking", ["Savings", "Credit Card"])
    print(f"Net Available: ${net:.2f}")
