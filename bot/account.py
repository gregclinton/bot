import re
from random import randint
from pathlib import Path

accounts = Path("accounts")
accounts.mkdir(exist_ok = True)

def scrape(text):
    # you should implement this yourself
    m = re.search(r"\bTLG\w*", text)
    return m.group() if m else None

def get(session):
    # you should implement this yourself
    path = accounts / session

    if path.exists():
        account = path.read_text()
    else:
        account = f"TLG{10000000 + randint(1, 9999999)}"
        path.write_text(account)

    return account