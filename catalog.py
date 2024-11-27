import chroma
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
