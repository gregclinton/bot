from fastapi import FastAPI, Request
import llm

app = FastAPI()

@app.post('/mall/{company}/messages/{thread}')
async def post_message(req: Request, company: str, thread: str):
    instructions = open(f"ar/{company}/Intake").read()
    prompt = (await req.json())['prompt']
    completion = llm.invoke(instructions, prompt)
    return completion if completion.startswith("{") else { "content": completion }