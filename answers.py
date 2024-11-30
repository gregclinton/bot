import llm
import json
import chroma

companies = ','.join(next(os.walk("ar"))[1])

input_instruction = f"""
You are going to help us to create a ChromaDb vectorstore for providing information to the public.
Glean from prompt the company or entity in question, and generate 20 questions about that entity.
For each question, think of a unique one-word filename for that question.
Output a JSON list of objects with filename key and question key.
Output raw JSON string without markdown.
"""

def invoke(_company_, query):
    questions = json.loads(llm.invoke(input_instruction, query))
    # chroma.create_answers_collection(company)
    return questions