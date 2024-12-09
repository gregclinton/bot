import requests

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
    url, prompt = (args["url"], args["prompt"])
    headers = { "Content-Type": "text/plain" }
    post = lambda path, data = "": requests.post(f"{url}/{path}", data = data, headers = headers).text

    url = url.strip()
    if url not in thread["bots"]:
        thread["bots"][url] = id = post("threads")
    else:
        id = thread["bots"][url]

    return post(f"threads/{id}/messages", prompt)