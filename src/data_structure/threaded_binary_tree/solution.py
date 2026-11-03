import sys


class TBT:
    def __init__(self):
        self.key = []
        self.L = []
        self.R = []
        self.lt = []
        self.rt = []
        self.root = -1

    def alloc(self, x):
        n = len(self.key)
        self.key.append(x)
        self.L.append(-1)
        self.R.append(-1)
        self.lt.append(True)
        self.rt.append(True)
        return n

    def insert(self, x):
        n = self.alloc(x)
        if self.root == -1:
            self.root = n
            return
        cur = self.root
        while True:
            if x == self.key[cur]:
                self.key.pop()
                self.L.pop()
                self.R.pop()
                self.lt.pop()
                self.rt.pop()
                return
            if x < self.key[cur]:
                if self.lt[cur]:
                    self.L[n] = self.L[cur]
                    self.R[n] = cur
                    self.L[cur] = n
                    self.lt[cur] = False
                    if self.L[n] != -1 and self.rt[self.L[n]]:
                        self.R[self.L[n]] = n
                    return
                cur = self.L[cur]
            else:
                if self.rt[cur]:
                    self.R[n] = self.R[cur]
                    self.L[n] = cur
                    self.R[cur] = n
                    self.rt[cur] = False
                    if self.R[n] != -1 and self.lt[self.R[n]]:
                        self.L[self.R[n]] = n
                    return
                cur = self.R[cur]

    def pred_node(self, i):
        if self.lt[i]:
            return self.L[i]
        j = self.L[i]
        while not self.rt[j]:
            j = self.R[j]
        return j

    def succ_node(self, i):
        if self.rt[i]:
            return self.R[i]
        j = self.R[i]
        while not self.lt[j]:
            j = self.L[j]
        return j

    def find(self, x):
        lo = -1
        hi = -1
        cur = self.root
        while cur != -1:
            if x == self.key[cur]:
                return cur, lo, hi
            if x < self.key[cur]:
                hi = cur
                if self.lt[cur]:
                    break
                cur = self.L[cur]
            else:
                lo = cur
                if self.rt[cur]:
                    break
                cur = self.R[cur]
        return -1, lo, hi

    def pred(self, x):
        f, lo, _ = self.find(x)
        p = lo if f == -1 else self.pred_node(f)
        if p == -1:
            return None
        return self.key[p]

    def succ(self, x):
        f, _, hi = self.find(x)
        s = hi if f == -1 else self.succ_node(f)
        if s == -1:
            return None
        return self.key[s]

    def inorder(self):
        if self.root == -1:
            return ""
        cur = self.root
        while not self.lt[cur]:
            cur = self.L[cur]
        res = []
        while cur != -1:
            res.append(str(self.key[cur]))
            cur = self.succ_node(cur)
        return " ".join(res)


def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    q = int(tokens[1])
    idx = 2
    tbt = TBT()
    for _ in range(n):
        tbt.insert(int(tokens[idx]))
        idx += 1

    out = []
    for _ in range(q):
        op = int(tokens[idx])
        idx += 1
        if op == 1:
            x = int(tokens[idx])
            idx += 1
            ans = tbt.pred(x)
            out.append(str(ans) if ans is not None else "NONE")
        elif op == 2:
            x = int(tokens[idx])
            idx += 1
            ans = tbt.succ(x)
            out.append(str(ans) if ans is not None else "NONE")
        elif op == 3:
            out.append(tbt.inorder())

    sys.stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
