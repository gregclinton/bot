import llm
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

def post(to, account, body):
    if to and body:
        body = body.strip()
        (accounts / account / f"{last_timestamp + 1}|{worker}|{to}").write_text(body)

        if to.startswith("TLG"):
            if worker == "Hal":
                telegram.post(to[3:], body)
        else:
            messages.post(worker, to, account, body)

for frm, account, body, timestamp in messages.inbox(worker):
    last_timestamp = timestamp

    if frm.startswith("TLG"):
        messages.log(frm, worker, account, body)

    incoming_accounts.add(account)
    (accounts / account).mkdir(exist_ok = True)
    (accounts / account / f"{timestamp}|{frm}|{worker}").write_text(body)

for account in incoming_accounts:
    text = ""
    all_msgs = [*instructions.iterdir(), *(accounts / account).iterdir()]
    for path in sorted(all_msgs, key = lambda p: float(p.name.split("|")[0])):
        timestamp, frm, to = path.name.split("|")
        timestamp = float(timestamp)
        time = datetime.fromtimestamp(timestamp).strftime("%A, %B %-d, %-I:%M %P")
        body = path.read_text()
        text += f"{time}\nFrom: {frm}\nTo: {to}\nAccount: {account}\n{body}\n-------------------------\n"

    response = llm.invoke(llm_provider, llm_model, "", text).strip() if text else ""
    to = body = ""

    for line in response.splitlines():
        if line.startswith("From:") or line.startswith("Account"):
            pass
        elif line.startswith("To:"):
            to = line.split(':')[1].strip()
        elif line.startswith("---"):
            post(to, account, body)
            to = body = ""
        else:
            body += f"{line}\n"

    post(to, account, body)