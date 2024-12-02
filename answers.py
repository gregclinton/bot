import llm
import json
import chroma
import os

input_instruction = """
Glean the company name from the prompt.
You are going to help us to create a vectorstore database for providing information to the public about a company.
Generate 20 questions about the company.
They should be questions that customers or those serviced by company would ask on a help line.
Nothing about the history, stock price, the organization, etc.
Should be blue-collar not suit kind of questions.
For each question, think of a unique one-word filename for that question.
Output raw JSON: {"company": "xxx", "items": [{"filename": "xxx", "question": "xxx"}]} -- no markdown.
"""

def invoke(_company_, agent, caller, query):
    o = json.loads(llm.invoke(input_instruction, query))
    company = o["company"]
    items = o["items"]
    dir = f"answers/{company}/"

    os.makedirs(dir, exist_ok = True)

    for item in items:
        instruction = """
Give a 1000-word answer to the question based on your training.
Give the answer in raw text.
The answer should be dense with facts.
Don't use headings. Don't use markdown.
This answer will be added to a vectorstore database to be used by a call center.
"""
        with open(dir + item["filename"] + ".txt", "w") as file:
            file.write(llm.invoke(instruction, item["question"]))

    chroma.create_answers_collection(company)
    return "Success."