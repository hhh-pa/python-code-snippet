import sys

def cross(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    s = int(tokens[0])
    idx = 1
    segs = []
    for _ in range(s):
        x1 = int(tokens[idx])
        y1 = int(tokens[idx + 1])
        x2 = int(tokens[idx + 2])
        y2 = int(tokens[idx + 3])
        idx += 4
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
        segs.append(((x1, y1), (x2, y2)))

    ord_arr = list(range(s))
    st = 192
    MASK = 0xFFFFFFFFFFFFFFFF
    MULT = 6364136223846793005
    ADD = 1442695040888963407
    for i in range(s - 1, 0, -1):
        st = (st * MULT + ADD) & MASK
        j = (st >> 33) % (i + 1)
        ord_arr[i], ord_arr[j] = ord_arr[j], ord_arr[i]

    traps = []
    nodes = []

    X0 = int(4e12)
    X1 = -int(4e12)
    for sg in segs:
        X0 = min(X0, min(sg[0][0], sg[1][0]) - 1)
        X1 = max(X1, max(sg[0][0], sg[1][0]) + 1)

    traps.append({'top': -1, 'bot': -1, 'lp': (X0, 0), 'rp': (X1, 0)})
    nodes.append({'kind': 0, 'trap': 0, 'p': (0, 0), 'seg': -1, 'left': -1, 'right': -1})

    def above(si, p):
        a = segs[si][0]
        b = segs[si][1]
        if a[0] == b[0]:
            return False
        return cross(a, b, p) > 0

    for oi in range(s):
        si = ord_arr[oi]
        p = segs[si][0]
        q = segs[si][1]

        leaves = [ni for ni in range(len(nodes)) if nodes[ni]['kind'] == 0]
        hits = []
        for ni in leaves:
            T = traps[nodes[ni]['trap']]
            if T['rp'][0] <= p[0] or T['lp'][0] >= q[0]:
                continue
            xm = (max(T['lp'][0], p[0]) + min(T['rp'][0], q[0])) / 2.0
            t = (xm - p[0]) / (q[0] - p[0])
            ys = p[1] + t * (q[1] - p[1])
            yt = 4e18
            yb = -4e18
            if T['top'] >= 0:
                sg = segs[T['top']]
                tt = (xm - sg[0][0]) / (sg[1][0] - sg[0][0])
                yt = sg[0][1] + tt * (sg[1][1] - sg[0][1])
            if T['bot'] >= 0:
                sg = segs[T['bot']]
                tt = (xm - sg[0][0]) / (sg[1][0] - sg[0][0])
                yb = sg[0][1] + tt * (sg[1][1] - sg[0][1])
            if yb < ys < yt:
                hits.append(ni)

        hits.sort(key=lambda ni: traps[nodes[ni]['trap']]['lp'][0])
        nh = len(hits)
        for hi in range(nh):
            ni = hits[hi]
            T = traps[nodes[ni]['trap']]
            first = (hi == 0)
            last = (hi == nh - 1)
            top = T['top']
            bot = T['bot']

            ulp = p if T['lp'][0] < p[0] else T['lp']
            urp = q if T['rp'][0] > q[0] else T['rp']

            upT = len(traps)
            traps.append({'top': top, 'bot': si, 'lp': ulp, 'rp': urp})
            loT = len(traps)
            traps.append({'top': si, 'bot': bot, 'lp': ulp, 'rp': urp})

            upN = len(nodes)
            nodes.append({'kind': 0, 'trap': upT, 'p': (0, 0), 'seg': -1, 'left': -1, 'right': -1})
            loN = len(nodes)
            nodes.append({'kind': 0, 'trap': loT, 'p': (0, 0), 'seg': -1, 'left': -1, 'right': -1})

            yN = len(nodes)
            nodes.append({'kind': 2, 'trap': -1, 'p': (0, 0), 'seg': si, 'left': upN, 'right': loN})
            rep = yN

            if first and T['lp'][0] < p[0]:
                lT = len(traps)
                traps.append({'top': top, 'bot': bot, 'lp': T['lp'], 'rp': p})
                lN = len(nodes)
                nodes.append({'kind': 0, 'trap': lT, 'p': (0, 0), 'seg': -1, 'left': -1, 'right': -1})
                xN = len(nodes)
                nodes.append({'kind': 1, 'trap': -1, 'p': p, 'seg': -1, 'left': lN, 'right': rep})
                rep = xN

            if last and T['rp'][0] > q[0]:
                rT = len(traps)
                traps.append({'top': top, 'bot': bot, 'lp': q, 'rp': T['rp']})
                rN = len(nodes)
                nodes.append({'kind': 0, 'trap': rT, 'p': (0, 0), 'seg': -1, 'left': -1, 'right': -1})
                xN = len(nodes)
                nodes.append({'kind': 1, 'trap': -1, 'p': q, 'seg': -1, 'left': rep, 'right': rN})
                rep = xN

            nodes[ni]['kind'] = 3
            nodes[ni]['left'] = rep

    def query(qq):
        ni = 0
        while True:
            nd = nodes[ni]
            if nd['kind'] == 0:
                return nd['trap']
            if nd['kind'] == 3:
                ni = nd['left']
                continue
            if nd['kind'] == 1:
                ni = nd['left'] if qq[0] < nd['p'][0] else nd['right']
                continue
            ni = nd['left'] if above(nd['seg'], qq) else nd['right']

    if idx >= len(tokens):
        return
    qq = int(tokens[idx])
    idx += 1

    out = []
    for _ in range(qq):
        if idx >= len(tokens):
            break
        gx = int(tokens[idx])
        gy = int(tokens[idx + 1])
        idx += 2
        trap_idx = query((gx, gy))
        T = traps[trap_idx]
        out.append(f"{T['top']} {T['bot']}")

    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
