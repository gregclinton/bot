import subprocess
import llm

input_instruction = """
Give a prompt you will generate a shell command to access the user's computer.
Output the raw command -- no markdown.
"""

def invoke(company, query):
    command = llm.invoke(input_instruction, query)

    return subprocess.run(command, shell=True, capture_output=True, text=True).stdout
