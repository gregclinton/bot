# python3 worker.py run Billing groq openai/gpt-oss-120b

import llm
import sys
import messages
import remote
from pathlib import Path
from account import scrape
import unique
import chronological

workers = Path("workers")

def run(worker, llm_provider, llm_model):
    while True:
        root = workers / worker
        instructions = root / "instructions"
        accounts = root / "accounts"

        def post(worker, to, account, body):
            body = body.strip()
            if body:
                if account not in f"{to} {body}":
                    body = f"In reference to account: {account}\n{body}"
                unique.path(accounts / account, f"{worker}|{to}").write_text(body)
                (remote if to == account else messages).post(worker, to, body)

        incoming_accounts = set()

        for frm, body, _, path in messages.inbox(worker):
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

            for line in response.splitlines():
                if line.startswith("To:"):
                    post(worker, to, account, body)
                    to = line.split(':')[1].strip()
                    body = ""
                elif not line.startswith("From:"):
                    body += f"{line}\n"

            post(worker, to, account, body)

if __name__ == "__main__":
    globals()[sys.argv[1]](*sys.argv[2:])