import requests
import os

key_name = "RUNPOD_POD_ID"
runpod_id = os.environ.get(key_name)

if not runpod_id:
    print(f"{key_name} not set.")
    exit(1)

url = f"https://{runpod_id}-4000.proxy.runpod.net"

def inbox(to):
    res = requests.get(f"{url}/messages/{to}?timeout=30")
    res.raise_for_status()
    for msg in res.json():
        yield msg["from"], msg["body"], msg["timestamp"]

def post(frm, to, body):
    requests.post(f"{url}/messages", json = { "from": frm, "to": to, "body": body }).raise_for_status()