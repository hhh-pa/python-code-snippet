import sys
from collections import deque

class CWNode:
    __slots__ = ('next', 'fail', 'depth', 'out')
    def __init__(self, d):
        self.next = [-1] * 26
        self.fail = 0
        self.depth = d
        self.out = []

def commentz_walter(patterns, text):
    num_patterns = len(patterns)
    results = [[] for _ in range(num_patterns)]
    if num_patterns == 0 or not text:
        return results

    w_min = min(len(p) for p in patterns)
    if w_min == 0 or w_min > len(text):
        return results

    trie = [CWNode(0)]
    char_min_depth = [w_min + 1] * 26

    for idx, pat in enumerate(patterns):
        u = 0
        pat_len = len(pat)
        for k in range(pat_len):
            ch = pat[pat_len - 1 - k]
            c = ord(ch) - ord('a')
            dep = k + 1
            if dep >= 2 and dep < char_min_depth[c]:
                char_min_depth[c] = dep
            if trie[u].next[c] == -1:
                next_id = len(trie)
                trie.append(CWNode(dep))
                trie[u].next[c] = next_id
            u = trie[u].next[c]
        trie[u].out.append(idx)

    q = deque()
    for c in range(26):
        nxt = trie[0].next[c]
        if nxt != -1:
            trie[nxt].fail = 0
            q.append(nxt)

    while q:
        u = q.popleft()
        for c in range(26):
            v = trie[u].next[c]
            if v != -1:
                f = trie[u].fail
                while f > 0 and trie[f].next[c] == -1:
                    f = trie[f].fail
                if trie[f].next[c] != -1:
                    f = trie[f].next[c]
                trie[v].fail = f
                q.append(v)

    n = len(text)
    j = w_min - 1
    while j < n:
        u = 0
        pos = j
        while True:
            c = ord(text[pos]) - ord('a')
            nxt = trie[u].next[c]
            if nxt == -1:
                break
            u = nxt
            for pat_idx in trie[u].out:
                results[pat_idx].append(pos)
            if pos == 0:
                break
            pos -= 1

        c_right = ord(text[j]) - ord('a')
        shift = char_min_depth[c_right] - 1
        if shift < 1:
            shift = 1
        j += shift

    return results

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    n = int(next(it))
    patterns = [next(it) for _ in range(n)]
    text = next(it)

    res = commentz_walter(patterns, text)
    out = []
    for i in range(n):
        if not res[i]:
            out.append("-1")
        else:
            out.append(" ".join(str(x) for x in res[i]))
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
