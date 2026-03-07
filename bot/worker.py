import llm
import re
import sys
import messages
from datetime import datetime
from pathlib import Path

llm_provider, llm_model, worker = sys.argv[1:]
root = Path("workers")
root.mkdir(exist_ok = True)
root = root / worker
root.mkdir(exist_ok = True)

accounts = root / "accounts"
accounts.mkdir(exist_ok = True)

instructions = root / "instructions"
instructions.mkdir(exist_ok = True)

# accounts/account/timestamp|frm|to   body
# instructions/timestamp|frm|fo   body

incoming_accounts = set()

for msg in messages.inbox(worker):
    frm, to, body, timestamp = msg["from"], msg["to"], msg["body"], msg["timestamp"]
    last_timestamp = timestamp
    # only account numbers starting with TLG, but not TLG23456, are real accounts
    # TLG23456 is for instructional purposes only
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

    response = llm.invoke(llm_provider, llm_model, "", text) if text else ""

    for part in re.split(r'\n-{4,}\n', response.strip()):
        lines = [l.strip() for l in part.splitlines() if l.strip()]
        if len(lines) > 2 and lines[0].startswith('From:') and lines[1].startswith('To:'):
            frm = lines[0].split(':',1)[1].strip()
            to = lines[1].split(':',1)[1].strip()
            body = "\n".join(lines[2:])
            if frm == worker:
                (accounts / account / f"{last_timestamp + 0.0001}|{frm}|{to}").write_text(body)
                messages.post(frm, to, body)