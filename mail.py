import llm

# print(llm.invoke("hi"))

with open('mail.txt', 'r') as file:
    lines = file.readlines()
    for line in file.readlines():
        print(line.strip()) 