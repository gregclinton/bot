import chat

def reset(thread):
    thread["workers"] = {}

def run(worker_name: str, prompt: str, thread: dict):
    """
    Prompts a worker with the given prompt.
    If the worker does not already exist it will be created.
    """
    workers = thread["workers"]

    if worker_name not in workers:
        workers[worker_name] = chat.reset({})

    return chat.run(prompt, workers[worker_name]) 
