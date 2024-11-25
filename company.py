# sudo docker run -v `pwd`:/root -w /root company:latest python3 company.py

import llm
from messages import Messages
import os

company = "sephora"
mgmt = f"{company}.txt"
calls = f"{company}.calls.txt"

departments = Messages.recipients(mgmt, lambda msg: msg.recipient != "company")

def run():
    for department in [departments]:
        account = None

        for msg in Messages.load(calls, lambda msg: msg.recipient == department):
            account = msg.account

        if not account:
            continue

        msgs = Messages.load(mgmt, lambda msg: msg.sender in ("Management") and msg.recipient in (department, "company"))
        msgs += Messages.load(calls, lambda msg: msg.account == account and department in (msg.sender, msg.recipient))

        instruction = f"You are a worker in {department}. "
        instruction += "Take care of messages to you only if they require a reply. "
        instruction += "The messages are shown in chronological order. "

        completion = llm.invoke(instruction, Messages.to_string(Messages.load("mail.txt") + msgs))
        Messages.append_string_to_file(calls, completion)
