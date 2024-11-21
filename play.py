import graphs
import chroma
from tools import shell

collection_name = "Greg-Clinton"

# chroma.store(collection_name, "Greg Clinton is 67 years old")

assistant = graphs.react("play", """
Keep your answers brief.
""",
[
    chroma.retriever(collection_name)
])

print(graphs.run(assistant, "How old is Greg Clinton?"))