import llm
import json
import chroma

input_instruction = f"""
You are going to help us to create a ChromaDb vectorstore for providing information to the public.
Glean from the prompt the company or entity in question, and generate 20 questions about that entity.
For each question, think of a unique one-word filename for that question.
Output a JSON list of objects with filename key and question key.
Output raw JSON string without markdown.
"""

def invoke(company, query):
    items = json.loads(llm.invoke(input_instruction, query))

    for item in items:
        instruction = "Give a 1000-word answer to the question. Give the answer in raw text. No headers. No markdown."
        with open(item.filename, "w") as file:
            file.write(llm.invoke(instruction, item.question))

    chroma.create_answers_collection(company)
    return "Success."