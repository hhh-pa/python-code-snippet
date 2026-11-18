"""Par swap rate + PV01 (FE ch 5)."""

import sys


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    n = int(toks[0])
    pv01 = 0.0
    dfn = 0.0
    for i in range(n):
        tau = float(toks[1 + 2 * i])
        df = float(toks[2 + 2 * i])
        pv01 += tau * df
        dfn = df
    rate = (1 - dfn) / pv01
    sys.stdout.write(f"SWAPRATE {rate:.6f}\nPV01 {pv01:.6f}")


if __name__ == "__main__":
    main()
