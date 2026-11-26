"""fractional_cascading: Berg 5.6 nested-catalog chain search.

One binary search in the first catalog, then O(1) bridge hops per
following catalog; walk right in each catalog while entries are in
[yl:yh]. Nesting (C[i+1] subset of C[i]) makes every hop land on the
lower_bound of yl.
"""

import bisect
import sys


def main():
    data = list(map(int, sys.stdin.read().split()))
    if not data:
        return
    pos = 0
    k = data[pos]
    pos += 1
    cats = []
    for _ in range(k):
        m = data[pos]
        pos += 1
        cats.append(data[pos : pos + m])
        pos += m
    bridges = []
    for i in range(k - 1):
        nxt = cats[i + 1]
        bridges.append([bisect.bisect_left(nxt, v) for v in cats[i]] + [len(nxt)])
    q = data[pos] if pos < len(data) else 0
    pos += 1
    out_lines = []
    for _ in range(q):
        yl, yh = data[pos], data[pos + 1]
        pos += 2
        if not k:
            continue
        starts = []
        for i in range(k):
            if i == 0:
                p = bisect.bisect_left(cats[0], yl)
            else:
                p = bridges[i - 1][starts[i - 1]]
            starts.append(p)
            rep = []
            c = cats[i]
            while p < len(c) and c[p] <= yh:
                rep.append(str(c[p]))
                p += 1
            out_lines.append(str(len(rep)) + (" " + " ".join(rep) if rep else ""))
    sys.stdout.write("\n".join(out_lines))


if __name__ == "__main__":
    main()
