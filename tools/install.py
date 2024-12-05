def invoke(tools, thread):
    thread["installed"].update(tools.strip().split(","))
    return f"As you requested, I installed {tools}. You can now use it to answer my above request." 
