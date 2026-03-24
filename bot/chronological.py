def paths(*folders):
    pairs = [(p.stat().st_mtime, p) for f in folders for p in f.iterdir()]
    pairs.sort()
    return pairs
