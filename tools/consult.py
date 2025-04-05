import chat
import httpx
import os
import tool

is_remote = lambda name: name.startswith("https:")

async def clear(thread):
    assistants = thread.get("assistants", {})

    async with httpx.AsyncClient(timeout = 60) as client:
        for name, id in assistants.items():
            if is_remote(name):
                await client.delete(f'{name}/threads/{id}')

    thread["assistants"] = {}

async def run(assistant: str, prompt: str, thread: dict):
    """
    Prompts an assistant with the given natural language prompt.
    The assistant can be a local or remote assistant.
    Local assistants have names like "billing", "sales", "support", etc.
    Remote assistants are urls beginning with "https://".
    You can create assistants ad hoc by coming up with a new assistant name and invoking this function.
    """
    print(f"{thread['assistant']} to {assistant}: {prompt}")
    thread["assistants"] = assistants = thread.get("assistants", {})

    if assistant not in assistants:
        if is_remote(assistant):
            async with httpx.AsyncClient(timeout = 60) as client:
                res = await client.post(f'{assistant}/threads')
                if res.status_code < 300:
                    assistants[assistant] = res.text
        else:
            assistants[assistant] = {
                "user": thread["assistant"],
                "assistant": assistant,
                "provider": "openai",
                "model": "gpt-4o-mini",
                "tools": tool.create(["bench", "model", "shell", "consult"]),
                "messages": []
            }

    t = assistants.get(assistant, None)

    if t:
        if is_remote(assistant):
            async with httpx.AsyncClient(timeout = 60) as client:
                return (await client.post(f'{assistant}/threads/{t}/messages', content = prompt)).text
        else:
            return await chat.run(prompt, t)
    else:
        return f"{assistant} not found."
