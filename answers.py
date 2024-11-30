import llm
import json
import chroma

input_instruction = """
You are going to help us to create a ChromaDb vectorstore for providing information to the public about {company}.
Generate 20 questions about {company}.
They should be questions that customers or those serviced by {company} would ask on a help line.
Nothing about the history, stock price, the organization, etc.
Should be blue-collar not suit kind of questions.
For each question, think of a unique one-word filename for that question.
Output a raw JSON list of objects with filename key and question key -- no markdown.
"""

def invoke(company, _):
    items = json.loads(llm.invoke(input_instruction.replace("{company}", company), f"Generate the JSON."))

    for item in items:
        instruction = "Give a 1000-word answer to the question based on your training. Give the answer in raw text. No headers. No markdown."
        with open(f"answers/{company}/" + item["filename"] + ".txt", "w") as file:
            file.write(llm.invoke(instruction, item["question"]))

    chroma.create_answers_collection(company)
    return "Success."