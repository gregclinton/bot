import llm

with open('mail.txt', 'r') as file:
    print(llm.invoke(file.read()))
exit()

with open('mail.txt', 'r') as file:
    for line in file.readlines():
        line = line.rstrip()
        if line.startswith("To: "):
            to = line.split(" ")[1]
            print(to) 