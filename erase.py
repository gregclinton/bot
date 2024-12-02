import messages

def invoke(company, agent, caller, command):
    messages.delete_caller(company, agent, caller)
    return f"{caller} history has been deleted for {agent} at {company}."
