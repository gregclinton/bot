# sudo docker run -v `pwd`:/root -w /root agent:latest python3 play.py
# sudo docker run -v `pwd`:/root -w /root agent:latest langgraph dev

from react import React
import chroma

collection_name = "Greg-Clinton"

# chroma.store(collection_name, "Greg Clinton is 67 years old")

graph = React("""
Keep your answers brief.
""",
[
    chroma.retriever(collection_name)
])

print(graph.run("How old is Greg Clinton?"))