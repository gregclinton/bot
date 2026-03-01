import messages

worker = "Balance"

for msg in messages.remote_inbox(worker):
    account = msg.body.split(":")[1].strip()
    messages.remote_post(worker, msg.frm, f"Account balance for {account} is $13.55.")
