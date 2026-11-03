import sys

sys.setrecursionlimit(200000)

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    n = int(next(it))
    m = int(next(it))

    adj = [[] for _ in range(n)]
    for _ in range(m):
        u = int(next(it))
        v = int(next(it))
        adj[u].append(v)

    for u in range(n):
        adj[u].sort()

    mtR = [-1] * n
    seen = [False] * n

    def bpm(u):
        for v in adj[u]:
            if seen[v]:
                continue
            seen[v] = True
            if mtR[v] == -1 or bpm(mtR[v]):
                mtR[v] = u
                return True
        return False

    for u in range(n):
        seen = [False] * n
        bpm(u)

    mtL = [-1] * n
    for v in range(n):
        if mtR[v] != -1:
            mtL[mtR[v]] = v

    paths = []
    for s in range(n):
        if mtR[s] == -1:
            p = [s]
            while mtL[p[-1]] != -1:
                p.append(mtL[p[-1]])
            paths.append(p)

    paths.sort(key=lambda x: x[0])
    out = [str(len(paths))]
    for p in paths:
        out.append(" ".join(str(x) for x in p))
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
