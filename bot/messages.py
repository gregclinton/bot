import telegram
from pathlib import Path
from shutil import rmtree
from threading import Thread

messages = Path("messages")
messages.mkdir(exist_ok = True)

def log(frm, to, body):
    print(f"From: {frm}\nTo: {to}\n{body}\n\n---------------------------\n", flush = True)

def poll_telegram():
    while True:
        try:
            for msg in telegram.inbox():
                post(f"TLG{msg['from']}", "Hal", msg["body"])
        except:
            pass

Thread(target = poll_telegram, daemon = True).start()

def inbox(name):
    folder = messages / name

    if folder.exists():
        for path in sorted(folder.iterdir(), key=lambda p: p.stat().st_mtime):
            yield {
                "from": path.name,
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
        (folder / frm).write_text(body)