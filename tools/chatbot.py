import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

name = __name__[6:] # strip "tools."
headers = { "Content-Type": "text/plain" }

def reset(thread):
    tools = thread["tools"]
    data = tools[name] = tools.get(name, {})
    data["bots"] = bots = data.get("bots", {})
    for url, id in bots.items():
        requests.delete(f'{url}/threads/{id}', headers = headers)
    bots.clear()

def run(url: str, prompt: str, thread: dict):
    "Talks with another chatbot at the given url and the given prompt."
    bots = thread["tools"][name]["bots"]
    post = lambda path, data = "": requests.post(f"{url}/{path}", verify = False, data = data, headers = headers).text

    if url not in bots:
        bots[url] = id = post("threads")
    else:
        id = bots[url]

    return post(f"threads/{id}/messages", prompt)