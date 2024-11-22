# sudo docker run -v `pwd`:/root -w /root agent:latest python3 play.py
# sudo docker run -v `pwd`:/root -w /root agent:latest langgraph dev

from react import React
from assistants import cast

print(React("Be good.", [cast]).run("Cast an admin to do command line activities."))