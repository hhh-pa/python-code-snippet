"""Binary-tree codec: preorder-with-nulls in, trimmed level-order out."""

import collections
import sys

sys.setrecursionlimit(200000)


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    n = int(toks[0])
    pre = toks[1 : 1 + n]
    vals = [None if t == "#" else int(t) for t in pre]
    pos = 0

    def build():
        nonlocal pos
        v = vals[pos]
        pos += 1
        if v is None:
            return None
        return [v, build(), build()]

    root = build()
    out = []
    dq = collections.deque([root])
    while dq:
        node = dq.popleft()
        if node is None:
            out.append("#")
        else:
            out.append(str(node[0]))
            dq.append(node[1])
            dq.append(node[2])
    while out and out[-1] == "#":
        out.pop()
    sys.stdout.write(" ".join(out))


if __name__ == "__main__":
    main()
