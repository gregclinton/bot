import remote

worker = "Balance"

for msg in remote.inbox(worker):
    account = msg.body.split(":")[1].strip()
    remote.post(worker, msg.frm, f"Account balance for {account} is $13.55.")
