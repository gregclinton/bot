import sys
import messages
import subprocess
import re

tool = sys.argv[1]

for frm, body, timestamp in messages.inbox(tool): 
    m = re.search(r"\bTLG\w*", f"{frm} {body}")
    if m:
        account = m.group()

        # will run a script with tool 
        out = subprocess.run(["sh", tool, account, body], capture_output = True, text = True)
        result = (out.stdout + out.stderr).strip()
        result = (result if account in result else f"In reference to account: {account}\n{result}")
        print(f"From: {tool}\nTo: {frm}\n{result}\n")  
        messages.post(tool, frm, result)