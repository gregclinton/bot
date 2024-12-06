from fastapi import FastAPI, Request
import llm
from tool import bench
from time import sleep

threads = {}
max_llm_invokes = 10

def post_off_server(url, prompt):
    # here we would connect with another chatbot
    # set up a thread
    # and chat until we got some answer
    return { "content": "Sorry, can't help you. "}

def invoke(thread_id, prompt):
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

        if llm.counter > max_llm_invokes:
            content = "Could you please rephrase that?"
        elif "url" in response:
            response = post_off_server(response["url"], response["prompt"])
            content = response.get("content")
        elif "tool" in response:
            tool = response["tool"]
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

def thread_reset(id):
    threads[id] = { "messages": [], "installed" : {"brevity", "install"} }

@app.post('/mall/threads/{id}/messages')
async def post_message(req: Request, id: str):
    llm.reset_counter()
    return invoke(id, (await req.json())['prompt'])

@app.delete('/mall/threads/{id}/messages')
async def delete_messages(req: Request, id: str):
    thread_reset(id)
    return { "status": "success" }

@app.delete('/mall/threads/{id}/messages/last')
async def delete_last_message(req: Request, id: str):
    threads[id]["messages"].pop()
    return { "status": "success" }

thread_id = 111111

@app.post('/mall/threads')
async def post_thread(req: Request):
    global thread_id
    thread_id += 1
    id = str(thread_id)
    thread_reset(id)
    return { "id": id }

thread_reset("123456")
# print(invoke("123456", "Look up Medicare part A in chromadb database.")["content"])
