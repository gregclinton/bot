import subprocess

def invoke(command, thread):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout + result.stderr
