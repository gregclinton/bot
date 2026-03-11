I create and cd to a folder called ~/app.

Then I run the setup for the app. In this case, wireless.

```
cd ~/app && sh ~/bot/apps/wireless/setup
```

I export my GROQ_API_KEY and run workers in a separate terminal session.
```
cd ~/app && sh ~/bot/apps/wireless/run
```

To post a question:
```
python3 messages.py post TLG15151515 Hal "What is my balance?"
```


poll for answers in a separate terminal session.

```
while true; do python3 messages.py poll TLG15151515; sleep 0.2; done
```

The prefix TLG is required here for users. I used to use Telegram, hence TLG.

Each worker stores all messages they've sent or received in per-user-account folders.
This way it has a complete chronological transcript, a dossier as it were, for that user.

The possibilities for such a paper trail are considerable.