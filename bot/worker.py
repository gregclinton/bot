import llm
import sys
import messages
from pathlib import Path
from account import scrape
import unique
import chronological

workers = Path("workers")

def run(worker, llm_provider, llm_model):
    root = workers / worker
    instructions = root / "instructions"
    accounts = root / "accounts"
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

        for timestamp, path in chronological.paths(instructions, accounts / account):
            frm, to, _ = path.name.split("|")
            body = path.read_text()
            text += f"\nFrom: {frm}\nTo: {to}\n{body}\n"

        to = frm
        text = text.replace("<account>", account)
        text += f"\nFrom: {worker}"
        response = llm.invoke(llm_provider, llm_model, "", text).strip()
        print(f"From: {worker}\n{response}\n")
        body = ""

        def post():
            stripped = body.strip()
            if stripped:
                if account not in f"{to} {stripped}":
                    stripped = f"In reference to account: {account}\n{stripped}"
                unique.path(accounts / account, f"{worker}|{to}").write_text(stripped)
                messages.post(worker, to, stripped)

        for line in response.splitlines():
            if line.startswith("To:"):
                post()
                to = line.split(':')[1].strip()
                body = ""
            elif not line.startswith("From:"):
                body += f"{line}\n"

        post()

if __name__ == "__main__":
    globals()[sys.argv[1]](*sys.argv[2:])