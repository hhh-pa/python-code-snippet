import sys

sys.setrecursionlimit(200000)

class Node:
    def __init__(self, p, xmin, xmax, left=-1, right=-1):
        self.p = p
        self.xmin = xmin
        self.xmax = xmax
        self.left = left
        self.right = right

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

    def build(ids):
        best = 0
        for i in range(1, len(ids)):
            if pts[ids[i]][1] > pts[ids[best]][1]:
                best = i
        pid = ids[best]
        L = ids[:best]
        R = ids[best + 1:]

        node_id = len(tree)
        tree.append(None)

        l = build(L) if L else -1
        r = build(R) if R else -1

        xmin = pts[pid][0]
        xmax = pts[pid][0]
        if l >= 0:
            xmin = min(xmin, tree[l].xmin)
            xmax = max(xmax, tree[l].xmax)
        if r >= 0:
            xmin = min(xmin, tree[r].xmin)
            xmax = max(xmax, tree[r].xmax)

        tree[node_id] = Node(pts[pid], xmin, xmax, l, r)
        return node_id

    root = build(xs)

    def query(v, x1, x2, y0, out_list):
        if v < 0:
            return
        nd = tree[v]
        if nd.p[1] >= y0 and x1 <= nd.p[0] <= x2:
            out_list.append(nd.p)
        if nd.left >= 0:
            c = tree[nd.left]
            if c.xmax >= x1 and c.xmin <= x2 and c.p[1] >= y0:
                query(nd.left, x1, x2, y0, out_list)
        if nd.right >= 0:
            c = tree[nd.right]
            if c.xmax >= x1 and c.xmin <= x2 and c.p[1] >= y0:
                query(nd.right, x1, x2, y0, out_list)

    if idx >= len(tokens):
        return
    q = int(tokens[idx])
    idx += 1

    out = []
    for _ in range(q):
        if idx >= len(tokens):
            break
        x1 = int(tokens[idx])
        x2 = int(tokens[idx + 1])
        y0 = int(tokens[idx + 2])
        idx += 3

        found = []
        query(root, x1, x2, y0, found)
        found.sort(key=lambda p: (p[0], p[1]))
        out.append(str(len(found)))
        if found:
            out.append(" ".join(f"{p[0]},{p[1]}" for p in found))

    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
