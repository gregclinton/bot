from fastapi import FastAPI, Request
import llm
from tool import bench
from time import sleep

app = FastAPI()
entities = {}

def invoke(entity, thread, prompt):
    instructions = open(f"ar/{entity}/Intake").read()
    messages = entities.setdefault(entity, {}).setdefault(thread, [])
    messages.append({"role": "user", "content": prompt})
    response = llm.invoke([{"role": "system", "content": instructions}] + messages)

    while "tool" in response:
        sleep(0.2)
        tool = response["tool"]
        prompt = response["prompt"]
        messages.append({"role": "assistant", "content": f"tool: {tool}, prompt: {prompt}"})
        if tool in bench:
            try:
                output = bench[tool]("", "", "", prompt)
                messages.append({"role": "assistant", "content": f"tool response: {output}"})
                response = llm.invoke([{"role": "system", "content": instructions}] + messages)
            except Exception as e:
                response = { "content": str(e) }
        else:
            response = { "content": "I made a mistake with a tool called " + response["tool"] + ". Apparently, there is no such tool." }

    messages.append({"role": "assistant", "content": response["content"]})
    #for msg in messages: print(msg)
    return response

@app.post('/mall/{entity}/messages/{thread}')
async def post_message(req: Request, entity: str, thread: str):
    return invoke(entity, thread, (await req.json())['prompt'])

# invoke("Code Castle", "12345", "Do you see chat.js? If so, display it.")
