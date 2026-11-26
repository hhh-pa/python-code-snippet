# Gamma/beta/factorial/binomial (NR 6.1).
import math
import sys

GCOF = [57.1562356658629235, -59.5979603554754912, 14.1360979747417471,
        -0.491913816097620199, 0.339946499848118887e-4, 0.465236289270485756e-4,
        -0.983744753048795646e-4, 0.158088703224912494e-3, -0.210264441724104883e-3,
        0.217439618115212643e-3, -0.164318106536763890e-3, 0.844182239838527433e-4,
        -0.261908384015814087e-4, 0.368991826595316234e-5]


def gammln(xx):
    y = xx
    x = xx
    tmp = x + 5.2421875000000000
    tmp = (x + 0.5) * math.log(tmp) - tmp
    ser = 0.999999999999997092
    for j in range(14):
        y += 1.0
        ser += GCOF[j] / y
    return tmp + math.log(2.5066282746310005 * ser / x)


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    op = toks[0]
    fact = [0.0] * 171
    fact[0] = 1.0
    for i in range(1, 171):
        fact[i] = i * fact[i - 1]
    factl = [gammln(i + 1.0) for i in range(2000)]
    if op == "GAMMALN":
        ans = gammln(float(toks[1]))
    elif op == "GAMMA":
        ans = math.exp(gammln(float(toks[1])))
    elif op == "BETA":
        z = float(toks[1])
        w = float(toks[2])
        ans = math.exp(gammln(z) + gammln(w) - gammln(z + w))
    elif op == "FACT":
        ans = fact[int(toks[1])]
    elif op == "FACTLN":
        n = int(toks[1])
        ans = factl[n] if n < 2000 else gammln(n + 1.0)
    else:
        n = int(toks[1])
        k = int(toks[2])
        if n < 171:
            ans = math.floor(0.5 + fact[n] / (fact[k] * fact[n - k]))
        else:
            ans = math.floor(0.5 + math.exp(factl[n] - factl[k] - factl[n - k]))
    w = 0.0 if abs(ans) < 5e-7 else ans
    sys.stdout.write("%.6f\n" % (w + 0.0))


main()
