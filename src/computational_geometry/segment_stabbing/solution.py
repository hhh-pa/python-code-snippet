import sys
import bisect

sys.setrecursionlimit(200000)

class SegmentTree:
    def __init__(self, n):
        self.n = n
        self.t = [[] for _ in range(4 * n)]

    def insert(self, v, l, r, ql, qr, idx):
        if ql >= r or qr <= l:
            return
        if ql <= l and r <= qr:
            self.t[v].append(idx)
            return
        m = (l + r) // 2
        self.insert(2 * v, l, m, ql, qr, idx)
        self.insert(2 * v + 1, m, r, ql, qr, idx)

    def query(self, v, l, r, i, out):
        out.extend(self.t[v])
        if r - l == 1:
            return
        m = (l + r) // 2
        if i < m:
            self.query(2 * v, l, m, i, out)
        else:
            self.query(2 * v + 1, m, r, i, out)

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    idx = 1
    L = []
    R = []
    u_set = set()
    for _ in range(n):
        l_val = int(tokens[idx])
        r_val = int(tokens[idx + 1])
        idx += 2
        L.append(l_val)
        R.append(r_val)
        u_set.add(l_val)
        u_set.add(r_val)

    u = sorted(u_set)
    m = len(u)
    st = SegmentTree(2 * m + 1)
    for i in range(n):
        li = bisect.bisect_left(u, L[i])
        ri = bisect.bisect_left(u, R[i])
        st.insert(1, 0, 2 * m + 1, 2 * li + 1, 2 * ri + 2, i)

    if idx >= len(tokens):
        return
    q = int(tokens[idx])
    idx += 1

    out = []
    for _ in range(q):
        if idx >= len(tokens):
            break
        x = int(tokens[idx])
        idx += 1
        if x < u[0]:
            ei = 0
        elif x > u[-1]:
            ei = 2 * m
        else:
            k = bisect.bisect_right(u, x) - 1
            ei = 2 * k + 1 if u[k] == x else 2 * k + 2

        found = []
        st.query(1, 0, 2 * m + 1, ei, found)
        found.sort()
        out.append(str(len(found)))
        if found:
            out.append(" ".join(str(f) for f in found))

    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
