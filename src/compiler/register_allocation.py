import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    idx = 0
    try:
        n = int(tokens[idx])
        m = int(tokens[idx + 1])
        k = int(tokens[idx + 2])
    except (ValueError, IndexError):
        return
    idx += 3

    adj = [set() for _ in range(n)]
    for _ in range(m):
        if idx >= len(tokens):
            break
        u = int(tokens[idx])
        v = int(tokens[idx + 1])
        idx += 2
        adj[u].add(v)
        adj[v].add(u)

    active = set(range(n))
    deg = [len(adj[u]) for u in range(n)]

    select_stack = []
    spilled = [False] * n

    while active:
        simplify_node = -1
        # C++ iterates over std::set<int> active in ascending order
        for u in sorted(active):
            # compute degree in active
            d = 0
            for v in adj[u]:
                if v in active:
                    d += 1
            if d < k:
                simplify_node = u
                break

        if simplify_node != -1:
            active.remove(simplify_node)
            select_stack.append(simplify_node)
        else:
            spill_node = min(active)
            active.remove(spill_node)
            spilled[spill_node] = True

    color = [-1] * n
    while select_stack:
        u = select_stack.pop()
        used_colors = set()
        for v in adj[u]:
            if color[v] != -1:
                used_colors.add(color[v])
        for c in range(k):
            if c not in used_colors:
                color[u] = c
                break
        if color[u] == -1:
            spilled[u] = True

    out = []
    for i in range(n):
        if spilled[i]:
            out.append(f"v{i}:SPILL")
        else:
            out.append(f"v{i}:R{color[i]}")

    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
