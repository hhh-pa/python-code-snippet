import sys

sys.setrecursionlimit(200000)


def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    a = [int(tokens[1 + i]) for i in range(n)]
    left = [-1] * n
    right = [-1] * n
    parent = [-1] * n
    stack = []
    for i in range(n):
        last = -1
        while stack and a[stack[-1]] > a[i]:
            last = stack.pop()
        if stack:
            right[stack[-1]] = i
            parent[i] = stack[-1]
        left[i] = last
        if last != -1:
            parent[last] = i
        stack.append(i)

    root = 0
    for i in range(n):
        if parent[i] == -1:
            root = i
            break

    tour = []
    depth = []
    first = [-1] * n

    def euler(u, d):
        first[u] = len(tour)
        tour.append(u)
        depth.append(d)
        if left[u] != -1:
            euler(left[u], d + 1)
            tour.append(u)
            depth.append(d)
        if right[u] != -1:
            euler(right[u], d + 1)
            tour.append(u)
            depth.append(d)

    euler(root, 0)
    m = len(tour)
    lg = [0] * (m + 1)
    for i in range(2, m + 1):
        lg[i] = lg[i // 2] + 1

    K = lg[m] + 1
    st = [[0] * m for _ in range(K)]
    for i in range(m):
        st[0][i] = i

    for k in range(1, K):
        half = 1 << (k - 1)
        length = 1 << k
        for i in range(m - length + 1):
            x = st[k - 1][i]
            y = st[k - 1][i + half]
            st[k][i] = x if depth[x] <= depth[y] else y

    idx = 1 + n
    q = int(tokens[idx])
    idx += 1
    out = []
    for _ in range(q):
        l = int(tokens[idx])
        r = int(tokens[idx + 1])
        idx += 2
        i = first[l]
        j = first[r]
        if i > j:
            i, j = j, i
        k = lg[j - i + 1]
        x = st[k][i]
        y = st[k][j - (1 << k) + 1]
        best_pos = x if depth[x] <= depth[y] else y
        out.append(str(a[tour[best_pos]]))

    sys.stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
