import messages
import time
import llm

while True:
    invoke = lambda sys, user: llm.invoke("groq", "openai/gpt-oss-20b", sys, user)
    read = lambda *files: "\n\n".join(open(f"markdown/{f}.md").read() for f in files)

    box = "chief"
    thread = messages.get(box)
    if thread:
        messages.post(box, box, invoke(read("hal"), thread))