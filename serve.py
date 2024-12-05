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

def invoke(thread, prompt):
    make_message = lambda role, content: { "role": role, "content": content }
    instructions = [make_message("system", open("instructions").read())]
    assistant = lambda content: make_message("assistant", content)
    bulk = None

    messages = threads.setdefault(thread, [])
    messages.append(make_message("user", prompt))
    response = llm.invoke(instructions + messages)
    content = response.get("content")

    while not content:
        sleep(0.2) # in case this loop runs away
        if llm.counter > max_llm_invokes:
            content = "Could you please rephrase that?"
        elif "url" in response:
            response = post_off_server(response["url"], response["prompt"])
            content = response.get("content")
        elif "tool" in response:
            tool = response["tool"]
            messages.append(assistant(f"tool: {tool}"))
            if tool in bench:
                try:
                    output = bench[tool](response)
                    if len(output) > 20000:
                        bulk = output
                        output = "<bulk>"
                    messages.append(assistant(f"tool response: {output}"))
                    response = llm.invoke(instructions + messages)
                    content = response.get("content")
                except Exception as e:
                    content = str(e)
            else:
                content = response["tool"] + " tool does not exist."

    messages.append(assistant(content))
    return { "content": bulk or content }

app = FastAPI()

@app.post('/mall/messages/{thread}')
async def post_message(req: Request, thread: str):
    llm.reset_counter()
    return invoke(thread, (await req.json())['prompt'])

# print(invoke("123456", "Hello.")["content"])
