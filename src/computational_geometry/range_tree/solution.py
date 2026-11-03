import sys
import bisect

sys.setrecursionlimit(200000)

class Node:
    def __init__(self, l, r, mid=-1, left=-1, right=-1):
        self.l = l
        self.r = r
        self.mid = mid
        self.left = left
        self.right = right
        self.yvec = []
        self.fcl = []
        self.fcr = []

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    idx = 1
    pts = []
    for _ in range(n):
        pts.append((int(tokens[idx]), int(tokens[idx + 1])))
        idx += 2

    xs = sorted(range(n), key=lambda i: (pts[i][0], pts[i][1]))
    tree = []

    def build(l, r):
        node_id = len(tree)
        tree.append(Node(l, r))

        yv = xs[l:r]
        yv.sort(key=lambda i: (pts[i][1], pts[i][0]))
        tree[node_id].yvec = yv

        if r - l == 1:
            tree[node_id].mid = l
            tree[node_id].left = -1
            tree[node_id].right = -1
            return node_id

        mid = (l + r) // 2
        tree[node_id].mid = mid
        L = build(l, mid)
        R = build(mid, r)
        tree[node_id].left = L
        tree[node_id].right = R

        ys = len(yv)
        fcl = [0] * (ys + 1)
        fcr = [0] * (ys + 1)
        ly = tree[L].yvec
        ry = tree[R].yvec

        ly_y = [pts[i][1] for i in ly]
        ry_y = [pts[i][1] for i in ry]

        INF = int(4e18)
        for i in range(ys + 1):
            yb = pts[yv[i]][1] if i < ys else INF
            fcl[i] = bisect.bisect_left(ly_y, yb)
            fcr[i] = bisect.bisect_left(ry_y, yb)

        tree[node_id].fcl = fcl
        tree[node_id].fcr = fcr
        return node_id

    root = build(0, n)

    if idx >= len(tokens):
        return
    q = int(tokens[idx])
    idx += 1

    INF = int(4e18)
    out = []
    for _ in range(q):
        if idx >= len(tokens):
            break
        x1 = int(tokens[idx])
        y1 = int(tokens[idx + 1])
        x2 = int(tokens[idx + 2])
        y2 = int(tokens[idx + 3])
        idx += 4

        found = []
        v = root
        while tree[v].left != -1:
            key = pts[xs[tree[v].mid]][0]
            if x2 < key:
                v = tree[v].left
            elif x1 > key:
                v = tree[v].right
            else:
                break

        if tree[v].left == -1:
            pid = tree[v].yvec[0]
            if x1 <= pts[pid][0] <= x2 and y1 <= pts[pid][1] <= y2:
                found.append(pid)
        else:
            syv = tree[v].yvec
            syv_y = [pts[i][1] for i in syv]
            lo0 = bisect.bisect_left(syv_y, y1)
            y2p = INF if y2 == INF - 1 else y2 + 1
            hi0 = bisect.bisect_left(syv_y, y2p)

            lv = tree[v].left
            rv = tree[v].right
            llo = tree[v].fcl[lo0]
            lhi = tree[v].fcl[hi0]
            rlo = tree[v].fcr[lo0]
            rhi = tree[v].fcr[hi0]

            # left walk
            u = lv
            a = llo
            b = lhi
            while True:
                if tree[u].left == -1:
                    if b > a:
                        pid = tree[u].yvec[0]
                        if x1 <= pts[pid][0]:
                            found.append(pid)
                    break
                key = pts[xs[tree[u].mid]][0]
                if x1 <= key:
                    c = tree[u].right
                    found.extend(tree[c].yvec[tree[u].fcr[a]:tree[u].fcr[b]])
                    na = tree[u].fcl[a]
                    nb = tree[u].fcl[b]
                    u = tree[u].left
                    a = na
                    b = nb
                else:
                    na = tree[u].fcr[a]
                    nb = tree[u].fcr[b]
                    u = tree[u].right
                    a = na
                    b = nb

            # right walk
            u = rv
            a = rlo
            b = rhi
            while True:
                if tree[u].left == -1:
                    if b > a:
                        pid = tree[u].yvec[0]
                        if pts[pid][0] <= x2:
                            found.append(pid)
                    break
                key = pts[xs[tree[u].mid]][0]
                if key <= x2:
                    c = tree[u].left
                    found.extend(tree[c].yvec[tree[u].fcl[a]:tree[u].fcl[b]])
                    na = tree[u].fcr[a]
                    nb = tree[u].fcr[b]
                    u = tree[u].right
                    a = na
                    b = nb
                else:
                    na = tree[u].fcl[a]
                    nb = tree[u].fcl[b]
                    u = tree[u].left
                    a = na
                    b = nb

        found.sort(key=lambda pid: (pts[pid][0], pts[pid][1]))
        out.append(str(len(found)))
        if found:
            out.append(" ".join(f"{pts[pid][0]},{pts[pid][1]}" for pid in found))

    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
