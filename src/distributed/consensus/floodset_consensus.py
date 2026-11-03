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

    init = [int(next(it)) for _ in range(n)]
    nf = int(next(it))
    faulty = [False] * n
    for _ in range(nf):
        faulty[int(next(it))] = True

    W = [{init[i]} for i in range(n)]
    for _ in range(f + 1):
        nW = [set(s) for s in W]
        for i in range(n):
            if not faulty[i]:
                for j in range(n):
                    if not faulty[j] and i != j:
                        nW[i].update(W[j])
        W = nW

    out = []
    for i in range(n):
        if not faulty[i]:
            out.append(f"P{i}: {min(W[i])}")
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
