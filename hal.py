import messages
import time
import llm

while True:
    msg = messages.get("/tmp/messages/1000")
    if msg:
        print(llm.invoke("groq", "openai/gpt-oss-20b", "You are Hal.", open(msg).read()))
    time.sleep(1)