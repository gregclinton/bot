import telegram
from pathlib import Path
from shutil import rmtree
import sys

messages = Path("messages")
messages.mkdir(exist_ok = True)

def log(frm, to, body):
    print(f"From: {frm}\nTo: {to}\n{body}\n\n---------------------------\n", flush = True)

def inbox(name):
    folder = messages / name

    if folder.exists():
        for path in sorted(folder.iterdir(), key=lambda p: p.stat().st_mtime):
            yield {
                "from": path.name.split("|")[1],
                "to": name,
                "body": path.read_text(),
                "timestamp": int(path.stat().st_mtime)
            }
        rmtree(folder)

def post(frm, to, body):
    log(frm, to, body)
    if to.startswith("TLG"):
        telegram.post(int(to[3:]), body)
    else:
        folder = messages / to
        folder.mkdir(exist_ok = True)
        order = len(list(folder.iterdir())) + 1000000
        (folder / f"{order}|{frm}").write_text(body)
        open("order","w").write(str(order + 1))

if __name__ == "__main__":
    frm, to, body = sys.argv[1:4]
    post(frm, to, body)
