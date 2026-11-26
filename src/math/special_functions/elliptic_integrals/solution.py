# Elliptic integrals and Jacobian elliptic functions (NR 6.12).
# Including the documented sncndn /= to *= correction.
import math
import sys


def ell_rf(x, y, z):
    errtol = 0.0025
    third = 1.0 / 3.0
    c1 = 1.0 / 24.0
    c2 = 0.1
    c3 = 3.0 / 44.0
    c4 = 1.0 / 14.0
    xt, yt, zt = x, y, z
    while True:
        sqrtx = math.sqrt(xt)
        sqrty = math.sqrt(yt)
        sqrtz = math.sqrt(zt)
        alamb = sqrtx * (sqrty + sqrtz) + sqrty * sqrtz
        xt = 0.25 * (xt + alamb)
        yt = 0.25 * (yt + alamb)
        zt = 0.25 * (zt + alamb)
        ave = third * (xt + yt + zt)
        delx = (ave - xt) / ave
        dely = (ave - yt) / ave
        delz = (ave - zt) / ave
        if not max(max(abs(delx), abs(dely)), abs(delz)) > errtol:
            break
    e2 = delx * dely - delz * delz
    e3 = delx * dely * delz
    return (1.0 + (c1 * e2 - c2 - c3 * e3) * e2 + c4 * e3) / math.sqrt(ave)


def ell_rc(x, y):
    errtol = 0.0012
    third = 1.0 / 3.0
    c1 = 0.3
    c2 = 1.0 / 7.0
    c3 = 0.375
    c4 = 9.0 / 22.0
    if y > 0.0:
        xt, yt, w = x, y, 1.0
    else:
        xt = x - y
        yt = -y
        w = math.sqrt(x) / math.sqrt(xt)
    while True:
        alamb = 2.0 * math.sqrt(xt) * math.sqrt(yt) + yt
        xt = 0.25 * (xt + alamb)
        yt = 0.25 * (yt + alamb)
        ave = third * (xt + yt + yt)
        s = (yt - ave) / ave
        if not abs(s) > errtol:
            break
    return w * (1.0 + s * s * (c1 + s * (c2 + s * (c3 + s * c4)))) / math.sqrt(ave)


def ell_rd(x, y, z):
    errtol = 0.0015
    c1 = 3.0 / 14.0
    c2 = 1.0 / 6.0
    c3 = 9.0 / 22.0
    c4 = 3.0 / 26.0
    c5 = 0.25 * c3
    c6 = 1.5 * c4
    xt, yt, zt = x, y, z
    sm = 0.0
    fac = 1.0
    while True:
        sqrtx = math.sqrt(xt)
        sqrty = math.sqrt(yt)
        sqrtz = math.sqrt(zt)
        alamb = sqrtx * (sqrty + sqrtz) + sqrty * sqrtz
        sm += fac / (sqrtz * (zt + alamb))
        fac = 0.25 * fac
        xt = 0.25 * (xt + alamb)
        yt = 0.25 * (yt + alamb)
        zt = 0.25 * (zt + alamb)
        ave = 0.2 * (xt + yt + 3.0 * zt)
        delx = (ave - xt) / ave
        dely = (ave - yt) / ave
        delz = (ave - zt) / ave
        if not max(max(abs(delx), abs(dely)), abs(delz)) > errtol:
            break
    ea = delx * dely
    eb = delz * delz
    ec = ea - eb
    ed = ea - 6.0 * eb
    ee = ed + ec + ec
    return 3.0 * sm + fac * (1.0 + ed * (-c1 + c5 * ed - c6 * delz * ee)
                             + delz * (c2 * ee + delz * (-c3 * ec + delz * c4 * ea))) \
        / (ave * math.sqrt(ave))


def ell_rj(x, y, z, p):
    errtol = 0.0015
    c1 = 3.0 / 14.0
    c2 = 1.0 / 3.0
    c3 = 3.0 / 22.0
    c4 = 3.0 / 26.0
    c5 = 0.75 * c3
    c6 = 1.5 * c4
    c7 = 0.5 * c2
    c8 = c3 + c3
    sm = 0.0
    fac = 1.0
    a = b = rcx = 0.0
    if p > 0.0:
        xt, yt, zt, pt = x, y, z, p
    else:
        xt = min(min(x, y), z)
        zt = max(max(x, y), z)
        yt = x + y + z - xt - zt
        a = 1.0 / (yt - p)
        b = a * (zt - yt) * (yt - xt)
        pt = yt + b
        rho = xt * zt / yt
        tau = p * pt / yt
        rcx = ell_rc(rho, tau)
    while True:
        sqrtx = math.sqrt(xt)
        sqrty = math.sqrt(yt)
        sqrtz = math.sqrt(zt)
        alamb = sqrtx * (sqrty + sqrtz) + sqrty * sqrtz
        t1 = pt * (sqrtx + sqrty + sqrtz) + sqrtx * sqrty * sqrtz
        alpha = t1 * t1
        t2 = pt + alamb
        beta = pt * t2 * t2
        sm += fac * ell_rc(alpha, beta)
        fac = 0.25 * fac
        xt = 0.25 * (xt + alamb)
        yt = 0.25 * (yt + alamb)
        zt = 0.25 * (zt + alamb)
        pt = 0.25 * (pt + alamb)
        ave = 0.2 * (xt + yt + zt + pt + pt)
        delx = (ave - xt) / ave
        dely = (ave - yt) / ave
        delz = (ave - zt) / ave
        delp = (ave - pt) / ave
        if not max(max(abs(delx), abs(dely)), max(abs(delz), abs(delp))) > errtol:
            break
    ea = delx * (dely + delz) + dely * delz
    eb = delx * dely * delz
    ec = delp * delp
    ed = ea - 3.0 * ec
    ee = eb + 2.0 * delp * (ea - ec)
    ans = 3.0 * sm + fac * (1.0 + ed * (-c1 + c5 * ed - c6 * ee)
                            + eb * (c7 + delp * (-c8 + delp * c4))
                            + delp * ea * (c2 - delp * c3) - c2 * delp * ec) \
        / (ave * math.sqrt(ave))
    if p <= 0.0:
        ans = a * (b * ans + 3.0 * (rcx - ell_rf(xt, yt, zt)))
    return ans


def ell_f(phi, ak):
    s = math.sin(phi)
    c = math.cos(phi)
    return s * ell_rf(c * c, (1.0 - s * ak) * (1.0 + s * ak), 1.0)


def ell_e(phi, ak):
    s = math.sin(phi)
    c = math.cos(phi)
    cc = c * c
    q = (1.0 - s * ak) * (1.0 + s * ak)
    t = s * ak
    return s * (ell_rf(cc, q, 1.0) - (t * t) * ell_rd(cc, q, 1.0) / 3.0)


def ell_pi(phi, en, ak):
    s = math.sin(phi)
    c = math.cos(phi)
    enss = en * s * s
    cc = c * c
    q = (1.0 - s * ak) * (1.0 + s * ak)
    return s * (ell_rf(cc, q, 1.0) - enss * ell_rj(cc, q, 1.0, 1.0 + enss) / 3.0)


def ell_sn(uu, emmc):
    ca = 1.0e-8
    emc = emmc
    u = uu
    if emc != 0.0:
        bo = emc < 0.0
        d = 0.0
        if bo:
            d = 1.0 - emc
            emc *= -1.0 / d
            d = math.sqrt(d)
            u *= d
        a = 1.0
        dn = 1.0
        em = [0.0] * 13
        en = [0.0] * 13
        l = 0
        c = 0.0
        for i in range(13):
            l = i
            em[i] = a
            emc = math.sqrt(emc)
            en[i] = emc
            c = 0.5 * (a + emc)
            if abs(a - emc) <= ca * a:
                break
            emc *= a
            a = c
        u *= c
        sn = math.sin(u)
        cn = math.cos(u)
        if sn != 0.0:
            a = cn / sn
            c *= a
            for ii in range(l, -1, -1):
                b = em[ii]
                a *= c
                c *= dn
                dn = (en[ii] + a) / (b + a)
                a = c / b
            a = 1.0 / math.sqrt(c * c + 1.0)
            sn = a if sn >= 0.0 else -a
            cn = c * sn
        if bo:
            a = dn
            dn = cn
            cn = a
            sn /= d
        return sn, cn, dn
    cn = 1.0 / math.cosh(u)
    return math.tanh(u), cn, cn


def canon(v):
    return 0.0 if abs(v) < 5e-7 else v


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    op = toks[0]
    args = [float(w) for w in toks[1:]]
    if op == "SN":
        sn, cn, dn = ell_sn(args[0], args[1])
        sys.stdout.write("%.6f %.6f %.6f\n" % (canon(sn) + 0.0, canon(cn) + 0.0, canon(dn) + 0.0))
    else:
        if op == "RF":
            ans = ell_rf(*args[:3])
        elif op == "RD":
            ans = ell_rd(*args[:3])
        elif op == "RJ":
            ans = ell_rj(*args[:4])
        elif op == "RC":
            ans = ell_rc(*args[:2])
        elif op == "ELLF":
            ans = ell_f(*args[:2])
        elif op == "ELLE":
            ans = ell_e(*args[:2])
        elif op == "ELLPI":
            ans = ell_pi(*args[:3])
        else:
            return
        sys.stdout.write("%.6f\n" % (canon(ans) + 0.0))


main()
