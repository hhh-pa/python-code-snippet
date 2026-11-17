"""N-queens enumeration (row-by-row backtracking, lex order)."""

import sys


def main():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    cols, diag1, diag2 = set(), set(), set()
    cur = []
    out = []
    sys.setrecursionlimit(10000)

    def place(r):
        if r == n:
            out.append(" ".join(map(str, cur)))
            return
        for c in range(n):
            if c in cols or (r - c) in diag1 or (r + c) in diag2:
                continue
            cols.add(c)
            diag1.add(r - c)
            diag2.add(r + c)
            cur.append(c)
            place(r + 1)
            cur.pop()
            cols.discard(c)
            diag1.discard(r - c)
            diag2.discard(r + c)

    place(0)
    sys.stdout.write(str(len(out)) + ("\n" + "\n".join(out) if out else ""))


if __name__ == "__main__":
    main()
