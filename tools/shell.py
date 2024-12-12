import subprocess

def run(command: str, thread: dict):
    """
    Run the given command in a Linux shell.
    You can run commands like ls, cat, echo, sed, curl, python3, etc.
    """
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout + result.stderr
