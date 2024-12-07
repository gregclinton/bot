import os

def run(tools, thread):
    tools = tools.split("\n")[0].strip()
    output = ""
    for tool in tools.split(","):
        tool =  tool.strip().lower()
        if os.path.isfile(f"how/{tool}"):
            installed = thread["installed"]
            installed.append(tool) if tool not in installed else None
            result = "successfully installed"
        else:
            result = "not found"
        output += f"The {tool} tool was {result}.\n"
    return output
