import llm
import json
import chroma

input_instruction = f"""
You are going to help us to create a ChromaDb vectorstore for providing information to the public about {company}.
Generate 20 questions about {company}.
For each question, think of a unique one-word filename for that question.
Output a raw JSON list of objects with filename key and question key -- no markdown.
"""

def invoke(company, query):
    input_instruction = input_instruction.replace("{company}", company)
    items = json.loads(llm.invoke(input_instruction, f"Generate the JSON."))

    for item in items:
        instruction = "Give a 1000-word answer to the question. Give the answer in raw text. No headers. No markdown."
        with open(item.filename, "w") as file:
            file.write(llm.invoke(instruction, item.question))

    chroma.create_answers_collection(company)
    return "Success."