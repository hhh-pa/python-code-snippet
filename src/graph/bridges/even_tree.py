import sys

sys.setrecursionlimit(200000)

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    n = int(next(it))
    m = int(next(it))
    
    adj = [[] for _ in range(n + 1)]
    for _ in range(m):
        u = int(next(it))
        v = int(next(it))
        adj[u].append(v)
        adj[v].append(u)
        
    cuts = 0
    def dfs(u, parent):
        nonlocal cuts
        subtree_size = 1
        for v in adj[u]:
            if v != parent:
                subtree_size += dfs(v, u)
        if subtree_size % 2 == 0 and parent != 0:
            cuts += 1
        return subtree_size

    dfs(1, 0)
    print(cuts)

if __name__ == "__main__":
    main()
