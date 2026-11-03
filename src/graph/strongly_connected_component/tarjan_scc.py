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

    dfn = [0] * n
    low = [0] * n
    on_stack = [False] * n
    st = []
    timer = 0
    sccs = []

    def dfs(u):
        nonlocal timer
        timer += 1
        dfn[u] = low[u] = timer
        st.append(u)
        on_stack[u] = True

        for v in adj[u]:
            if dfn[v] == 0:
                dfs(v)
                if low[v] < low[u]:
                    low[u] = low[v]
            elif on_stack[v]:
                if dfn[v] < low[u]:
                    low[u] = dfn[v]

        if low[u] == dfn[u]:
            scc = []
            while True:
                node = st.pop()
                on_stack[node] = False
                scc.append(node)
                if node == u:
                    break
            scc.sort()
            sccs.append(scc)

    for i in range(n):
        if dfn[i] == 0:
            dfs(i)

    sccs.sort(key=lambda scc: scc[0])

    out = [str(len(sccs))]
    for scc in sccs:
        out.append(" ".join(str(x) for x in scc))
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
