# sudo docker run -v `pwd`:/root -w /root company:latest python3 company.py

import llm
from messages import Messages, Message
import os

company = "sephora"
mgmt = f"{company}.txt"
calls = f"{company}.calls.txt"

departments = Messages.recipients(mgmt, lambda msg: msg.recipient != "company")

def invoke():
    max_iterations = 10
    n_iterations = 0

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
                    instructions = f"You are a worker in {department}. " + file.read()

                completion = llm.invoke(instructions, msgs)
                last_msg = Message.from_string(completion)
                Messages.append_string_to_file(calls, last_msg.to_string())
                if last_msg.recipient == account:
                    return last_msg.body

    return "I don't know."
