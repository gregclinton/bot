from fastapi import FastAPI, Request
import llm
from tool import bench
from time import sleep

threads = {}
max_llm_invokes = 10

def invoke(thread_id, prompt):
    llm.reset_counter()
    thread = threads[thread_id]
    messages = thread["messages"]
    message = lambda role, content: { "role": role, "content": content }
    messages.append(message("user", prompt))
    content = None
    bulk = None

    while not content:
        sleep(0.2) # in case this loop runs away
        how = [message("system", "\n\n".join(open(f"how/{f}").read() for f in thread["installed"]))]
        response = llm.invoke(how + messages)
        content = response.get("content")
        tool = response.get("tool")

        if llm.counter > max_llm_invokes:
            content = "Could you please rephrase that?"
        elif tool
            if tool in bench:
                try:
                    output = bench[tool](response["text"], thread)
                    if len(output) > 20000:
                        bulk = output
                        output = "success"
                    messages.append(message("user", output))
                except Exception as e:
                    content = str(e)
            else:
                content = response["tool"] + " tool does not exist."

    messages.append(message("assistant", content))
    return { "content": bulk or content }

app = FastAPI()

def clear(id):
    if id in threads:
        for url, id in enumerate(threads[id]["bots"]):
            requests.delete(f'{url}/threads/{id}/messages', headers = { 'Content-Type': 'application/json' })

    threads[id] = { "messages": [], "installed" : {"brevity", "install"}, "bots": {} }
    return id

@app.post('/threads/{id}/messages')
async def post_message(req: Request, id: str):
    return invoke(id, (await req.json())['prompt'])

@app.delete('/threads/{id}/messages')
async def delete_messages(req: Request, id: str):
    clear(id)
    return { "status": "success" }

@app.delete('/threads/{id}/messages/last')
async def delete_last_message(req: Request, id: str):
    threads[id]["messages"].pop()
    return { "status": "success" }

thread_id = 111111

@app.post('/threads')
async def post_thread(req: Request):
    global thread_id
    thread_id += 1
    return { "id": clear(str(thread_id)) }

# print(invoke(clear("123456"), "Look up Medicare part A in chromadb database.")["content"])
