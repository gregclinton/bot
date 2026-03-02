# python3 workers/worker.py groq openai/gpt-oss-120b Above Hal

import llm
import re
import storage
import sys
import messages
from types import SimpleNamespace

llm_provider, llm_model, chief, worker = sys.argv[1:]
root = storage.root / "workers" / worker
accounts = root / "accounts"
instructions = root / "instructions"
accounts.mkdir(parents = True, exist_ok = True)

# /storage/workers/worker/accounts/account/order-timestamp-frm-to   body
# /storage/workers/worker/instructions/order-timestamp-frm   body
#  we can't allow hyphens in frm or to

def format_msg(msg):
    time = datetime.fromtimestamp(msg.timestamp)
    return f"{time}\nFrom: {msg.frm}\nTo: {msg.to}\n{msg.body}\n----------------------------\n"

def post(worker, account, order, timestamp, text):
    for part in re.split(r'\n-{4,}\n', text.strip()):
        lines = [l.strip() for l in part.splitlines() if l.strip()]
        if len(lines) > 2 and lines[0].startswith('From:') and lines[1].startswith('To:'):
            frm = lines[0].split(':',1)[1].strip()
            to = lines[1].split(':',1)[1].strip()
            body = "\n".join(lines[2:])
            if frm == worker:
                (accounts / account / f"{order}-{timestamp}-{frm}-{to}").write_text(body)
                messages.post(frm, to, body)

incoming_accounts = set()
order = 0
timestamp = 0

for msg in messages.inbox(worker):
    if msg.frm == chief:
        (instructions / f"{msg.order}-{msg.timestamp}-{msg.frm}").write_text(msg.body)
    else:
        m = re.search(r"\bCX1\w*", f"{msg.frm} {msg.body}")
        if m:
            account = m.group()
            incoming_accounts.add(account)
            (accounts / account / f"{msg.order}-{msg.timestamp}-{msg.frm}-{msg.to}").write_text(msg.body)
            if msg.order > order:
                order = msg.order
                timestamp = msg.timestamp

for account in incoming_accounts:
    # concatenate all instructions and all msgs for this account and pass to llm
    # datetime.now().strftime("%A, %B %-d, %-I:%M %P")
    text = ""
    response = llm.invoke(llm_provider, llm_model, "", text)
    post(worker, account, order + 1, timestamp, response)
