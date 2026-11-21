"""kd_tree: exact Berg 5.2 BUILDKDTREE + SEARCHKDTREE.

Build: a single point becomes a leaf; otherwise at even depth split
with the vertical line through the median x (ceil(n/2)-th smallest),
points on or left of the line go left and the rest right; at odd
depth likewise with a horizontal line on y. Input points have distinct
x and distinct y coordinates, as assumed in the book.
Query: visit only nodes whose region intersects R; report whole
subtrees whose region is fully contained in R; test leaves.
Regions are tracked in doubled coordinates so every bound is a closed
integer bound: x <= xm becomes x2 <= 2*xm, x > xm becomes
x2 >= 2*xm+1 for integer x.
"""

import sys

sys.setrecursionlimit(100000)


class _Node:
    __slots__ = ("axis", "leaf", "left", "pt", "right", "split")

    def __init__(self, leaf, pt, axis, split, left, right):
        self.leaf = leaf
        self.pt = pt
        self.axis = axis
        self.split = split
        self.left = left
        self.right = right


def _build(pts, idx, depth, tree):
    if len(idx) == 1:
        tree.append(_Node(True, pts[idx[0]], -1, 0, -1, -1))
        return len(tree) - 1
    ax = depth % 2
    idx.sort(key=lambda i: pts[i][ax])
    mid = (len(idx) - 1) // 2
    left = _build(pts, idx[: mid + 1], depth + 1, tree)
    right = _build(pts, idx[mid + 1 :], depth + 1, tree)
    tree.append(_Node(False, None, ax, pts[idx[mid]][ax], left, right))
    return len(tree) - 1


def _report(tree, v, out):
    node = tree[v]
    if node.leaf:
        out.append(node.pt)
        return
    _report(tree, node.left, out)
    _report(tree, node.right, out)


def _visit(tree, v, qxl, qxr, qyl, qyh, xlo, xhi, ylo, yhi, out):
    if (xhi is not None and xhi < qxl) or (xlo is not None and xlo > qxr):
        return
    if (yhi is not None and yhi < qyl) or (ylo is not None and ylo > qyh):
        return
    if (
        xlo is not None
        and xhi is not None
        and ylo is not None
        and yhi is not None
        and qxl <= xlo
        and xhi <= qxr
        and qyl <= ylo
        and yhi <= qyh
    ):
        _report(tree, v, out)
        return
    node = tree[v]
    if node.leaf:
        x, y = node.pt
        if qxl <= 2 * x <= qxr and qyl <= 2 * y <= qyh:
            out.append(node.pt)
        return
    s2 = 2 * node.split
    if node.axis == 0:
        _visit(tree, node.left, qxl, qxr, qyl, qyh, xlo, s2, ylo, yhi, out)
        _visit(tree, node.right, qxl, qxr, qyl, qyh, s2 + 1, xhi, ylo, yhi, out)
    else:
        _visit(tree, node.left, qxl, qxr, qyl, qyh, xlo, xhi, ylo, s2, out)
        _visit(tree, node.right, qxl, qxr, qyl, qyh, xlo, xhi, s2 + 1, yhi, out)


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
    root = _build(pts, list(range(n)), 0, tree) if n else -1
    out_lines = []
    for _ in range(q):
        xl, yl, xr, yh = data[pos], data[pos + 1], data[pos + 2], data[pos + 3]
        pos += 4
        found = []
        if n:
            _visit(
                tree,
                root,
                2 * xl,
                2 * xr,
                2 * yl,
                2 * yh,
                None,
                None,
                None,
                None,
                found,
            )
        found.sort()
        out_lines.append(str(len(found)))
        if found:
            out_lines.append(" ".join(f"{x},{y}" for x, y in found))
    sys.stdout.write("\n".join(out_lines))


if __name__ == "__main__":
    main()
