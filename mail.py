import llm

# print(llm.invoke("hi"))

with open('mail.txt', 'r') as file:
    for line in file.readlines():
        print(line.strip()) 