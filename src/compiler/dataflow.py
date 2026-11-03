import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    mode = tokens[0]
    n = int(tokens[1])
    idx = 2

    exprs = []
    eidx = {}
    if mode == "AVAIL":
        ne = int(tokens[idx])
        idx += 1
        for _ in range(ne):
            eid = tokens[idx]
            v1 = tokens[idx + 1]
            # op = tokens[idx + 2]
            v2 = tokens[idx + 3]
            idx += 4
            eidx[eid] = len(exprs)
            exprs.append((eid, v1, v2))

    succ = [[] for _ in range(n)]
    defs = [[] for _ in range(n)]
    uses = [[] for _ in range(n)]
    gens = [[] for _ in range(n)]
    allvars = []

    for b in range(n):
        ns = int(tokens[idx])
        idx += 1
        for _ in range(ns):
            succ[b].append(int(tokens[idx]))
            idx += 1
        nd = int(tokens[idx])
        idx += 1
        for _ in range(nd):
            v = tokens[idx]
            idx += 1
            defs[b].append(v)
            allvars.append(v)
        if mode == "AVAIL":
            ng = int(tokens[idx])
            idx += 1
            for _ in range(ng):
                gens[b].append(tokens[idx])
                idx += 1
        else:
            nu = int(tokens[idx])
            idx += 1
            for _ in range(nu):
                v = tokens[idx]
                idx += 1
                uses[b].append(v)
                allvars.append(v)

    pred = [[] for _ in range(n)]
    for b in range(n):
        for s in succ[b]:
            pred[s].append(b)

    DEF = [0] * n
    USE = [0] * n
    GEN = [0] * n
    KILL = [0] * n
    names = []

    if mode == "LIVE":
        names = sorted(list(set(allvars)))
        U = len(names)
        vi = {name: i for i, name in enumerate(names)}
        for b in range(n):
            for v in defs[b]:
                DEF[b] |= (1 << vi[v])
            for v in uses[b]:
                USE[b] |= (1 << vi[v])
    elif mode == "REACH":
        dvar = []
        dids = [[] for _ in range(n)]
        for b in range(n):
            for v in defs[b]:
                dids[b].append(len(dvar))
                dvar.append(v)
        U = len(dvar)
        names = [f"d{i}" for i in range(U)]
        for b in range(n):
            for did in dids[b]:
                GEN[b] |= (1 << did)
            mine_set = set(dids[b])
            defs_set = set(defs[b])
            for i in range(U):
                if i not in mine_set and dvar[i] in defs_set:
                    KILL[b] |= (1 << i)
    else:  # AVAIL
        U = len(exprs)
        names = [e[0] for e in exprs]
        for b in range(n):
            for g in gens[b]:
                GEN[b] |= (1 << eidx[g])
            defs_set = set(defs[b])
            for i in range(U):
                _, v1, v2 = exprs[i]
                if v1 in defs_set or v2 in defs_set:
                    KILL[b] |= (1 << i)

    ALL = 0 if U == 0 else ((1 << U) - 1)
    IN = [0] * n
    OUT = [ALL] * n if mode == "AVAIL" else [0] * n

    iters = 0
    if mode == "LIVE":
        ch = True
        while ch:
            ch = False
            iters += 1
            for b in range(n - 1, -1, -1):
                o = 0
                for s in succ[b]:
                    o |= IN[s]
                ni = (USE[b] | (o & (~DEF[b]))) & ALL
                if o != OUT[b] or ni != IN[b]:
                    OUT[b] = o
                    IN[b] = ni
                    ch = True
    else:
        ch = True
        while ch:
            ch = False
            iters += 1
            for b in range(n):
                if mode == "REACH":
                    ni = 0
                    if b != 0:
                        for p in pred[b]:
                            ni |= OUT[p]
                else:
                    if b == 0:
                        ni = 0
                    elif not pred[b]:
                        ni = ALL
                    else:
                        ni = ALL
                        for p in pred[b]:
                            ni &= OUT[p]
                no = (GEN[b] | (ni & (~KILL[b]))) & ALL
                if ni != IN[b] or no != OUT[b]:
                    IN[b] = ni
                    OUT[b] = no
                    ch = True

    out = []
    for b in range(n):
        in_names = [names[i] for i in range(U) if (IN[b] >> i) & 1]
        out_names = [names[i] for i in range(U) if (OUT[b] >> i) & 1]
        out.append(f"B{b} IN={{{','.join(in_names)}}} OUT={{{','.join(out_names)}}}")
    out.append(f"ITERATIONS {iters}")
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
