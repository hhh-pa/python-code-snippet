import sys


class VEBTree:
    def __init__(self, universe):
        self.u = universe
        self.min_val = -1
        self.max_val = -1
        self.summary = None
        self.cluster = None

        k = 0
        while (1 << k) < self.u:
            k += 1
        lower_k = k // 2
        upper_k = k - lower_k
        self.lower_sqrt = 1 << lower_k
        self.upper_sqrt = 1 << upper_k

        if self.u > 2:
            self.cluster = [None] * self.upper_sqrt

    def high(self, x):
        return x // self.lower_sqrt

    def low(self, x):
        return x % self.lower_sqrt

    def index(self, h, l):
        return h * self.lower_sqrt + l

    def empty_insert(self, x):
        self.min_val = x
        self.max_val = x

    def minimum(self):
        return self.min_val

    def maximum(self):
        return self.max_val

    def member(self, x):
        if x < 0 or x >= self.u:
            return False
        if x == self.min_val or x == self.max_val:
            return True
        if self.u == 2:
            return False
        c = self.cluster[self.high(x)]
        if c is None:
            return False
        return c.member(self.low(x))

    def insert(self, x):
        if x < 0 or x >= self.u:
            return
        if self.min_val == -1:
            self.empty_insert(x)
            return
        if x == self.min_val or x == self.max_val:
            return
        if x < self.min_val:
            x, self.min_val = self.min_val, x
        if self.u > 2:
            h = self.high(x)
            l = self.low(x)
            if self.cluster[h] is None:
                self.cluster[h] = VEBTree(self.lower_sqrt)
            c = self.cluster[h]
            if c.minimum() == -1:
                if self.summary is None:
                    self.summary = VEBTree(self.upper_sqrt)
                self.summary.insert(h)
                c.empty_insert(l)
            else:
                c.insert(l)
        if x > self.max_val:
            self.max_val = x

    def remove(self, x):
        if not self.member(x):
            return
        self.remove_present(x)

    def remove_present(self, x):
        if self.min_val == self.max_val:
            self.min_val = -1
            self.max_val = -1
            return
        if self.u == 2:
            self.min_val = 1 if x == 0 else 0
            self.max_val = self.min_val
            return
        if x == self.min_val:
            first_cluster = self.summary.minimum()
            x = self.index(
                first_cluster, self.cluster[first_cluster].minimum()
            )
            self.min_val = x
        h = self.high(x)
        l = self.low(x)
        c = self.cluster[h]
        c.remove_present(l)
        if c.minimum() == -1:
            self.summary.remove_present(h)
            if x == self.max_val:
                summary_max = self.summary.maximum()
                if summary_max == -1:
                    self.max_val = self.min_val
                else:
                    self.max_val = self.index(
                        summary_max, self.cluster[summary_max].maximum()
                    )
        elif x == self.max_val:
            self.max_val = self.index(h, c.maximum())

    def successor(self, x):
        if self.min_val == -1 or x >= self.max_val:
            return -1
        if x < self.min_val:
            return self.min_val
        if self.u == 2:
            if x == 0 and self.max_val == 1:
                return 1
            return -1
        h = self.high(x)
        l = self.low(x)
        c = self.cluster[h]
        max_low = c.maximum() if c else -1
        if max_low != -1 and l < max_low:
            offset = c.successor(l)
            return self.index(h, offset)
        succ_cluster = self.summary.successor(h) if self.summary else -1
        if succ_cluster == -1:
            return -1
        offset = self.cluster[succ_cluster].minimum()
        return self.index(succ_cluster, offset)

    def predecessor(self, x):
        if self.min_val == -1 or x <= self.min_val:
            return -1
        if x > self.max_val:
            return self.max_val
        if self.u == 2:
            if x == 1 and self.min_val == 0:
                return 0
            return -1
        h = self.high(x)
        l = self.low(x)
        c = self.cluster[h]
        min_low = c.minimum() if c else -1
        if min_low != -1 and l > min_low:
            offset = c.predecessor(l)
            return self.index(h, offset)
        pred_cluster = self.summary.predecessor(h) if self.summary else -1
        if pred_cluster == -1:
            if self.min_val != -1 and x > self.min_val:
                return self.min_val
            return -1
        offset = self.cluster[pred_cluster].maximum()
        return self.index(pred_cluster, offset)


def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    u = int(tokens[0])
    q = int(tokens[1])
    idx = 2
    tree = VEBTree(u)
    out = []
    for _ in range(q):
        if idx >= len(tokens):
            break
        t = int(tokens[idx])
        idx += 1
        if t == 1:
            x = int(tokens[idx])
            idx += 1
            tree.insert(x)
        elif t == 2:
            x = int(tokens[idx])
            idx += 1
            tree.remove(x)
        elif t == 3:
            x = int(tokens[idx])
            idx += 1
            out.append("1" if tree.member(x) else "0")
        elif t == 4:
            x = int(tokens[idx])
            idx += 1
            out.append(str(tree.successor(x)))
        elif t == 5:
            x = int(tokens[idx])
            idx += 1
            out.append(str(tree.predecessor(x)))
        elif t == 6:
            out.append(f"{tree.minimum()} {tree.maximum()}")

    sys.stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
