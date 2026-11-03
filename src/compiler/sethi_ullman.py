import sys

sys.setrecursionlimit(200000)

class Node:
    def __init__(self, leaf, label, l=None, r=None, su=1):
        self.leaf = leaf
        self.label = label
        self.l = l
        self.r = r
        self.su = su

def parse_tree(toks):
    p = 0

    def parse_node():
        nonlocal p
        if toks[p] == "(":
            p += 1
            op = toks[p]
            p += 1
            L = parse_node()
            R = parse_node()
            p += 1  # ')'
            su = (L.su + 1) if (L.su == R.su) else max(L.su, R.su)
            return Node(False, op, L, R, su)
        label = toks[p]
        p += 1
        return Node(True, label, su=1)

    return parse_node()

def order(n, out):
    if n.leaf:
        out.append(n.label)
        return
    if n.r.su > n.l.su:
        order(n.r, out)
        order(n.l, out)
    else:
        order(n.l, out)
        order(n.r, out)
    out.append(n.label)

def tokenize(line):
    toks = []
    cur = []
    for c in line:
        if c in ' \t':
            if cur:
                toks.append("".join(cur))
                cur = []
        elif c in '()':
            if cur:
                toks.append("".join(cur))
                cur = []
            toks.append(c)
        else:
            cur.append(c)
    if cur:
        toks.append("".join(cur))
    return toks

def main():
    lines = sys.stdin.read().splitlines()
    if not lines:
        return
    idx = 0
    while idx < len(lines) and not lines[idx].strip():
        idx += 1
    if idx >= len(lines):
        return
    try:
        T = int(lines[idx].strip())
    except ValueError:
        return
    idx += 1

    out = []
    for _ in range(T):
        while idx < len(lines) and not lines[idx].strip():
            idx += 1
        if idx >= len(lines):
            break
        line = lines[idx]
        idx += 1
        toks = tokenize(line)
        if not toks:
            continue
        r = parse_tree(toks)
        out.append(f"SU {r.su}")
        o = []
        order(r, o)
        out.append("ORDER " + " ".join(o))

    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
