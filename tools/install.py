import tool

def invoke(tools):
    tool.installed.update(tools.split(","))
    return f"As you requested, I installed {tools}. You can now use it to answer my above request." 
