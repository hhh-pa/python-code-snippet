# Quadratic and cubic equations (NR 5.6).
import math
import sys


def fmt2(r, im):
    a = 0.0 if abs(r) < 5e-7 else r
    b = 0.0 if abs(im) < 5e-7 else im
    return "%.6f %.6f" % (a + 0.0, b + 0.0)


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    op = toks[0]
    if op == "QUAD":
        a, b, c = float(toks[1]), float(toks[2]), float(toks[3])
        disc = b * b - 4 * a * c
        if disc >= 0.0:
            sq = math.sqrt(disc)
            q = -0.5 * (b + (-sq if b < 0.0 else sq))
            if q == 0.0:
                x1 = x2 = 0.0
            else:
                x1 = q / a
                x2 = c / q
            sys.stdout.write(fmt2(x1, 0.0) + "\n" + fmt2(x2, 0.0) + "\n")
        else:
            sr = 0.0
            si = math.sqrt(-disc)
            if b * sr < 0.0:
                sr = -sr
                si = -si
            qr = -0.5 * (b + sr)
            qi = -0.5 * si
            if qr == 0.0 and qi == 0.0:
                sys.stdout.write(fmt2(0.0, 0.0) + "\n" + fmt2(0.0, 0.0) + "\n")
            else:
                den = qr * qr + qi * qi
                sys.stdout.write(fmt2(qr / a, qi / a) + "\n")
                sys.stdout.write(fmt2(c * qr / den, -c * qi / den) + "\n")
    elif op == "CUBIC":
        a, b, c = float(toks[1]), float(toks[2]), float(toks[3])
        q = (a * a - 3 * b) / 9.0
        r = (2 * a * a * a - 9 * a * b + 27 * c) / 54.0
        if r * r < q * q * q:
            th = math.acos(max(-1.0, min(1.0, r / math.sqrt(q * q * q))))
            s = -2 * math.sqrt(q)
            sys.stdout.write(fmt2(s * math.cos(th / 3) - a / 3, 0.0) + "\n")
            sys.stdout.write(fmt2(s * math.cos((th + 2 * math.pi) / 3) - a / 3, 0.0) + "\n")
            sys.stdout.write(fmt2(s * math.cos((th - 2 * math.pi) / 3) - a / 3, 0.0) + "\n")
        else:
            sq = math.sqrt(max(0.0, r * r - q * q * q))
            av = (-1.0 if r < 0.0 else 1.0)
            av = -av * math.pow(abs(r) + sq, 1.0 / 3.0)
            bv = 0.0 if av == 0.0 else q / av
            x1 = av + bv - a / 3
            re = -0.5 * (av + bv) - a / 3
            im = math.sqrt(3.0) / 2 * (av - bv)
            sys.stdout.write(fmt2(x1, 0.0) + "\n")
            sys.stdout.write(fmt2(re, im) + "\n")
            sys.stdout.write(fmt2(re, -im) + "\n")
    elif op == "ASINH":
        x = float(toks[1])
        if x >= 0.0:
            v = math.log(x + math.sqrt(x * x + 1))
        else:
            v = -math.log(-x + math.sqrt(x * x + 1))
        w = 0.0 if abs(v) < 5e-7 else v
        sys.stdout.write("%.6f\n" % (w + 0.0))
    else:
        x = float(toks[1])
        v = math.log(x + math.sqrt(x * x - 1))
        w = 0.0 if abs(v) < 5e-7 else v
        sys.stdout.write("%.6f\n" % (w + 0.0))


main()
