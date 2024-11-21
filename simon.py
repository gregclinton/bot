import graphs
import chroma

chroma.store("flowers", ["roses are red", "violets are blue"])

graph = graphs.react("simon", """
Your name is Simon. Just do your best.
""", [
    chroma.retriever('flowers')
])

print(graph.run(graph, "What color are roses?"))