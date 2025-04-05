import chat
import httpx
import os

is_remote = lambda name: name.startswith("https:")

async def reset(thread):
    assistants = thread.get("assistants", {})

    async with httpx.AsyncClient(timeout = 60) as client:
        for name, id in assistants.items():
            if is_remote(name):
                await client.delete(f'{name}/threads/{id}')

    thread["assistants"] = {}

async def run(assistant: str, prompt: str, thread: dict):
    "Prompts an assistant with the given prompt."
    print(f"{thread["assistant"]} to {assistant}: {prompt}")
    assistants = thread.get("assistants", {})
    found = False

    if assistant in assistants:
        found = True
    else:
        if is_remote(assistant):
            async with httpx.AsyncClient(timeout = 60) as client:
                res = await client.post(f'{assistant}/threads')
                if res.status_code < 300:
                    assistants[assistant] = res.text
                    found = True
        else:
            if os.path.exists(f"assistants/{assistant}"):
                assistants[assistant] = await chat.reset({"user": thread["assistant"], "assistant": assistant})
                found = True

    if found:
        if is_remote(assistant):
            async with httpx.AsyncClient(timeout = 60) as client:
                return (await client.post(f'{assistant}/threads/{assistants[assistant]}/messages', content = prompt)).text
        else:
            return await chat.run(prompt, assistants[assistant])
    else:
        return f"{assistant} not found."
