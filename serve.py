from fastapi import FastAPI, Request
import llm
import json

app = FastAPI()

@app.post('/mall/{company}/messages/{thread}')
async def post_message(req: Request, company: str, thread: str):
    instructions = open(f"ar/{company}/Intake").read()
    prompt = (await req.json())['prompt']
    completion = llm.invoke(instructions, prompt)
    return json.loads(completion) if completion.startswith("{") else { "content": completion }