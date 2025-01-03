import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers = { "Content-Type": "text/plain" }

name = __name__[6:] # strip "tools." 

def reset(thread):
    thread["tools"] = tools = thread.get("tools", {})
    tools[name] = data = tools.get(name, {})
    data["bots"] = bots = data.get("bots", {})
    for url, id in bots.items():
        requests.delete(f'{url}/threads/{id}', headers = headers)
    bots.clear()

def run(url: str, prompt: str, thread: dict):
    "Talks with another bot at the given url and the given prompt. When finished with the bot, sign off by saying 'bye'."
    bots = thread["tools"][name]["bots"]
    post = lambda path, data = "": requests.post(f"{url}/{path}", verify = False, data = data, headers = headers).text

    if url not in bots:
        bots[url] = id = post("threads")
    else:
        id = bots[url]

    return post(f"threads/{id}/messages", prompt)
