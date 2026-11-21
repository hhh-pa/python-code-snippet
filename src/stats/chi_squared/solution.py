"""Chi-squared tests (Think Stats 2e ch 14)."""

import sys


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    if toks[0] == "GOF":
        k = int(toks[1])
        obs = list(map(int, toks[2 : 2 + k]))
        probs = list(map(float, toks[2 + k : 2 + 2 * k]))
        n = sum(obs)
        stat = 0.0
        for o, pr in zip(obs, probs):
            e = n * pr
            d = o - e
            stat += (d * d) / e
        sys.stdout.write(f"STAT {stat:.6f}\nDOF {k - 1}")
    else:
        r = int(toks[1])
        c = int(toks[2])
        cells = list(map(int, toks[3 : 3 + r * c]))
        total = sum(cells)
        rows = [sum(cells[i * c : (i + 1) * c]) for i in range(r)]
        cols = [sum(cells[i::c]) for i in range(c)]
        stat = 0.0
        for i in range(r):
            for j in range(c):
                e = (rows[i] * cols[j]) / total
                if e == 0.0:
                    continue
                d = cells[i * c + j] - e
                stat += (d * d) / e
        sys.stdout.write(f"STAT {stat:.6f}\nDOF {(r - 1) * (c - 1)}")


if __name__ == "__main__":
    main()
