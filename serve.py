from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
import chat

app = FastAPI(default_response_class=PlainTextResponse)

threads = {}

def clear(id):
    for url, bot_id in threads.get(id, {}).get("bots", {}).items():
        requests.delete(f'{url}/threads/{bot_id}', headers={ 'Content-Type': 'text/plain' })

    threads[id] = { "messages": [], "docs": ["brevity", "speech", "code", "plotly"], "bots": {}, "runs": [] }
    return id

@app.post('/threads/{id}/messages')
async def post_message(req: Request, id: str):
    thread = threads[id]
    thread["runs"].append(len(thread["messages"]))
    return chat.run((await req.body()).decode("utf-8"), thread)

@app.delete('/threads/{id}')
async def delete_thread(id: str):
    threads.pop(id, None)
    return "success"

@app.delete('/threads/{id}/messages')
async def delete_messages(id: str):
    clear(id)
    return "success"

@app.delete('/threads/{id}/messages/last')
async def delete_last_message(id: str):
    if id in threads:
        thread = threads[id]
        del thread["messages"][thread["runs"].pop():]
    return "success"

id = 111111

@app.post('/threads')
async def post_thread():
    global id
    id += 1
    return clear(str(id))
