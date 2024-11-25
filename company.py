# sudo docker run -v `pwd`:/root -w /root company:latest python3 company.py

import llm
from messages import Email

departments = set()
emails = Email.load("sephora.txt")

for email in emails:
    if email.sender == "Management" and email.recipient != "company":
        departments.add(email.recipient)

for department in departments:
    instruction = f"You are an worker in {department}. "
    instruction += "Take care of emails to you only if they require a reply. "
    instruction += "The emails are shown in chronological order. "
    account = None

    for email in emails:
        if email.recipient == department:
            account = email.account

    if not account:
        continue

    prompt = ""

    for email in emails + Email.load("mail.txt"):
        come_from_above = lambda: email.sender in ["Management"]
        visible_to_us = lambda: email.recipient in [department, "company"]
        to_or_from_us = lambda: email.recipient == department or email.sender == department
        re_the_account = lambda: email.account == account

        if (come_from_above() and visible_to_us()) or (re_the_account() and to_or_from_us()):
            prompt += email.to_string()

    print(llm.invoke(instruction, prompt))
