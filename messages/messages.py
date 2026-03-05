from pathlib import Path
from fastapi import FastAPI, Request, Query
from fastapi.staticfiles import StaticFiles
from shutil import rmtree

messages = Path("messages")
messages.mkdir(exist_ok = True)

app = FastAPI()

from fastapi import Query

@app.post("/messages")
async def post_message(frm: str = Query(..., alias = "from"), to: str = Query(...), body: str = Query(...)):
    folder = messages / to
    print(f"From: {frm}\nTo: {to}\n{body}\n---------------------------\n", flush=True)
    folder.mkdir(exist_ok = True)
    (folder / frm).write_text(body)
    return {"status": "ok"}

@app.get("/messages")
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