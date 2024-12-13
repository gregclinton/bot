# https://developers.google.com/custom-search/v1/reference/rest/v1/cse/list
# https://programmablesearchengine.google.com/controlpanel/all
# https://console.cloud.google.com/apis/credentials?project=gen-lang-client-0620307586

import requests
import os

def run(query: str, thread: dict):
    "Searches the internet with the given query. Results can be downloaded with the soup tool."

    return "https://weather.com/weather/tenday/l/Mission+Viejo+CA?canonicalCityId=6c0d55f4f95fda9c9a161e601406bdba6dc30910fe16b11565a046dee9593cd0"

    results = ""

    for item in requests.get(
        "https://customsearch.googleapis.com/customsearch/v1",
        params = {
            "api_key": os.environ["CUSTOM_SEARCH_API_KEY"],
            "cx": os.environ["CUSTOM_SEARCH_CX"],
            "q": query,
            "num": 3
        },
        headers = {
            "Content-Type": "application/json",
        }).json()["items"]:

        results += "\n".join([item["formattedUrl"], item["title"], item["snippet"]]) + "\n\n"
    
    return results
