import llm
import sys
import messages
from pathlib import Path
import re

def run(worker, llm_provider, llm_model):
    last_timestamp = 0

    def post(worker, to, account, body):
        if body:
            if account not in f"{to} {body}":
                body = f"In reference to account: {account}\n{body}"
            body = body.strip()
            (accounts / account / f"{last_timestamp + 1}|{worker}|{to}").write_text(body)
            messages.post(worker, to, body)

    instructions = root / "instructions"
    incoming_accounts = set()

    for frm, body, timestamp in messages.inbox(worker):
        last_timestamp = timestamp
        m = re.search(r"\bTLG\w*", f"{frm} {body}")
        if m:
            account = m.group()
            incoming_accounts.add(account)
            folder = accounts / account
        else:
            folder = instructions
        folder.mkdir(parents = True, exist_ok = True)
        (folder / f"{timestamp}|{frm}|{worker}").write_text(body)

    for account in incoming_accounts:
        text = ""
        all_msgs = [*instructions.iterdir(), *(accounts / account).iterdir()]
        for path in sorted(all_msgs, key = lambda p: float(p.name.split("|")[0])):
            _, frm, to = path.name.split("|")
            body = path.read_text()
            text += f"\nFrom: {frm}\nTo: {to}\n{body}\n"

        to = frm
        text = text.replace("????????", account)
        text += f"\nFrom: {worker}"
        response = llm.invoke(llm_provider, llm_model, "", text).strip()
        print(f"From: {worker}\n{response}\n")
        body = ""

        for line in response.splitlines():
            if line.startswith("To:"):
                post(worker, to, account, body)
                to = line.split(':')[1].strip()
                body = ""
            elif not line.startswith("From:"):
                body += f"{line}\n"

        post(worker, to, account, body)

def chat(worker, account, timestamp):
    root = Path("workers") / worker
    accounts = root / "accounts"
    accounts.mkdir(parents = True, exist_ok = True)
    folder = accounts / account

    if folder.exists():
        for path in folder.iterdir():
            ts, frm, _ = path.name.split("|")
            ts = int(ts)
            if ts > timestamp and frm in [worker, account]:
                body = path.read_text()
                yield frm, body, ts

if __name__ == "__main__":
    globals()[sys.argv[1]](*sys.argv[2:])