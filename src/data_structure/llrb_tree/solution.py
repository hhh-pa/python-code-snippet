import sys

sys.setrecursionlimit(200000)

RED = True
BLACK = False


class Node:
    __slots__ = ("key", "val", "color", "sz", "left", "right")

    def __init__(self, key, val, color=RED, sz=1):
        self.key = key
        self.val = val
        self.color = color
        self.sz = sz
        self.left = None
        self.right = None


def is_red(h):
    return h is not None and h.color == RED


def node_size(h):
    return h.sz if h else 0


def update_size(h):
    if h:
        h.sz = 1 + node_size(h.left) + node_size(h.right)


def rotate_left(h):
    x = h.right
    h.right = x.left
    x.left = h
    x.color = h.color
    h.color = RED
    x.sz = h.sz
    update_size(h)
    return x


def rotate_right(h):
    x = h.left
    h.left = x.right
    x.right = h
    x.color = h.color
    h.color = RED
    x.sz = h.sz
    update_size(h)
    return x


def flip_colors(h):
    h.color = not h.color
    h.left.color = not h.left.color
    h.right.color = not h.right.color


def balance(h):
    if is_red(h.right) and not is_red(h.left):
        h = rotate_left(h)
    if is_red(h.left) and is_red(h.left.left):
        h = rotate_right(h)
    if is_red(h.left) and is_red(h.right):
        flip_colors(h)
    update_size(h)
    return h


def move_red_left(h):
    flip_colors(h)
    if is_red(h.right.left):
        h.right = rotate_right(h.right)
        h = rotate_left(h)
        flip_colors(h)
    return h


def move_red_right(h):
    flip_colors(h)
    if is_red(h.left.left):
        h = rotate_right(h)
        flip_colors(h)
    return h


def put_node(h, key, val):
    if h is None:
        return Node(key, val, RED, 1)
    if key < h.key:
        h.left = put_node(h.left, key, val)
    elif key > h.key:
        h.right = put_node(h.right, key, val)
    else:
        h.val = val
    return balance(h)


def min_node(h):
    while h.left:
        h = h.left
    return h


def delete_min(h):
    if h.left is None:
        return None
    if not is_red(h.left) and not is_red(h.left.left):
        h = move_red_left(h)
    h.left = delete_min(h.left)
    return balance(h)


def delete_node(h, key):
    if key < h.key:
        if not is_red(h.left) and not is_red(h.left.left):
            h = move_red_left(h)
        h.left = delete_node(h.left, key)
    else:
        if is_red(h.left):
            h = rotate_right(h)
        if key == h.key and h.right is None:
            return None
        if not is_red(h.right) and not is_red(h.right.left):
            h = move_red_right(h)
        if key == h.key:
            m = min_node(h.right)
            h.key = m.key
            h.val = m.val
            h.right = delete_min(h.right)
        else:
            h.right = delete_node(h.right, key)
    return balance(h)


class LLRBTree:
    def __init__(self):
        self.root = None

    def put(self, key, val):
        self.root = put_node(self.root, key, val)
        self.root.color = BLACK

    def get(self, key):
        cur = self.root
        while cur:
            if key == cur.key:
                return cur.val
            if key < cur.key:
                cur = cur.left
            else:
                cur = cur.right
        return None

    def contains(self, key):
        return self.get(key) is not None

    def remove(self, key):
        if not self.contains(key):
            return
        if not is_red(self.root.left) and not is_red(self.root.right):
            self.root.color = RED
        self.root = delete_node(self.root, key)
        if self.root is not None:
            self.root.color = BLACK

    def rank(self, key):
        cur = self.root
        ans = 0
        while cur:
            if key < cur.key:
                cur = cur.left
            elif key > cur.key:
                ans += 1 + node_size(cur.left)
                cur = cur.right
            else:
                ans += node_size(cur.left)
                break
        return ans

    def range_count(self, lo, hi):
        if lo > hi:
            return 0
        return self.rank(hi) - self.rank(lo) + (1 if self.contains(hi) else 0)

    def floor(self, key):
        cur = self.root
        found = None
        while cur:
            if key == cur.key:
                return cur.key
            if key < cur.key:
                cur = cur.left
            else:
                found = cur.key
                cur = cur.right
        return found


def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    q = int(tokens[0])
    idx = 1
    tree = LLRBTree()
    out = []
    for _ in range(q):
        if idx >= len(tokens):
            break
        op = int(tokens[idx])
        idx += 1
        if op == 1:
            k = int(tokens[idx])
            v = int(tokens[idx + 1])
            idx += 2
            tree.put(k, v)
        elif op == 2:
            k = int(tokens[idx])
            idx += 1
            tree.remove(k)
        elif op == 3:
            k = int(tokens[idx])
            idx += 1
            v = tree.get(k)
            out.append(str(v) if v is not None else "NONE")
        elif op == 4:
            lo = int(tokens[idx])
            hi = int(tokens[idx + 1])
            idx += 2
            out.append(str(tree.range_count(lo, hi)))
        elif op == 5:
            k = int(tokens[idx])
            idx += 1
            fk = tree.floor(k)
            out.append(str(fk) if fk is not None else "NONE")

    sys.stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
