import llm
import sys
import messages
from pathlib import Path
from account import scrape
from random import choice

workers = Path("workers")

def chronology(*folders):
    pairs = [(p.stat().st_mtime, p) for f in folders for p in f.iterdir()]
    pairs.sort()
    return pairs

def run(worker, llm_provider, llm_model):
    root = workers / worker
    instructions = root / "instructions"
    accounts = root / "accounts"

    def write(folder, frm, to, body):
        folder.mkdir(parents = True, exist_ok = True)
        while True:
            random = ''.join(choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(5))
            path = folder / f"{frm}|{to}|{random}"
            if not path.exists():
                path.write_text(body)
                break

    def post(worker, to, account, body):
        if body:
            if account not in f"{to} {body}":
                body = f"In reference to account: {account}\n{body}"
            body = body.strip()
            write(accounts / account, worker, to, body)
            if to != account:
                messages.post(worker, to, body)

    incoming_accounts = set()

    for frm, body in messages.inbox(worker):
        account = scrape(f"{frm} {body}")
        if account:
            incoming_accounts.add(account)
            folder = accounts / account
        else:
            folder = instructions
        write(folder, frm, worker, body)

    for account in incoming_accounts:
        text = ""

        for timestamp, path in chronology(instructions, accounts / account):
            frm, to, _ = path.name.split("|")
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
        for timestamp, path in chronology(folder):
            if timestamp > after:
                frm, to, _ = path.name.split("|")
                if account in [frm, to]:
                    body = path.read_text()
                    yield frm, body, timestamp

if __name__ == "__main__":
    globals()[sys.argv[1]](*sys.argv[2:])