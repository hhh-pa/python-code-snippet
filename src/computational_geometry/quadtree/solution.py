import sys

sys.setrecursionlimit(200000)

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    S = int(tokens[1])
    cap = int(tokens[2])
    idx = 3

    px = []
    py = []
    for _ in range(n):
        px.append(int(tokens[idx]))
        py.append(int(tokens[idx + 1]))
        idx += 2

    nodes = []

    def rec(ids, x, y, s):
        if len(ids) <= cap or s == 1:
            node_idx = len(nodes)
            nodes.append({
                'leaf': True,
                'x': x,
                'y': y,
                's': s,
                'c': [-1, -1, -1, -1],
                'ids': ids
            })
            return node_idx

        h = s // 2
        q = [[], [], [], []]
        for i in ids:
            k = (0 if px[i] < x + h else 1) + (0 if py[i] < y + h else 2)
            q[k].append(i)

        node_idx = len(nodes)
        node = {
            'leaf': False,
            'x': x,
            'y': y,
            's': s,
            'c': [-1, -1, -1, -1],
            'ids': []
        }
        nodes.append(node)

        qx = [x, x + h, x, x + h]
        qy = [y, y, y + h, y + h]
        qs = [h, s - h, h, s - h]

        for k in range(4):
            node['c'][k] = -1 if not q[k] else rec(q[k], qx[k], qy[k], qs[k])
        return node_idx

    rec(list(range(n)), 0, 0, S)

    out = [str(len(nodes))]
    for nd in nodes:
        if not nd['leaf']:
            out.append(f"I {nd['x']} {nd['y']} {nd['s']} {nd['c'][0]} {nd['c'][1]} {nd['c'][2]} {nd['c'][3]}")
        else:
            ids_str = (" " + " ".join(str(i) for i in nd['ids'])) if nd['ids'] else ""
            out.append(f"L {nd['x']} {nd['y']} {nd['s']} {len(nd['ids'])}{ids_str}")

    def count_pts(ni, x1, y1, x2, y2):
        nd = nodes[ni]
        if nd['leaf']:
            c = 0
            for i in nd['ids']:
                if x1 <= px[i] <= x2 and y1 <= py[i] <= y2:
                    c += 1
            return c
        h = nd['s'] // 2
        rx = [nd['x'], nd['x'] + h, nd['x'], nd['x'] + h]
        ry = [nd['y'], nd['y'], nd['y'] + h, nd['y'] + h]
        rs = [h, nd['s'] - h, h, nd['s'] - h]
        tot = 0
        for k in range(4):
            ck = nd['c'][k]
            if ck == -1:
                continue
            if rx[k] > x2 or rx[k] + rs[k] - 1 < x1 or ry[k] > y2 or ry[k] + rs[k] - 1 < y1:
                continue
            tot += count_pts(ck, x1, y1, x2, y2)
        return tot

    if idx < len(tokens):
        qq = int(tokens[idx])
        idx += 1
        for _ in range(qq):
            if idx >= len(tokens):
                break
            x1 = int(tokens[idx])
            y1 = int(tokens[idx + 1])
            x2 = int(tokens[idx + 2])
            y2 = int(tokens[idx + 3])
            idx += 4
            out.append(str(count_pts(0, x1, y1, x2, y2)))

    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
