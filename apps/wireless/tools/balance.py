# python3 balance.py

import messages

tool = "Balance"

for msg in messages.inbox(tool):
    account = msg.body.split(":")[1].strip()

    # for this toy example we fake it
    # but here you would access your company's systems
    # to get the real balance
    balance = 13.55

    messages.post(tool, msg.frm, f"Account balance for {account} is ${balance}.")
