# Sobol quasi-random sequence (NR 7.8).
import sys

MAXBIT = 30
MAXDIM = 6
MDEG = (1, 2, 3, 3, 4, 4)
IP = (0, 1, 1, 2, 1, 4)
IVINIT = (1, 1, 1, 1, 1, 1, 3, 1, 3, 3, 1, 1, 5, 7, 7, 3, 3, 5,
          15, 11, 5, 15, 13, 9)
M32 = 0xFFFFFFFF


def canon(v):
    return 0.0 if abs(v) < 5e-7 else v


def main():
    toks = sys.stdin.read().split()
    if not toks or toks[0] != "SOBOL":
        return
    dim, npoints = int(toks[1]), int(toks[2])
    ix = [0] * MAXDIM
    iu = [[0] * MAXDIM for _ in range(MAXBIT)]
    for j in range(4):
        for k in range(MAXDIM):
            iu[j][k] = IVINIT[j * MAXDIM + k]
    fac = 1.0 / (1 << MAXBIT)
    for k in range(MAXDIM):
        for j in range(MDEG[k]):
            iu[j][k] = (iu[j][k] << (MAXBIT - 1 - j)) & M32
        for j in range(MDEG[k], MAXBIT):
            ipp = IP[k]
            i = iu[j - MDEG[k]][k]
            i ^= (i >> MDEG[k])
            for l in range(MDEG[k] - 1, 0, -1):
                if ipp & 1:
                    i ^= iu[j - l][k]
                ipp >>= 1
            iu[j][k] = i & M32
    inn = 0
    lines = []
    for _ in range(npoints):
        im = inn
        inn += 1
        j = 0
        while j < MAXBIT:
            if not im & 1:
                break
            im >>= 1
            j += 1
        words = []
        for k in range(dim):
            ix[k] ^= iu[j][k]
            o = ix[k] * fac
            words.append("%.6f" % (canon(o) + 0.0))
        lines.append(" ".join(words))
    sys.stdout.write("\n".join(lines) + "\n")


main()
