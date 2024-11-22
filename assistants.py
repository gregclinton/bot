from react import React 

assistants = {}

def cast(job_title, instructions, tools):
    assistants[job_title] = React(instructions, tools)
    return get(job_title)

def get(job_title):
    return assistants[job_title]