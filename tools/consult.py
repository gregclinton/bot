import chat

def reset(thread):
    thread["workers"] = {}

def run(worker: str, prompt: str, thread: dict):
    "Prompts a worker with the given prompt."
    workers = thread["workers"]

    if worker not in workers:
        workers[worker] = chat.reset({"user": thread["worker"], "worker": worker})

    return chat.run(prompt, workers[worker])
