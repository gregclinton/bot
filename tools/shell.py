import subprocess

def descriptions():
    return (
        "Run Linux shell commands like ls, cat, echo, sed, curl, python3, etc.",
        "The shell command to be executed."
    )

def run(command, thread):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout + result.stderr
