import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    n = int(next(it))
    ch = [[] for _ in range(n)]
    for _ in range(n - 1):
        p = int(next(it))
        c = int(next(it))
        ch[p].append(c)

    L = int(next(it))
    leaf = [''] * n
    alpha = []
    for _ in range(L):
        id_ = int(next(it))
        st = next(it)
        leaf[id_] = st
        alpha.append(st)

    alpha = sorted(set(alpha))
    order = []
    seen = [False] * n
    st = [0]
    seen[0] = True
    while st:
        u = st.pop()
        order.append(u)
        for v in ch[u]:
            if not seen[v]:
                seen[v] = True
                st.append(v)

    fs = [set() for _ in range(n)]
    fcost = 0
    for k in range(len(order) - 1, -1, -1):
        u = order[k]
        if not ch[u]:
            fs[u].add(leaf[u])
            continue
        best = 10**9
        bs = set()
        for a in alpha:
            mm = 0
            for v in ch[u]:
                if a not in fs[v]:
                    mm += 1
            if mm < best:
                best = mm
                bs = {a}
            elif mm == best:
                bs.add(a)
        fs[u] = bs
        fcost += best

    INF = 10**9
    na = len(alpha)
    ai = {alpha[i]: i for i in range(na)}
    sc = [[INF] * na for _ in range(n)]

    for k in range(len(order) - 1, -1, -1):
        u = order[k]
        if not ch[u]:
            sc[u][ai[leaf[u]]] = 0
            continue
        for a in range(na):
            tot = 0
            for v in ch[u]:
                best = INF
                sc_v = sc[v]
                for b in range(na):
                    val = sc_v[b] + (0 if a == b else 1)
                    if val < best:
                        best = val
                tot += best
            sc[u][a] = tot

    scost = min(sc[0])
    print(f"{fcost} {scost}")
    print("".join(sorted(fs[0])))

if __name__ == "__main__":
    main()
