"""BGP path-vector routing simulation (Tanenbaum 5)."""

import sys


def _better(cand, frm, cur):
    return (
        cur is None
        or len(cand) < len(cur[1])
        or (len(cand) == len(cur[1]) and frm < cur[0])
    )


def _rounds(n, adj, origin):
    rib = [None] * n
    rib[origin] = (origin, [origin])
    discards = [0] * n
    for _ in range(n * n):
        adv = []
        for a in range(n):
            if rib[a] is not None:
                for f in adj[a]:
                    adv.append((f, a, rib[a][1]))
        changed = False
        for f, frm, path in adv:
            if f in path:
                discards[f] += 1
                continue
            cand = [f, *path]
            if _better(cand, frm, rib[f]):
                rib[f] = (frm, cand)
                changed = True
        if not changed:
            break
    return rib, discards


def _run(n, links, origin):
    adj = [[] for _ in range(n)]
    for a, b in links:
        adj[a].append(b)
        adj[b].append(a)
    rib, discards = _rounds(n, adj, origin)
    out = []
    for a in range(n):
        if a == origin:
            out.append(f"ORIGIN {origin}")
        elif rib[a] is None:
            out.append("UNREACHABLE")
        else:
            nx, path = rib[a]
            out.append(f"{nx} " + " ".join(map(str, path)))
    out.append("DISCARDS " + " ".join(map(str, discards)))
    return out


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    n, m = int(toks[0]), int(toks[1])
    links = []
    i = 2
    for _ in range(m):
        links.append((int(toks[i]), int(toks[i + 1])))
        i += 2
    origin = int(toks[i])
    sys.stdout.write("\n".join(_run(n, links, origin)))


if __name__ == "__main__":
    main()
