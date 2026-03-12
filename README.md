I create a folder called ~/app and run all commands from there.

I run setup for the app, in this case, wireless, and post questions.

```bash
sh ~/bot/apps/wireless/setup
python3 messages.py post TLG15151515 Hal "What is my balance?"
```

In another terminal session I export my GROQ_API_KEY and run the workers.

```sh
sh ~/bot/apps/wireless/run
```

In another terminal session I poll for answers.

```sh
while true; do python3 messages.py poll TLG15151515; sleep 0.2; done
```

Each worker stores all messages it sends or receives in per-user-account folders.
So it has a complete chronological transcript, a dossier as it were, for each user.

The possibilities for such a paper trail are considerable.