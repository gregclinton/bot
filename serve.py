from fastapi import FastAPI, Request
import chat

logging.getLogger('uvicorn').setLevel(logging.ERROR)

app = FastAPI()

threads = {}

def clear(id):
    if id in threads:
        for url, id in enumerate(threads[id]["bots"]):
            requests.delete(f'{url}/threads/{id}/messages', headers = { 'Content-Type': 'application/json' })

    threads[id] = { "messages": [], "installed" : {"brevity", "shell"}, "bots": {} }
    return id

@app.post('/threads/{id}/messages')
async def post_message(req: Request, id: str):
    return chat.rum(threads[id], (await req.json())['prompt'])

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
