import sys

sys.setrecursionlimit(1000000)


def has_cycle(n, edges):
    for u, v in edges:
        if u == v:
            return True
    adj = [[] for _ in range(n)]
    for u, v in edges:
        if 0 <= u < n and 0 <= v < n:
            adj[u].append(v)
            adj[v].append(u)
    seen = [False] * n

    def dfs(u, parent):
        seen[u] = True
        for w in adj[u]:
            if not seen[w]:
                if dfs(w, u):
                    return True
            elif w != parent:
                return True
        return False

    return any(not seen[u] and dfs(u, -1) for u in range(n))


def main():
    data = list(map(int, sys.stdin.read().split()))
    if len(data) < 2 or data[0] < 0 or data[1] < 0:
        return
    n, m = data[0], data[1]
    vals = data[2:]
    edges = [(vals[2 * i], vals[2 * i + 1]) for i in range(min(m, len(vals) // 2))]
    print(1 if has_cycle(n, edges) else 0)


if __name__ == "__main__":
    main()
