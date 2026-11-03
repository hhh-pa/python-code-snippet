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

    vote = [next(it) for _ in range(n)]
    all_yes = all(v == "YES" for v in vote)
    decision = "COMMIT" if all_yes else "ABORT"

    out = [f"DECISION: {decision}"]
    for i in range(n):
        state = "ABORT" if vote[i] == "TIMEOUT" else decision
        out.append(f"P{i}: {state}")
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
