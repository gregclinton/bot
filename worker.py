import llm
import re
import sys
import messages
from datetime import datetime
from pathlib import Path
import telegram

llm_provider, llm_model, worker = sys.argv[1:]
root = Path("workers")
root.mkdir(exist_ok = True)
root = root / worker
root.mkdir(exist_ok = True)

accounts = root / "accounts"
accounts.mkdir(exist_ok = True)

instructions = root / "instructions"
instructions.mkdir(exist_ok = True)

# accounts/account/timestamp|from|to   body
#     instructions/timestamp|from|fo   body

incoming_accounts = set()
last_timestamp = 0

def post(worker, frm, to, body):
    if frm == worker and to and body:
        body = body.strip()
        (accounts / account / f"{last_timestamp + 1}|{frm}|{to}").write_text(body)
        if to.startswith("TLG"):
            if frm == "Hal":
                telegram.post(to[3:], body)
        else:
            messages.post(frm, to, body)

for msg in messages.inbox(worker):
    frm, to, body, timestamp = msg["from"], msg["to"], msg["body"], msg["timestamp"]
    last_timestamp = timestamp

    m = re.search(r"\bTLG\w*", f"{frm} {body}")
    if m and m.group() != "TLG12345678":
        account = m.group()
        incoming_accounts.add(account)
        (accounts / account).mkdir(exist_ok = True)
        (accounts / account / f"{timestamp}|{frm}|{to}").write_text(body)
    else:
        (instructions / f"{timestamp}|{frm}|{to}").write_text(body)

for account in incoming_accounts:
    text = ""
    all_msgs = [*instructions.iterdir(), *(accounts / account).iterdir()]
    for path in sorted(all_msgs, key = lambda p: float(p.name.split("|")[0])):
        timestamp, frm, to = path.name.split("|")
        timestamp = float(timestamp)
        time = datetime.fromtimestamp(timestamp).strftime("%A, %B %-d, %-I:%M %P")
        body = path.read_text()
        text += f"{time}\nFrom: {frm}\nTo: {to}\n{body}\n----------------------------\n"

    response = llm.invoke(llm_provider, llm_model, "", text).strip() if text else ""
    frm = to = body = ""

    for line in response.splitlines():
        if line.startswith("From:"):
            frm = line.split(':')[1].strip()
        elif line.startswith("To:"):
            to = line.split(':')[1].strip()
        elif line.startswith("---"):
            post(worker, frm, to, body)
            frm = to = body = ""
        else:
            body += f"{line}\n"

    post(worker, frm, to, body)