import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    try:
        n = int(next(it))
        f = int(next(it))
    except StopIteration:
        return

    v = [int(next(it)) for _ in range(n)]
    k = int(next(it))
    faulty = [0] * n
    for _ in range(k):
        faulty[int(next(it))] = 1

    w = [0] * n
    has = [0] * n
    b = [0] * n
    for i in range(n):
        if faulty[i]:
            continue
        cnt = {}
        for j in range(n):
            if faulty[j]:
                continue
            cnt[v[j]] = cnt.get(v[j], 0) + 1
        best = 0
        bc = 0
        for val, count in cnt.items():
            if count > bc:
                bc = count
                best = val
        if bc >= n - f:
            w[i] = best
            has[i] = 1
            b[i] = 1

    band = 1
    for i in range(n):
        if not faulty[i] and not b[i]:
            band = 0

    dec = 0
    have = 0
    if band:
        for i in range(n):
            if not faulty[i] and has[i]:
                dec = w[i]
                have = 1
                break

    out = []
    for i in range(n):
        if faulty[i]:
            out.append(f"P{i}: FAULTY")
        else:
            w_str = str(w[i]) if has[i] else "NONE"
            out.append(f"P{i}: w={w_str} b={b[i]}")
    out.append(f"BINARY: {band}")
    if band and have:
        out.append(f"DECISION: {dec}")
    else:
        out.append("DECISION: ABSTAIN")

    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
