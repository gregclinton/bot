# https://developers.google.com/custom-search/v1/reference/rest/v1/cse/list
# https://programmablesearchengine.google.com/controlpanel/all
# https://console.cloud.google.com/apis/credentials?project=gen-lang-client-0620307586

from boilerpy3 import extractors
import requests
import os
from datetime import datetime

def run(query: str, thread: dict):
    "Searches the internet with the given query."

    today = datetime.now().strftime("%B %d, %Y")
    text = f"Mish-mash of google search results from today, {today}, extracted by boilerpy3: \n\n\n"

    extractor = extractors.KeepEverythingExtractor()

    for item in requests.get(
        "https://customsearch.googleapis.com/customsearch/v1",
        params = {
            "key": os.environ["CUSTOM_SEARCH_API_KEY"],
            "cx": os.environ["CUSTOM_SEARCH_CX"],
            "q": query,
            "num": 3
        }).json()["items"]:

        res = requests.get(item["link"], headers = {'User-Agent': 'Chrome/50.0.2661.102'})

        if res.ok:
            text += extractor.get_content(res.text).replace("\n", " ")

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

