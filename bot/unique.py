from random import choice

def path(folder, name):
    folder.mkdir(parents = True, exist_ok = True)
    while True:
        random = ''.join(choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(5))
        path = folder / f"{name}|{random}"
        if not path.exists():
            return path