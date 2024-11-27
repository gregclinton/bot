import chroma
import llm

def invoke(query):
    entry = chroma.collection("catalog").query(query_texts=[query], n_results=1)["documents"][0][0]
    context = f"A search of our product catalog yielded: \n{entry}"
    instructions = "Provide the answer to the question given the context."
    prompt = f"Context: {context}\nQuestion: {query}\nAnswer: "
    return llm.invoke(instructions, prompt)
