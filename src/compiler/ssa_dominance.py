import sys
from collections import deque

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    idx = 0
    try:
        n = int(tokens[idx])
        m = int(tokens[idx + 1])
    except (ValueError, IndexError):
        return
    idx += 2

    adj = [[] for _ in range(n + 1)]
    rev_adj = [[] for _ in range(n + 1)]

    for _ in range(m):
        if idx >= len(tokens):
            break
        u = int(tokens[idx])
        v = int(tokens[idx + 1])
        idx += 2
        adj[u].append(v)
        rev_adj[v].append(u)

    dom = [set() for _ in range(n + 1)]
    dom[1] = {1}
    all_nodes = set(range(1, n + 1))
    for i in range(2, n + 1):
        dom[i] = set(all_nodes)

    changed = True
    while changed:
        changed = False
        for i in range(2, n + 1):
            if not rev_adj[i]:
                new_dom = set()
            else:
                new_dom = set(dom[rev_adj[i][0]])
                for p in rev_adj[i][1:]:
                    new_dom.intersection_update(dom[p])
            new_dom.add(i)
            if new_dom != dom[i]:
                dom[i] = new_dom
                changed = True

    idom = [0] * (n + 1)
    for i in range(2, n + 1):
        for d in dom[i]:
            if d != i and len(dom[i]) == len(dom[d]) + 1:
                idom[i] = d
                break

    # Dominance Frontier DF(X)
    df = [set() for _ in range(n + 1)]
    for x in range(1, n + 1):
        for y in adj[x]:
            if idom[y] != x:
                df[x].add(y)

    for x in range(1, n + 1):
        for z in range(1, n + 1):
            if idom[z] == x:
                for y in df[z]:
                    if idom[y] != x:
                        df[x].add(y)

    if idx >= len(tokens):
        return
    def_count = int(tokens[idx])
    idx += 1
    defs = set()
    for _ in range(def_count):
        defs.add(int(tokens[idx]))
        idx += 1

    # IDF for phi placement
    phi_blocks = set()
    w = deque(defs)
    while w:
        x = w.popleft()
        for y in df[x]:
            if y not in phi_blocks:
                phi_blocks.add(y)
                if y not in defs:
                    w.append(y)

    idom_str = "".join(f"idom({i})={idom[i]} " for i in range(2, n + 1))
    if phi_blocks:
        phi_str = " ".join(str(b) for b in sorted(phi_blocks))
    else:
        phi_str = "NONE"

    sys.stdout.write(f"{idom_str}\n{phi_str}\n")

if __name__ == "__main__":
    main()
