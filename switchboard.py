import llm
import company
import json
import os

companies = ','.join(next(os.walk("ar"))[1])

input_instruction = f"""
Glean from the prompt a company and output JSON object with a company key.

Here is the list of available companies: {companies}

Output raw JSON string without markdown.
"""

def invoke(_company_, agent, caller, query):
    company.next = json.loads(llm.invoke(input_instruction, query))["company"]
    return f"Your user is now in {company.next}."