import sys


class IndexMinPQ:
    def __init__(self, n):
        self.n = n
        self.sz = 0
        self.pq = [0] * (n + 1)
        self.qp = [-1] * n
        self.keys = [0] * n

    def less(self, i, j):
        ki = self.keys[i]
        kj = self.keys[j]
        if ki != kj:
            return ki < kj
        return i < j

    def exch(self, a, b):
        pq = self.pq
        qp = self.qp
        pq[a], pq[b] = pq[b], pq[a]
        qp[pq[a]] = a
        qp[pq[b]] = b

    def swim(self, k):
        pq = self.pq
        while k > 1 and self.less(pq[k], pq[k // 2]):
            self.exch(k, k // 2)
            k //= 2

    def sink(self, k):
        sz = self.sz
        pq = self.pq
        while 2 * k <= sz:
            j = 2 * k
            if j < sz and self.less(pq[j + 1], pq[j]):
                j += 1
            if not self.less(pq[j], pq[k]):
                break
            self.exch(k, j)
            k = j

    def insert(self, i, key):
        if self.qp[i] != -1:
            self.change(i, key)
            return
        self.sz += 1
        pos = self.sz
        self.qp[i] = pos
        self.pq[pos] = i
        self.keys[i] = key
        self.swim(pos)

    def change(self, i, key):
        self.keys[i] = key
        pos = self.qp[i]
        self.swim(pos)
        self.sink(pos)

    def has(self, i):
        return 0 <= i < self.n and self.qp[i] != -1

    def min_index(self):
        return self.pq[1]

    def del_min(self):
        m = self.pq[1]
        self.exch(1, self.sz)
        self.sz -= 1
        self.sink(1)
        self.qp[m] = -1
        return m

    def erase(self, i):
        k = self.qp[i]
        self.exch(k, self.sz)
        self.sz -= 1
        self.swim(k)
        self.sink(k)
        self.qp[i] = -1


def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    q = int(tokens[1])
    idx = 2
    pq = IndexMinPQ(n)
    out = []
    for _ in range(q):
        op = int(tokens[idx])
        idx += 1
        if op == 1:
            i = int(tokens[idx])
            k = int(tokens[idx + 1])
            idx += 2
            if 0 <= i < n:
                pq.insert(i, k)
        elif op == 2:
            if pq.sz == 0:
                out.append("EMPTY")
            else:
                out.append(str(pq.min_index()))
        elif op == 3:
            if pq.sz == 0:
                out.append("EMPTY")
            else:
                out.append(str(pq.del_min()))
        elif op == 4:
            i = int(tokens[idx])
            idx += 1
            if pq.has(i):
                pq.erase(i)
                out.append("OK")
            else:
                out.append("NONE")
        elif op == 5:
            i = int(tokens[idx])
            idx += 1
            if pq.has(i):
                out.append(str(pq.keys[i]))
            else:
                out.append("NONE")

    sys.stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
