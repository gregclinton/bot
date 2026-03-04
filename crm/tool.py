import sys
import messages
import subprocess

tool = sys.argv[1:]

for msg in messages.inbox(tool):
    # will run a script with tool name
    out = subprocess.run(["sh", tool, msg.body], capture_output = True, text = True)
    messages.post(tool, msg.frm, out.stdout + out.stderr)