import subprocess
import llm

input_instruction = """
Give a prompt you will generate a shell command to access the user's computer.
Path names are given relative to the current working directory.
Output the raw command -- no markdown.
"""

def invoke(query):
    command = llm.invoke(input_instruction, query)
    print(query)

    output = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(output)
    return output
