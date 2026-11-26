"""Distribution fitting (Think Stats 2e ch 5)."""

import math
import sys


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    n, nb = int(toks[0]), int(toks[1])
    xs = list(map(float, toks[2 : 2 + n]))
    mean = sum(xs) / n
    var = sum((x - mean) * (x - mean) for x in xs) / (n - 1)
    logs = [math.log10(x) for x in xs]
    lmean = sum(logs) / n
    lvar = sum((x - lmean) * (x - lmean) for x in logs) / (n - 1)
    out = [
        f"BINOMIAL {mean / nb:.6f}",
        f"POISSON {mean:.6f}",
        f"EXPONENTIAL {1 / mean:.6f}",
        f"NORMAL {mean:.6f} {math.sqrt(var):.6f}",
        f"LOGNORMAL {lmean:.6f} {math.sqrt(lvar):.6f}",
    ]
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()
