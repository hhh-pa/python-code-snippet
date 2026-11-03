import sys

sys.setrecursionlimit(200000)


class Node:
    __slots__ = ("lo", "hi", "id", "max_hi", "height", "left", "right")

    def __init__(self, lo, hi, id):
        self.lo = lo
        self.hi = hi
        self.id = id
        self.max_hi = hi
        self.height = 1
        self.left = None
        self.right = None


def node_height(u):
    return u.height if u else 0


def pull(u):
    if not u:
        return
    hl = node_height(u.left)
    hr = node_height(u.right)
    u.height = 1 + (hl if hl > hr else hr)
    m = u.hi
    if u.left and u.left.max_hi > m:
        m = u.left.max_hi
    if u.right and u.right.max_hi > m:
        m = u.right.max_hi
    u.max_hi = m


def rotate_left(x):
    y = x.right
    x.right = y.left
    y.left = x
    pull(x)
    pull(y)
    return y


def rotate_right(y):
    x = y.left
    y.left = x.right
    x.right = y
    pull(y)
    pull(x)
    return x


def balance(u):
    if not u:
        return None
    pull(u)
    bf = node_height(u.left) - node_height(u.right)
    if bf > 1:
        if node_height(u.left.left) < node_height(u.left.right):
            u.left = rotate_left(u.left)
        return rotate_right(u)
    if bf < -1:
        if node_height(u.right.right) < node_height(u.right.left):
            u.right = rotate_right(u.right)
        return rotate_left(u)
    return u


def cmp_key(lo1, hi1, id1, lo2, hi2, id2):
    if lo1 != lo2:
        return -1 if lo1 < lo2 else 1
    if hi1 != hi2:
        return -1 if hi1 < hi2 else 1
    if id1 != id2:
        return -1 if id1 < id2 else 1
    return 0


def insert_node(u, lo, hi, id):
    if not u:
        return Node(lo, hi, id)
    c = cmp_key(lo, hi, id, u.lo, u.hi, u.id)
    if c < 0:
        u.left = insert_node(u.left, lo, hi, id)
    elif c > 0:
        u.right = insert_node(u.right, lo, hi, id)
    else:
        return u
    return balance(u)


def remove_node(u, lo, hi, id):
    if not u:
        return None
    c = cmp_key(lo, hi, id, u.lo, u.hi, u.id)
    if c < 0:
        u.left = remove_node(u.left, lo, hi, id)
    elif c > 0:
        u.right = remove_node(u.right, lo, hi, id)
    else:
        if not u.left or not u.right:
            return u.left if u.left else u.right
        succ = u.right
        while succ.left:
            succ = succ.left
        u.lo = succ.lo
        u.hi = succ.hi
        u.id = succ.id
        u.right = remove_node(u.right, succ.lo, succ.hi, succ.id)
    return balance(u)


def query_node(u, qlo, qhi, out):
    if not u or u.max_hi < qlo:
        return
    query_node(u.left, qlo, qhi, out)
    if u.lo <= qhi and qlo <= u.hi:
        out.append(u.id)
    if u.lo <= qhi:
        query_node(u.right, qlo, qhi, out)


class IntervalTree:
    def __init__(self):
        self.root = None
        self.by_id = {}

    def insert(self, lo, hi, id):
        if id in self.by_id:
            old_lo, old_hi = self.by_id[id]
            self.root = remove_node(self.root, old_lo, old_hi, id)
        self.by_id[id] = (lo, hi)
        self.root = insert_node(self.root, lo, hi, id)

    def remove(self, id):
        if id not in self.by_id:
            return
        lo, hi = self.by_id.pop(id)
        self.root = remove_node(self.root, lo, hi, id)

    def query(self, qlo, qhi):
        out = []
        query_node(self.root, qlo, qhi, out)
        out.sort()
        return out


def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    q = int(tokens[0])
    idx = 1
    tree = IntervalTree()
    out = []
    for _ in range(q):
        if idx >= len(tokens):
            break
        t = int(tokens[idx])
        idx += 1
        if t == 1:
            lo = int(tokens[idx])
            hi = int(tokens[idx + 1])
            i = int(tokens[idx + 2])
            idx += 3
            tree.insert(lo, hi, i)
        elif t == 2:
            i = int(tokens[idx])
            idx += 1
            tree.remove(i)
        elif t == 3:
            lo = int(tokens[idx])
            hi = int(tokens[idx + 1])
            idx += 2
            res = tree.query(lo, hi)
            if not res:
                out.append("NONE")
            else:
                out.append(" ".join(map(str, res)))

    sys.stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
