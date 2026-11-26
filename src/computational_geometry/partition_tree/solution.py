"""partition_tree: Berg 16.1 simplicial partition + SELECTINHALFPLANE.

Build: singletons become leaves; otherwise kd-style bisection into at
most 4 classes (by x, then by y), each class of size >= 2 getting a
box-derived triangle. Query: count points in the closed half-plane
a*x+b*y+c >= 0, selecting fully covered children and recursing into
intersected ones.
"""

import sys

sys.setrecursionlimit(100000)


def _bisect(pts, idx, ax):
    if len(idx) <= 1:
        return [idx]
    idx = sorted(idx, key=lambda i: (pts[i][ax], pts[i][1 - ax], i))
    mid = (len(idx) + 1) // 2
    return [idx[:mid], idx[mid:]]


def _triangle(pts, idx):
    xs = [pts[i][0] for i in idx]
    ys = [pts[i][1] for i in idx]
    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)
    w = xmax - xmin
    h = ymax - ymin
    return [(xmin, ymin), (xmax + h + 1, ymin), (xmin, ymax + w + 1)]


def _build(pts, idx, tree):
    if len(idx) == 1:
        tree.append({"leaf": True, "pt": pts[idx[0]], "count": 1})
        return len(tree) - 1
    classes = []
    for half in _bisect(pts, idx, 0):
        classes.extend(_bisect(pts, half, 1))
    kids = []
    for c in classes:
        v = _build(pts, c, tree)
        tri = None if tree[v]["leaf"] else _triangle(pts, c)
        kids.append((tri, v))
    tree.append({"leaf": False, "kids": kids, "count": len(idx)})
    return len(tree) - 1


def _select(tree, v, a, b, c):
    node = tree[v]
    if node["leaf"]:
        x, y = node["pt"]
        return 1 if a * x + b * y + c >= 0 else 0
    total = 0
    for tri, u in node["kids"]:
        if tri is None:
            total += _select(tree, u, a, b, c)
            continue
        vals = [a * x + b * y + c for x, y in tri]
        if all(vv >= 0 for vv in vals):
            total += tree[u]["count"]
        elif any(vv >= 0 for vv in vals):
            total += _select(tree, u, a, b, c)
    return total


def main():
    data = list(map(int, sys.stdin.read().split()))
    if not data:
        return
    n = data[0]
    pts = [(data[1 + 2 * i], data[2 + 2 * i]) for i in range(n)]
    pos = 1 + 2 * n
    q = data[pos] if pos < len(data) else 0
    pos += 1
    tree = []
    root = _build(pts, list(range(n)), tree) if n else -1
    out_lines = []
    for _ in range(q):
        a, b, c = data[pos], data[pos + 1], data[pos + 2]
        pos += 3
        out_lines.append(str(_select(tree, root, a, b, c) if n else 0))
    sys.stdout.write("\n".join(out_lines))


if __name__ == "__main__":
    main()
