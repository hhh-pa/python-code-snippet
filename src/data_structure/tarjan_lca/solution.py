import sys

sys.setrecursionlimit(200000)


def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    adj = [[] for _ in range(n + 1)]
    idx = 1
    for _ in range(n - 1):
        u = int(tokens[idx])
        v = int(tokens[idx + 1])
        idx += 2
        adj[u].append(v)
        adj[v].append(u)

    q = int(tokens[idx])
    idx += 1
    qid = [[] for _ in range(n + 1)]
    qother = [[] for _ in range(n + 1)]
    ans = [0] * q

    for i in range(q):
        a = int(tokens[idx])
        b = int(tokens[idx + 1])
        idx += 2
        qid[a].append(i)
        qother[a].append(b)
        qid[b].append(i)
        qother[b].append(a)

    parent = list(range(n + 1))
    ancestor = list(range(n + 1))
    visited = [False] * (n + 1)

    def find(x):
        root = x
        while parent[root] != root:
            root = parent[root]
        curr = x
        while curr != root:
            nxt = parent[curr]
            parent[curr] = root
            curr = nxt
        return root

    def dfs(u, p):
        parent[u] = u
        ancestor[u] = u
        for v in adj[u]:
            if v == p:
                continue
            dfs(v, u)
            parent[find(v)] = find(u)
            ancestor[find(u)] = u
        visited[u] = True
        u_qid = qid[u]
        u_qother = qother[u]
        for i in range(len(u_qid)):
            v = u_qother[i]
            if visited[v]:
                ans[u_qid[i]] = ancestor[find(v)]

    dfs(1, 0)
    sys.stdout.write("\n".join(map(str, ans)) + ("\n" if ans else ""))


if __name__ == "__main__":
    main()
