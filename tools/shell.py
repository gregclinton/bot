import subprocess

def run(command: str, thread: dict):
    """
    Runs the given command, like ls, cat, sed, echo, curl, python3, etc. in a Linux shell.
    Commands run in a docker container sandbox, so feel free to write to disk, etc.
    You and each of your workers have their own working directory.
    """
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout or result.stderr
