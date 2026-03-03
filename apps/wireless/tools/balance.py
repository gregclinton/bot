# python3 balance.py

import messages

tool = "Balance"

for msg in messages.inbox(tool):
    account = msg.body.split(":")[1].strip()
    messages.post(tool, msg.frm, f"Account balance for {account} is $13.55.")
