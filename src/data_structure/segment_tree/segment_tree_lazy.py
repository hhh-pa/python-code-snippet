import sys

sys.setrecursionlimit(200000)


def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    q = int(tokens[1])
    idx = 2
    arr = [int(tokens[idx + i]) for i in range(n)]
    idx += n

    tree = [0] * (4 * n)
    lazy = [0] * (4 * n)

    def build(node, l, r):
        if l == r:
            tree[node] = arr[l]
            return
        mid = (l + r) // 2
        lc = 2 * node
        rc = lc + 1
        build(lc, l, mid)
        build(rc, mid + 1, r)
        tree[node] = tree[lc] + tree[rc]

    if n > 0:
        build(1, 0, n - 1)

    def push_down(node, l, r):
        val = lazy[node]
        if val != 0:
            mid = (l + r) // 2
            lc = 2 * node
            rc = lc + 1

            tree[lc] += val * (mid - l + 1)
            lazy[lc] += val

            tree[rc] += val * (r - mid)
            lazy[rc] += val

            lazy[node] = 0

    def update(node, l, r, ql, qr, val):
        if ql <= l and r <= qr:
            tree[node] += val * (r - l + 1)
            lazy[node] += val
            return
        push_down(node, l, r)
        mid = (l + r) // 2
        lc = 2 * node
        rc = lc + 1
        if ql <= mid:
            update(lc, l, mid, ql, qr, val)
        if qr > mid:
            update(rc, mid + 1, r, ql, qr, val)
        tree[node] = tree[lc] + tree[rc]

    def query(node, l, r, ql, qr):
        if ql <= l and r <= qr:
            return tree[node]
        push_down(node, l, r)
        mid = (l + r) // 2
        s = 0
        if ql <= mid:
            s += query(2 * node, l, mid, ql, qr)
        if qr > mid:
            s += query(2 * node + 1, mid + 1, r, ql, qr)
        return s

    out = []
    for _ in range(q):
        op = tokens[idx]
        if op == "UPDATE":
            l = int(tokens[idx + 1])
            r = int(tokens[idx + 2])
            val = int(tokens[idx + 3])
            idx += 4
            update(1, 0, n - 1, l - 1, r - 1, val)
        elif op == "QUERY":
            l = int(tokens[idx + 1])
            r = int(tokens[idx + 2])
            idx += 3
            out.append(str(query(1, 0, n - 1, l - 1, r - 1)))

    sys.stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
