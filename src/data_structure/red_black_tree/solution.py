import sys

RED = 0
BLACK = 1


class Node:
    __slots__ = ("key", "color", "left", "right", "p")

    def __init__(self, key=0, color=BLACK, left=None, right=None, p=None):
        self.key = key
        self.color = color
        self.left = left
        self.right = right
        self.p = p


class RedBlackTree:
    def __init__(self):
        self.nil = Node(0, BLACK)
        self.nil.left = self.nil
        self.nil.right = self.nil
        self.nil.p = self.nil
        self.root = self.nil

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.nil:
            y.left.p = x
        y.p = x.p
        if x.p == self.nil:
            self.root = y
        elif x == x.p.left:
            x.p.left = y
        else:
            x.p.right = y
        y.left = x
        x.p = y

    def right_rotate(self, y):
        x = y.left
        y.left = x.right
        if x.right != self.nil:
            x.right.p = y
        x.p = y.p
        if y.p == self.nil:
            self.root = x
        elif y == y.p.right:
            y.p.right = x
        else:
            y.p.left = x
        x.right = y
        y.p = x

    def rb_insert_fixup(self, z):
        while z.p.color == RED:
            if z.p == z.p.p.left:
                y = z.p.p.right
                if y.color == RED:
                    z.p.color = BLACK
                    y.color = BLACK
                    z.p.p.color = RED
                    z = z.p.p
                else:
                    if z == z.p.right:
                        z = z.p
                        self.left_rotate(z)
                    z.p.color = BLACK
                    z.p.p.color = RED
                    self.right_rotate(z.p.p)
            else:
                y = z.p.p.left
                if y.color == RED:
                    z.p.color = BLACK
                    y.color = BLACK
                    z.p.p.color = RED
                    z = z.p.p
                else:
                    if z == z.p.left:
                        z = z.p
                        self.right_rotate(z)
                    z.p.color = BLACK
                    z.p.p.color = RED
                    self.left_rotate(z.p.p)
        self.root.color = BLACK

    def insert(self, key):
        y = self.nil
        x = self.root
        while x != self.nil:
            y = x
            if key == x.key:
                return
            if key < x.key:
                x = x.left
            else:
                x = x.right
        z = Node(key, RED, self.nil, self.nil, y)
        if y == self.nil:
            self.root = z
        elif key < y.key:
            y.left = z
        else:
            y.right = z
        self.rb_insert_fixup(z)

    def rb_transplant(self, u, v):
        if u.p == self.nil:
            self.root = v
        elif u == u.p.left:
            u.p.left = v
        else:
            u.p.right = v
        v.p = u.p

    def tree_minimum(self, x):
        while x.left != self.nil:
            x = x.left
        return x

    def rb_delete_fixup(self, x):
        while x != self.root and x.color == BLACK:
            if x == x.p.left:
                w = x.p.right
                if w.color == RED:
                    w.color = BLACK
                    x.p.color = RED
                    self.left_rotate(x.p)
                    w = x.p.right
                if w.left.color == BLACK and w.right.color == BLACK:
                    w.color = RED
                    x = x.p
                else:
                    if w.right.color == BLACK:
                        w.left.color = BLACK
                        w.color = RED
                        self.right_rotate(w)
                        w = x.p.right
                    w.color = x.p.color
                    x.p.color = BLACK
                    w.right.color = BLACK
                    self.left_rotate(x.p)
                    x = self.root
            else:
                w = x.p.left
                if w.color == RED:
                    w.color = BLACK
                    x.p.color = RED
                    self.right_rotate(x.p)
                    w = x.p.left
                if w.right.color == BLACK and w.left.color == BLACK:
                    w.color = RED
                    x = x.p
                else:
                    if w.left.color == BLACK:
                        w.right.color = BLACK
                        w.color = RED
                        self.left_rotate(w)
                        w = x.p.left
                    w.color = x.p.color
                    x.p.color = BLACK
                    w.left.color = BLACK
                    self.right_rotate(x.p)
                    x = self.root
        x.color = BLACK

    def find_node(self, k):
        cur = self.root
        while cur != self.nil:
            if k == cur.key:
                return cur
            if k < cur.key:
                cur = cur.left
            else:
                cur = cur.right
        return self.nil

    def remove(self, key):
        z = self.find_node(key)
        if z == self.nil:
            return
        y = z
        y_original_color = y.color
        if z.left == self.nil:
            x = z.right
            self.rb_transplant(z, z.right)
        elif z.right == self.nil:
            x = z.left
            self.rb_transplant(z, z.left)
        else:
            y = self.tree_minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.p == z:
                x.p = y
            else:
                self.rb_transplant(y, y.right)
                y.right = z.right
                y.right.p = y
            self.rb_transplant(z, y)
            y.left = z.left
            y.left.p = y
            y.color = z.color
        if y_original_color == BLACK:
            self.rb_delete_fixup(x)

    def search(self, key):
        return self.find_node(key) != self.nil

    def predecessor(self, key):
        cur = self.root
        pred = None
        while cur != self.nil:
            if cur.key < key:
                pred = cur.key
                cur = cur.right
            else:
                cur = cur.left
        return pred

    def successor(self, key):
        cur = self.root
        succ = None
        while cur != self.nil:
            if cur.key > key:
                succ = cur.key
                cur = cur.left
            else:
                cur = cur.right
        return succ


def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    q = int(tokens[0])
    idx = 1
    tree = RedBlackTree()
    out = []
    for _ in range(q):
        if idx >= len(tokens):
            break
        op = int(tokens[idx])
        x = int(tokens[idx + 1])
        idx += 2
        if op == 1:
            tree.insert(x)
        elif op == 2:
            tree.remove(x)
        elif op == 3:
            out.append("1" if tree.search(x) else "0")
        elif op == 4:
            p = tree.predecessor(x)
            out.append(str(p) if p is not None else "NONE")
        elif op == 5:
            s = tree.successor(x)
            out.append(str(s) if s is not None else "NONE")

    sys.stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
