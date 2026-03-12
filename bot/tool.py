import sys
import messages
import subprocess
import re

tool = sys.argv[1]

for frm, body, timestamp in messages.inbox(tool):
    # will run a script with tool name
    out = subprocess.run(["sh", tool, body], capture_output = True, text = True)
    result = (out.stdout + out.stderr).strip()
    print(f"From: {tool}\nTo: {frm}\n{result}\n")  
    messages.post(tool, frm, result)