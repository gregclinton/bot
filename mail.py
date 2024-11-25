import llm
from messages import Email
import cuts

departments = set()
emails = []

with open('mail.txt', 'r') as file:
    all_mail = file.read()
    
with open('sephora.txt', 'r') as file:
    all_mail += file.read()

for cut in cuts.split(all_mail):
    email = Email.from_string(cut)
    if email.sender == "Management" and email.recipient != "company":
        departments.add(email.recipient)
    emails.append(email)

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

    for email in emails:
        come_from_above = lambda: email.sender in ["Management"]
        visible_to_us = lambda: email.recipient in [department, "company"]
        to_or_from_us = lambda: email.recipient == department or email.sender == department
        re_the_account = lambda: email.account == account

        if (come_from_above() and visible_to_us()) or (re_the_account() and to_or_from_us()):
            prompt += email.to_string()

    with open('mail.txt', 'r') as file:
        for cut in cuts.split(llm.invoke(instruction, prompt)):
            all_mail += Email.from_string(cut).to_string()

print(all_mail)
exit()
with open('mail.txt', 'w') as file:
    file.write(all_mail)