import requests
import os
import sys

key_name = "RUNPOD_POD_ID"
runpod_id = os.environ.get(key_name)

if not runpod_id:
    print(f"{key_name} not set.")
    exit(1)

url = f"https://{runpod_id}-4000.proxy.runpod.net"

def inbox(to):
    res = requests.get(f"{url}/messages/{to}")
    res.raise_for_status()
    for msg in res.json():
        yield msg["from"], msg["body"], msg["timestamp"]

def post(frm, to, body):
    requests.post(f"{url}/messages", json = { "from": frm, "to": to, "body": body }).raise_for_status()

if __name__ == "__main__":
    globals()[sys.argv[1]](*sys.argv[2:])