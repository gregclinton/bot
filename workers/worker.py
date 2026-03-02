# python3 workers/worker.py groq openai/gpt-oss-120b Above Hal

import llm
import re
import storage
import sys
import messages
from types import SimpleNamespace

llm_provider, llm_model, chief, worker = sys.argv[1:]
accounts = storage.root / "workers" / worker
accounts.mkdir(parents = True, exist_ok = True)

def format_msg(msg):
    return f"{msg.time}\nFrom: {msg.frm}\nTo: {msg.to}\n{msg.body}\n----------------------------\n"

def post(worker, account, text):
    for part in re.split(r'\n-{4,}\n', text.strip()):
        lines = [l.strip() for l in part.splitlines() if l.strip()]
        if len(lines) > 2 and lines[0].startswith('From:') and lines[1].startswith('To:'):
            frm = lines[0].split(':',1)[1].strip()
            to = lines[1].split(':',1)[1].strip()
            body = "\n".join(lines[2:])
            if frm == worker:
                with (accounts / account).open("a") as f:
                    msg = SimpleNamespace(frm = frm, to = to, body = body, time = datetime.now().strftime("%A, %B %-d, %-I:%M %P"))
                    text = format_msg(msg)
                    f.write(text)
                    print(text)
                messages.post(frm, to, body)

for msg in messages.inbox(worker):
    account = False
    text = format_msg(msg)

    if msg.frm == chief:
        for path in accounts.iterdir():
            with (accounts / account).open("a") as f:
                f.write(text)
    else:
        m = re.search(r"\bCX1\w*", f"{msg.frm} {msg.body}")
        if m:
            account = m.group()

    if account:
        path = accounts / account
        with path.open("a") as f:
            f.write(text)
        post(worker, account, llm.invoke(llm_provider, llm_model, "", path.read_text()).strip())