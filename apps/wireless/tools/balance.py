import requests

worker = "Balance"
messages = "https://example.com/messages"

res = requests.get(f"{messages}/{worker}")

for msg in res.json():
    requests.post(f"{messages}/{msg["frm"]}", {"frm": worker, "to": msg["frm"], "body": f"{msg["body"]}\nBalance is $13.55.")
