import chat
import httpx

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
    assistants = thread.get("assistants", {})

    if assistant not in assistants:
        if is_remote(assistant):
            async with httpx.AsyncClient(timeout = 60) as client:
                assistants[assistant] = (await client.post(f'{assistant}/threads')).text
        else:
            assistants[assistant] = await chat.reset({"user": thread["assistant"], "assistant": assistant})

    if is_remote(assistant):
        async with httpx.AsyncClient(timeout = 60) as client:
            return (await client.post(f'{assistant}/threads/{assistants[assistant]}/messages', content = prompt)).text
    else:
        return await chat.run(prompt, assistants[assistant])
