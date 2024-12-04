from fastapi import FastAPI, Request
import llm
import tool
from time import sleep

app = FastAPI()
entities = {}

def invoke(entity, thread, prompt):
    sleep(0.2)
    instructions = open(f"ar/{entity}/Intake").read()
    messages = entities.setdefault(entity, {}).setdefault(thread, [])
    messages.append({"role": "user", "content": prompt})
    response = llm.invoke([{"role": "system", "content": instructions}] + messages)

    if "tool" in response:
        if response["tool"] in tool.bench:         
            try:
                response = { "content": tool.bench[response["tool"]]("", "", "", response["prompt"]) }
            except Exception as e:
                response = { "content": str(e) }
        else:
            response = { "content": "I made a mistake with a tool called " + response["tool"] + ". Apparently, there is no such tool." }

    messages.append({"role": "assistant", "content": response["content"]})
    return response

@app.post('/mall/{entity}/messages/{thread}')
async def post_message(req: Request, entity: str, thread: str):
    return invoke(entity, thread, (await req.json())['prompt'])

print(invoke("Code Castle", "12345", "List my python files.")["content"])
