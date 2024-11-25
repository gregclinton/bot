# sudo docker run -v `pwd`:/root -w /root company:latest python3 company.py

import llm
from messages import Messages

company = "sephora"
path = company + ".txt"
departments = Messages.recipients(path, lambda msg: msg.recipient != "company")

for department in ["Sales"]:
    account = None
    xxx = Messages.load("xxx.txt")

    for msg in xxx:
        if msg.recipient == department:
            account = msg.account

    if not account:
        continue

    def condition(msg):
        come_from_above = lambda: msg.sender in ("Management")
        visible_to_us = lambda: msg.recipient in (department, "company")
        to_or_from_us = lambda: department in (msg.sender, msg.recipient)
        re_the_account = lambda: msg.account == account

        return (come_from_above() and visible_to_us()) or (re_the_account() and to_or_from_us())

    instruction = f"You are an worker in {department}. "
    instruction += "Take care of msgs to you only if they require a reply. "
    instruction += "The msgs are shown in chronological order. "

    msgs = Messages.load("mail.txt") + Messages.load(path, condition) + xxx
    completion = llm.invoke(instruction, Messages.to_string(msgs))
    print(Messages.to_string(msgs + Messages.from_string(completion)))
