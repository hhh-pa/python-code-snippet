import sys

def orient3(a, b, c, d):
    abx = b[0] - a[0]
    aby = b[1] - a[1]
    abz = b[2] - a[2]
    acx = c[0] - a[0]
    acy = c[1] - a[1]
    acz = c[2] - a[2]
    adx = d[0] - a[0]
    ady = d[1] - a[1]
    adz = d[2] - a[2]
    cx = aby * acz - abz * acy
    cy = abz * acx - abx * acz
    cz = abx * acy - aby * acx
    return cx * adx + cy * ady + cz * adz

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    idx = 1
    pts = []
    for _ in range(n):
        pts.append((int(tokens[idx]), int(tokens[idx + 1]), int(tokens[idx + 2])))
        idx += 3

    ord_arr = list(range(n))
    st = 199
    MASK = 0xFFFFFFFFFFFFFFFF
    MULT = 6364136223846793005
    ADD = 1442695040888963407
    for i in range(n - 1, 0, -1):
        st = (st * MULT + ADD) & MASK
        j = (st >> 33) % (i + 1)
        ord_arr[i], ord_arr[j] = ord_arr[j], ord_arr[i]

    p0 = ord_arr[0]
    p1 = ord_arr[1]
    p2 = ord_arr[2]
    p3 = ord_arr[3]

    t = [p0, p1, p2, p3]
    facets = []
    for skip in range(4):
        v = [t[i] for i in range(4) if i != skip]
        if orient3(pts[v[0]], pts[v[1]], pts[v[2]], pts[t[skip]]) > 0:
            v[1], v[2] = v[2], v[1]
        facets.append((v[0], v[1], v[2]))

    def orientInner(a, b, c):
        return (orient3(pts[a], pts[b], pts[c], pts[p0]) +
                orient3(pts[a], pts[b], pts[c], pts[p1]) +
                orient3(pts[a], pts[b], pts[c], pts[p2]) +
                orient3(pts[a], pts[b], pts[c], pts[p3]))

    for oi in range(4, n):
        p = ord_arr[oi]
        vis = []
        for f, fc in enumerate(facets):
            if orient3(pts[fc[0]], pts[fc[1]], pts[fc[2]], pts[p]) > 0:
                vis.append(f)
        if not vis:
            continue

        vis_set = set(vis)
        ecount = {}
        for f in vis:
            fc = facets[f]
            for e in range(3):
                u = fc[e]
                v = fc[(e + 1) % 3]
                if u > v:
                    u, v = v, u
                ecount[(u, v)] = ecount.get((u, v), 0) + 1

        nf = [facets[f] for f in range(len(facets)) if f not in vis_set]
        for edge in sorted(ecount.keys()):
            if ecount[edge] == 1:
                u, v = edge
                a, b = u, v
                if orientInner(a, b, p) > 0:
                    a, b = b, a
                nf.append((a, b, p))
        facets = nf

    out = []
    for fc in facets:
        v = sorted(fc)
        out.append(tuple(v))
    out.sort()

    res = [str(len(out))]
    for tt in out:
        res.append(f"{tt[0]} {tt[1]} {tt[2]}")
    sys.stdout.write("\n".join(res) + "\n")

if __name__ == "__main__":
    main()
