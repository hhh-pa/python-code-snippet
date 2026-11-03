import sys
from collections import deque

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    n = int(next(it))
    m = int(next(it))

    g = [[] for _ in range(n)]
    for _ in range(m):
        u = int(next(it))
        v = int(next(it))
        if u != v:
            g[u].append(v)
            g[v].append(u)

    for u in range(n):
        g[u] = sorted(set(g[u]))

    match_ = [-1] * n
    p = [-1] * n
    base = list(range(n))
    used = [0] * n
    bloss = [0] * n
    used_lca = [0] * n

    def lca(a, b):
        nonlocal used_lca
        used_lca = [0] * n
        while True:
            a = base[a]
            used_lca[a] = 1
            if match_[a] == -1:
                break
            a = p[match_[a]]
        while True:
            b = base[b]
            if used_lca[b]:
                return b
            if match_[b] == -1:
                break
            b = p[match_[b]]
        return -1

    def mark_path(v, b, child):
        while base[v] != b:
            bloss[base[v]] = 1
            bloss[base[match_[v]]] = 1
            p[v] = child
            child = match_[v]
            v = p[match_[v]]

    def find_path(root):
        nonlocal p, base, used, bloss
        p = [-1] * n
        base = list(range(n))
        used = [0] * n
        used[root] = 1
        q = deque([root])

        while q:
            v = q.popleft()
            for to in g[v]:
                if base[v] == base[to] or match_[v] == to:
                    continue
                if to == root or (match_[to] != -1 and p[match_[to]] != -1):
                    cur = lca(v, to)
                    bloss = [0] * n
                    mark_path(v, cur, to)
                    mark_path(to, cur, v)
                    for i in range(n):
                        if bloss[base[i]]:
                            base[i] = cur
                            if not used[i]:
                                used[i] = 1
                                q.append(i)
                elif p[to] == -1:
                    p[to] = v
                    if match_[to] == -1:
                        cur = to
                        while cur != -1:
                            prev = p[cur]
                            nxt = match_[prev] if prev != -1 else -1
                            match_[cur] = prev
                            if prev != -1:
                                match_[prev] = cur
                            cur = nxt
                        return True
                    else:
                        nxt = match_[to]
                        used[nxt] = 1
                        q.append(nxt)
        return False

    for v in range(n):
        if match_[v] == -1:
            find_path(v)

    prs = []
    for i in range(n):
        if match_[i] != -1 and i < match_[i]:
            prs.append((i, match_[i]))
    prs.sort()

    out = [str(len(prs))]
    for u, v in prs:
        out.append(f"{u} {v}")
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
