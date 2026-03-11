I create and cd to a folder called ~/app and copy *.py there.
I also export my LLM API keys such as GROQ_API_KEY.
Then I run `sh ~/bot/apps/wireless/setup`.

I run the workers in a separate terminal session:
```
sh ~/bot/apps/wireless/run
```

To post a question:
```
python3 messages.py post TLG15151515 Hal "What is my balance?"
```

I poll for answers in a separate terminal session.

```
while true; do python3 messages poll TLG15151515; sleep 0.2 done
```

The prefix TLG is required here for users. I used to use Telegram, hence TLG.

Each worker stores all messages they've sent or received in per-user-account folders.
This way it has a complete chronological transcript, a dossier as it were, for that user.
One could imagine all that one could do with such a trail.