import llm
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv
import os

load_dotenv("keys")

def collection():
    return chromadb.PersistentClient(path="./chroma_data").get_or_create_collection(
        name="catalog",
        embedding_function=embedding_functions.OpenAIEmbeddingFunction(
            api_key=os.environ["OPENAI_API_KEY"],
            model_name="text-embedding-ada-002"
        )
    )

def create():
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

    collection().add(documents=documents, metadatas=metadatas, ids=ids)

def query(query):
    return collection().query(query_texts=[query], n_results=1)["documents"][0]

print(query("I'm interested in a man's hat."))


import os
import chromadb
from chromadb.utils import embedding_functions

# Set your OpenAI API key
os.environ["OPENAI_API_KEY"] = "your_openai_api_key"

# Define the embedding function using OpenAI
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.getenv("OPENAI_API_KEY"),
    model_name="text-embedding-ada-002"  # You can choose another model
)

# Initialize a persistent ChromaDB client
client = chromadb.PersistentClient(path="./chroma_data")

# Create or access a collection with the embedding function
collection = client.get_or_create_collection(
    name="my_collection",
    embedding_function=openai_ef
)

# Add documents, IDs, and optional metadata
collection.add(
    documents=["Document 1 text", "Document 2 text"],
    ids=["doc1", "doc2"],
    metadatas=[{"source": "source1"}, {"source": "source2"}]
)

print("Data stored successfully!")
