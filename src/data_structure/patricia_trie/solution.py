import sys

sys.setrecursionlimit(200000)


def lcp_len(a, b):
    n = min(len(a), len(b))
    i = 0
    while i < n and a[i] == b[i]:
        i += 1
    return i


class RadixNode:
    __slots__ = ("edge", "has_val", "val", "sub_count", "children")

    def __init__(self, edge):
        self.edge = edge
        self.has_val = False
        self.val = 0
        self.sub_count = 0
        self.children = {}


def update_count(u):
    cnt = 1 if u.has_val else 0
    for child in u.children.values():
        cnt += child.sub_count
    u.sub_count = cnt


def insert_rec(u, rem, val):
    if not rem:
        u.has_val = True
        u.val = val
        update_count(u)
        return
    c = rem[0]
    if c not in u.children:
        leaf = RadixNode(rem)
        leaf.has_val = True
        leaf.val = val
        leaf.sub_count = 1
        u.children[c] = leaf
        update_count(u)
        return

    v = u.children[c]
    k = lcp_len(rem, v.edge)
    if k == len(v.edge):
        insert_rec(v, rem[k:], val)
        update_count(u)
        return

    mid = RadixNode(v.edge[:k])
    v.edge = v.edge[k:]
    old_c = v.edge[0]
    mid.children[old_c] = v

    if k == len(rem):
        mid.has_val = True
        mid.val = val
    else:
        leaf_edge = rem[k:]
        leaf = RadixNode(leaf_edge)
        leaf.has_val = True
        leaf.val = val
        leaf.sub_count = 1
        mid.children[leaf_edge[0]] = leaf

    update_count(mid)
    u.children[c] = mid
    update_count(u)


def erase_rec(u, rem):
    if not rem:
        if not u.has_val:
            return
        u.has_val = False
        update_count(u)
        return
    c = rem[0]
    if c not in u.children:
        return

    v = u.children[c]
    k = lcp_len(rem, v.edge)
    if k < len(v.edge):
        return

    erase_rec(v, rem[k:])

    if not v.has_val and len(v.children) == 0:
        del u.children[c]
    elif not v.has_val and len(v.children) == 1:
        grandchild = next(iter(v.children.values()))
        grandchild.edge = v.edge + grandchild.edge
        u.children[c] = grandchild
    update_count(u)


class PatriciaTrie:
    def __init__(self):
        self.root = RadixNode("")

    def insert(self, word, val):
        insert_rec(self.root, word, val)

    def erase(self, word):
        erase_rec(self.root, word)

    def search(self, word):
        u = self.root
        rem = word
        while rem:
            c = rem[0]
            if c not in u.children:
                return None
            v = u.children[c]
            k = lcp_len(rem, v.edge)
            if k < len(v.edge):
                return None
            rem = rem[k:]
            u = v
        return u.val if u.has_val else None

    def count_prefix(self, prefix):
        u = self.root
        rem = prefix
        while rem:
            c = rem[0]
            if c not in u.children:
                return 0
            v = u.children[c]
            k = lcp_len(rem, v.edge)
            if k == len(rem):
                return v.sub_count
            if k < len(v.edge):
                return 0
            rem = rem[k:]
            u = v
        return u.sub_count


def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    q = int(tokens[0])
    idx = 1
    trie = PatriciaTrie()
    out = []
    for _ in range(q):
        if idx >= len(tokens):
            break
        t = int(tokens[idx])
        word = tokens[idx + 1]
        idx += 2
        if t == 1:
            val = int(tokens[idx])
            idx += 1
            trie.insert(word, val)
        elif t == 2:
            trie.erase(word)
        elif t == 3:
            res = trie.search(word)
            out.append(str(res) if res is not None else "NOT_FOUND")
        elif t == 4:
            out.append(str(trie.count_prefix(word)))

    sys.stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
