"""DCF + Gordon DDM valuation (Gestion ch 7-9)."""

import sys


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    r = float(toks[0])
    g = float(toks[1])
    n = int(toks[2])
    fcfs = list(map(float, toks[3 : 3 + n]))
    d1 = float(toks[3 + n])
    df = 1.0
    pv = 0.0
    for fcf in fcfs:
        df *= 1 + r
        pv += fcf / df
    tv = fcfs[-1] * (1 + g) / (r - g)
    dcf = pv + tv / df
    ddm = d1 / (r - g)
    sys.stdout.write(f"DCF {dcf:.6f}\nDDM {ddm:.6f}")


if __name__ == "__main__":
    main()
