import requests

worker = "Balance"
messages = "https://example.com/messages"

res = requests.get(f"{messages}/{worker}")

for msg in res.json():
    account = msg["body"].split(":")[1].strip()
    requests.post(f"{messages}/{msg["frm"]}", {"frm": worker, "to": msg["frm"], "body": f"Account balance for {account} is $13.55.")
