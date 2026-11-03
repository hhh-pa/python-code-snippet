import sys

sys.setrecursionlimit(200000)


class Node:
    __slots__ = ("key", "left", "right", "parent")

    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.parent = None


class SplayTree:
    def __init__(self):
        self.root = None

    def rotate_left(self, x):
        y = x.right
        if not y:
            return
        x.right = y.left
        if y.left:
            y.left.parent = x
        y.parent = x.parent
        if not x.parent:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def rotate_right(self, x):
        y = x.left
        if not y:
            return
        x.left = y.right
        if y.right:
            y.right.parent = x
        y.parent = x.parent
        if not x.parent:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.right = x
        x.parent = y

    def splay(self, x):
        while x.parent:
            p = x.parent
            g = p.parent
            if not g:
                # Zig
                if x == p.left:
                    self.rotate_right(p)
                else:
                    self.rotate_left(p)
            elif x == p.left and p == g.left:
                # Zig-Zig
                self.rotate_right(g)
                self.rotate_right(p)
            elif x == p.right and p == g.right:
                # Zig-Zig
                self.rotate_left(g)
                self.rotate_left(p)
            elif x == p.right and p == g.left:
                # Zig-Zag
                self.rotate_left(p)
                self.rotate_right(g)
            else:
                # Zig-Zag
                self.rotate_right(p)
                self.rotate_left(g)

    def insert(self, key):
        if not self.root:
            self.root = Node(key)
            return
        cur = self.root
        p = None
        while cur:
            p = cur
            if key < cur.key:
                cur = cur.left
            elif key > cur.key:
                cur = cur.right
            else:
                self.splay(cur)
                return
        node = Node(key)
        node.parent = p
        if key < p.key:
            p.left = node
        else:
            p.right = node
        self.splay(node)

    def find(self, key):
        cur = self.root
        last = None
        while cur:
            last = cur
            if key < cur.key:
                cur = cur.left
            elif key > cur.key:
                cur = cur.right
            else:
                self.splay(cur)
                return True
        if last:
            self.splay(last)
        return False

    def remove(self, key):
        if not self.find(key):
            return
        left_sub = self.root.left
        right_sub = self.root.right
        if left_sub:
            left_sub.parent = None
        if right_sub:
            right_sub.parent = None

        if not left_sub:
            self.root = right_sub
        else:
            m = left_sub
            while m.right:
                m = m.right
            self.root = left_sub
            self.splay(m)
            self.root.right = right_sub
            if right_sub:
                right_sub.parent = self.root

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
    tree = SplayTree()
    out = []
    for _ in range(q):
        if idx >= len(tokens):
            break
        op = tokens[idx]
        idx += 1
        if op == "INSERT":
            val = int(tokens[idx])
            idx += 1
            tree.insert(val)
        elif op == "FIND":
            val = int(tokens[idx])
            idx += 1
            out.append("FOUND" if tree.find(val) else "NOT_FOUND")
        elif op == "DELETE":
            val = int(tokens[idx])
            idx += 1
            tree.remove(val)
        elif op == "PRINT":
            arr = tree.get_inorder()
            out.append(" ".join(map(str, arr)))

    sys.stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
