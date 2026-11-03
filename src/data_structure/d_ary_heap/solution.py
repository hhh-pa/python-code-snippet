import sys


class DaryHeap:
    def __init__(self, d):
        self.d = max(2, d)
        self.a = []

    def swim(self, k):
        d = self.d
        a = self.a
        while k > 0:
            p = (k - 1) // d
            if a[k] >= a[p]:
                break
            a[k], a[p] = a[p], a[k]
            k = p

    def sink(self, k):
        d = self.d
        a = self.a
        n = len(a)
        while True:
            m = k
            base = d * k
            for j in range(1, d + 1):
                c = base + j
                if c < n and a[c] < a[m]:
                    m = c
            if m == k:
                break
            a[k], a[m] = a[m], a[k]
            k = m

    def insert(self, x):
        self.a.append(x)
        self.swim(len(self.a) - 1)

    def extract_min(self):
        if not self.a:
            return None
        res = self.a[0]
        last = self.a.pop()
        if self.a:
            self.a[0] = last
            self.sink(0)
        return res

    def peek(self):
        return self.a[0] if self.a else None


def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    d = int(tokens[0])
    q = int(tokens[1])
    idx = 2
    h = DaryHeap(d)
    out = []
    for _ in range(q):
        op = int(tokens[idx])
        idx += 1
        if op == 1:
            x = int(tokens[idx])
            idx += 1
            h.insert(x)
        elif op == 2:
            res = h.extract_min()
            out.append(str(res) if res is not None else "EMPTY")
        elif op == 3:
            res = h.peek()
            out.append(str(res) if res is not None else "EMPTY")

    sys.stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
