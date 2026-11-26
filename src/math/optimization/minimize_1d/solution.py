# One-dimensional minimization (NR 10.1-10.4): bracketing
# (mnbrak), golden section search, Brent's method, and
# derivative-using dBrent.
# Reference: Press et al., Numerical Recipes 3e, Sections 10.1-10.4.
# No online-judge problem found -- fixtures are self-generated
# (scipy oracle), no header link.
import math
import sys

fn = ""
fp = []


def func(t):
    if fn == "POLY":
        s = 0.0
        for i in range(len(fp) - 1, -1, -1):
            s = s * t + fp[i]
        return s
    elif fn == "TRIG":
        return fp[0] * math.sin(fp[1] * t + fp[2])
    else:
        return fp[0] * math.pow(fp[1] * t + fp[2], fp[3])


def func_df(t):
    if fn == "POLY":
        s = 0.0
        for i in range(len(fp) - 1, 0, -1):
            s = s * t + i * fp[i]
        return s
    elif fn == "TRIG":
        return fp[0] * fp[1] * math.cos(fp[1] * t + fp[2])
    else:
        return fp[0] * fp[3] * fp[1] * math.pow(fp[1] * t + fp[2], fp[3] - 1.0)


def sgn(a, b):
    return abs(a) if b >= 0.0 else -abs(a)


class Bracket:
    pass


br = Bracket()


def bracket(a, b):
    GOLD = 1.618034
    GLIMIT = 100.0
    TINY = 1.0e-20
    br.ax = a
    br.bx = b
    br.fa = func(br.ax)
    br.fb = func(br.bx)
    if br.fb > br.fa:
        br.ax, br.bx = br.bx, br.ax
        br.fb, br.fa = br.fa, br.fb
    br.cx = br.bx + GOLD * (br.bx - br.ax)
    br.fc = func(br.cx)
    while br.fb > br.fc:
        r = (br.bx - br.ax) * (br.fb - br.fc)
        q = (br.bx - br.cx) * (br.fb - br.fa)
        u = br.bx - ((br.bx - br.cx) * q - (br.bx - br.ax) * r) / (
            2.0 * sgn(max(abs(q - r), TINY), q - r))
        ulim = br.bx + GLIMIT * (br.cx - br.bx)
        if (br.bx - u) * (u - br.cx) > 0.0:
            fu = func(u)
            if fu < br.fc:
                br.ax = br.bx
                br.bx = u
                br.fa = br.fb
                br.fb = fu
                return
            elif fu > br.fb:
                br.cx = u
                br.fc = fu
                return
            u = br.cx + GOLD * (br.cx - br.bx)
            fu = func(u)
        elif (br.cx - u) * (u - ulim) > 0.0:
            fu = func(u)
            if fu < br.fc:
                br.bx, br.cx, u = br.cx, u, u + GOLD * (u - br.cx)
                br.fb, br.fc, fu = br.fc, fu, func(u)
        elif (u - ulim) * (ulim - br.cx) >= 0.0:
            u = ulim
            fu = func(u)
        else:
            u = br.cx + GOLD * (br.cx - br.bx)
            fu = func(u)
        br.ax, br.bx, br.cx = br.bx, br.cx, u
        br.fa, br.fb, br.fc = br.fb, br.fc, fu


def golden(tol):
    R = 0.61803399
    C = 1.0 - R
    x0 = br.ax
    x3 = br.cx
    if abs(br.cx - br.bx) > abs(br.bx - br.ax):
        x1 = br.bx
        x2 = br.bx + C * (br.cx - br.bx)
    else:
        x2 = br.bx
        x1 = br.bx - C * (br.bx - br.ax)
    f1 = func(x1)
    f2 = func(x2)
    while abs(x3 - x0) > tol * (abs(x1) + abs(x2)):
        if f2 < f1:
            x0, x1, x2 = x1, x2, R * x2 + C * x3
            f1, f2 = f2, func(x2)
        else:
            x3, x2, x1 = x2, x1, R * x1 + C * x0
            f2, f1 = f1, func(x1)
    if f1 < f2:
        return x1, f1
    else:
        return x2, f2


class TooMany(Exception):
    pass


def brent(tol):
    ITMAX = 100
    CGOLD = 0.3819660
    ZEPS = 2.220446049250313e-16 * 1.0e-3
    d = 0.0
    e = 0.0
    a = br.ax if br.ax < br.cx else br.cx
    b = br.ax if br.ax > br.cx else br.cx
    x = w = v = br.bx
    fw = fv = fx = func(x)
    for _ in range(ITMAX):
        xm = 0.5 * (a + b)
        tol1 = tol * abs(x) + ZEPS
        tol2 = 2.0 * tol1
        if abs(x - xm) <= (tol2 - 0.5 * (b - a)):
            return x, fx
        if abs(e) > tol1:
            r = (x - w) * (fx - fv)
            q = (x - v) * (fx - fw)
            p = (x - v) * q - (x - w) * r
            q = 2.0 * (q - r)
            if q > 0.0:
                p = -p
            q = abs(q)
            etemp = e
            e = d
            if abs(p) >= abs(0.5 * q * etemp) or p <= q * (a - x) or p >= q * (b - x):
                e = a - x if x >= xm else b - x
                d = CGOLD * e
            else:
                d = p / q
                u = x + d
                if u - a < tol2 or b - u < tol2:
                    d = sgn(tol1, xm - x)
        else:
            e = a - x if x >= xm else b - x
            d = CGOLD * e
        u = x + d if abs(d) >= tol1 else x + sgn(tol1, d)
        fu = func(u)
        if fu <= fx:
            if u >= x:
                a = x
            else:
                b = x
            v, w, x = w, x, u
            fv, fw, fx = fw, fx, fu
        else:
            if u < x:
                a = u
            else:
                b = u
            if fu <= fw or w == x:
                v = w
                w = u
                fv = fw
                fw = fu
            elif fu <= fv or v == x or v == w:
                v = u
                fv = fu
    raise TooMany()


def dbrent(tol):
    ITMAX = 100
    ZEPS = 2.220446049250313e-16 * 1.0e-3
    d = 0.0
    e = 0.0
    a = br.ax if br.ax < br.cx else br.cx
    b = br.ax if br.ax > br.cx else br.cx
    x = w = v = br.bx
    fw = fv = fx = func(x)
    dw = dv = dx = func_df(x)
    for _ in range(ITMAX):
        xm = 0.5 * (a + b)
        tol1 = tol * abs(x) + ZEPS
        tol2 = 2.0 * tol1
        if abs(x - xm) <= (tol2 - 0.5 * (b - a)):
            return x, fx
        if abs(e) > tol1:
            d1 = 2.0 * (b - a)
            d2 = d1
            if dw != dx:
                d1 = (w - x) * dx / (dx - dw)
            if dv != dx:
                d2 = (v - x) * dx / (dx - dv)
            u1 = x + d1
            u2 = x + d2
            ok1 = (a - u1) * (u1 - b) > 0.0 and dx * d1 <= 0.0
            ok2 = (a - u2) * (u2 - b) > 0.0 and dx * d2 <= 0.0
            olde = e
            e = d
            if ok1 or ok2:
                if ok1 and ok2:
                    d = d1 if abs(d1) < abs(d2) else d2
                elif ok1:
                    d = d1
                else:
                    d = d2
                if abs(d) <= abs(0.5 * olde):
                    u = x + d
                    if u - a < tol2 or b - u < tol2:
                        d = sgn(tol1, xm - x)
                else:
                    e = a - x if dx >= 0.0 else b - x
                    d = 0.5 * e
            else:
                e = a - x if dx >= 0.0 else b - x
                d = 0.5 * e
        else:
            e = a - x if dx >= 0.0 else b - x
            d = 0.5 * e
        if abs(d) >= tol1:
            u = x + d
            fu = func(u)
        else:
            u = x + sgn(tol1, d)
            fu = func(u)
            if fu > fx:
                return x, fx
        du = func_df(u)
        if fu <= fx:
            if u >= x:
                a = x
            else:
                b = x
            v, fv, dv = w, fw, dw
            w, fw, dw = x, fx, dx
            x, fx, dx = u, fu, du
        else:
            if u < x:
                a = u
            else:
                b = u
            if fu <= fw or w == x:
                v, fv, dv = w, fw, dw
                w, fw, dw = u, fu, du
            elif fu < fv or v == x or v == w:
                v, fv, dv = u, fu, du
    raise TooMany()


def fmt6(v):
    o = v
    if abs(o) < 5e-7:
        o = 0.0
    return "%.6f" % (o + 0.0)


def main():
    global fn, fp
    toks = sys.stdin.read().split()
    if not toks:
        return
    op = toks[0]
    fn = toks[1]
    p = 2
    if fn == "POLY":
        d = int(toks[p])
        p += 1
        fp = [float(toks[p + i]) for i in range(d + 1)]
        p += d + 1
    elif fn == "POW":
        fp = [float(toks[p + i]) for i in range(4)]
        p += 4
    else:
        fp = [float(toks[p + i]) for i in range(3)]
        p += 3
    a = float(toks[p])
    b = float(toks[p + 1])
    if op == "BRACKET":
        bracket(a, b)
        print(" ".join(fmt6(v) for v in (br.ax, br.bx, br.cx, br.fa, br.fb, br.fc)))
    elif op in ("GOLDEN", "BRENT", "DBRENT"):
        tol = float(toks[p + 2])
        bracket(a, b)
        try:
            if op == "GOLDEN":
                xmin, fmin = golden(tol)
            elif op == "BRENT":
                xmin, fmin = brent(tol)
            else:
                xmin, fmin = dbrent(tol)
        except TooMany:
            print("0.000000 0.000000 1")
            return
        print("%s %s 0" % (fmt6(xmin), fmt6(fmin)))


main()
