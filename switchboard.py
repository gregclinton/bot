import llm
import company
import json

input_instruction = """
Glean from the prompt a company and output JSON object
with company field set to one of sephora, cox or wendys.

Output raw JSON string without markdown.
"""

output_instruction = """
Generate an answer to the given question given the context.
"""

def invoke(query):
    company.name = json.loads(llm.invoke(input_instruction, query))["company"]
    prompt = f"Context: {company.name}\nQuestion: {query}\nAnswer: "
    return llm.invoke(output_instruction, prompt)