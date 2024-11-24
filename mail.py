import llm

# print(llm.invoke("hi"))

with open('mail.txt', 'r') as file:
    for line in file.readlines():
        line = line.rstrip()
        if line.startswith("To: "):
            to = line.split(" ")[1]
            print(to) 