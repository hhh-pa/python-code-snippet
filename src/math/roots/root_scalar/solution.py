# Scalar root finding (NR 9.1-9.4).
import math
import sys


class Funcs:
    def __init__(self, name, p):
        self.name = name
        self.p = p

    def func(self, t):
        if self.name == "POLY":
            s = 0.0
            for i in range(len(self.p) - 1, -1, -1):
                s = s * t + self.p[i]
            return s
        elif self.name == "EXP":
            return self.p[0] * math.exp(self.p[1] * t) + self.p[2]
        elif self.name == "TRIG":
            return self.p[0] * math.sin(self.p[1] * t + self.p[2])
        elif self.name == "LOG":
            return self.p[0] * math.log(self.p[1] * t + self.p[2])
        return self.p[0] * math.pow(self.p[1] * t + self.p[2], self.p[3])

    def funcd(self, t):
        if self.name == "POLY":
            s = 0.0
            for i in range(len(self.p) - 1, 0, -1):
                s = s * t + i * self.p[i]
            return s
        elif self.name == "EXP":
            return self.p[0] * self.p[1] * math.exp(self.p[1] * t)
        elif self.name == "TRIG":
            return self.p[0] * self.p[1] * math.cos(self.p[1] * t + self.p[2])
        elif self.name == "LOG":
            return self.p[0] * self.p[1] / (self.p[1] * t + self.p[2])
        return self.p[0] * self.p[3] * self.p[1] * \
            math.pow(self.p[1] * t + self.p[2], self.p[3] - 1.0)


def rtbis(f, x1, x2, xacc):
    fv = f.func(x1)
    fmid0 = f.func(x2)
    if fv * fmid0 >= 0.0:
        return 0.0, 1
    if fv < 0.0:
        dx = x2 - x1
        rtb = x1
    else:
        dx = x1 - x2
        rtb = x2
    for _ in range(50):
        dx *= 0.5
        xmid = rtb + dx
        fmid = f.func(xmid)
        if fmid <= 0.0:
            rtb = xmid
        if abs(dx) < xacc or fmid == 0.0:
            return rtb, 0
    return rtb, 1


def rtflsp(f, x1, x2, xacc):
    fl = f.func(x1)
    fh = f.func(x2)
    if fl * fh > 0.0:
        return 0.0, 1
    if fl < 0.0:
        xl, xh = x1, x2
    else:
        xl, xh = x2, x1
        fl, fh = fh, fl
    dx = xh - xl
    rtf = xl
    for _ in range(30):
        rtf = xl + dx * fl / (fl - fh)
        fv = f.func(rtf)
        if fv < 0.0:
            dele = xl - rtf
            xl, fl = rtf, fv
        else:
            dele = xh - rtf
            xh, fh = rtf, fv
        dx = xh - xl
        if abs(dele) < xacc or fv == 0.0:
            return rtf, 0
    return rtf, 1


def rtsec(f, x1, x2, xacc):
    fl = f.func(x1)
    fv = f.func(x2)
    if abs(fl) < abs(fv):
        rts, xl = x1, x2
        fl, fv = fv, fl
    else:
        xl, rts = x1, x2
    for _ in range(30):
        dx = (xl - rts) * fv / (fv - fl)
        xl, fl = rts, fv
        rts += dx
        fv = f.func(rts)
        if abs(dx) < xacc or fv == 0.0:
            return rts, 0
    return rts, 1


def signb(a, b):
    return abs(a) * (1.0 if b >= 0.0 else -1.0)


def zriddr(f, x1, x2, xacc):
    fl = f.func(x1)
    fh = f.func(x2)
    if not ((fl > 0.0 and fh < 0.0) or (fl < 0.0 and fh > 0.0)):
        if fl == 0.0:
            return x1, 0
        if fh == 0.0:
            return x2, 0
        return 0.0, 1
    xl, xh = x1, x2
    ans = -9.99e99
    for _ in range(60):
        xm = 0.5 * (xl + xh)
        fm = f.func(xm)
        s = math.sqrt(fm * fm - fl * fh)
        if s == 0.0:
            return ans, 0
        xnew = xm + (xm - xl) * ((1.0 if fl >= fh else -1.0) * fm / s)
        if abs(xnew - ans) <= xacc:
            return ans, 0
        ans = xnew
        fnew = f.func(ans)
        if fnew == 0.0:
            return ans, 0
        if signb(fm, fnew) != fm:
            xl, xh, fl, fh = xm, ans, fm, fnew
        elif signb(fl, fnew) != fl:
            xh, fh = ans, fnew
        else:
            xl, fl = ans, fnew
        if abs(xh - xl) <= xacc:
            return ans, 0
    return ans, 1


def zbrent(f, x1, x2, tol):
    eps = 2.220446049250313e-16
    a, b, c = x1, x2, x2
    d = e = 0.0
    fa, fb = f.func(a), f.func(b)
    if (fa > 0.0 and fb > 0.0) or (fa < 0.0 and fb < 0.0):
        return 0.0, 1
    fc = fb
    for _ in range(100):
        if (fb > 0.0 and fc > 0.0) or (fb < 0.0 and fc < 0.0):
            c, fc = a, fa
            e = d = b - a
        if abs(fc) < abs(fb):
            a, b, c, fa, fb, fc = b, c, a, fb, fc, fa
        tol1 = 2.0 * eps * abs(b) + 0.5 * tol
        xm = 0.5 * (c - b)
        if abs(xm) <= tol1 or fb == 0.0:
            return b, 0
        if abs(e) >= tol1 and abs(fa) > abs(fb):
            s = fb / fa
            if a == c:
                p = 2.0 * xm * s
                q = 1.0 - s
            else:
                q = fa / fc
                r = fb / fc
                p = s * (2.0 * xm * q * (q - r) - (b - a) * (r - 1.0))
                q = (q - 1.0) * (r - 1.0) * (s - 1.0)
            if p > 0.0:
                q = -q
            p = abs(p)
            min1 = 3.0 * xm * q - abs(tol1 * q)
            min2 = abs(e * q)
            if 2.0 * p < (min1 if min1 < min2 else min2):
                e, d = d, p / q
            else:
                d = e = xm
        else:
            d = e = xm
        a, fa = b, fb
        if abs(d) > tol1:
            b += d
        else:
            b += abs(tol1) * (1.0 if xm >= 0.0 else -1.0)
        fb = f.func(b)
    return b, 1


def rtnewt(f, x1, x2, xacc):
    rtn = 0.5 * (x1 + x2)
    for _ in range(20):
        fv = f.func(rtn)
        dv = f.funcd(rtn)
        dx = fv / dv
        rtn -= dx
        if (x1 - rtn) * (rtn - x2) < 0.0:
            return 0.0, 1
        if abs(dx) < xacc:
            return rtn, 0
    return rtn, 1


def rtsafe(f, x1, x2, xacc):
    fl = f.func(x1)
    fh = f.func(x2)
    if (fl > 0.0 and fh > 0.0) or (fl < 0.0 and fh < 0.0):
        return 0.0, 1
    if fl == 0.0:
        return x1, 0
    if fh == 0.0:
        return x2, 0
    xl, xh = (x1, x2) if fl < 0.0 else (x2, x1)
    rts = 0.5 * (x1 + x2)
    dxold = dx = abs(x2 - x1)
    fv = f.func(rts)
    dv = f.funcd(rts)
    for _ in range(100):
        if ((rts - xh) * dv - fv) * ((rts - xl) * dv - fv) > 0.0 \
                or abs(2.0 * fv) > abs(dxold * dv):
            dxold = dx
            dx = 0.5 * (xh - xl)
            rts = xl + dx
            if xl == rts:
                return rts, 0
        else:
            dxold = dx
            dx = fv / dv
            temp = rts
            rts -= dx
            if temp == rts:
                return rts, 0
        if abs(dx) < xacc:
            return rts, 0
        fv = f.func(rts)
        dv = f.funcd(rts)
        if fv < 0.0:
            xl = rts
        else:
            xh = rts
    return rts, 1


def canon(v):
    return 0.0 if abs(v) < 5e-7 else v


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    op = toks[0]
    name = toks[1]
    p = 2
    if name == "POLY":
        d = int(toks[p])
        fp = [float(w) for w in toks[p + 1:p + 2 + d]]
        p += 2 + d
    elif name == "POW":
        fp = [float(w) for w in toks[p:p + 4]]
        p += 4
    else:
        fp = [float(w) for w in toks[p:p + 3]]
        p += 3
    x1, x2, xacc = float(toks[p]), float(toks[p + 1]), float(toks[p + 2])
    f = Funcs(name, fp)
    if op == "BISECT":
        ans, flag = rtbis(f, x1, x2, xacc)
    elif op == "SECANT":
        ans, flag = rtsec(f, x1, x2, xacc)
    elif op == "FALSEPOS":
        ans, flag = rtflsp(f, x1, x2, xacc)
    elif op == "RIDDER":
        ans, flag = zriddr(f, x1, x2, xacc)
    elif op == "BRENT":
        ans, flag = zbrent(f, x1, x2, xacc)
    elif op == "NEWTON":
        ans, flag = rtnewt(f, x1, x2, xacc)
    elif op == "RTSAFE":
        ans, flag = rtsafe(f, x1, x2, xacc)
    else:
        return
    if flag:
        sys.stdout.write("0.000000 1\n")
    else:
        sys.stdout.write("%.6f 0\n" % (canon(ans) + 0.0))


main()
