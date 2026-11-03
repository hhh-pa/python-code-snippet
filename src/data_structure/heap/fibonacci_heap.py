import sys

sys.setrecursionlimit(200000)


class FibNode:
    __slots__ = (
        "id",
        "key",
        "degree",
        "marked",
        "parent",
        "child",
        "left",
        "right",
    )

    def __init__(self, i, k):
        self.id = i
        self.key = k
        self.degree = 0
        self.marked = False
        self.parent = None
        self.child = None
        self.left = self
        self.right = self


class FibonacciHeap:
    def __init__(self):
        self.min_node = None
        self.total_nodes = 0
        self.node_map = {}

    def link_roots(self, y, x):
        # Remove y from root list
        y.left.right = y.right
        y.right.left = y.left
        # Make y a child of x
        y.parent = x
        if not x.child:
            x.child = y
            y.left = y
            y.right = y
        else:
            y.right = x.child
            y.left = x.child.left
            x.child.left.right = y
            x.child.left = y
        x.degree += 1
        y.marked = False

    def consolidate(self):
        max_deg = 50
        A = [None] * max_deg

        root_list = []
        if self.min_node:
            cur = self.min_node
            while True:
                root_list.append(cur)
                cur = cur.right
                if cur == self.min_node:
                    break

        for w in root_list:
            x = w
            d = x.degree
            while d < max_deg and A[d] is not None:
                y = A[d]
                if x.key > y.key:
                    x, y = y, x
                self.link_roots(y, x)
                A[d] = None
                d += 1
            if d < max_deg:
                A[d] = x

        self.min_node = None
        for i in range(max_deg):
            if A[i] is not None:
                if not self.min_node:
                    self.min_node = A[i]
                    self.min_node.left = self.min_node
                    self.min_node.right = self.min_node
                else:
                    A[i].right = self.min_node
                    A[i].left = self.min_node.left
                    self.min_node.left.right = A[i]
                    self.min_node.left = A[i]
                    if A[i].key < self.min_node.key:
                        self.min_node = A[i]

    def cut(self, x, y):
        if x.right == x:
            y.child = None
        else:
            x.left.right = x.right
            x.right.left = x.left
            if y.child == x:
                y.child = x.right
        y.degree -= 1
        x.right = self.min_node
        x.left = self.min_node.left
        self.min_node.left.right = x
        self.min_node.left = x
        x.parent = None
        x.marked = False

    def cascading_cut(self, y):
        z = y.parent
        if z:
            if not y.marked:
                y.marked = True
            else:
                self.cut(y, z)
                self.cascading_cut(z)

    def insert(self, i, key):
        node = FibNode(i, key)
        self.node_map[i] = node
        if not self.min_node:
            self.min_node = node
        else:
            node.right = self.min_node
            node.left = self.min_node.left
            self.min_node.left.right = node
            self.min_node.left = node
            if node.key < self.min_node.key:
                self.min_node = node
        self.total_nodes += 1

    def get_min(self):
        if not self.min_node:
            return None
        return self.min_node.id, self.min_node.key

    def extract_min(self):
        z = self.min_node
        if not z:
            return None
        out_id = z.id
        out_key = z.key

        if z.child:
            children = []
            cur = z.child
            while True:
                children.append(cur)
                cur = cur.right
                if cur == z.child:
                    break
            for ch in children:
                ch.right = self.min_node
                ch.left = self.min_node.left
                self.min_node.left.right = ch
                self.min_node.left = ch
                ch.parent = None

        z.left.right = z.right
        z.right.left = z.left

        if z == z.right:
            self.min_node = None
        else:
            self.min_node = z.right
            self.consolidate()

        self.total_nodes -= 1
        del self.node_map[z.id]
        return out_id, out_key

    def decrease_key(self, i, new_key):
        if i not in self.node_map:
            return
        x = self.node_map[i]
        if new_key > x.key:
            return
        x.key = new_key
        y = x.parent
        if y and x.key < y.key:
            self.cut(x, y)
            self.cascading_cut(y)
        if x.key < self.min_node.key:
            self.min_node = x


def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    q = int(tokens[0])
    idx = 1
    heap = FibonacciHeap()
    out = []
    for _ in range(q):
        if idx >= len(tokens):
            break
        op = tokens[idx]
        idx += 1
        if op == "INSERT":
            i = int(tokens[idx])
            val = int(tokens[idx + 1])
            idx += 2
            heap.insert(i, val)
        elif op == "MIN":
            res = heap.get_min()
            if res:
                out.append(f"{res[0]} {res[1]}")
            else:
                out.append("EMPTY")
        elif op == "EXTRACT_MIN":
            res = heap.extract_min()
            if res:
                out.append(f"{res[0]} {res[1]}")
            else:
                out.append("EMPTY")
        elif op == "DECREASE_KEY":
            i = int(tokens[idx])
            val = int(tokens[idx + 1])
            idx += 2
            heap.decrease_key(i, val)

    sys.stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
