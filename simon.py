import graphs
import chroma
from tools import shell

chroma.store("Greg-Clinton", "Greg Clinton is 67 years old")

graph = graphs.react("simon", """
Your name is Simon. Do your best.
""", [
    chroma.retriever('flowers')
])

print(graphs.run(graph, "How old is Greg Clinton?"))