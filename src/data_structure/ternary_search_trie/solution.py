import sys

sys.setrecursionlimit(200000)


class TSTNode:
    __slots__ = ("ch", "has_val", "val", "left", "mid", "right")

    def __init__(self, ch):
        self.ch = ch
        self.has_val = False
        self.val = 0
        self.left = None
        self.mid = None
        self.right = None


class TernarySearchTrie:
    def __init__(self):
        self.root = None

    def put(self, u, key, val, d):
        c = key[d]
        if u is None:
            u = TSTNode(c)
        if c < u.ch:
            u.left = self.put(u.left, key, val, d)
        elif c > u.ch:
            u.right = self.put(u.right, key, val, d)
        elif d + 1 < len(key):
            u.mid = self.put(u.mid, key, val, d + 1)
        else:
            u.has_val = True
            u.val = val
        return u

    def insert(self, key, val):
        if not key:
            return
        self.root = self.put(self.root, key, val, 0)

    def get_node(self, u, key, d):
        while u:
            c = key[d]
            if c < u.ch:
                u = u.left
            elif c > u.ch:
                u = u.right
            elif d + 1 < len(key):
                u = u.mid
                d += 1
            else:
                return u
        return None

    def search(self, key):
        if not key:
            return None
        u = self.get_node(self.root, key, 0)
        if u and u.has_val:
            return u.val
        return None

    def collect(self, u, prefix_chars, res):
        if not u:
            return
        self.collect(u.left, prefix_chars, res)
        prefix_chars.append(u.ch)
        if u.has_val:
            res.append("".join(prefix_chars))
        self.collect(u.mid, prefix_chars, res)
        prefix_chars.pop()
        self.collect(u.right, prefix_chars, res)

    def keys_with_prefix(self, prefix):
        res = []
        if not prefix:
            return res
        u = self.get_node(self.root, prefix, 0)
        if not u:
            return res
        if u.has_val:
            res.append(prefix)
        cur = list(prefix)
        self.collect(u.mid, cur, res)
        return res

    def longest_prefix_of(self, query):
        if not query:
            return ""
        u = self.root
        d = 0
        best_len = 0
        found = False
        n = len(query)
        while u and d < n:
            c = query[d]
            if c < u.ch:
                u = u.left
            elif c > u.ch:
                u = u.right
            else:
                d += 1
                if u.has_val:
                    best_len = d
                    found = True
                u = u.mid
        if not found:
            return ""
        return query[:best_len]

    def collect_match(self, u, prefix_chars, d, pat, res):
        if not u:
            return
        c = pat[d]
        if c == "." or c < u.ch:
            self.collect_match(u.left, prefix_chars, d, pat, res)
        if c == "." or c == u.ch:
            prefix_chars.append(u.ch)
            if d + 1 == len(pat):
                if u.has_val:
                    res.append("".join(prefix_chars))
            else:
                self.collect_match(u.mid, prefix_chars, d + 1, pat, res)
            prefix_chars.pop()
        if c == "." or c > u.ch:
            self.collect_match(u.right, prefix_chars, d, pat, res)

    def keys_that_match(self, pat):
        res = []
        if not pat:
            return res
        cur = []
        self.collect_match(self.root, cur, 0, pat, res)
        return res


def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    q = int(tokens[1])
    idx = 2
    tst = TernarySearchTrie()
    for _ in range(n):
        word = tokens[idx]
        val = int(tokens[idx + 1])
        idx += 2
        tst.insert(word, val)

    out = []
    for _ in range(q):
        if idx >= len(tokens):
            break
        t = int(tokens[idx])
        arg = tokens[idx + 1]
        idx += 2
        if t == 1:
            val = tst.search(arg)
            out.append(str(val) if val is not None else "NOT_FOUND")
        elif t == 2:
            res = tst.keys_with_prefix(arg)
            out.append(" ".join(res) if res else "NONE")
        elif t == 3:
            res = tst.longest_prefix_of(arg)
            out.append(res if res else "NONE")
        elif t == 4:
            res = tst.keys_that_match(arg)
            out.append(" ".join(res) if res else "NONE")

    sys.stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
