import telegram
from pathlib import Path
from shutil import rmtree
import sys
from glob import glob

messages = Path("messages")
messages.mkdir(exist_ok = True)

def log(frm, to, body):
    print(f"From: {frm}\nTo: {to}\n{body}\n\n---------------------------\n", flush = True)

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
    log(frm, to, body)
    if to.startswith("TLG"):
        telegram.post(int(to[3:]), body)
    else:
        folder = messages / to
        folder.mkdir(exist_ok = True)
        order = len(list(folder.glob((folder / frm).name + "*")))
        (folder / f"{frm}|{order + 1:06d}").write_text(body)

if __name__ == "__main__":
    frm, to, body = sys.argv[1:4]
    post(frm, to, body)