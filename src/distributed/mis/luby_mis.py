import sys

def pri(u):
    return (((u + 1) * 2654435761) >> 16) & 0xFFFFFFFF

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    try:
        n = int(next(it))
        m = int(next(it))
    except StopIteration:
        return

    adj = [[] for _ in range(n)]
    for _ in range(m):
        u = int(next(it))
        v = int(next(it))
        adj[u].append(v)
        adj[v].append(u)

    removed = [False] * n
    in_mis = [False] * n

    while True:
        cands = []
        for u in range(n):
            if not removed[u]:
                mx = True
                for v in adj[u]:
                    if not removed[v] and pri(v) > pri(u):
                        mx = False
                        break
                if mx:
                    cands.append(u)
        if not cands:
            break
        for u in cands:
            in_mis[u] = True
            removed[u] = True
            for v in adj[u]:
                removed[v] = True

    res = [i for i in range(n) if in_mis[i]]
    res.sort()
    out = [str(len(res))]
    if res:
        out.append(" ".join(map(str, res)))
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
