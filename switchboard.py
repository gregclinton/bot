import llm
import company
import json

input_instruction = """
Glean from the prompt a company and output JSON object
with company field set to one of Sephora, Cox or Wendy's.

Output raw JSON string without markdown.
"""

def invoke(query):
    company.name = json.loads(llm.invoke(input_instruction, query))["company"]
    return f"Success. Switched to {company.name}"