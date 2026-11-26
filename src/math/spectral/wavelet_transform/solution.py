# One- and multi-dimensional discrete wavelet transform (pyramid
# algorithm) with Daubechies filters: Daub4, Daubs (DAUB4/12/20),
# and Daub4i (DAUB4 on the interval with preconditioning).
# Reference: Press et al., Numerical Recipes 3e, Section 13.11
# (wt1/wtn/Daub4/Daubs/Daub4i from wavelet.h).
# Documented decisions: n must be a power of 2 (the book's stated
# precondition; its bitmask wraparound needs it); n = 1, 2 pass
# through unchanged with flag 0 (the book's silent `n < 4`
# return); Daub4i's filt likewise no-ops below n = 8; unknown
# filter names flag (window-name precedent); wtn flags unless
# every dim >= 1 and the product is a power of 2 (equivalent to
# the book's product-only throw for positive dims); isign >= 0
# transforms, isign < 0 inverts, exactly as the book; Daub4's
# C1/C3 last digits differ from Daubs::c4's and are each kept
# verbatim (0.8365163037378077 vs ...079, -0.1294095225512603
# vs ...604).
# No online-judge problem found -- fixtures are self-generated
# (roundtrip/energy/hand-check oracle), no header link.
import sys


def fmt6(v):
    w = 0.0 if abs(v) < 5e-7 else v
    return "%.6f" % (w + 0.0)


def ispow2(n):
    return n >= 1 and (n & (n - 1)) == 0


D4_C0 = 0.4829629131445341
D4_C1 = 0.8365163037378077
D4_C2 = 0.2241438680420134
D4_C3 = -0.1294095225512603

C4 = [0.4829629131445341, 0.8365163037378079,
      0.2241438680420134, -0.1294095225512604]
C12 = [0.111540743350, 0.494623890398, 0.751133908021,
       0.315250351709, -0.226264693965, -0.129766867567,
       0.097501605587, 0.027522865530, -0.031582039318,
       0.000553842201, 0.004777257511, -0.001077301085]
C20 = [0.026670057901, 0.188176800078, 0.527201188932,
       0.688459039454, 0.281172343661, -0.249846424327,
       -0.195946274377, 0.127369340336, 0.093057364604,
       -0.071394147166, -0.029457536822, 0.033212674059,
       0.003606553567, -0.010733175483, 0.001395351747,
       0.001992405295, -0.000685856695, -0.000116466855,
       0.000093588670, -0.000013264203]


def daub4_filt(a, n, isign):
    if n < 4:
        return
    wksp = [0.0] * n
    nh = n >> 1
    if isign >= 0:
        i = 0
        j = 0
        while j < n - 3:
            wksp[i] = D4_C0 * a[j] + D4_C1 * a[j + 1] + D4_C2 * a[j + 2] + \
                D4_C3 * a[j + 3]
            wksp[i + nh] = D4_C3 * a[j] - D4_C2 * a[j + 1] + D4_C1 * a[j + 2] - \
                D4_C0 * a[j + 3]
            i += 1
            j += 2
        wksp[i] = D4_C0 * a[n - 2] + D4_C1 * a[n - 1] + D4_C2 * a[0] + \
            D4_C3 * a[1]
        wksp[i + nh] = D4_C3 * a[n - 2] - D4_C2 * a[n - 1] + D4_C1 * a[0] - \
            D4_C0 * a[1]
    else:
        wksp[0] = D4_C2 * a[nh - 1] + D4_C1 * a[n - 1] + D4_C0 * a[0] + \
            D4_C3 * a[nh]
        wksp[1] = D4_C3 * a[nh - 1] - D4_C0 * a[n - 1] + D4_C1 * a[0] - \
            D4_C2 * a[nh]
        i = 0
        j = 2
        while i < nh - 1:
            wksp[j] = D4_C2 * a[i] + D4_C1 * a[i + nh] + D4_C0 * a[i + 1] + \
                D4_C3 * a[i + nh + 1]
            j += 1
            wksp[j] = D4_C3 * a[i] - D4_C0 * a[i + nh] + D4_C1 * a[i + 1] - \
                D4_C2 * a[i + nh + 1]
            j += 1
            i += 1
    for i in range(n):
        a[i] = wksp[i]


def daubs_make(n):
    if n == 4:
        src = C4
    elif n == 12:
        src = C12
    elif n == 20:
        src = C20
    else:
        return None
    cc = list(src)
    cr = [0.0] * n
    sig = -1.0
    for i in range(n):
        cr[n - 1 - i] = sig * cc[i]
        sig = -sig
    return (n, -(n >> 1), -(n >> 1), cc, cr)


def daubs_filt(a, n, isign, tab):
    ncof, ioff, joff, cc, cr = tab
    if n < 4:
        return
    wksp = [0.0] * n
    nmod = ncof * n
    n1 = n - 1
    nh = n >> 1
    if isign >= 0:
        ii = 0
        i = 0
        while i < n:
            ni = i + 1 + nmod + ioff
            nj = i + 1 + nmod + joff
            for k in range(ncof):
                jf = n1 & (ni + k + 1)
                jr = n1 & (nj + k + 1)
                wksp[ii] += cc[k] * a[jf]
                wksp[ii + nh] += cr[k] * a[jr]
            ii += 1
            i += 2
    else:
        ii = 0
        i = 0
        while i < n:
            ai = a[ii]
            ai1 = a[ii + nh]
            ni = i + 1 + nmod + ioff
            nj = i + 1 + nmod + joff
            for k in range(ncof):
                jf = n1 & (ni + k + 1)
                jr = n1 & (nj + k + 1)
                wksp[jf] += cc[k] * ai
                wksp[jr] += cr[k] * ai1
            ii += 1
            i += 2
    for j in range(n):
        a[j] = wksp[j]


R00 = 0.603332511928053
R01 = 0.690895531839104
R02 = -0.398312997698228
R10 = -0.796543516912183
R11 = 0.546392713959015
R12 = -0.258792248333818
R20 = 0.0375174604524466
R21 = 0.457327659851769
R22 = 0.850088102549165
R23 = 0.223820356983114
R24 = -0.129222743354319
R30 = 0.0100372245644139
R31 = 0.122351043116799
R32 = 0.227428111655837
R33 = -0.836602921223654
R34 = 0.483012921773304
R43 = 0.443149049637559
R44 = 0.767556669298114
R45 = 0.374955331645687
R46 = 0.190151418429955
R47 = -0.194233407427412
R53 = 0.231557595006790
R54 = 0.401069519430217
R55 = -0.717579999353722
R56 = -0.363906959570891
R57 = 0.371718966535296
R65 = 0.230389043796969
R66 = 0.434896997965703
R67 = 0.870508753349866
R75 = -0.539822500731772
R76 = 0.801422961990337
R77 = -0.257512919478482


def daub4i_filt(a, n, isign):
    if n < 8:
        return
    wksp = [0.0] * n
    nh = n >> 1
    if isign >= 0:
        wksp[0] = R00 * a[0] + R01 * a[1] + R02 * a[2]
        wksp[nh] = R10 * a[0] + R11 * a[1] + R12 * a[2]
        wksp[1] = R20 * a[0] + R21 * a[1] + R22 * a[2] + R23 * a[3] + \
            R24 * a[4]
        wksp[nh + 1] = R30 * a[0] + R31 * a[1] + R32 * a[2] + R33 * a[3] + \
            R34 * a[4]
        i = 2
        j = 3
        while j < n - 4:
            wksp[i] = D4_C0 * a[j] + D4_C1 * a[j + 1] + D4_C2 * a[j + 2] + \
                D4_C3 * a[j + 3]
            wksp[i + nh] = D4_C3 * a[j] - D4_C2 * a[j + 1] + \
                D4_C1 * a[j + 2] - D4_C0 * a[j + 3]
            i += 1
            j += 2
        wksp[nh - 2] = R43 * a[n - 5] + R44 * a[n - 4] + R45 * a[n - 3] + \
            R46 * a[n - 2] + R47 * a[n - 1]
        wksp[n - 2] = R53 * a[n - 5] + R54 * a[n - 4] + R55 * a[n - 3] + \
            R56 * a[n - 2] + R57 * a[n - 1]
        wksp[nh - 1] = R65 * a[n - 3] + R66 * a[n - 2] + R67 * a[n - 1]
        wksp[n - 1] = R75 * a[n - 3] + R76 * a[n - 2] + R77 * a[n - 1]
    else:
        wksp[0] = R00 * a[0] + R10 * a[nh] + R20 * a[1] + R30 * a[nh + 1]
        wksp[1] = R01 * a[0] + R11 * a[nh] + R21 * a[1] + R31 * a[nh + 1]
        wksp[2] = R02 * a[0] + R12 * a[nh] + R22 * a[1] + R32 * a[nh + 1]
        if n == 8:
            wksp[3] = R23 * a[1] + R33 * a[5] + R43 * a[2] + R53 * a[6]
            wksp[4] = R24 * a[1] + R34 * a[5] + R44 * a[2] + R54 * a[6]
        else:
            wksp[3] = R23 * a[1] + R33 * a[nh + 1] + D4_C0 * a[2] + \
                D4_C3 * a[nh + 2]
            wksp[4] = R24 * a[1] + R34 * a[nh + 1] + D4_C1 * a[2] - \
                D4_C2 * a[nh + 2]
            wksp[n - 5] = D4_C2 * a[nh - 3] + D4_C1 * a[n - 3] + \
                R43 * a[nh - 2] + R53 * a[n - 2]
            wksp[n - 4] = D4_C3 * a[nh - 3] - D4_C0 * a[n - 3] + \
                R44 * a[nh - 2] + R54 * a[n - 2]
        i = 2
        j = 5
        while i < nh - 3:
            wksp[j] = D4_C2 * a[i] + D4_C1 * a[i + nh] + D4_C0 * a[i + 1] + \
                D4_C3 * a[i + nh + 1]
            j += 1
            wksp[j] = D4_C3 * a[i] - D4_C0 * a[i + nh] + D4_C1 * a[i + 1] - \
                D4_C2 * a[i + nh + 1]
            j += 1
            i += 1
        wksp[n - 3] = R45 * a[nh - 2] + R55 * a[n - 2] + R65 * a[nh - 1] + \
            R75 * a[n - 1]
        wksp[n - 2] = R46 * a[nh - 2] + R56 * a[n - 2] + R66 * a[nh - 1] + \
            R76 * a[n - 1]
        wksp[n - 1] = R47 * a[nh - 2] + R57 * a[n - 2] + R67 * a[nh - 1] + \
            R77 * a[n - 1]
    for i in range(n):
        a[i] = wksp[i]


def daub4i_condition(a, n, isign):
    if n < 4:
        return
    if isign >= 0:
        t0 = 0.324894048898962 * a[0] + 0.0371580151158803 * a[1]
        t1 = 1.00144540498130 * a[1]
        t2 = 1.08984305289504 * a[n - 2]
        t3 = -0.800813234246437 * a[n - 2] + 2.09629288435324 * a[n - 1]
    else:
        t0 = 3.07792649138669 * a[0] - 0.114204567242137 * a[1]
        t1 = 0.998556681198888 * a[1]
        t2 = 0.917563310922261 * a[n - 2]
        t3 = 0.350522032550918 * a[n - 2] + 0.477032578540915 * a[n - 1]
    a[0] = t0
    a[1] = t1
    a[n - 2] = t2
    a[n - 1] = t3


def apply_filt(a, n, isign, f, tab):
    if f == "DAUB4":
        daub4_filt(a, n, isign)
    elif f in ("DAUBS4", "DAUBS12", "DAUBS20"):
        daubs_filt(a, n, isign, tab)
    elif f == "DAUB4I":
        daub4i_filt(a, n, isign)


def apply_condition(a, n, isign, f):
    if f == "DAUB4I":
        daub4i_condition(a, n, isign)


def wt1(a, isign, f, tab):
    n = len(a)
    if n < 4:
        return
    if isign >= 0:
        apply_condition(a, n, 1, f)
        nn = n
        while nn >= 4:
            apply_filt(a, nn, isign, f, tab)
            nn >>= 1
    else:
        nn = 4
        while nn <= n:
            apply_filt(a, nn, isign, f, tab)
            nn <<= 1
        apply_condition(a, n, -1, f)


def wtn(a, nn, isign, f, tab):
    ntot = 1
    for d in nn:
        ntot *= d
    if not ispow2(ntot):
        raise ValueError("lengths must be powers of 2")
    nprev = 1
    for dim in nn:
        n = dim
        wksp = [0.0] * n
        nnew = n * nprev
        if n > 4:
            i2 = 0
            while i2 < ntot:
                for i1 in range(nprev):
                    i3 = i1 + i2
                    for k in range(n):
                        wksp[k] = a[i3]
                        i3 += nprev
                    if isign >= 0:
                        apply_condition(wksp, n, 1, f)
                        nt = n
                        while nt >= 4:
                            apply_filt(wksp, nt, isign, f, tab)
                            nt >>= 1
                    else:
                        nt = 4
                        while nt <= n:
                            apply_filt(wksp, nt, isign, f, tab)
                            nt <<= 1
                        apply_condition(wksp, n, -1, f)
                    i3 = i1 + i2
                    for k in range(n):
                        a[i3] = wksp[k]
                        i3 += nprev
                i2 += nnew
        nprev = nnew


def emit(a, flag):
    print(" ".join([fmt6(v) for v in a] + [str(flag)]))


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    op = toks[0]
    if op == "WT1":
        n = int(toks[1])
        f = toks[2]
        isign = int(toks[3])
        shapeok = 1 <= n <= 1048576
        ok = shapeok and f in ("DAUB4", "DAUBS4", "DAUBS12", "DAUBS20",
                               "DAUB4I") and ispow2(n)
        if ok:
            a = [float(t) for t in toks[4:4 + n]]
            tab = None
            if f == "DAUBS4":
                tab = daubs_make(4)
            elif f == "DAUBS12":
                tab = daubs_make(12)
            elif f == "DAUBS20":
                tab = daubs_make(20)
            wt1(a, isign, f, tab)
            emit(a, 0)
        else:
            emit([0.0] * (n if shapeok else 0), 1)
    elif op == "WTN":
        ndim = int(toks[1])
        nn = [int(t) for t in toks[2:2 + max(ndim, 0)]]
        f = toks[2 + max(ndim, 0)]
        isign = int(toks[3 + max(ndim, 0)])
        prod = 1
        dimsok = ndim >= 1
        for d in nn:
            if d < 1 or prod > 1048576 // d:
                dimsok = False
                break
            prod *= d
        ok = dimsok and f in ("DAUB4", "DAUBS4", "DAUBS12", "DAUBS20",
                              "DAUB4I") and ispow2(prod)
        if ok:
            base = 4 + max(ndim, 0)
            a = [float(t) for t in toks[base:base + prod]]
            tab = None
            if f == "DAUBS4":
                tab = daubs_make(4)
            elif f == "DAUBS12":
                tab = daubs_make(12)
            elif f == "DAUBS20":
                tab = daubs_make(20)
            try:
                wtn(a, nn, isign, f, tab)
                emit(a, 0)
            except ValueError:
                emit([0.0] * prod, 1)
        else:
            emit([0.0] * (prod if dimsok else 0), 1)


main()
