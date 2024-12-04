from fastapi import FastAPI, Request
import llm
import json

app = FastAPI()
entities = {}

@app.post('/mall/{entity}/messages/{thread}')
async def post_message(req: Request, entity: str, thread: str):
    instructions = open(f"ar/{entity}/Intake").read()
    prompt = (await req.json())['prompt']
    messages = entities.setdefault(entity, {}).setdefault(thread, [])
    messages.append({"role": "user", "content": prompt})
    completion = llm.invoke([{"role": "system", "content": instructions}] + messages)
    messages.append({"role": "assistant", "content": completion})
    return json.loads(completion) if completion.startswith("{") else { "content": completion }