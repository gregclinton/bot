from fastapi import FastAPI, Request, Response
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
            requests.delete(f'{url}/threads/{id}', headers = { 'Content-Type': 'text/plain' })

    threads[id] = { "messages": [], "installed" : ["brevity", "plot"], "bots": {} }
    return id

plain_text = lambda text: Response(text, media_type="text/plain")

@app.post('/threads/{id}/messages')
async def post_message(req: Request, id: str):
    return plain_text(chat.run(threads[id], (await req.body()).decode("utf-8")))

@app.delete('/threads/{id}')
async def delete_thread(req: Request, id: str):
    threads.pop(id, None)
    return plain_text("success")

@app.delete('/threads/{id}/messages')
async def delete_messages(req: Request, id: str):
    clear(id)
    return plain_text("success")

@app.delete('/threads/{id}/messages/last')
async def delete_last_message(req: Request, id: str):
    threads[id]["messages"].pop()
    return plain_text("success")

id = 111111

@app.post('/threads')
async def post_thread(req: Request):
    global id
    id += 1
    return plain_text(clear(str(id)))
