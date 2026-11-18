"""Standard error and bootstrap CIs (Think Stats 2e ch 8)."""

import math
import sys

MOD = 1 << 31


def _half_even(x):
    q = math.floor(x)
    f = x - q
    if f > 0.5:
        return q + 1
    if f < 0.5:
        return q
    return q if q % 2 == 0 else q + 1


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    n = int(toks[0])
    xs = list(map(int, toks[1 : 1 + n]))
    b = int(toks[1 + n])
    rng = int(toks[2 + n])
    mean = sum(xs) / n
    var = sum((x - mean) * (x - mean) for x in xs) / (n - 1)
    se = math.sqrt(var) / math.sqrt(n)
    lo = mean - 1.96 * se
    hi = mean + 1.96 * se
    means = []
    for _ in range(b):
        tot = 0
        for _ in range(n):
            rng = (1103515245 * rng + 12345) % MOD
            tot += xs[rng % n]
        means.append(tot / n)
    means.sort()
    blo = means[min(b, max(1, _half_even((2.5 * (b + 1)) / 100))) - 1]
    bhi = means[min(b, max(1, _half_even((97.5 * (b + 1)) / 100))) - 1]
    sys.stdout.write(f"SE {se:.6f}\nCI {lo:.6f} {hi:.6f}\nBOOT {blo:.6f} {bhi:.6f}")


if __name__ == "__main__":
    main()
