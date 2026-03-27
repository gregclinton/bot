import re
from random import randint

def scrape(text):
    # you should implement this yourself
    m = re.search(r"\bTLG\w*", text)
    return m.group() if m else None

def create():
    # you should implement this yourself
    return f"TLG{10000000 + randint(1, 9999999)}"