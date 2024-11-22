from react import React
from tools import search, shell

assistants = {}

def cast(job_title, instructions, tools):
    """
Cast an AI assistant with a job title, instructions and a set of tools.
Tools is a comma separated string of tools that may include search and/or shell.
You must provide at least one tool.
    """
    print(f"{job_title} {instructions} {tools}")
    tools = list(map(lambda t : {"search": search, "shell": shell}[t], tools.split(",")))
    assistants[job_title] = React(instructions, tools)
    return get(job_title)

def get(job_title):
    return assistants[job_title]