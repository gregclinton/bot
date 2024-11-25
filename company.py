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
        come_from_above = lambda: msg.sender in ["Management"]
        visible_to_us = lambda: msg.recipient in [department, "company"]
        to_or_from_us = lambda: msg.recipient == department or msg.sender == department
        re_the_account = lambda: msg.account == account

        return (come_from_above() and visible_to_us()) or (re_the_account() and to_or_from_us())

    msgs = Messages.load("mail.txt") + Messages.load(path) + xxx

    instruction = f"You are an worker in {department}. "
    instruction += "Take care of msgs to you only if they require a reply. "
    instruction += "The msgs are shown in chronological order. "

    prompt = Messages.to_string(msgs)
    print(prompt)
    exit()
    print(llm.invoke(instruction, prompt))
