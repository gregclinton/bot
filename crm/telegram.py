import requests
import os

token = os.environ.get("HAL_TOKEN")
endpoint = f"https://api.telegram.org/bot{token}"

res = requests.get(f"{endpoint}/getUpdates")
print(res)
