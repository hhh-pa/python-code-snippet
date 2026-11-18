"""Pupils, windows, vignetting (geom ch 5)."""

import sys


def _snap(x):
    return 0.0 if abs(x) < 5e-7 else x


def _image(a, b, c, d, z_end, rim, forward):
    if d == 0.0:
        if b > 0.0:
            sp = 1e15
        elif b < 0.0:
            sp = -1e15
        else:
            sp = 1e15
    elif forward:
        sp = -b / d
    else:
        sp = b / d
    if forward:
        z = z_end + sp
        mag = a + sp * c
    else:
        z = z_end - sp
        mag = a - sp * c
    return z, abs(mag) * rim


def _chain(zs, fs, order, zstart, forward):
    a, b, c, d = 1.0, 0.0, 0.0, 1.0
    zcur = zstart
    for i in order:
        dz = zs[i] - zcur
        a += c * dz
        b += d * dz
        if fs[i] != 0.0:
            if forward:
                c -= a / fs[i]
                d -= b / fs[i]
            else:
                c += a / fs[i]
                d += b / fs[i]
        zcur = zs[i]
    return a, b, c, d, zcur


def _vignette(zs, fs, aps, ho, zo, s):
    uc = (0.0 - ho) / (zs[s] - zo)
    up = (aps[s] - ho) / (zs[s] - zo)
    um = (-aps[s] - ho) / (zs[s] - zo)
    hc, hp, hm = ho, ho, ho
    vuc, vup, vum = uc, up, um
    zcur = zo
    vig = 1.0
    for i in range(len(zs)):
        dz = zs[i] - zcur
        hc += vuc * dz
        hp += vup * dz
        hm += vum * dz
        bw = max(abs(hp - hc), abs(hm - hc))
        f = 1.0 if bw == 0.0 else (aps[i] - abs(hc)) / bw
        if f < vig:
            vig = f
        if fs[i] != 0.0:
            vuc -= hc / fs[i]
            vup -= hp / fs[i]
            vum -= hm / fs[i]
        zcur = zs[i]
    return max(0.0, min(1.0, vig))


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    ho = float(toks[0])
    zo = float(toks[1])
    n = int(toks[2])
    zs = [0.0] * n
    fs = [0.0] * n
    aps = [0.0] * n
    for i in range(n):
        zs[i] = float(toks[3 + 3 * i])
        fs[i] = float(toks[4 + 3 * i])
        aps[i] = float(toks[5 + 3 * i])
    s = int(toks[3 + 3 * n])
    w = int(toks[4 + 3 * n])
    a, b, c, d, zcur = _chain(zs, fs, range(s - 1, -1, -1), zs[s], False)
    enz, enr = _image(a, b, c, d, zcur, aps[s], False)
    a, b, c, d, zcur = _chain(zs, fs, range(s + 1, n), zs[s], True)
    exz, exr = _image(a, b, c, d, zcur, aps[s], True)
    a, b, c, d, zcur = _chain(zs, fs, range(w - 1, -1, -1), zs[w], False)
    wnz, wnr = _image(a, b, c, d, zcur, aps[w], False)
    vig = _vignette(zs, fs, aps, ho, zo, s)
    out = [
        f"ENPUPIL {_snap(enz):.6f} {_snap(enr):.6f}",
        f"EXPUPIL {_snap(exz):.6f} {_snap(exr):.6f}",
        f"ENWINDOW {_snap(wnz):.6f} {_snap(wnr):.6f}",
        f"VIG {_snap(vig):.6f}",
    ]
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()
