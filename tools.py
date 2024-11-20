from langchain_community.tools import TavilySearchResults

search = TavilySearchResults(
    max_results=2,
    search_depth="advanced",
    include_answer=True,
    include_raw_content=False,
    include_images=False
)

def shell(line):
    """
        run a shell command
    """
    print(line, flush = True)
    return subprocess.run(line, shell = True, capture_output = True, text = True).stdout