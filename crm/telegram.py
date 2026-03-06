import requests
import os

token = os.environ.get("TELEGRAM_TOKEN")
endpoint = f"https://api.telegram.org/bot{token}"

for msg in requests.get(f"{endpoint}/getUpdates").json()["result"]:
    print(msg)
