def invoke(tools, thread):
    tools = tools.split("\n")[0].strip()
    thread["installed"].update(tools.split(","))
    return f"As you requested, I installed {tools}. You can now use it to answer my above request." 
