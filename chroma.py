import chromadb
from chromadb.utils import embedding_functions
import llm

input_instruction = """
From the user prompt generate a proper search string for a Products vectorstore.
"""

output_instruction = """
Generate an answer to the given question given the context.
"""

def invoke(query):
    search = llm.invoke(input_instruction, query)

    entry = chroma.collection("catalog").query(query_texts=[search], n_results=1)["documents"][0][0]

    context = f"A search of our product catalog yielded: \n{entry}"

    prompt = f"Context: {context}\nQuestion: {query}\nAnswer: "
    return llm.invoke(output_instruction, prompt)


def collection(name):
    return chromadb.PersistentClient(path="./chroma_data").get_or_create_collection(
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