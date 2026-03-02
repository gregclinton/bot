# python3 install.py Hal

from pathlib import Path
import requests
import os
import sys

pod_id = os.environ.get("POD_ID", "ABCD")
endpoint = f"https://{pod_id}-4000.proxy.runpod.net/messages"

if __name__ == "__main__":
    worker = sys.argv[1]
    body = Path(worker).read_text()
    requests.post(endpoint, json = { "frm": "Above", "to": worker, "body": body }).raise_for_status()
