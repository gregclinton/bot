import messages

def invoke(company, department, caller, command):
    messages.delete_caller(company, caller)
    return f"{caller} thread has been deleted."
