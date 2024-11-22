from langchain_community.tools import tool, TavilySearchResults

tools = {}

def put(name, tool):
    tools[name] = tool

def get(name):
    return tools[name]

search = TavilySearchResults(
    max_results=2,
    search_depth="advanced",
    include_answer=True,
    include_raw_content=False,
    include_images=False
)

put("search", search)

@tool
def shell(line):
    """
        run a shell command
    """
    import subprocess
    return subprocess.run(line, shell = True, capture_output = True, text = True)

put("shell", shell)