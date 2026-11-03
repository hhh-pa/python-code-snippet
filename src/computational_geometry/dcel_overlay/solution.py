import sys
from functools import cmp_to_key

sys.setrecursionlimit(200000)

def cross(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

def proper(a, b, c, d):
    d1 = cross(c, d, a)
    d2 = cross(c, d, b)
    d3 = cross(a, b, c)
    d4 = cross(a, b, d)
    return (((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and
            ((d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0)))

def tparam(a, b, c, d):
    rx = b[0] - a[0]
    ry = b[1] - a[1]
    qx = d[0] - c[0]
    qy = d[1] - c[1]
    num = (c[0] - a[0]) * qy - (c[1] - a[1]) * qx
    den = rx * qy - ry * qx
    if den < 0:
        den = -den
        num = -num
    return (num, den)

def flt(a, b):
    return a[0] * b[1] < b[0] * a[1]

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    idx = 0
    n1 = int(tokens[idx])
    idx += 1
    p1 = []
    for _ in range(n1):
        p1.append((int(tokens[idx]), int(tokens[idx + 1])))
        idx += 2

    n2 = int(tokens[idx])
    idx += 1
    p2 = []
    for _ in range(n2):
        p2.append((int(tokens[idx]), int(tokens[idx + 1])))
        idx += 2

    xs = []
    for i in range(n1):
        for j in range(n2):
            a = p1[i]
            b = p1[(i + 1) % n1]
            c = p2[j]
            d = p2[(j + 1) % n2]
            if proper(a, b, c, d):
                xs.append({
                    'e1': i,
                    'e2': j,
                    't1': tparam(a, b, c, d),
                    't2': tparam(c, d, a, b)
                })

    X = len(xs)
    V = n1 + n2 + X

    def xvid(k):
        return n1 + n2 + k

    on1 = [[] for _ in range(n1)]
    on2 = [[] for _ in range(n2)]
    for k in range(X):
        on1[xs[k]['e1']].append(k)
        on2[xs[k]['e2']].append(k)

    for i in range(n1):
        on1[i].sort(key=cmp_to_key(lambda k, l: -1 if flt(xs[k]['t1'], xs[l]['t1']) else 1))
    for j in range(n2):
        on2[j].sort(key=cmp_to_key(lambda k, l: -1 if flt(xs[k]['t2'], xs[l]['t2']) else 1))

    ues = []
    for i in range(n1):
        prev = i
        for k in on1[i]:
            ues.append((prev, xvid(k), 1, i))
            prev = xvid(k)
        ues.append((prev, (i + 1) % n1, 1, i))

    for j in range(n2):
        prev = n1 + j
        for k in on2[j]:
            ues.append((prev, xvid(k), 2, j))
            prev = xvid(k)
        ues.append((prev, n1 + (j + 1) % n2, 2, j))

    E = len(ues)
    hes = []
    for ue_u, ue_v, ue_poly, ue_e in ues:
        k = len(hes)
        hes.append({'from': ue_u, 'to': ue_v, 'twin': k + 1, 'poly': ue_poly, 'e': ue_e})
        hes.append({'from': ue_v, 'to': ue_u, 'twin': k, 'poly': ue_poly, 'e': ue_e})

    H = len(hes)
    out = [[] for _ in range(V)]
    for h in range(H):
        out[hes[h]['from']].append(h)

    ccw = [[] for _ in range(V)]
    for v in range(n1 + n2):
        hs = list(out[v])

        def dirOf(h):
            poly = hes[h]['poly']
            e = hes[h]['e']
            if poly == 1:
                a = p1[e]
                b = p1[(e + 1) % n1]
                vv = p1[v]
                w = b if (vv[0] == a[0] and vv[1] == a[1]) else a
                return (w[0] - vv[0], w[1] - vv[1])
            vv = v - n1
            a = p2[e]
            b = p2[(e + 1) % n2]
            cur = p2[vv]
            w = b if (cur[0] == a[0] and cur[1] == a[1]) else a
            return (w[0] - cur[0], w[1] - cur[1])

        def cmp_h(h1, h2):
            d1 = dirOf(h1)
            d2 = dirOf(h2)
            q1 = 0 if (d1[1] > 0 or (d1[1] == 0 and d1[0] > 0)) else 1
            q2 = 0 if (d2[1] > 0 or (d2[1] == 0 and d2[0] > 0)) else 1
            if q1 != q2:
                return -1 if q1 < q2 else 1
            cp = d1[0] * d2[1] - d1[1] * d2[0]
            if cp > 0:
                return -1
            elif cp < 0:
                return 1
            return 0

        hs.sort(key=cmp_to_key(cmp_h))
        ccw[v] = hs

    for k in range(X):
        v = xvid(k)
        e1 = xs[k]['e1']
        e2 = xs[k]['e2']
        a = p1[e1]
        b = p1[(e1 + 1) % n1]
        c = p2[e2]
        ch1 = [e1] + [xvid(kk) for kk in on1[e1]] + [(e1 + 1) % n1]
        ch2 = [n1 + e2] + [xvid(kk) for kk in on2[e2]] + [n1 + (e2 + 1) % n2]
        i1 = ch1.index(v)
        i2 = ch2.index(v)
        toA = ch1[i1 - 1]
        toB = ch1[i1 + 1]
        toC = ch2[i2 - 1]
        toD = ch2[i2 + 1]
        hA = hB = hC = hD = -1
        for h in out[v]:
            t = hes[h]['to']
            if t == toA:
                hA = h
            elif t == toB:
                hB = h
            elif t == toC:
                hC = h
            else:
                hD = h
        if cross(a, b, c) > 0:
            ccw[v] = [hB, hC, hA, hD]
        else:
            ccw[v] = [hB, hD, hA, hC]

    pos = [-1] * H
    for v in range(V):
        for i, h in enumerate(ccw[v]):
            pos[h] = i

    nxt = [-1] * H
    for h in range(H):
        w = hes[h]['to']
        t = hes[h]['twin']
        k = len(ccw[w])
        p = pos[t]
        nxt[h] = ccw[w][(p - 1 + k) % k]

    vis = [False] * H
    cycles = 0
    for h in range(H):
        if not vis[h]:
            cycles += 1
            curr = h
            while not vis[curr]:
                vis[curr] = True
                curr = nxt[curr]

    par = list(range(V))
    def find(x):
        if par[x] == x:
            return x
        par[x] = find(par[x])
        return par[x]

    for ue in ues:
        ru = find(ue[0])
        rv = find(ue[1])
        if ru != rv:
            par[ru] = rv

    C = sum(1 for v in range(V) if find(v) == v)
    sys.stdout.write(f"{V} {E} {cycles - C + 1}\n")

if __name__ == "__main__":
    main()
