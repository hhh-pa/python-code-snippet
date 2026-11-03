import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    nU = int(tokens[0])
    nV = int(tokens[1])
    m = int(tokens[2])
    adj = [[] for _ in range(nU)]
    idx = 3
    for _ in range(m):
        u = int(tokens[idx])
        v = int(tokens[idx + 1])
        idx += 2
        adj[u].append(v)

    x = 42
    def rnd(n):
        nonlocal x
        x = (1103515245 * x + 12345) % (1 << 31)
        return x % n

    rk = list(range(nV))
    for i in range(nV - 1, 0, -1):
        j = rnd(i + 1)
        rk[i], rk[j] = rk[j], rk[i]

    pos = [0] * nV
    for r in range(nV):
        pos[rk[r]] = r

    mate = [-1] * nU
    used = [False] * nV

    for u in range(nU):
        best = -1
        bp = nV + 1
        for v in adj[u]:
            if not used[v] and pos[v] < bp:
                best = v
                bp = pos[v]
        if best != -1:
            mate[u] = best
            used[best] = True

    pr = [(u, mate[u]) for u in range(nU) if mate[u] != -1]
    print(len(pr))
    out = [f"{u} {v}" for u, v in pr]
    if out:
        sys.stdout.write("\n".join(out) + "\n")

if __name__ == '__main__':
    main()
