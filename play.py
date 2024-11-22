# sudo docker run -v `pwd`:/root -w /root agent:latest python3 play.py
# sudo docker run -v `pwd`:/root -w /root agent:latest langgraph dev

from react import React
from assistants import cast, call

print(React("Be good.", [cast, call]).run("""
Cast an admin assistant to do command line activities.
Then call it to list files in the current working directory and show me the listing.
"""))