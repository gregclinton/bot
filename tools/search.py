# https://developers.google.com/custom-search/v1/reference/rest/v1/cse/list
# https://programmablesearchengine.google.com/controlpanel/all
# https://console.cloud.google.com/apis/credentials?project=gen-lang-client-0620307586

from boilerpy3 import extractors
import llm
import os
from datetime import datetime
import requests

def run(query: str, thread: dict):
    "Searches the internet with the given query."

    today = datetime.now().strftime("%B %d, %Y")
    text = f"Search result summaries from today, {today}: \n\n\n"

    extractor = extractors.KeepEverythingExtractor()
    count = 0

    for item in requests.get(
        "https://customsearch.googleapis.com/customsearch/v1",
        params = {
            "key": os.environ["CUSTOM_SEARCH_API_KEY"],
            "cx": os.environ["CUSTOM_SEARCH_CX"],
            "q": query,
            "num": 5
        }).json()["items"]:

        try:
            res = requests.get(item["link"], headers = {'User-Agent': 'Chrome/50.0.2661.102'}, timeout = 5)
            if res.ok:
                boiled = extractor.get_content(res.text).replace("\n", " ")
                text += llm.mini(boiled + f"\n\n\nQuery:\n{query}\nAnswer:\n") + "\n\n\n"
                count += 1
        except:
            pass

        if count == 3:
            break

    return llm.mini(text + f"Summarize the above various search results:\n")
