import llm
import company
import json
import os

companies = ','.join(next(os.walk("ar"))[1])

input_instruction = f"""
Glean from the prompt a company and output JSON object

Here is the list of available companies: {companies}

Output raw JSON string without markdown.
"""

def invoke(company, query):
    company.next = json.loads(llm.invoke(input_instruction, query))["company"]
    return f"Success. Switched to {company.next}"