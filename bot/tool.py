import sys
import messages
import subprocess
import re

tool = sys.argv[1]

for frm, account, body, timestamp in messages.inbox(tool):
    # will run a script with tool name
    out = subprocess.run(["sh", tool, body], capture_output = True, text = True)
    result = out.stdout + out.stderr
    print(f"{tool}:\n{result.strip()}\n")  
    messages.post(tool, frm, account, result)