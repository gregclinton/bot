import sys
import messages
import subprocess
from account import scrape

tool = sys.argv[1]

for frm, body, _ in messages.inbox(tool):
    account = scrape(f"{frm} {body}")
    if account:
        out = subprocess.run(["sh", tool, account, body], capture_output = True, text = True)
        result = (out.stdout + out.stderr).strip()

        if account not in result:
            result = f"In reference to account: {account}\n{result}"

        print(f"From: {tool}\nTo: {frm}\n{result}\n")
        messages.post(tool, frm, result)