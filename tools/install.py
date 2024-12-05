import serve

def invoke(tools):
    serve.installed.update(tools.split(","))
    return f"Added {tools}." 
