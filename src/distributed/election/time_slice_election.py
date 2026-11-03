import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    try:
        n = int(next(it))
    except StopIteration:
        return

    id_vals = [int(next(it)) for _ in range(n)]
    mn = min(id_vals)

    ts_rounds = mn * n + n
    vs_rounds = n * (mn + 1)
    vs_msgs = n
    for x in id_vals:
        if x == mn:
            continue
        h = vs_rounds // (x + 1)
        if h > n:
            h = n
        vs_msgs += h

    out = [
        f"TIME-SLICE ROUNDS: {ts_rounds} MESSAGES: {n}",
        f"VARIABLE-SPEED ROUNDS: {vs_rounds} MESSAGES: {vs_msgs}",
        f"LEADER: {mn}",
    ]
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
