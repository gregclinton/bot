import requests
import os
import sys

key = "MESSAGES_URL"
url = os.environ.get(key)

if not url:
    print(f"{key} not set.")
    exit(1)

def inbox(to):
    res = requests.get(f"{url}/messages/{to}")
    res.raise_for_status()
    for msg in res.json():
        yield msg["from"], msg["body"], msg["timestamp"]

def post(frm, to, body):
    requests.post(f"{url}/messages", json = { "from": frm, "to": to, "body": body }).raise_for_status()

if __name__ == "__main__":
    globals()[sys.argv[1]](*sys.argv[2:])