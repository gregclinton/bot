import chat
import httpx
import os
import tool

is_remote = lambda name: name.startswith("https:")

async def clear(thread):
    async with httpx.AsyncClient(timeout = 60) as client:
        for name, t in thread.get("assistants", {}).items():
            if is_remote(name):
                await client.delete(f'{name}/threads/{t}')
            else:
                await tool.clear(t)

    thread.pop("assistants", None)

async def run(assistant: str, prompt: str, thread: dict):
    """
    Prompts an assistant with the given natural language prompt.
    The assistant can be a local or remote assistant.
    Local assistants can have names like "tom", "dick", "harry", "jane", "maria", etc. 
    Or names like "billing", "sales", "support", etc.
    You can create local assistants ad hoc by coming up with a new assistant name and invoking this function.
    Remote assistants are urls beginning with "https://".
    """
    print(f"{thread['assistant']} to {assistant}: {prompt}", flush = True)
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
                "model": "gpt-4.1-nano",
                "tools": ["bench"],
            }

    t = assistants.get(assistant)

    if t:
        if is_remote(assistant):
            async with httpx.AsyncClient(timeout = 60) as client:
                return (await client.post(f'{assistant}/threads/{t}/messages', content = prompt)).text
        else:
            return await chat.run(prompt, t)
    else:
        return f"{assistant} not found."
