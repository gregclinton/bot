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
                completion = { "content": tool.bench[msg.to_]("", "", "", completion["prompt"]) }
                del response["tool"]
            except Exception as e:
                response = { "content": str(e) }
    else:
        messages.append({"role": "assistant", "content": response["content"]})
    return response

@app.post('/mall/{entity}/messages/{thread}')
async def post_message(req: Request, entity: str, thread: str):
    return invoke(entity, thread, (await req.json())['prompt'])

print(invoke("Plaza", "12345", "My name is Greg.")["content"])
print(invoke("Plaza", "12345", "What is my name?")["content"])