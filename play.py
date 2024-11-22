# sudo docker run -v `pwd`:/root -w /root agent:latest python3 play.py
# sudo docker run -v `pwd`:/root -w /root agent:latest langgraph dev

import assistants
from tools import search

print(assistants.cast("coder", "Keep your answers brief.", [search]).run("Weather today in sf?"))