import sys
import messages
import subprocess
import re

tool = sys.argv[1]

for frm, to, body, timestamp in messages.inbox(tool):
    # will run a script with tool name
    out = subprocess.run(["sh", tool, body], capture_output = True, text = True)
    result = out.stdout + out.stderr
    m = re.search(r"\bTLG\w*", f"{body}")
    result = f"Account: {m.group()}\n{result}" if m else result
    messages.post(tool, frm, result)