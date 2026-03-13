I run setup.

```sh
sh ~/bot/apps/wireless/setup
```

In a separate terminal I export my GROQ_API_KEY and run the workers.

```sh
sh ~/bot/apps/wireless/run
```

Back in the first terminal I post questions...

```sh
python3 messages.py post TLG15151515 Hal "What is my balance?"
```

...and poll for answers.

```sh
python3 messages.py poll TLG15151515
```

Each worker stores all messages it sends or receives in per-user-account folders.
So it has a complete chronological transcript, a dossier as it were, for each user.

The possibilities for such a paper trail are considerable.