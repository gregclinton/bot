import chat

def reset(thread):
    thread["assistants"] = {}

def run(assistant: str, prompt: str, thread: dict):
    "Prompts a assistant with the given prompt."
    assistants = thread["assistants"]

    if assistant not in assistants:
        assistants[assistant] = chat.reset({"user": thread["assistant"], "assistant": assistant})

    return chat.run(prompt, assistants[assistant])
