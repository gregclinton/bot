# sudo docker run -v `pwd`:/root -w /root company:latest python3 company.py

import llm
from messages import Messages

company = "sephora"
path = company + ".txt"
departments = Messages.recipients(path, lambda msg: msg.recipient != "company")
msgs = Messages.load(path)

print (departments)
exit()
for msg in msgs:
    if msg.sender == "Management" and msg.recipient != "company":
        departments.add(msg.recipient)

for department in ["Sales"]:
    account = None

    for msg in msgs:
        if msg.recipient == department:
            account = msg.account

    if not account:
        continue

    prompt = ""

    for msg in Messages.load("mail.txt") + msgs:
        come_from_above = lambda: msg.sender in ["Management"]
        visible_to_us = lambda: msg.recipient in [department, "company"]
        to_or_from_us = lambda: msg.recipient == department or msg.sender == department
        re_the_account = lambda: msg.account == account

        if (come_from_above() and visible_to_us()) or (re_the_account() and to_or_from_us()):
            prompt += msg.to_string()
        break

    instruction = f"You are an worker in {department}. "
    instruction += "Take care of msgs to you only if they require a reply. "
    instruction += "The msgs are shown in chronological order. "

    print(prompt)

    print(llm.invoke(instruction, prompt))
