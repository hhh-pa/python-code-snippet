import random
import sys

MAX_LEVEL = 16


class SkipNode:
    __slots__ = ("val", "forward")

    def __init__(self, val, level):
        self.val = val
        self.forward = [None] * (level + 1)


class SkipList:
    def __init__(self):
        self.head = SkipNode(-1, MAX_LEVEL)
        self.current_level = 0
        self.rng = random.Random(42)

    def random_level(self):
        lvl = 0
        while (self.rng.getrandbits(1) == 1) and lvl < MAX_LEVEL:
            lvl += 1
        return lvl

    def insert(self, val):
        update = [None] * (MAX_LEVEL + 1)
        cur = self.head
        for i in range(self.current_level, -1, -1):
            while cur.forward[i] and cur.forward[i].val < val:
                cur = cur.forward[i]
            update[i] = cur

        cur = cur.forward[0]
        if cur and cur.val == val:
            return

        rlevel = self.random_level()
        if rlevel > self.current_level:
            for i in range(self.current_level + 1, rlevel + 1):
                update[i] = self.head
            self.current_level = rlevel

        new_node = SkipNode(val, rlevel)
        for i in range(rlevel + 1):
            new_node.forward[i] = update[i].forward[i]
            update[i].forward[i] = new_node

    def search(self, val):
        cur = self.head
        for i in range(self.current_level, -1, -1):
            while cur.forward[i] and cur.forward[i].val < val:
                cur = cur.forward[i]
        cur = cur.forward[0]
        return cur is not None and cur.val == val

    def remove(self, val):
        update = [None] * (MAX_LEVEL + 1)
        cur = self.head
        for i in range(self.current_level, -1, -1):
            while cur.forward[i] and cur.forward[i].val < val:
                cur = cur.forward[i]
            update[i] = cur

        cur = cur.forward[0]
        if cur and cur.val == val:
            for i in range(self.current_level + 1):
                if update[i].forward[i] != cur:
                    break
                update[i].forward[i] = cur.forward[i]
            while self.current_level > 0 and self.head.forward[self.current_level] is None:
                self.current_level -= 1

    def get_all(self):
        res = []
        cur = self.head.forward[0]
        while cur:
            res.append(str(cur.val))
            cur = cur.forward[0]
        return res


def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    q = int(tokens[0])
    idx = 1
    sl = SkipList()
    out = []
    for _ in range(q):
        if idx >= len(tokens):
            break
        op = tokens[idx]
        idx += 1
        if op == "INSERT":
            val = int(tokens[idx])
            idx += 1
            sl.insert(val)
        elif op == "SEARCH":
            val = int(tokens[idx])
            idx += 1
            out.append("FOUND" if sl.search(val) else "NOT_FOUND")
        elif op == "DELETE":
            val = int(tokens[idx])
            idx += 1
            sl.remove(val)
        elif op == "PRINT":
            arr = sl.get_all()
            out.append(" ".join(arr))

    sys.stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
