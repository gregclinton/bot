from fastapi import FastAPI, Request
import llm
from tool import bench
from time import sleep

app = FastAPI()
entities = {}
max_llm_invokes = 10

def invoke(entity, thread, prompt):
    instructions = open(f"ar/{entity}").read()
    messages = entities.setdefault(entity, {}).setdefault(thread, [])
    messages.append({"role": "user", "content": prompt})
    response = llm.invoke([{"role": "system", "content": instructions}] + messages)

    if "entity" in response:
        return response

    while "content" not in response and llm.counter < max_llm_invokes:
        if "path" in response:
            response = invoke(response["path"], "111222", response["prompt"])
        elif "tool" in response:
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

print(invoke("Plaza/Intake", "12345", "What is my balance?")["content"])
