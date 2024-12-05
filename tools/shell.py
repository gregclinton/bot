import subprocess

def invoke(args):
    result = subprocess.run(args["text"], shell=True, capture_output=True, text=True)
    return result.stdout + result.stderr
