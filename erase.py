import messages

def invoke(company, agent, caller, command):
    messages.delete_caller(company, caller)
    return f"{caller} thread has been deleted."
