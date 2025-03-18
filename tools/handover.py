def run(assistant: str, thread: dict):
    "Hands over your job to another assistant."
    thread["assistant"] = assistant
    return thread