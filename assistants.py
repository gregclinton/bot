from react import React
from tools import search, shell
from langchain_community.tools import tool

assistants = {}

@tool
def cast(job_title, instructions, tools):
    """
Cast an AI assistant with a job title, instructions and a set of tools.
Tools is a comma separated string of tool names.
These may include search, cast, chroma and/or shell.
You must provide at least one tool.
    """
    assistants[job_title] = React(instructions, list(map(lambda t : {"search": search, "shell": shell}[t], tools.split(","))))
    return "success"

def get(job_title):
    return assistants[job_title]