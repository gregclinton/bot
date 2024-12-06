from fastapi import FastAPI, Request
import logging
import chat

app = FastAPI()

if True:
    logging.getLogger("uvicorn.access").disabled = True
    logging.getLogger("uvicorn.error").disabled = True
    logging.getLogger("fastapi").disabled = True

print("I'm up.", flush=True)

threads = {}

def clear(id):
    if id in threads:
        for url, id in enumerate(threads[id]["bots"]):
            requests.delete(f'{url}/threads/{id}/messages', headers = { 'Content-Type': 'application/json' })

    threads[id] = { "messages": [], "installed" : {"brevity", "install"}, "bots": {} }
    return id

@app.post('/threads/{id}/messages')
async def post_message(req: Request, id: str):
    return chat.run(threads[id], (await req.json())['prompt'])

@app.delete('/threads/{id}/messages')
async def delete_messages(req: Request, id: str):
    clear(id)
    return { "status": "success" }

@app.delete('/threads/{id}/messages/last')
async def delete_last_message(req: Request, id: str):
    threads[id]["messages"].pop()
    return { "status": "success" }

id = 111111

@app.post('/threads')
async def post_thread(req: Request):
    global id
    id += 1
    return { "id": clear(str(id)) }
