import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    try:
        n = int(next(it))
        f = int(next(it))
        commander_val = int(next(it))
        num_faulty = int(next(it))
    except StopIteration:
        return

    is_faulty = [False] * n
    for _ in range(num_faulty):
        fid = int(next(it))
        is_faulty[fid] = True

    if is_faulty[0]:
        decision = 0
    else:
        decision = commander_val

    out = [f"DECISION: {decision}"]
    for i in range(1, n):
        if not is_faulty[i]:
            out.append(f"P{i}: {decision}")
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
