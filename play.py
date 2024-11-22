# sudo docker run -v `pwd`:/root -w /root agent:latest python3 play.py
# sudo docker run -v `pwd`:/root -w /root agent:latest langgraph dev

from react import React
import assistants

print(React("Be good.", [assistants.cast, assistants.call]).run("""
Cast an AI assistant with job title "admin" to do command line activities.
Then call it to list files in the current working directory and show me the listing.
"""))