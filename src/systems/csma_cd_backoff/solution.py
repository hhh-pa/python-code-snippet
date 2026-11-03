import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    try:
        q = int(next(it))
    except StopIteration:
        return

    for _ in range(q):
        k = int(next(it))
        tot = 0
        wins = []
        for j in range(1, k + 1):
            d = int(next(it))
            e = min(j, 10)
            win = 1 << e
            wins.append(win)
            dd = abs(d)
            tot += dd % win
        out = [str(tot)]
        for w in wins:
            out.append(str(w))
        print(" ".join(out))

if __name__ == "__main__":
    main()
