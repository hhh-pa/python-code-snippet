"""Least squares fit + R^2 (Think Stats 2e ch 10)."""

import sys


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    n = int(toks[0])
    xs = [0] * n
    ys = [0] * n
    for i in range(n):
        xs[i] = int(toks[1 + 2 * i])
        ys[i] = int(toks[2 + 2 * i])
    mx = sum(xs) / n
    my = sum(ys) / n
    c = 0.0
    vx = 0.0
    for x, y in zip(xs, ys):
        dx = x - mx
        dy = y - my
        c += dx * dy
        vx += dx * dx
    if vx == 0.0:
        slope, inter, r2 = 0.0, my, 0.0
    else:
        slope = c / vx
        inter = my - slope * mx
        ssres = 0.0
        sstot = 0.0
        for x, y in zip(xs, ys):
            pred = slope * x + inter
            r = y - pred
            ssres += r * r
            d = y - my
            sstot += d * d
        r2 = 0.0 if sstot == 0.0 else 1 - ssres / sstot
    sys.stdout.write(f"SLOPE {slope:.6f}\nINTER {inter:.6f}\nRSQ {r2:.6f}")


if __name__ == "__main__":
    main()
