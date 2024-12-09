import subprocess

def meta():
    return {
        "description": "Run Linux shell commands like ls, cat, echo, sed, curl, python3, etc.",
        "parameters": {
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The shell command to be executed."
                }
            },
            "required": ["command"]
        }
    }

def run(args, thread):
    result = subprocess.run(args["command"], shell=True, capture_output=True, text=True)
    return result.stdout + result.stderr
