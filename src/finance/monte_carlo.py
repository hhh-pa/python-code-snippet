"""Monte Carlo GBM option pricing (FRM ch 4)."""

import math
import sys

MASK = 0xFFFFFFFFFFFFFFFF
A = 6364136223846793005
C = 1442695040888963407
DEN = 9007199254740992.0


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    s0 = float(toks[0])
    k = float(toks[1])
    t = float(toks[2])
    r = float(toks[3])
    sg = float(toks[4])
    m = int(toks[5])
    st = int(toks[6])
    zs = []
    while len(zs) < m:
        st = (st * A + C) & MASK
        u1 = ((st >> 11) + 1) / DEN
        st = (st * A + C) & MASK
        u2 = ((st >> 11) + 1) / DEN
        rad = math.sqrt(-2.0 * math.log(u1))
        ang = (2.0 * math.pi) * u2
        zs.append(rad * math.cos(ang))
        if len(zs) < m:
            zs.append(rad * math.sin(ang))
    drift = (r - sg * sg / 2) * t
    vol = sg * math.sqrt(t)
    tot_c = 0.0
    tot_p = 0.0
    for z in zs:
        sp = s0 * math.exp(drift + vol * z)
        sm = s0 * math.exp(drift + vol * -z)
        tot_c += max(sp - k, 0.0)
        tot_c += max(sm - k, 0.0)
        tot_p += max(k - sp, 0.0)
        tot_p += max(k - sm, 0.0)
    disc = math.exp(-r * t)
    call = disc * (tot_c / (2 * m))
    put = disc * (tot_p / (2 * m))
    sys.stdout.write(f"CALL {call:.6f}\nPUT {put:.6f}")


if __name__ == "__main__":
    main()
