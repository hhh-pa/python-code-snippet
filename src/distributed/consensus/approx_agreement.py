import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    try:
        n = int(next(it))
        f = int(next(it))
        R = int(next(it))
    except StopIteration:
        return

    vals = [float(next(it)) for _ in range(n)]

    for _ in range(R):
        nvals = [0.0] * n
        recvd = sorted(vals)
        lo = f
        hi = n - f
        if hi <= lo:
            nvals = list(vals)
            vals = nvals
            continue
        avg = sum(recvd[lo:hi]) / (hi - lo)
        for i in range(n):
            nvals[i] = avg
        vals = nvals

    out = [f"P{i}: {vals[i]:.6f}" for i in range(n)]
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
