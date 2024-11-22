# sudo docker run -v `pwd`:/root -w /root agent:latest python3 play.py
# sudo docker run -v `pwd`:/root -w /root agent:latest langgraph dev

import assistants

assistants.cast("coder", "Keep your answers brief.", "cast")

print(assistants.get("coder").run("Cast an admin to do command line activities."))