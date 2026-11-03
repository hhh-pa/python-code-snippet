import sys

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

    g = [[] for _ in range(n)]
    gr = [[] for _ in range(n)]
    self_loop = [False] * n
    for _ in range(m):
        u = int(next(it))
        v = int(next(it))
        if u < 0 or u >= n or v < 0 or v >= n:
            continue
        g[u].append(v)
        gr[v].append(u)
        if u == v:
            self_loop[u] = True

    seen = [False] * n
    order = []
    for s in range(n):
        if seen[s]:
            continue
        st = [[s, 0]]
        seen[s] = True
        while st:
            u, k = st[-1]
            if k < len(g[u]):
                st[-1][1] += 1
                v = g[u][k]
                if not seen[v]:
                    seen[v] = True
                    st.append([v, 0])
            else:
                order.append(u)
                st.pop()

    comp = [-1] * n
    nc = 0
    for s in reversed(order):
        if comp[s] != -1:
            continue
        st = [s]
        comp[s] = nc
        while st:
            u = st.pop()
            for v in gr[u]:
                if comp[v] == -1:
                    comp[v] = nc
                    st.append(v)
        nc += 1

    size = [0] * nc
    for c in comp:
        size[c] += 1

    cyc = [u for u in range(n) if size[comp[u]] > 1 or self_loop[u]]
    if not cyc:
        print("NO DEADLOCK")
    else:
        print("DEADLOCK " + " ".join(map(str, cyc)))

if __name__ == "__main__":
    main()
