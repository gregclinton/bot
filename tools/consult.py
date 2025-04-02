import chat

def reset(thread):
    thread["assistants"] = {}

async def run(assistant: str, prompt: str, thread: dict):
    "Prompts an assistant with the given prompt."
    assistants = thread["assistants"]

    if assistant not in assistants:
        assistants[assistant] = chat.reset({"user": thread["assistant"], "assistant": assistant})

    return await chat.run(prompt, assistants[assistant])
