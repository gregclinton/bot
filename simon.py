import graphs
import chroma
from tools import shell

collection_name = "Greg-Clinton"

# chroma.store(collection_name, "Greg Clinton is 67 years old")

graph = graphs.react("simon", """
Your name is Simon. Do your best.
""", [
    chroma.retriever(collection_name)
])

print(graphs.run(graph, "How old is Greg Clinton?"))