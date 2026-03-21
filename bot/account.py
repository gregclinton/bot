import re

def scrape(text):
    m = re.search(r"\bTLG\w*", text)
    return m.group() if m else None