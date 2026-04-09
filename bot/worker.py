import llm
import sys
import messages
from pathlib import Path
from account import scrape
import unique
import chronological

def run(worker, llm_provider, llm_model):
    root = Path("workers") / worker
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
            text += f"\n\nFrom: {frm}\nTo: {to}\n{body}"

        to = frm
        text = text.replace("<account>", account)
        text += f"\nFrom: {worker}"
        response = llm.invoke(llm_provider, llm_model, "Be brief.", text)
        print(f"From: {worker}\n{response}\n")
        body = ""

        def post():
            if body.strip():
                text = f"In reference to account: {account}\n{body}" if account not in f"{to} {body}" else body
                unique.path(accounts / account, f"{worker}|{to}").write_text(text)
                messages.post(worker, to, text)

        for line in response.splitlines():
            if line.startswith("To:"):
                post()
                to = line.split(':')[1].strip()
                body = ""
            elif not line.startswith("From:"):
                body += f"\n{line}"

        post()

if __name__ == "__main__":
    globals()[sys.argv[1]](*sys.argv[2:])