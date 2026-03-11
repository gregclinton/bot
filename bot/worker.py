import llm
import sys
import messages
from datetime import datetime
from pathlib import Path
import re

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
#     instructions/timestamp|from|to   body

incoming_accounts = set()
last_timestamp = 0

def post(to, account, body):
    if to and body:
        body = body.strip()
        (accounts / account / f"{last_timestamp + 1}|{worker}|{to}").write_text(body)
        messages.post(worker, to, body)

for frm, body, timestamp in messages.inbox(worker):
    if frm.startswith("TLG"):
        print(f"From Customer:\nTo: {worker}\n{body}\n")

    last_timestamp = timestamp
    m = re.search(r"\bTLG\w*", f"{frm} {body}")
    if m:
        account = m.group()
        incoming_accounts.add(account)
        (accounts / account).mkdir(exist_ok = True)
        (accounts / account / f"{timestamp}|{frm}|{worker}").write_text(body)
    else:
        (instructions / f"{timestamp}|{frm}|{worker}").write_text(body)

for account in incoming_accounts:
    text = ""
    all_msgs = [*instructions.iterdir(), *(accounts / account).iterdir()]
    for path in sorted(all_msgs, key = lambda p: float(p.name.split("|")[0])):
        timestamp, frm, to = path.name.split("|")
        body = path.read_text()
        anonymize = lambda id: "Customer" if id.startswith("TLG") else id
        text += f"\nFrom {anonymize(frm)}:\nTo: {anonymize(to)}\n{body}\n"

    text += f"\nFrom {worker}:"
    response = llm.invoke(llm_provider, llm_model, "", text).strip() if text else ""
    print(f"From {worker}:\n{response.strip()}\n")

    to = body = ""

    for line in response.splitlines():
        if line.startswith("To:"):
            post(to, account, body)
            to = line.split(':')[1].strip()
            to = account if to == "Customer" else to
            body = ""
        else:
            body += f"{line}\n"

    post(to, account, body)