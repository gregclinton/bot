from bs4 import BeautifulSoup
import requests

def run(url: str, thread: dict):
    "Downloads page with the given url and returns text cleaned by beautifulsoup."

    return BeautifulSoup(requests.get(url).text, "html.parser").get_text(separator=" ")
