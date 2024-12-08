import os

def run(tools, thread):
    tools = tools.split("\n")[0].strip()
    output = ""
    for tool in tools.split(","):
        tool =  tool.strip().lower()
        if os.path.isfile(f"how/{tool}"):
            how = thread["how"]
            how.append(tool) if tool not in how else None
            result = "successfully installed"
        else:
            result = "not found"
        output += f"The {tool} tool was {result}.\n"
    return output
