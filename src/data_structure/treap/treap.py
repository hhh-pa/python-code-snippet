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
    # Splits into (l, r) where all in l have key <= given key, all in r have key > given key
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


class Treap:
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
        l = merge(l, m)
        self.root = merge(l, r)

    def find(self, key):
        cur = self.root
        while cur:
            if cur.key == key:
                return True
            if key < cur.key:
                cur = cur.left
            else:
                cur = cur.right
        return False

    def erase(self, key):
        l, r = split(self.root, key - 1)
        m, r = split(r, key)
        self.root = merge(l, r)

    def get_inorder(self):
        res = []
        cur = self.root
        st = []
        while st or cur:
            while cur:
                st.append(cur)
                cur = cur.left
            cur = st.pop()
            res.append(cur.key)
            cur = cur.right
        return res


def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    q = int(tokens[0])
    idx = 1
    treap = Treap()
    out = []
    for _ in range(q):
        if idx >= len(tokens):
            break
        op = tokens[idx]
        idx += 1
        if op == "INSERT":
            val = int(tokens[idx])
            idx += 1
            treap.insert(val)
        elif op == "FIND":
            val = int(tokens[idx])
            idx += 1
            out.append("FOUND" if treap.find(val) else "NOT_FOUND")
        elif op == "ERASE":
            val = int(tokens[idx])
            idx += 1
            treap.erase(val)
        elif op == "PRINT":
            arr = treap.get_inorder()
            out.append(" ".join(map(str, arr)))

    sys.stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
