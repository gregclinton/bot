import chat

def reset(thread):
    thread["workers"] = {}

def run(worker_name: str, prompt: str, thread: dict):
    """
    Prompts a worker with the given prompt.
    If the worker does not already exist it will be created.
    When finished with the worker, dismiss him.
    Use the instruct tool to keep track of your worker names and their purposes.

    With workers you can divvy up a large job into many smaller jobs.
    This helps avoid context window bloat as each worker will have its own context window.
    workers can have their own workers or a hierarchy of workers.

    You can also think of workers as specialists.
    Divvy up a knowledge base into specialized silos and assign a worker to each one.

    You yourself might be a worker and not know it. No way to know.
    """
    workers = thread["workers"]

    if worker_name not in workers:
        workers[worker_name] = chat.reset({})

    return chat.run(prompt, workers[worker_name]) 
