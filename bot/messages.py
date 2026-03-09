from pathlib import Path
from shutil import rmtree

# messages/to/from|order  body

messages = Path("messages")
messages.mkdir(exist_ok = True)

def log(frm, to, account, body):
    print(f"From: {frm}\nTo: {to}\nAccount: {account}\n{body}\n==========================", flush = True)

def inbox(name):
    folder = messages / name

    if folder.exists():
        for path in sorted(folder.iterdir(), key=lambda p: p.stat().st_mtime):
            frm, to, text, timestamp = path.name.split("|")[0], name, path.read_text(), int(path.stat().st_mtime)
            lines = text.split("\n")
            account = lines[0].split(":")[1].strip()
            body = "\n".join(lines[1:])
            yield frm, to, account, body, timestamp
        rmtree(folder)

def post(frm, to, account, body):
    log(frm, to, account, body)
    folder = messages / to
    folder.mkdir(exist_ok = True)
    order = len(list(folder.glob((folder / frm).name + "*")))
    body = body if body.startswith("Account:") else f"Account: {account}\n{body}"
    (folder / f"{frm}|{order + 1:06d}").write_text(body)