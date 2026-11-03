import sys


def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    q = int(tokens[1])
    idx = 2

    # Iterative Segment Tree
    size = 1
    while size < n:
        size *= 2
    INF = float("inf")
    tree = [INF] * (2 * size)

    for i in range(n):
        tree[size + i] = int(tokens[idx + i])
    idx += n

    for i in range(size - 1, 0, -1):
        tree[i] = min(tree[2 * i], tree[2 * i + 1])

    out = []
    for _ in range(q):
        op = tokens[idx]
        x = int(tokens[idx + 1])
        y = int(tokens[idx + 2])
        idx += 3
        if op == "q":
            l = x - 1 + size
            r = y + size  # exclusive: [l, r)
            res = INF
            while l < r:
                if l & 1:
                    if tree[l] < res:
                        res = tree[l]
                    l += 1
                if r & 1:
                    r -= 1
                    if tree[r] < res:
                        res = tree[r]
                l //= 2
                r //= 2
            out.append(str(res))
        elif op == "u":
            pos = x - 1 + size
            tree[pos] = y
            pos //= 2
            while pos > 0:
                tree[pos] = min(tree[2 * pos], tree[2 * pos + 1])
                pos //= 2

    sys.stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
