# Complex arithmetic (NR 5.5). Port of the C++ reference.
import math
import sys


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    op = toks[0]
    ar = float(toks[1])
    ai = float(toks[2])
    r = 0.0
    im = 0.0
    if op == "DIV":
        br = float(toks[3])
        bi = float(toks[4])
        if abs(br) >= abs(bi):
            t = bi / br
            den = br + bi * t
            r = (ar + ai * t) / den
            im = (ai - ar * t) / den
        else:
            t = br / bi
            den = bi + br * t
            r = (ar * t + ai) / den
            im = (ai * t - ar) / den
    elif op == "SQRT":
        w = 0.0
        if ar != 0.0 or ai != 0.0:
            if abs(ar) >= abs(ai):
                t = ai / ar
                w = math.sqrt(abs(ar)) * math.sqrt((1.0 + math.sqrt(1.0 + t * t)) / 2.0)
            else:
                t = ar / ai
                w = math.sqrt(abs(ai)) * math.sqrt((abs(t) + math.sqrt(1.0 + t * t)) / 2.0)
        if w == 0.0:
            r = 0.0
            im = 0.0
        elif ar >= 0.0:
            r = w
            im = ai / (2.0 * w)
        elif ai >= 0.0:
            r = abs(ai) / (2.0 * w)
            im = w
        else:
            r = abs(ai) / (2.0 * w)
            im = -w
    elif op == "EXP":
        e = math.exp(ar)
        r = e * math.cos(ai)
        im = e * math.sin(ai)
    elif op == "LOG":
        r = math.log(math.hypot(ar, ai))
        im = math.atan2(ai, ar)
    else:
        br = float(toks[3])
        bi = float(toks[4])
        lr = math.log(math.hypot(ar, ai))
        li = math.atan2(ai, ar)
        er = lr * br - li * bi
        ei = lr * bi + li * br
        e = math.exp(er)
        r = e * math.cos(ei)
        im = e * math.sin(ei)
    if abs(r) < 5e-7:
        r = 0.0
    if abs(im) < 5e-7:
        im = 0.0
    sys.stdout.write("%.6f %.6f\n" % (r + 0.0, im + 0.0))


main()
