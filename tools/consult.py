import chat
import httpx

is_remote = lambda name: name.startswith("https:")

def reset(thread):
    assistants = thread["assistants"]

    with httpx.Client() as client:
        for assistant in assistants.items():
            if is_remote(assistant):
                client.delete(f'{assistant}/threads/{id}'))

    thread["assistants"] = {}

async def run(assistant: str, prompt: str, thread: dict):
    "Prompts an assistant with the given prompt."
    assistants = thread["assistants"]

    if assistant not in assistants:
        if is_remote(assistant):
            with httpx.Client() as client:
                assistants[assistant] = (await client.post(f'{assistant}/threads')).text
        else:
            assistants[assistant] = chat.reset({"user": thread["assistant"], "assistant": assistant})

    if is_remote(assistant):
        with httpx.Client() as client:
            return (await client.post(f'{assistant}/threads/{assistants[assistant]}/messages', content = prompt)).text
    else:
        return await chat.run(prompt, assistants[assistant])
