# sudo docker run -v `pwd`:/root -w /root agent:latest python3 play.py
# sudo docker run -v `pwd`:/root -w /root agent:latest langgraph dev

import assistants
from tools import search

assistants.cast("coder", "Keep your answers brief.", [search])

print(assistants.get("coder").run("Hello"))