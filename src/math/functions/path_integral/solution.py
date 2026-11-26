# Hypergeometric 2F1 by path integration (NR 5.14).
import math
import sys


def deriv(a, b, c, zr, zi, dzr, dzi, fr, fi, gr, gi):
    dfr = dzr * gr - dzi * gi
    dfi = dzr * gi + dzi * gr
    abr = a * b
    kr = c - (a + b + 1.0) * zr
    ki = -(a + b + 1.0) * zi
    t1r = abr * fr
    t1i = abr * fi
    t2r = kr * gr - ki * gi
    t2i = kr * gi + ki * gr
    nr = t1r - t2r
    ni = t1i - t2i
    dr = zr * (1.0 - zr) + zi * zi
    di = zi * (1.0 - zr) - zr * zi
    dd = dr * dr + di * di
    qr = (nr * dr + ni * di) / dd
    qi = (ni * dr - nr * di) / dd
    dgr = dzr * qr - dzi * qi
    dgi = dzr * qi + dzi * qr
    return dfr, dfi, dgr, dgi


def series(a, b, c, zr, zi):
    pr = 1.0
    pi = 0.0
    fr = 1.0
    fi = 0.0
    gr = 0.0
    gi = 0.0
    for j in range(1, 61):
        f = (a + j - 1) * (b + j - 1) / ((c + j - 1) * j)
        jf = j * f
        gr += jf * pr
        gi += jf * pi
        nr = (pr * zr - pi * zi) * f
        ni = (pr * zi + pi * zr) * f
        pr = nr
        pi = ni
        fr += pr
        fi += pi
    return fr, fi, gr, gi


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    a, b, c, zr, zi = (float(v) for v in toks[:5])
    r = math.sqrt(zr * zr + zi * zi)
    if r <= 0.5:
        fr, fi, _, _ = series(a, b, c, zr, zi)
    else:
        if zr < 0.0:
            z0r, z0i = -0.5, 0.0
        elif zr <= 1.0:
            z0r, z0i = 0.5, 0.0
        elif zi >= 0.0:
            z0r, z0i = 0.0, 0.5
        else:
            z0r, z0i = 0.0, -0.5
        fr, fi, gr, gi = series(a, b, c, z0r, z0i)
        dzr = zr - z0r
        dzi = zi - z0i
        nst = 800
        h = 1.0 / nst
        cr, ci = z0r, z0i
        for _ in range(nst):
            k1 = deriv(a, b, c, cr, ci, dzr, dzi, fr, fi, gr, gi)
            mr = cr + 0.5 * h * dzr
            mi = ci + 0.5 * h * dzi
            k2 = deriv(a, b, c, mr, mi, dzr, dzi, fr + 0.5 * h * k1[0], fi + 0.5 * h * k1[1],
                       gr + 0.5 * h * k1[2], gi + 0.5 * h * k1[3])
            k3 = deriv(a, b, c, mr, mi, dzr, dzi, fr + 0.5 * h * k2[0], fi + 0.5 * h * k2[1],
                       gr + 0.5 * h * k2[2], gi + 0.5 * h * k2[3])
            er = cr + h * dzr
            ei = ci + h * dzi
            k4 = deriv(a, b, c, er, ei, dzr, dzi, fr + h * k3[0], fi + h * k3[1],
                       gr + h * k3[2], gi + h * k3[3])
            fr += h * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]) / 6.0
            fi += h * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]) / 6.0
            gr += h * (k1[2] + 2 * k2[2] + 2 * k3[2] + k4[2]) / 6.0
            gi += h * (k1[3] + 2 * k2[3] + 2 * k3[3] + k4[3]) / 6.0
            cr, ci = er, ei
    if abs(fr) < 5e-7:
        fr = 0.0
    if abs(fi) < 5e-7:
        fi = 0.0
    sys.stdout.write("%.6f %.6f\n" % (fr + 0.0, fi + 0.0))


main()
