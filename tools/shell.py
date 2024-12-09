import subprocess

chat.tools.append(
  { 
        "type": "function",
        "function": {
            "name": "shell",
            "description": "Run Linux shell commands like ls, cat, echo, sed, curl, python3, etc.",
            "parameters": {
                "type": "string"
            }
        }
    }
)

def run(command, thread):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout + result.stderr
