from pathlib import Path
from shutil import rmtree
import sys

# messages/to/from|order  body

messages = Path("messages")
messages.mkdir(exist_ok = True)

def inbox(name):
    folder = messages / name

    if folder.exists():
        for path in sorted(folder.iterdir(), key=lambda p: p.stat().st_mtime):
            yield {
                "from": path.name.split("|")[0],
                "to": name,
                "body": path.read_text(),
                "timestamp": int(path.stat().st_mtime)
            }
        rmtree(folder)

def post(frm, to, body):
    print(f"From: {frm}\nTo: {to}\n{body}\n==========================", flush = True)
    folder = messages / to
    folder.mkdir(exist_ok = True)
    order = len(list(folder.glob((folder / frm).name + "*")))
    (folder / f"{frm}|{order + 1:06d}").write_text(body)

def parse(cuts, text):
    frm = to = body = ""

    for line in text.splitlines():
        if line.startswith("From:"):
            frm = line.split(':')[1].strip()
        elif line.startswith("To:"):
            to = line.split(':')[1].strip()
        elif line.startswith(cuts) and frm and to and body:
            yield {"from": frm, "to": to, "body": body}
            frm = to = body = ""
        else:
            body += f"{line}\n"

    if frm and to and body:
        yield { "from": frm, "to": to, "body": body }

def instruct(text):
    for msg in parse("===", text):
        post(msg["from"], msg["to"], msg["body"])
    
if __name__ == "__main__":
    globals()[sys.argv[1]](*sys.argv[2:])