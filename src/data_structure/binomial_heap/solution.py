import sys


class BinomialHeap:
    def __init__(self):
        self.key = []
        self.parent = []
        self.child = []
        self.sibling = []
        self.degree = []
        self.head = -1

    def alloc(self, x):
        n = len(self.key)
        self.key.append(x)
        self.parent.append(-1)
        self.child.append(-1)
        self.sibling.append(-1)
        self.degree.append(0)
        return n

    def link(self, y, z):
        # y becomes child of z
        self.parent[y] = z
        self.sibling[y] = self.child[z]
        self.child[z] = y
        self.degree[z] += 1

    def merge_lists(self, h1, h2):
        if h1 == -1:
            return h2
        if h2 == -1:
            return h1
        deg = self.degree
        sib = self.sibling
        if deg[h1] <= deg[h2]:
            h = t = h1
            h1 = sib[h1]
        else:
            h = t = h2
            h2 = sib[h2]
        while h1 != -1 and h2 != -1:
            if deg[h1] <= deg[h2]:
                sib[t] = h1
                t = h1
                h1 = sib[h1]
            else:
                sib[t] = h2
                t = h2
                h2 = sib[h2]
        sib[t] = h1 if h1 != -1 else h2
        return h

    def unite(self, h1, h2):
        h = self.merge_lists(h1, h2)
        if h == -1:
            return -1
        deg = self.degree
        sib = self.sibling
        key = self.key
        prev = -1
        x = h
        next_node = sib[x]
        while next_node != -1:
            if deg[x] != deg[next_node] or (
                sib[next_node] != -1 and deg[sib[next_node]] == deg[x]
            ):
                prev = x
                x = next_node
            elif key[x] <= key[next_node]:
                sib[x] = sib[next_node]
                self.link(next_node, x)
            else:
                if prev == -1:
                    h = next_node
                else:
                    sib[prev] = next_node
                self.link(x, next_node)
                x = next_node
            next_node = sib[x]
        return h

    def insert(self, x):
        node = self.alloc(x)
        self.head = self.unite(self.head, node)

    def minimum(self):
        if self.head == -1:
            return None
        o = self.key[self.head]
        r = self.sibling[self.head]
        while r != -1:
            if self.key[r] < o:
                o = self.key[r]
            r = self.sibling[r]
        return o

    def extract_min(self):
        if self.head == -1:
            return None
        m = self.head
        mp = -1
        p = -1
        r = self.head
        while r != -1:
            if self.key[r] < self.key[m]:
                m = r
                mp = p
            p = r
            r = self.sibling[r]
        res = self.key[m]
        if mp == -1:
            self.head = self.sibling[m]
        else:
            self.sibling[mp] = self.sibling[m]

        rev = -1
        c = self.child[m]
        while c != -1:
            nx = self.sibling[c]
            self.sibling[c] = rev
            self.parent[c] = -1
            rev = c
            c = nx

        self.head = self.unite(self.head, rev)
        return res


def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    q = int(tokens[0])
    idx = 1
    h = BinomialHeap()
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
            res = h.minimum()
            out.append(str(res) if res is not None else "EMPTY")

    sys.stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
