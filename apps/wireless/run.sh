while true; do python3 worker.py groq openai/gpt-oss-120b Above Hal; sleep 1; done &
while true; do python3 worker.py groq openai/gpt-oss-120b Above Billing; sleep 1; done &
while true; do python3 balance.py; sleep 1; done &
