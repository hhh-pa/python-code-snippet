import sys

CODONS = {
    "F": ["TTT", "TTC"],
    "L": ["TTA", "TTG", "CTT", "CTC", "CTA", "CTG"],
    "I": ["ATT", "ATC", "ATA"],
    "M": ["ATG"],
    "V": ["GTT", "GTC", "GTA", "GTG"],
    "S": ["TCT", "TCC", "TCA", "TCG", "AGT", "AGC"],
    "P": ["CCT", "CCC", "CCA", "CCG"],
    "T": ["ACT", "ACC", "ACA", "ACG"],
    "A": ["GCT", "GCC", "GCA", "GCG"],
    "Y": ["TAT", "TAC"],
    "H": ["CAT", "CAC"],
    "Q": ["CAA", "CAG"],
    "N": ["AAT", "AAC"],
    "K": ["AAA", "AAG"],
    "D": ["GAT", "GAC"],
    "E": ["GAA", "GAG"],
    "C": ["TGT", "TGC"],
    "W": ["TGG"],
    "R": ["CGT", "CGC", "CGA", "CGG", "AGA", "AGG"],
    "G": ["GGT", "GGC", "GGA", "GGG"],
}


def _build_net(prot):
    edges = []
    nid, entry = 0, 0
    for aa in prot:
        nid += 1
        nex = nid
        for cod in sorted(CODONS[aa]):
            u = entry
            for ch in cod:
                nid += 1
                edges.append((u, nid, ch))
                u = nid
            if u != nex:
                edges = [
                    (a if a != u else nex, b if b != u else nex, c) for a, b, c in edges
                ]
                nid -= 1
        entry = nex
    into = {}
    for a, b, c in edges:
        into.setdefault(b, []).append((a, c))
    for v in into:
        into[v].sort(key=lambda e: (e[1], e[0]))
    return nid + 1, entry, into


def _fill_dp(s, nnodes, into, sub, ins, dele):
    n = len(s)
    inf = float("inf")
    dmat = [[inf] * nnodes for _ in range(n + 1)]
    par = [[None] * nnodes for _ in range(n + 1)]
    dmat[0][0] = 0
    for i in range(1, n + 1):
        dmat[i][0] = i * dele
        par[i][0] = ("del", 0)
    for v in range(1, nnodes):
        best, bp = inf, None
        for u, ch in into.get(v, []):
            cand = dmat[0][u] + ins
            if cand < best:
                best, bp = cand, ("ins", u, ch)
        dmat[0][v] = best
        par[0][v] = bp
    for i in range(1, n + 1):
        for v in range(1, nnodes):
            dmat[i][v], par[i][v] = _fill_cell(dmat, par, s, into, sub, ins, dele, i, v)
    return dmat, par


def _fill_cell(dmat, par, s, into, sub, ins, dele, i, v):
    best, bp = float("inf"), None
    for u, ch in into.get(v, []):
        cs = dmat[i - 1][u] + (0 if s[i - 1] == ch else sub)
        if cs < best:
            best, bp = cs, ("sub", u, ch)
    cd = dmat[i - 1][v] + dele
    if cd < best:
        best, bp = cd, ("del", v)
    for u, ch in into.get(v, []):
        ci = dmat[i][u] + ins
        if ci < best:
            best, bp = ci, ("ins", u, ch)
    return best, bp


def _traceback(par, n, t):
    out = []
    i, v = n, t
    while not (i == 0 and v == 0):
        p = par[i][v]
        if p[0] == "del":
            i -= 1
        elif p[0] == "ins":
            out.append(p[2])
            v = p[1]
        else:
            out.append(p[2])
            i -= 1
            v = p[1]
    out.reverse()
    return "".join(out)


def main():
    toks = sys.stdin.read().split()
    if len(toks) < 6:
        return
    sub, ins, dele = int(toks[1]), int(toks[2]), int(toks[3])
    s, prot = toks[4], toks[5]
    nnodes, t, into = _build_net(prot)
    dmat, par = _fill_dp(s, nnodes, into, sub, ins, dele)
    sys.stdout.write(f"{dmat[len(s)][t]}\n{_traceback(par, len(s), t)}")


if __name__ == "__main__":
    main()
