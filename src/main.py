# main.py
from compute_balance_diff import compute_net_balance
from send_sms import send_text

net = compute_net_balance("Checking", ["Savings", "Credit Card"])
msg = f"Your current available balance is ${net:.2f}"
send_text(msg)
print("Text sent:", msg)
