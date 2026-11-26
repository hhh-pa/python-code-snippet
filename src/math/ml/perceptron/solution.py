"""Perceptron (AIMA 19, Eq 19.8, exact rational weights)."""

import math
import sys

MOD = 1 << 31


def _run(feats, labels, updates, an, ad, seed):
    n = len(feats)
    d = len(feats[0])
    num = [0] * (d + 1)
    rng = seed
    mistakes = 0
    for _ in range(updates):
        rng = (1103515245 * rng + 12345) % MOD
        i = rng % n
        x = feats[i]
        s = num[0] + sum(num[j + 1] * x[j] for j in range(d))
        h = 1 if s >= 0 else 0
        if h != labels[i]:
            mistakes += 1
            delta = an * (labels[i] - h)
            num[0] += delta
            for j in range(d):
                num[j + 1] += delta * x[j]
    return num, mistakes


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    d, n, u, an, ad, seed = (
        int(toks[0]),
        int(toks[1]),
        int(toks[2]),
        int(toks[3]),
        int(toks[4]),
        int(toks[5]),
    )
    feats, labels = [], []
    i = 6
    for _ in range(n):
        feats.append(list(map(int, toks[i : i + d])))
        labels.append(int(toks[i + d]))
        i += d + 1
    num, mistakes = _run(feats, labels, u, an, ad, seed)
    fracs = []
    for v in num:
        g = math.gcd(v, ad)
        fracs.append(f"{v // g}/{ad // g}")
    correct = 0
    for x, y in zip(feats, labels):
        s = num[0] + sum(num[j + 1] * x[j] for j in range(d))
        if (1 if s >= 0 else 0) == y:
            correct += 1
    sys.stdout.write(" ".join(fracs) + f"\nACC {correct} {n}\nMISTAKES {mistakes}")


if __name__ == "__main__":
    main()
