# sudo docker run -v `pwd`:/root -w /root company:latest python3 company.py

import llm
import messages
from messages import Message, load
import os

company = "sephora"
mgmt = f"{company}.txt"
calls = f"{company}.calls.txt"
departments = messages.recipients(mgmt, lambda msg: msg.recipient != "company")

def invoke(account, prompt):
    messages.append_to_file(calls, [Message(account, "Sales", prompt)])
    
    max_iterations = 3
    n_iterations = 0

    while n_iterations < max_iterations:
        n_iterations += 1

        for department in departments:
            msgs = load(mgmt, lambda msg: msg.sender in ("Management") and msg.recipient in (department, "company"))
            msgs += load(calls, lambda msg: msg.account == account and department in (msg.sender, msg.recipient))

            with open("instructions", "r") as file:
                instructions = file.read().replace("{department}", department)

            completion = llm.invoke(instructions, messages.to_string(msgs))
            sanity = lambda msg: msg.sender == department and msg.recipient not in (msg.sender, "Management") and (msg.recipient != account or msg.sender == "Sales")
            msgs = messages.from_string(completion, sanity)

            if len(msgs) == 1 and department == "Sales":
                messages.append_to_file(calls, msgs)
                return msgs[0].body
            elif len(msgs) > 0:
                for msg in msgs:
                    if msg.recipient != account:
                        messages.append_to_file(calls, [msg])
                        
    msg = Message("Sales", account, "Could you repeat that?")
    messages.append_to_file(calls, [msg])
    return msg.body

invoke("account-375491", "Hello.")
