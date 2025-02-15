import chat
import os

def reset(thread):
    thread["workers"] = {}

def run(worker_name: str, prompt: str, thread: dict):
    """
    Prompts a worker with the given prompt.
    If the worker does not already exist it will be created.

    When choosing a worker name, make it one word, all lowercase, and a normal name, like "bob" or "alice".
    Use the notes file in your current directory to keep track of worker names and what they are used for.

    With workers you can divvy up a large job into many smaller jobs.
    This helps avoid context window bloat as each worker will have its own context window.
    Workers can have their own workers or a hierarchy of workers.

    You can think of workers as specialists.
    Divvy up a knowledge base into specialized silos and assign a worker to each one.

    You can also think of your workers as your team.
    """
    workers = thread["workers"]

    if worker_name not in workers:
        workers[worker_name] = chat.reset({})

    os.makedirs(worker_name, exist_ok=True)
    os.chdir(worker_name)
    reply = chat.run(prompt, workers[worker_name])
    os.chdir("..")
    return reply