# Maximum-entropy (all-poles) power spectrum from Burg LP
# coefficients by evaluating the prediction-error filter on the
# unit circle.
# Reference: Press et al., Numerical Recipes 3e, Section 13.8
# (evlmem; takes memcof-style (d, xms) as explicit input).
# Documented decisions: the book's literal 6.28318530717959 is
# used verbatim for theta; a zero denominator is unguarded in
# the book (fixtures keep it positive).
# No online-judge problem found -- fixtures are self-generated
# (numpy oracle), no header link.
import math
import sys


def evlmem(fdt, d, xms):
    sumr = 1.0
    sumi = 0.0
    wr = 1.0
    wi = 0.0
    m = len(d)
    theta = 6.28318530717959 * fdt
    wtemp = math.sin(0.5 * theta)
    wpr = -2.0 * wtemp * wtemp
    wpi = math.sin(theta)
    for i in range(m):
        wtemp = wr
        wr = wtemp * wpr - wi * wpi + wr
        wi = wi * wpr + wtemp * wpi + wi
        sumr -= d[i] * wr
        sumi -= d[i] * wi
    return xms / (sumr * sumr + sumi * sumi)


def fmt6(v):
    o = v
    if abs(o) < 5e-7:
        o = 0.0
    return "%.6f" % (o + 0.0)


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    op = toks[0]
    if op == "MEMSPEC":
        m = int(toks[1])
        k = int(toks[2])
        d = [float(t) for t in toks[3:3 + max(0, m)]]
        xms = float(toks[3 + max(0, m)])
        f = [float(t) for t in toks[4 + max(0, m):4 + max(0, m) + max(0, k)]]
        parts = [fmt6(evlmem(ff, d, xms)) for ff in f]
        parts.append("0")
        print(" ".join(parts))


main()
