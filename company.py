# sudo docker run -v `pwd`:/root -w /root company:latest python3 company.py

import llm
from messages import Messages

company = "sephora"
path = company + ".txt"
departments = Messages.recipients(path, lambda msg: msg.recipient != "company")

for department in ["Sales"]:
    account = None

    for msg in Messages.load("xxx.txt", lambda msg: msg.recipient == department):
        account = msg.account

    if not account:
        continue

    def keep(msg):
        come_from_above = lambda: msg.sender in ("Management")
        visible_to_us = lambda: msg.recipient in (department, "company")
        to_or_from_us = lambda: department in (msg.sender, msg.recipient)
        re_the_account = lambda: msg.account == account

        return (come_from_above() and visible_to_us()) or (re_the_account() and to_or_from_us())

    instruction = f"You are a worker in {department}. "
    instruction += "Take care of messages to you only if they require a reply. "
    instruction += "The messages are shown in chronological order. "

    msgs = Messages.load(path, keep) + Messages.load("xxx.txt", keep)
    with open("mail.txt", "r") as file:
        completion = llm.invoke(instruction, file.read() + Messages.to_string(msgs))

    print(Messages.to_string(msgs + Messages.from_string(completion)))
