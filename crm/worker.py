# cp crm and app tools py files to a folder and cd there
# python3 worker.py groq openai/gpt-oss-120b Above Hal

import llm
import re
import storage
import sys
import messages
from types import SimpleNamespace
from datetime import datetime

llm_provider, llm_model, chief, worker = sys.argv[1:]
root = storage.root / "workers" / worker

accounts = root / "accounts"
accounts.mkdir(parents = True, exist_ok = True)

instructions = root / "instructions"
instructions.mkdir(parents = True, exist_ok = True)

# accounts/account/order-timestamp-frm-to   body
# instructions/order-timestamp-frm-fo   body
#  we can't allow hyphens in frm or to

incoming_accounts = set()
order = 0
timestamp = 0

for msg in messages.inbox(worker):
    if msg.frm == chief:
        (instructions / f"{2 * msg.order}-{msg.timestamp}-{msg.frm}-{worker}").write_text(msg.body)
    else:
        m = re.search(r"\bCX1\w*", f"{msg.frm} {msg.body}")
        if m:
            account = m.group()
            incoming_accounts.add(account)
            (accounts / account).mkdir(parents = True, exist_ok = True)
            (accounts / account / f"{2 * msg.order}-{msg.timestamp}-{msg.frm}-{msg.to}").write_text(msg.body)
            if msg.order > order:
                order = msg.order
                timestamp = msg.timestamp

for account in incoming_accounts:
    text = ""
    for path in sorted([*instructions.iterdir(), *(accounts / account).iterdir()], key = lambda p: p.name.split("-")[0]):
        order, timestamp, frm, to = path.name.split("-")      
        order = int(order)
        timestamp = int(timestamp)
        time = datetime.fromtimestamp(timestamp).strftime("%A, %B %-d, %-I:%M %P")
        body = path.read_text()
        text += f"{time}\nFrom: {frm}\nTo: {to}\n{body}\n----------------------------\n"

    response = llm.invoke(llm_provider, llm_model, "", text)

    for part in re.split(r'\n-{4,}\n', response.strip()):
        lines = [l.strip() for l in part.splitlines() if l.strip()]
        if len(lines) > 2 and lines[0].startswith('From:') and lines[1].startswith('To:'):
            frm = lines[0].split(':',1)[1].strip()
            to = lines[1].split(':',1)[1].strip()
            body = "\n".join(lines[2:])
            if frm == worker:
                (accounts / account / f"{2 * order + 1}-{timestamp}-{frm}-{to}").write_text(body)
                messages.post(frm, to, body)