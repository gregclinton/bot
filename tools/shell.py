import subprocess

def run(command: str, thread: dict):
    "Runs the given command, like ls, cat, sed, echo, curl, python3, etc. in a Linux shell."
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout or result.error
