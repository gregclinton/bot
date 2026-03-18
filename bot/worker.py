import llm
import sys
import messages
from pathlib import Path
import re

workers = Path("workers")

def run(worker, llm_provider, llm_model):
    root = workers / worker
    instructions = root / "instructions"
    accounts = root / "accounts"

    def write(folder, frm, to, body):
        folder.mkdir(parents = True, exist_ok = True)
        order = 1000000 + len(list(folder.iterdir()))
        (folder / f"{order}|{frm}|{to}").write_text(body)

    def post(worker, to, account, body):
        if body:
            if account not in f"{to} {body}":
                body = f"In reference to account: {account}\n{body}"
            body = body.strip()
            write(accounts / account, worker, to, body)
            messages.post(worker, to, body)

    incoming_accounts = set()

    for frm, body, _ in messages.inbox(worker):
        m = re.search(r"\bTLG\w*", f"{frm} {body}")
        if m:
            account = m.group()
            incoming_accounts.add(account)
            folder = accounts / account
        else:
            folder = instructions
        write(folder, frm, worker, body)

    for account in incoming_accounts:
        text = ""
        all_msgs = [*instructions.iterdir(), *(accounts / account).iterdir()]
        for path in sorted(all_msgs, key = lambda p: p.stat().st_mtime):
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

def chat(worker, account, after):
    folder = workers / worker / "accounts" / account

    if folder.exists():
        for path in folder.iterdir():
            order, frm, to = path.name.split("|")
            order = int(order)
            if order > after and frm in [worker, account] and to in [worker, account]:
                body = path.read_text()
                yield order, frm, body

if __name__ == "__main__":
    globals()[sys.argv[1]](*sys.argv[2:])