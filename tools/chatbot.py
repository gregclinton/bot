import requests

tool = __name__[6:] # strip "tools."

def restart(thread):
    data = thread["tools"].get(tool, {})
    data["bots"] = bots = data.get("bots", {})
    for url, id in bots.items():
        requests.delete(f'{url}/threads/{id}', headers={ 'Content-Type': 'text/plain' })
    bots.clear()

def meta():
    return {
        "description": "Talk with another chatbot.",
        "parameters": {
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The other chatbot's url."
                },
                "prompt": {
                    "type": "string",
                    "description": "Your prompt to the other chatbot."
                }
            },
            "required": ["url", "prompt"]
        }
    }

def run(args, thread):
    url = args["url"]
    bots = thread["tools"][tool]["bots"]
    headers = { "Content-Type": "text/plain" }
    post = lambda path, data = "": requests.post(f"{url}/{path}", data = data, headers = headers).text

    if url not in bots:
        bots[url] = id = post("threads")
    else:
        id = bots[url]

    return post(f"threads/{id}/messages", args["prompt"])