import llm

departments = set()

with open('mail.txt', 'r') as file:
    for line in file.readlines():
        line = line.rstrip()
        if line.startswith("To: "):
            recipient = line.split(" ")[1]
            if '@' not in recipient and recipient not in ["above", "company"]:
                departments.add(recipient)

for department in ["Betty"]:
    print(department)
exit()

with open('mail.txt', 'r') as file:
    print(llm.invoke(file.read()))