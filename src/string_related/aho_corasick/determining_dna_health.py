import sys
from collections import deque
import bisect

class Node:
    __slots__ = ('next', 'fail', 'dict_link', 'gene_ids', 'pref_health')
    def __init__(self):
        self.next = [0] * 26
        self.fail = 0
        self.dict_link = 0
        self.gene_ids = []
        self.pref_health = [0]

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    n = int(next(it))

    genes = [next(it) for _ in range(n)]
    gene_health = [int(next(it)) for _ in range(n)]

    trie = [Node()]

    for i in range(n):
        s = genes[i]
        u = 0
        for ch in s:
            idx = ord(ch) - ord('a')
            if not trie[u].next[idx]:
                trie[u].next[idx] = len(trie)
                trie.append(Node())
            u = trie[u].next[idx]
        trie[u].gene_ids.append(i)
        trie[u].pref_health.append(trie[u].pref_health[-1] + gene_health[i])

    q = deque()
    for c in range(26):
        v = trie[0].next[c]
        if v:
            q.append(v)

    while q:
        u = q.popleft()
        for c in range(26):
            v = trie[u].next[c]
            if v:
                f = trie[u].fail
                while f and not trie[f].next[c]:
                    f = trie[f].fail
                trie[v].fail = trie[f].next[c]
                trie[v].dict_link = trie[v].fail if trie[trie[v].fail].gene_ids else trie[trie[v].fail].dict_link
                q.append(v)

    s_count = int(next(it))
    min_health = -1
    max_health = -1

    for _ in range(s_count):
        first = int(next(it))
        last = int(next(it))
        strand = next(it)

        total = 0
        u = 0
        for ch in strand:
            idx = ord(ch) - ord('a')
            while u and not trie[u].next[idx]:
                u = trie[u].fail
            u = trie[u].next[idx]

            curr = u
            while curr:
                node = trie[curr]
                if node.gene_ids:
                    l_idx = bisect.bisect_left(node.gene_ids, first)
                    r_idx = bisect.bisect_right(node.gene_ids, last)
                    if r_idx > l_idx:
                        total += node.pref_health[r_idx] - node.pref_health[l_idx]
                curr = node.dict_link

        if min_health == -1 or total < min_health:
            min_health = total
        if max_health == -1 or total > max_health:
            max_health = total

    print(f"{min_health} {max_health}")

if __name__ == "__main__":
    main()
