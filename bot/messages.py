from pathlib import Path
from shutil import rmtree
import unique
import sys
from account import scrape
import chronological

# messages/to/from|random  body
# chats/account/from|random  body

messages = Path("messages")
chats = Path("chats")

def inbox(to):
    folder = messages / to

    if folder.exists():
        for path in sorted(folder.iterdir(), key = lambda p: p.stat().st_mtime):
            frm = path.name.split("|")[0]
            body = path.read_text()
            yield frm, body, path

        rmtree(folder)

def post(frm, to, body):
    unique.path(messages / to, frm).write_text(body)
    account = scrape(f"{frm} {to}")
    if account:
        unique.path(chats / account, frm).write_text(body)

def chat(account, after):
    folder = chats / account

    if folder.exists():
        for timestamp, path in chronological.paths(folder):
            if timestamp > after:
                frm = path.name.split("|")[0]
                body = path.read_text()
                yield "me" if frm == account else "ai", body, timestamp

if __name__ == "__main__":
    globals()[sys.argv[1]](*sys.argv[2:])