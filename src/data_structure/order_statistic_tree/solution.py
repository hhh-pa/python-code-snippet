import random
import sys

sys.setrecursionlimit(200000)


class Node:
    __slots__ = ("key", "priority", "size", "left", "right")

    def __init__(self, key, priority):
        self.key = key
        self.priority = priority
        self.size = 1
        self.left = None
        self.right = None


def get_sz(t):
    return t.size if t else 0


def update_sz(t):
    if t:
        t.size = 1 + get_sz(t.left) + get_sz(t.right)


def split(t, key):
    if not t:
        return None, None
    if key < t.key:
        l, t.left = split(t.left, key)
        update_sz(t)
        return l, t
    else:
        t.right, r = split(t.right, key)
        update_sz(t)
        return t, r


def merge(l, r):
    if not l or not r:
        return l if l else r
    if l.priority > r.priority:
        l.right = merge(l.right, r)
        update_sz(l)
        return l
    else:
        r.left = merge(l, r.left)
        update_sz(r)
        return r


class OrderStatisticTree:
    def __init__(self):
        self.root = None
        self.rng = random.Random(1337)

    def insert(self, key):
        l, r = split(self.root, key)
        cur = l
        while cur and cur.right:
            cur = cur.right
        if cur and cur.key == key:
            self.root = merge(l, r)
            return
        m = Node(key, self.rng.randint(0, 0x7FFFFFFF))
        self.root = merge(merge(l, m), r)

    def remove(self, key):
        l, r = split(self.root, key - 1)
        m, r = split(r, key)
        self.root = merge(l, r)

    def size(self):
        return get_sz(self.root)

    def os_select(self, k):
        if k < 1 or k > get_sz(self.root):
            return None
        cur = self.root
        while cur:
            left_sz = get_sz(cur.left)
            if k == left_sz + 1:
                return cur.key
            if k <= left_sz:
                cur = cur.left
            else:
                k -= left_sz + 1
                cur = cur.right
        return None

    def os_rank(self, key):
        ans = 0
        cur = self.root
        while cur:
            if key <= cur.key:
                cur = cur.left
            else:
                ans += get_sz(cur.left) + 1
                cur = cur.right
        return ans


class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, i, d):
        n = self.n
        while i <= n:
            self.bit[i] += d
            i += i & -i

    def kth(self, k):
        i = 0
        step = 1
        while step * 2 <= self.n:
            step *= 2
        while step > 0:
            j = i + step
            if j <= self.n and self.bit[j] < k:
                k -= self.bit[j]
                i = j
            step //= 2
        return i + 1


def josephus_permutation(n, m):
    fw = Fenwick(n)
    for i in range(1, n + 1):
        fw.add(i, 1)
    pos = 0
    rem = n
    order = []
    while rem > 0:
        pos = (pos + m - 1) % rem
        idx = fw.kth(pos + 1)
        order.append(str(idx))
        fw.add(idx, -1)
        rem -= 1
    return order


def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    q = int(tokens[0])
    idx = 1
    tree = OrderStatisticTree()
    out = []
    for _ in range(q):
        if idx >= len(tokens):
            break
        op = int(tokens[idx])
        idx += 1
        if op == 1:
            x = int(tokens[idx])
            idx += 1
            tree.insert(x)
        elif op == 2:
            x = int(tokens[idx])
            idx += 1
            tree.remove(x)
        elif op == 3:
            k = int(tokens[idx])
            idx += 1
            val = tree.os_select(k)
            out.append(str(val) if val is not None else "NONE")
        elif op == 4:
            x = int(tokens[idx])
            idx += 1
            out.append(str(tree.os_rank(x)))
        elif op == 5:
            n = int(tokens[idx])
            m = int(tokens[idx + 1])
            idx += 2
            order = josephus_permutation(n, m)
            out.append(" ".join(order))

    sys.stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
