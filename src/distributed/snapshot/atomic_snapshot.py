import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    try:
        n = int(next(it))
        q = int(next(it))
    except StopIteration:
        return

    state = [0] * n
    sn = 0
    out = []

    for _ in range(q):
        op = next(it)
        if op == "U":
            i = int(next(it))
            v = int(next(it))
            state[i] = v
        else:
            c = int(next(it))
            c1 = list(state)
            for _ in range(c):
                u = int(next(it))
                v = int(next(it))
                state[u] = v
            c2 = list(state)
            collects = 2 if c1 == c2 else 3
            c2_str = " ".join(map(str, c2))
            out.append(f"SCAN {sn}: {c2_str} collects={collects}")
            sn += 1

    st_str = " ".join(map(str, state))
    out.append(f"STATE: {st_str}")
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
