from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from shutil import rmtree

messages = Path("messages")
messages.mkdir(exist_ok = True)

app = FastAPI()

@app.post("/messages/{name}")
async def post_message(req: Request, name: str):
    folder = messages / name
    msg = await req.json()
    frm, body = msg["frm"], msg["body"]
    print(f"From: {frm}\nTo: {name}\n{body}\n---------------------------\n", flush = True)
    folder.mkdir(exist_ok = True)
    (folder / frm).write_text(body)

@app.get("/messages/{name}")
async def get_messages(name: str):
    folder = messages / name
    msgs = []

    if folder.exists():
        for path in sorted(folder.iterdir(), key = lambda p: p.stat().st_mtime):
            msgs.append({
                "frm": path.name,
                "to": name,
                "body": path.read_text(),
                "timestamp": path.stat().st_mtime
            })

    if folder.exists():
        rmtree(folder)
    return msgs

app.mount("/", StaticFiles(directory = "chat", html = True))