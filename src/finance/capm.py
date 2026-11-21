"""CAPM beta + expected return (Gestion ch 2)."""

import sys


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    n = int(toks[0])
    ris = [0.0] * n
    rms = [0.0] * n
    for i in range(n):
        ris[i] = float(toks[1 + 2 * i])
        rms[i] = float(toks[2 + 2 * i])
    rf = float(toks[1 + 2 * n])
    mi = sum(ris) / n
    mm = sum(rms) / n
    c = 0.0
    vm = 0.0
    for ri, rm in zip(ris, rms):
        di = ri - mi
        dm = rm - mm
        c += di * dm
        vm += dm * dm
    beta = 0.0 if vm == 0.0 else c / vm
    exp = rf + beta * (mm - rf)
    sys.stdout.write(f"BETA {beta:.6f}\nEXP {exp:.6f}")


if __name__ == "__main__":
    main()
