import chromadb
from chromadb.utils import embedding_functions
import llm
import os
import json

input_instruction = """
From the user prompt generate the most appropriate collection and search to use with our ChromaDb vectorstore.

Currently we have the following collections: {collections}

Output object with collection and search fields as raw JSON string without markdown.
"""

output_instruction = """
Generate an answer to the given question given the context.
"""

client = chromadb.PersistentClient(path="./chroma_data")

def invoke(query):
    collections = ", ".join(map(lambda collection:  collection.name, client.list_collections()))

    o = json.loads(llm.invoke(input_instruction.replace("{collections}", collections), query))

    entry = collection(o["collection"]).query(query_texts=[o["search"]], n_results=1)["documents"][0][0]

    context = f"A database search yielded: \n{entry}"

    prompt = f"Context: {context}\nQuestion: {query}\nAnswer: "
    return llm.invoke(output_instruction, prompt)


def collection(name):
    return client.get_or_create_collection(
        name=name,
        embedding_function=embedding_functions.OpenAIEmbeddingFunction(
            api_key=os.environ["OPENAI_API_KEY"],
            model_name="text-embedding-ada-002"
        )
    )

if False:
    documents = []
    metadatas = []
    ids = []
    id = 10000

    for shoppers in ["men", "women"]:
        instruction = "Yor are a creative catalog writer."
        for product in ["hats", "shirts", "pants", "shoes"]:
            prompt = f"Invent a catlog description (about 200 words) and price for {shoppers}'s {product}. Pure text format, no markdown."
            documents.append(llm.invoke(instruction, prompt))
            metadatas.append({"section": f"{shoppers}'s {product}"})
            ids.append(f"id-{id}")
            id += 1

    def create(name, documents, metadatas, ids):
        collection(name).add(documents=documents, metadatas=metadatas, ids=ids)