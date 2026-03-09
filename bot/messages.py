from pathlib import Path
from shutil import rmtree

# messages/to/account/from|order  body

messages = Path("messages")
messages.mkdir(exist_ok = True)

def log(frm, to, account, body):
    pass #print(f"From: {frm}\nTo: {to}\nAccount: {account}\n{body}\n==========================", flush = True)

def inbox(name):
    folder = messages / name

    if folder.exists():
        paths = []

        for account in folder.iterdir():
            for path in account.iterdir():
                paths.append(path)

        for path in sorted(paths, key = lambda p: p.stat().st_mtime):
            frm = path.name.split("|")[0]
            account, body, timestamp = path.parent.name, path.read_text(), int(path.stat().st_mtime)
            yield frm, account, body, timestamp

        rmtree(folder)

def post(frm, to, account, body):
    log(frm, to, account, body)
    folder = messages / to / account
    folder.mkdir(parents = True, exist_ok = True)
    order = len(list(folder.glob((folder / frm).name + "*")))
    (folder / f"{frm}|{order + 1:06d}").write_text(body)