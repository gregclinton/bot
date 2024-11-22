# sudo docker run -v `pwd`:/root -w /root agent:latest python3 play.py
# sudo docker run -v `pwd`:/root -w /root agent:latest langgraph dev

from react import React
from assistants import cast, get

print(React("Be good.", [cast]).run("Cast an admin to do command line activities."))

print(get("System Administrator").run("List the files in the current working directory."))