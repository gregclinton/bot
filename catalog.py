import llm

for product in ["men's hats"]:
    print(llm.invoke(
        "Yor are a creative catalog writer.", 
        f"Invent a catlog description (about 200 words) and price for {product}. Pure text format, no markdown.")
    )
exit()

import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv
import os

load_dotenv("keys")

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.environ["OPENAI_API_KEY"],
    model_name="text-embedding-ada-002"
)

client = chromadb.Client()

collection = client.create_collection(
    name = "catalog",
    embedding_function = openai_ef
)

if False:
    documents = ["Document 1 text", "Document 2 text"]
    metadatas = [{"source": "source1"}, {"source": "source2"}]
    ids = ["id1", "id2"]
    collection.add(documents=documents, metadatas=metadatas, ids=ids)

print(collection.query(query_texts=["Document 1"], n_results=1)["documents"][0])
