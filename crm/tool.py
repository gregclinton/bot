import sys
import messages
import subprocess

tool = sys.argv[1]
print(tool)

for msg in messages.inbox(tool):
    # will run a script with tool name
    out = subprocess.run(["sh", tool, msg.body], capture_output = True, text = True)
    result = out.stdout + out.stderr
    messages.post(tool, msg.frm, result)