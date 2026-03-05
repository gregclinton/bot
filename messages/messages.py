from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from shutil import rmtree

messages = Path("messages")
messages.mkdir(exist_ok = True)

app = FastAPI()

@app.post("/messages")
async def post_message(req: Request):
    return "ok"
    msg = await req.json()
    frm, to, body = msg["from"], msg["to"], msg["body"]
    folder = messages / to
    folder.mkdir(exist_ok = True)
    (folder / frm).write_text(body)
    print(f"From: {frm}\nTo: {to}\n{body}\n---------------------------\n", flush=True)
    return {"status": "ok"}

@app.get("/messages/{name}")
async def get_messages(name: str):
    folder = messages / name
    msgs = []

    if folder.exists():
        for path in sorted(folder.iterdir(), key=lambda p: p.stat().st_mtime):
            msgs.append({
                "from": path.name,
                "to": name,
                "body": path.read_text(),
                "timestamp": path.stat().st_mtime
            })
        rmtree(folder)

    return msgs

app.mount("/", StaticFiles(directory = "chat", html = True))