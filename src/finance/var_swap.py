"""Variance-swap replication strike (FE ch 14)."""

import math
import sys


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    t = float(toks[0])
    r = float(toks[1])
    fwd = float(toks[2])
    m = int(toks[3])
    ks = [0.0] * m
    calls = [0.0] * m
    puts = [0.0] * m
    for i in range(m):
        ks[i] = float(toks[4 + 3 * i])
        calls[i] = float(toks[5 + 3 * i])
        puts[i] = float(toks[6 + 3 * i])
    k0 = ks[0]
    for k in ks:
        if k <= fwd:
            k0 = k
    acc = 0.0
    for i in range(m):
        if i == 0:
            dk = ks[1] - ks[0]
        elif i == m - 1:
            dk = ks[m - 1] - ks[m - 2]
        else:
            dk = (ks[i + 1] - ks[i - 1]) / 2
        if ks[i] < k0:
            q = puts[i]
        elif ks[i] > k0:
            q = calls[i]
        else:
            q = (calls[i] + puts[i]) / 2
        acc += dk / (ks[i] * ks[i]) * q
    adj = fwd / k0 - 1
    kvar = (2 * math.exp(r * t) / t) * acc - (adj * adj) / t
    vol = math.sqrt(max(kvar, 0.0))
    sys.stdout.write(f"VARSTRIKE {kvar:.6f}\nVOLSTRIKE {vol:.6f}")


if __name__ == "__main__":
    main()
