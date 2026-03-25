import llm
import sys
import messages
from pathlib import Path
from account import scrape
import unique

workers = Path("workers")

def chronology(*folders):
    pairs = [(p.stat().st_mtime, p) for f in folders for p in f.iterdir()]
    pairs.sort()
    return pairs

def run(worker, llm_provider, llm_model):
    root = workers / worker
    instructions = root / "instructions"
    accounts = root / "accounts"

    def post(worker, to, account, body):
        body = body.strip()
        if body:
            if account not in f"{to} {body}":
                body = f"In reference to account: {account}\n{body}"
            unique.path(accounts / account, f"{worker}|{to}").write_text(body)
            if to != account:
                messages.post(worker, to, body)

    incoming_accounts = set()

    for frm, body, path in messages.inbox(worker):
        account = scrape(f"{frm} {body}")
        if account:
            incoming_accounts.add(account)
            folder = accounts / account
        else:
            folder = instructions
        path.rename(unique.path(folder, f"{frm}|{worker}"))

    for account in incoming_accounts:
        text = ""

        for timestamp, path in chronology(instructions, accounts / account):
            frm, to, _ = path.name.split("|")
            body = path.read_text()
            text += f"\nFrom: {frm}\nTo: {to}\n{body}\n"

        to = frm
        text = text.replace("<account>", account)
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
        for timestamp, path in chronology(folder):
            if timestamp > after:
                frm, to, _ = path.name.split("|")
                if account in [frm, to]:
                    body = path.read_text()
                    yield frm, body, timestamp

if __name__ == "__main__":
    globals()[sys.argv[1]](*sys.argv[2:])