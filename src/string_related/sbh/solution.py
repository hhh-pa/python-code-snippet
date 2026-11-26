import sys
from collections import defaultdict


def main():
    toks = sys.stdin.read().split()
    if len(toks) < 3:
        return
    kmers = toks[2:]
    adj = defaultdict(list)
    deg = defaultdict(int)
    for km in kmers:
        u, v = km[:-1], km[1:]
        adj[u].append(km)
        deg[u] += 1
        deg[v] -= 1
    for u in adj:
        adj[u].sort(reverse=True)
    nodes = sorted(set(adj.keys()) | {km[1:] for km in kmers})
    start = next((u for u in nodes if deg[u] == 1), min(adj.keys()))
    stack, path = [start], []
    while stack:
        u = stack[-1]
        if adj[u]:
            stack.append(adj[u].pop()[1:])
        else:
            path.append(stack.pop())
    path.reverse()
    out = path[0]
    for node in path[1:]:
        out += node[-1]
    sys.stdout.write(out)


if __name__ == "__main__":
    main()
