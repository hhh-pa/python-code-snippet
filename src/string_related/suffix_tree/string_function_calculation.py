"""String function calculation with a suffix tree.

Max over all distinct substrings of length times occurrences.
Input: a single lowercase string token. Output: the maximum.

Direct port of src/string_related/suffix_tree/string_function_calculation.clj:
Ukkonen's online suffix-tree construction over the string plus a terminal
mark, then the answer is the max over tree nodes of string depth times
subtree leaf count. O(n) time and O(n) space.
"""

import sys


class _Node:
    __slots__ = ("link", "start", "end", "leaf", "next")

    def __init__(self, start, end, leaf):
        self.link = 0
        self.start = start
        self.end = end
        self.leaf = leaf
        self.next = {}


def _build_tree(t):
    """Suffix tree nodes for char list t via the online (Ukkonen) method."""
    nodes = [_Node(0, -1, False)]
    active = 0
    edge = 0
    alen = 0
    rem = 0
    for pos in range(len(t)):
        rem += 1
        last_new = -1
        while rem > 0:
            if alen == 0:
                edge = pos
            cur_char = t[edge]
            nxt = nodes[active].next.get(cur_char)
            if nxt is None:
                leaf = len(nodes)
                nodes.append(_Node(pos, -1, True))
                nodes[active].next[cur_char] = leaf
                if last_new != -1:
                    nodes[last_new].link = active
                last_new = -1
            else:
                nd = nodes[nxt]
                elen = (pos if nd.leaf else nd.end) - nd.start + 1
                if alen >= elen:
                    edge += elen
                    alen -= elen
                    active = nxt
                    continue
                epos = nd.start + alen
                if t[epos] == t[pos]:
                    if last_new != -1 and active != 0:
                        nodes[last_new].link = active
                    alen += 1
                    break
                split = len(nodes)
                nodes.append(_Node(nd.start, nd.start + alen - 1, False))
                leaf = len(nodes)
                nodes.append(_Node(pos, -1, True))
                nodes[active].next[cur_char] = split
                nodes[split].next[t[pos]] = leaf
                nd.start += alen
                nodes[split].next[t[epos]] = nxt
                if last_new != -1:
                    nodes[last_new].link = split
                last_new = split
            rem -= 1
            if active == 0 and alen > 0:
                alen -= 1
                edge = pos - rem + 1
            elif active != 0:
                active = nodes[active].link
    return nodes


def _tree_value(nodes, n):
    """Max over tree nodes of string depth times leaf count.

    n is the input length without the terminal mark; leaf edges stop
    before the terminal so the mark never contributes to any depth.
    """
    order = []
    stack = [0]
    while stack:
        u = stack.pop()
        order.append(u)
        stack.extend(nodes[u].next.values())
    depth = [0] * len(nodes)
    for v in order:
        dv = depth[v]
        for w in nodes[v].next.values():
            nd = nodes[w]
            if nd.leaf:
                depth[w] = dv + (n - nd.start)
            else:
                depth[w] = dv + (nd.end - nd.start + 1)
    count = [0] * len(nodes)
    ans = n
    for v in reversed(order):
        nd = nodes[v]
        if nd.leaf:
            c = 1
        else:
            c = 0
            for w in nd.next.values():
                c += count[w]
        count[v] = c
        val = depth[v] * c
        if val > ans:
            ans = val
    return ans


def string_value(s):
    """Max over distinct substrings of length times occurrences."""
    n = len(s)
    if n == 0:
        return 0
    return _tree_value(_build_tree(list(s) + ["$"]), n)


def main():
    data = sys.stdin.read()
    if not data.strip():
        return
    s = data.split()[0]
    if not all("a" <= c <= "z" for c in s):
        sys.stderr.write("error: expected a single lowercase string token\n")
        return
    sys.stdout.write(str(string_value(s)) + "\n")


if __name__ == "__main__":
    main()
