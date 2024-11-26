# sudo docker run -v `pwd`:/root -w /root company:latest python3 company.py

import llm
from messages import Messages, Message
import os

company = "sephora"
mgmt = f"{company}.txt"
calls = f"{company}.calls.txt"

no_company = lambda msg: msg.recipient != "company"
departments = list(Messages.recipients(mgmt, no_company))

def invoke(account, prompt):
    Messages.append_string_to_file(msgs, Message(account, "Sales", prompt).to_string())
    
    max_iterations = 3
    n_iterations = 0
    reply = "Could you repeat that?"

    while n_iterations < max_iterations:
        n_iterations += 1

        for department in departments:
            account = None

            for msg in Messages.load(calls, lambda msg: msg.recipient == department):
                account = msg.account

            if account:
                msgs = Messages.load(mgmt, lambda msg: msg.sender in ("Management") and msg.recipient in (department, "company"))
                msgs += Messages.load(calls, lambda msg: msg.account == account and department in (msg.sender, msg.recipient))

                with open("instructions", "r") as file:
                    instructions = file.read().replace("{department}", department)

                completion = llm.invoke(instructions, Messages.to_string(msgs))
                sanity = lambda msg: msg.sender == department and msg.recipient not in (msg.sender, "Management") and (msg.recipient != account or msg.sender == "Sales")
                msgs = Messages.from_string(completion, sanity)

                if len(msgs) == 1 and department == "Sales":
                    reply = msgs[0].body
                elif len(msgs) > 0
                    for msg in msgs:
                        if msg.recipient != account:
                            Messages.append_string_to_file(calls, msg.to_string())
                        
                            
    Messages.append_string_to_file(msgs, Message("Sales", account, reply).to_string())
    return reply
