"""CDS hazard bootstrap + par spread (FE ch 16)."""

import math
import sys


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    rec = float(toks[0])
    r = float(toks[1])
    n = int(toks[2])
    ts = [0.0] * n
    ds = [0.0] * n
    for i in range(n):
        ts[i] = float(toks[3 + 2 * i])
        ds[i] = float(toks[4 + 2 * i])
    hazards = []
    prev_t = 0.0
    prev_s = 1.0
    prot = 0.0
    prem = 0.0
    for i in range(n):
        df = math.exp(-r * ts[i])
        s = ds[i] / df
        lam = -(math.log(s / prev_s)) / (ts[i] - prev_t)
        hazards.append(lam)
        prot += df * (prev_s - s)
        prem += (ts[i] - prev_t) * df * s
        prev_t = ts[i]
        prev_s = s
    prot *= 1 - rec
    spread = prot / prem
    out = [
        "HAZARDS " + " ".join(f"{x:.6f}" for x in hazards),
        f"SPREAD {spread:.6f}",
        f"SPREAD_BPS {spread * 10000:.6f}",
    ]
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()
