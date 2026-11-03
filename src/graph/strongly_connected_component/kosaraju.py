import sys
from collections import Counter

sys.setrecursionlimit(200000)

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    n = int(next(it))
    m = int(next(it))

    graph = [[] for _ in range(n)]
    rev_graph = [[] for _ in range(n)]

    while True:
        try:
            a = int(next(it)) - 1
            b = int(next(it)) - 1
            graph[a].append(b)
            rev_graph[b].append(a)
        except StopIteration:
            break

    marked = [False] * n
    post_order = []

    def dfs1(v):
        marked[v] = True
        for w in rev_graph[v]:
            if not marked[w]:
                dfs1(w)
        post_order.append(v)

    for v in range(n):
        if not marked[v]:
            dfs1(v)

    marked2 = [False] * n
    components = [-1] * n
    count = 0

    def dfs2(v):
        marked2[v] = True
        components[v] = count
        for w in graph[v]:
            if not marked2[w]:
                dfs2(w)

    while post_order:
        c = post_order.pop()
        if not marked2[c]:
            dfs2(c)
            count += 1

    counts = Counter(components)
    odd = 0
    even = 0
    for size in counts.values():
        if size % 2 != 0:
            odd += size
        else:
            even += size

    print(odd - even)

if __name__ == "__main__":
    main()
