import sys

sys.setrecursionlimit(200000)

def orient(sp, px, py):
    return (sp[2] - sp[0]) * (py - sp[1]) - (sp[3] - sp[1]) * (px - sp[0])

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    idx = 1
    segs = []
    for _ in range(n):
        segs.append((int(tokens[idx]), int(tokens[idx + 1]), int(tokens[idx + 2]), int(tokens[idx + 3])))
        idx += 4

    nodes = []

    def build(ids):
        if not ids:
            return -1
        sp_id = ids[0]
        sp = segs[sp_id]
        at = [sp_id]
        left = []
        right = []
        for i in ids[1:]:
            s = segs[i]
            o1 = orient(sp, s[0], s[1])
            o2 = orient(sp, s[2], s[3])
            if o1 < 0 and o2 < 0:
                left.append(i)
            elif o1 > 0 and o2 > 0:
                right.append(i)
            else:
                at.append(i)
        curr_idx = len(nodes)
        node = {
            'sp': sp,
            'at': at,
            'L': -1,
            'R': -1
        }
        nodes.append(node)
        node['L'] = build(left)
        node['R'] = build(right)
        return curr_idx

    build(list(range(n)))

    out = [str(len(nodes))]
    for nd in nodes:
        sp = nd['sp']
        at_str = " ".join(str(i) for i in nd['at'])
        out.append(f"{sp[0]} {sp[1]} {sp[2]} {sp[3]} {nd['L']} {nd['R']} {len(nd['at'])} {at_str}")

    if idx < len(tokens):
        q = int(tokens[idx])
        idx += 1
        for _ in range(q):
            if idx >= len(tokens):
                break
            x = int(tokens[idx])
            y = int(tokens[idx + 1])
            idx += 2
            node = 0
            path = []
            while True:
                o = orient(nodes[node]['sp'], x, y)
                if o < 0:
                    if nodes[node]['L'] == -1:
                        break
                    path.append("L")
                    node = nodes[node]['L']
                elif o > 0:
                    if nodes[node]['R'] == -1:
                        break
                    path.append("R")
                    node = nodes[node]['R']
                else:
                    path.append("=")
                    break
            path_str = " ".join(path) if path else "-"
            out.append(f"{path_str} {node}")

    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
