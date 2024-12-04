from fastapi import FastAPI, Request
import llm
import json
import tool

app = FastAPI()
entities = {}

def invoke(entity, thread, prompt):
    instructions = open(f"ar/{entity}/Intake").read()
    messages = entities.setdefault(entity, {}).setdefault(thread, [])
    messages.append({"role": "user", "content": prompt})
    completion = llm.invoke([{"role": "system", "content": instructions}] + messages)
    messages.append({"role": "assistant", "content": completion})
    completion = json.loads(completion) if completion.startswith("{") else completion
    if "tool" in completion:
        if completion["tool"] in tool.bench:
            try:
                completion = { "content": tool.bench[msg.to_]("", "", "", completion["prompt"]) }
                del completion["tool"]
            except Exception as e:
                completion = { "content": str(e) }
    return { "content": completion }

@app.post('/mall/{entity}/messages/{thread}')
async def post_message(req: Request, entity: str, thread: str):
    return invoke(entity, thread, (await req.json())['prompt'])

print(invoke("Plaza", "12345", "Hello")["content"])