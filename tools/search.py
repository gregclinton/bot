# https://developers.google.com/custom-search/v1/reference/rest/v1/cse/list
# https://programmablesearchengine.google.com/controlpanel/all
# https://console.cloud.google.com/apis/credentials?project=gen-lang-client-0620307586

from boilerpy3 import extractors
import requests
import os

def run(query: str, thread: dict):
    "Searches the internet with the given query."

    text = "Mish-mash of google search results extracted by boilerpy3: \n\n\n"

    for item in requests.get(
        "https://customsearch.googleapis.com/customsearch/v1",
        params = {
            "key": os.environ["CUSTOM_SEARCH_API_KEY"],
            "cx": os.environ["CUSTOM_SEARCH_CX"],
            "q": query,
            "num": 3
        }).json()["items"]:
        text += extractors.KeepEverythingExtractor().get_content_from_url(item["link"]).replace("\n", " ")

    return requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers = {
            'Authorization': 'Bearer ' + os.environ['OPENAI_API_KEY'],
            'Content-Type': 'application/json',
        },
        json = {
            "model": "gpt-4o-mini",
            "temperature": 0,
            "messages": [{"role": "user", "content": text + f"\n\n\nQuery:\n{query}\nAnswer:\n"}]
        }).json()["choices"][0]["message"]["content"]

