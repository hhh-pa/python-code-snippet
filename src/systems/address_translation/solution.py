"""Page-table walk address translation (CS:APP ch 9)."""

import sys


def _run(w, m, k, paths, queries):
    table = {}
    for vpns, ppn in paths:
        table[tuple(vpns)] = ppn
    out = []
    for va in queries:
        if va >= (1 << (k * w + m)):
            out.append("FAULT 0")
            continue
        vpn = va >> m
        idx = [(vpn >> (w * (k - 1 - i))) & ((1 << w) - 1) for i in range(k)]
        hit = None
        for level in range(1, k + 1):
            pre = tuple(idx[:level])
            if not any(p[:level] == pre for p in table):
                hit = f"FAULT {level}"
                break
        if hit is None:
            ppn = table[tuple(idx)]
            hit = (
                f"FAULT {k}" if ppn < 0 else f"PA {(ppn << m) | (va & ((1 << m) - 1))}"
            )
        out.append(hit)
    return out


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    w, m, k = int(toks[0]), int(toks[1]), int(toks[2])
    t = int(toks[3])
    paths = []
    i = 4
    for _ in range(t):
        vpns = list(map(int, toks[i : i + k]))
        ppn = int(toks[i + k])
        paths.append((vpns, ppn))
        i += k + 1
    q = int(toks[i])
    queries = list(map(int, toks[i + 1 : i + 1 + q]))
    sys.stdout.write("\n".join(_run(w, m, k, paths, queries)))


if __name__ == "__main__":
    main()
