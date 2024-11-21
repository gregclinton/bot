import graphs
import chroma

collection_name = "Greg-Clinton"

# chroma.store(collection_name, "Greg Clinton is 67 years old")

graphs.react("play", """
Keep your answers brief.
""",
[
    chroma.retriever(collection_name)
])

print(graphs.run("play", "How old is Greg Clinton?"))