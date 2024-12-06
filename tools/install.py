from importlib import import_module

def invoke(tools, thread):
    tools = tools.split("\n")[0].strip()
    output = ""
    for tool in tools.split(","):
        tool =  tool.strip()
        if import_module(f"tools.{tool}"):
            installed = thread["installed"]
            installed.append(tool) if tool not in installed else None
            output += f"The {tool} tool was successfully installed. You can now use it to answer my above request.\n"
        else:
            output += f"The {tool} tool was not found.\n"
    return output
