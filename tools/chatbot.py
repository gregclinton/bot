import requests

tool = __name__[6:] # strip "tools."

def reset(thread):
    tools = thread["tools"]
    data = tools[tool] = tools.get(tool, {})
    data["bots"] = bots = data.get("bots", {})
    for url, id in bots.items():
        requests.delete(f'{url}/threads/{id}', headers={ 'Content-Type': 'text/plain' })
    bots.clear()

def run(url: str, prompt: str, thread: dict):
    "Talks with another chatbot at the given url and the given prompt."
    bots = thread["tools"][tool]["bots"]
    headers = { "Content-Type": "text/plain" }
    post = lambda path, data = "": requests.post(f"{url}/{path}", data = data, headers = headers).text

    if url not in bots:
        bots[url] = id = post("threads")
    else:
        id = bots[url]

    return post(f"threads/{id}/messages", prompt)