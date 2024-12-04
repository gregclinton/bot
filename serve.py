from fastapi import FastAPI, Request
import llm
from tool import bench
from time import sleep
import random

entities = {}
max_llm_invokes = 10

def invoke(entity, thread, prompt):
    instructions = open(f"ar/{entity}").read()
    make_message = lambda role, content: { "role": role, "content": content }
    system = lambda content: make_message("system", content)
    user = lambda content: make_message("user", content)
    assistant = lambda content: make_message("assistant", content)
    content = lambda text: { "content": text }
    bulk = ""

    messages = entities.setdefault(entity, {}).setdefault(thread, [])
    messages.append(user(prompt))
    response = llm.invoke([system(instructions)] + messages)

    if "entity" in response:
        return response

    while "content" not in response:
        sleep(0.2) # in case this loop runs away
        if llm.counter > max_llm_invokes:
            response = content("Could you please rephrase that?")
        elif "path" in response:
            thread = str(random.randint(111111, 999999))
            response = invoke(response["path"], thread, response["prompt"])
        elif "tool" in response:
            tool = response["tool"]
            prompt = response["prompt"]
            messages.append(assistant(f"tool: {tool}, prompt: {prompt}"))
            if tool in bench:
                try:
                    output = bench[tool](prompt)
                    if len(output) > 20000:
                        bulk = output
                        output = "<bulk>"
                    messages.append(assistant(f"tool response: {output}"))
                    response = llm.invoke([system(instructions)] + messages)
                except Exception as e:
                    response = content(str(e))
            else:
                response = content("I made a mistake with a tool called " + response["tool"] + ". Apparently, there is no such tool.")

    messages.append(assistant(response["content"]))
    return content(bulk) if bulk else response

app = FastAPI()

@app.post('/mall/{entity}/messages/{thread}')
async def post_message(req: Request, entity: str, thread: str):
    llm.reset_counter()
    return invoke(entity, thread, (await req.json())['prompt'])

# print(invoke("Plaza/Intake", "123456", "My name is Greg Clinton. What is my balance?")["content"])
