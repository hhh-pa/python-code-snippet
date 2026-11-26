"""Cost-of-carry forwards + FRA valuation (Gestion ch 10, FE ch 3-4)."""

import math
import sys


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    s, r, q, t = map(float, toks[0:4])
    eqf = s * math.exp((r - q) * t)
    s, rd, rf, t = map(float, toks[4:8])
    fxf = s * math.exp((rd - rf) * t)
    s, r, u, y, t = map(float, toks[8:13])
    commf = s * math.exp((r + u - y) * t)
    n, tau, rm, rk, df = map(float, toks[13:18])
    frav = n * tau * (rm - rk) * df
    out = [f"EQF {eqf:.6f}", f"FXF {fxf:.6f}", f"COMMF {commf:.6f}", f"FRAV {frav:.6f}"]
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()
