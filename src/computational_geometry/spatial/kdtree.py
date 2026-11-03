import sys
import math

sys.setrecursionlimit(200000)

class KDNode:
    def __init__(self, pt, left=-1, right=-1, axis=0):
        self.pt = pt
        self.left = left
        self.right = right
        self.axis = axis

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    idx = 1
    pts = []
    for _ in range(n):
        pts.append((float(tokens[idx]), float(tokens[idx + 1])))
        idx += 2

    tree = []

    def build(l, r, depth):
        if l >= r:
            return -1
        axis = depth % 2
        mid = l + (r - l) // 2

        sub = pts[l:r]
        if axis == 0:
            sub.sort(key=lambda p: p[0])
        else:
            sub.sort(key=lambda p: p[1])
        pts[l:r] = sub

        node_idx = len(tree)
        tree.append(KDNode(pts[mid], axis=axis))

        left_child = build(l, mid, depth + 1)
        right_child = build(mid + 1, r, depth + 1)

        tree[node_idx].left = left_child
        tree[node_idx].right = right_child
        return node_idx

    build(0, len(pts), 0)

    def range_query(u, xmin, ymin, xmax, ymax):
        if u == -1:
            return 0
        node = tree[u]
        count = 1 if (xmin <= node.pt[0] <= xmax and ymin <= node.pt[1] <= ymax) else 0

        if node.axis == 0:
            if xmin <= node.pt[0]:
                count += range_query(node.left, xmin, ymin, xmax, ymax)
            if xmax >= node.pt[0]:
                count += range_query(node.right, xmin, ymin, xmax, ymax)
        else:
            if ymin <= node.pt[1]:
                count += range_query(node.left, xmin, ymin, xmax, ymax)
            if ymax >= node.pt[1]:
                count += range_query(node.right, xmin, ymin, xmax, ymax)
        return count

    best_dist_sq = 1e18
    best_pt = (0.0, 0.0)

    def nearest_neighbor(u, qx, qy):
        nonlocal best_dist_sq, best_pt
        if u == -1:
            return
        node = tree[u]
        d_sq = (node.pt[0] - qx) ** 2 + (node.pt[1] - qy) ** 2
        if d_sq < best_dist_sq:
            best_dist_sq = d_sq
            best_pt = node.pt

        axis_diff = (qx - node.pt[0]) if node.axis == 0 else (qy - node.pt[1])
        first = node.left if axis_diff <= 0 else node.right
        second = node.right if axis_diff <= 0 else node.left

        nearest_neighbor(first, qx, qy)
        if axis_diff * axis_diff < best_dist_sq:
            nearest_neighbor(second, qx, qy)

    if idx >= len(tokens):
        return
    num_queries = int(tokens[idx])
    idx += 1

    out = []
    for _ in range(num_queries):
        if idx >= len(tokens):
            break
        qtype = tokens[idx]
        idx += 1
        if qtype == "RANGE":
            x1 = float(tokens[idx])
            y1 = float(tokens[idx + 1])
            x2 = float(tokens[idx + 2])
            y2 = float(tokens[idx + 3])
            idx += 4
            out.append(str(range_query(0, x1, y1, x2, y2)))
        elif qtype == "NN":
            qx = float(tokens[idx])
            qy = float(tokens[idx + 1])
            idx += 2
            best_dist_sq = 1e18
            best_pt = (0.0, 0.0)
            nearest_neighbor(0, qx, qy)
            out.append(f"{best_pt[0]:.2f} {best_pt[1]:.2f} {math.sqrt(best_dist_sq):.2f}")

    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
