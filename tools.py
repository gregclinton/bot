from langchain_community.tools import tool, TavilySearchResults

search = TavilySearchResults(
    max_results=2,
    search_depth="advanced",
    include_answer=True,
    include_raw_content=False,
    include_images=False
)

@tool
def shell(line):
    """
        run a shell command
    """
    import subprocess
    return subprocess.run(line, shell = True, capture_output = True, text = True).stdout