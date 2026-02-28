from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(default_response_class=PlainTextResponse)

@app.post('/threads/{id}/messages')
async def post_message(req: Request, id: str):
    if id in threads:
        return await chat.run((await req.body()).decode("utf-8"), threads[id])
    else:
        return "Connection has ended."

app.mount("/", StaticFiles(directory = "client", html = True))