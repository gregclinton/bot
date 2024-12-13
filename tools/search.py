# https://developers.google.com/custom-search/v1/reference/rest/v1/cse/list
# https://programmablesearchengine.google.com/controlpanel/all
# https://console.cloud.google.com/apis/credentials?project=gen-lang-client-0620307586

import requests
import os

def run(query: str, thread: dict):
    "Searches the internet with the given query."

    res = requests.get(
        "https://customsearch.googleapis.com/customsearch/v1",
        params = {
            "api_key": os.environ["CUSTOM_SEARCH_API_KEY"],
            "cx": os.environ["CUSTOM_SEARCH_CX"],
            "q": query
        }
        headers = {
            "Content-Type": "application/json",
        }).json()

    return res
