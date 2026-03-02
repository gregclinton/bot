# python3 workers/worker.py run groq openai/gpt-oss-120b Above Hal

import llm
import re
import storage
import sys
import messages

llm_provider, llm_model, chief, worker = sys.argv[1:]

def post(worker, text):
    for part in re.split(r'\n-{4,}\n', text.strip()):
        lines = [l.strip() for l in part.splitlines() if l.strip()]
        if len(lines) > 2 and lines[0].startswith('From:') and lines[1].startswith('To:'):
            frm = lines[0].split(':',1)[1].strip()
            to = lines[1].split(':',1)[1].strip()
            body = "\n".join(lines[2:])
            if frm == worker:
                print(f"From: {frm}\nTo: {to}\n{body}\n")
                messages.post(frm, to, body)

accounts = storage.root / "workers" / worker
accounts.mkdir(parents = True, exist_ok = True)

for msg in messages.inbox(worker):
    dashes = "----------------------------\n"
    format_time = lambda msg: msg.time.strftime("%A, %B %-d, %-I:%M %P")
    format_msg = lambda msg: f"{dashes}{format_time(msg)}\nFrom: {msg.frm}\nTo: {msg.to}\n{msg.body}\n"
    account = False

    if msg.frm == chief:
        for path in accounts.iterdir():
            with (accounts / account).open("a") as f:
                f.write(format_msg(msg))
    else:
        m = re.search(r"\bCX1\w*", f"{msg.frm} {msg.body}")
        if m:
            account = m.group()
            with (accounts / account).open("a") as f:
                f.write(format_msg(msg))

    if account:
        post(worker, llm.invoke(llm_provider, llm_model, "", (accounts / account).read_text()).strip())