import bisect
import sys


def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    q = int(tokens[0])
    idx = 1
    is_ext = []
    val = []
    for _ in range(q):
        op = int(tokens[idx])
        idx += 1
        if op == 1:
            val.append(int(tokens[idx]))
            idx += 1
            is_ext.append(0)
        else:
            val.append(0)
            is_ext.append(1)

    E = [i for i in range(q) if is_ext[i]]
    m = len(E)
    ins = [(val[i], i) for i in range(q) if not is_ext[i]]
    ins.sort()

    p = list(range(m + 1))

    def find(x):
        root = x
        while p[root] != root:
            root = p[root]
        curr = x
        while curr != root:
            nxt = p[curr]
            p[curr] = root
            curr = nxt
        return root

    def occupy(x):
        p[x] = find(x + 1)

    ans = [0] * m
    has = [False] * m

    for v, t in ins:
        j0 = bisect.bisect_right(E, t)
        j = find(j0)
        if j < m:
            ans[j] = v
            has[j] = True
            occupy(j)

    out = []
    for j in range(m):
        if has[j]:
            out.append(str(ans[j]))
        else:
            out.append("EMPTY")

    sys.stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
