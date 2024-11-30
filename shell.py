import subprocess

def invoke(company, command):
    return subprocess.run(command, shell=True, capture_output=True, text=True).stdout
