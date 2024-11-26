# sudo docker run -v `pwd`:/root -w /root company:latest python3 company.py

import llm
from messages import Messages, Message
import os

company = "sephora"
mgmt = f"{company}.txt"
calls = f"{company}.calls.txt"

no_company = lambda msg: msg.recipient != "company"
recipients = lambda path: Messages.recipients(path, no_company)
departments = list(recipients(mgmt) | recipients(calls))

def invoke():
    max_iterations = 10
    n_iterations = 0
    reply = "I don't know."

    # todo: monitor tokens and other health and Management sends alerts to company

    while n_iterations < max_iterations:
        n_iterations += 1
        i = 0

        while i < len(departments): # departments might grow during this loop
            department = departments[i]
            i += 1
            account = None

            for msg in Messages.load(calls, lambda msg: msg.recipient == department):
                account = msg.account

            if account:
                msgs = Messages.load(mgmt, lambda msg: msg.sender in ("Management") and msg.recipient in (department, "company"))
                msgs += Messages.load(calls, lambda msg: msg.account == account and department in (msg.sender, msg.recipient))

                with open("instructions", "r") as file:
                    instructions = f"You are a worker in {department}. " + file.read()

                completion = llm.invoke(instructions, Messages.to_string(msgs))
                sanity = lambda msg: msg.sender == department and msg.recipient != department
                msgs = Messages.from_string(completion, sanity)

                Messages.append_string_to_file(calls, Messages.to_string(msgs))

                for msg in msgs:
                    if msg.recipient == account:
                        reply = msg.body
                    elif msg.recipient not in departments:
                        departments.append(msg.recipient)

    return reply
