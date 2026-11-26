"""RAID-5 parity + single-disk reconstruction (MOS 5.4)."""

import sys


def _write(data, par, failed, drives, stripes, s, d, v):
    if not (0 <= s < stripes and 0 <= d < drives) or d == s % drives or d in failed:
        return "REJECTED"
    par[s] ^= data[s][d] ^ v
    data[s][d] = v
    return "OK"


def _read(data, par, failed, drives, stripes, s, d):
    if not (0 <= s < stripes and 0 <= d < drives):
        return "REJECTED"
    if d in failed and len(failed) > 1:
        return "UNRECOVERABLE"
    if d not in failed:
        return f"BYTE {par[s] if d == s % drives else data[s][d]}"
    x = 0
    for dd in range(drives):
        if dd != d:
            x ^= par[s] if dd == s % drives else data[s][dd]
    return f"BYTE {x}"


def _parity(data, par, failed, drives, stripes, s):
    if not 0 <= s < stripes:
        return "REJECTED"
    pd = s % drives
    if pd in failed and len(failed) > 1:
        return "UNRECOVERABLE"
    if pd not in failed:
        return f"PARITY {pd} {par[s]}"
    x = 0
    for dd in range(drives):
        if dd != pd:
            x ^= data[s][dd]
    return f"PARITY {pd} {x}"


def _run(drives, stripes, ops):
    data = [[0] * drives for _ in range(stripes)]
    par = [0] * stripes
    failed = set()
    out = []
    for op in ops:
        if op[0] == "W":
            out.append(_write(data, par, failed, drives, stripes, *op[1:]))
        elif op[0] == "R":
            out.append(_read(data, par, failed, drives, stripes, *op[1:]))
        elif op[0] == "F":
            if 0 <= op[1] < drives:
                failed.add(op[1])
                out.append("OK")
            else:
                out.append("REJECTED")
        else:
            out.append(_parity(data, par, failed, drives, stripes, op[1]))
    return out


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    drives, stripes, e = int(toks[0]), int(toks[1]), int(toks[2])
    ops = []
    i = 3
    for _ in range(e):
        if toks[i] == "W":
            ops.append(("W", int(toks[i + 1]), int(toks[i + 2]), int(toks[i + 3])))
            i += 4
        elif toks[i] == "R":
            ops.append(("R", int(toks[i + 1]), int(toks[i + 2])))
            i += 3
        elif toks[i] == "F":
            ops.append(("F", int(toks[i + 1])))
            i += 2
        else:
            ops.append(("P", int(toks[i + 1])))
            i += 2
    sys.stdout.write("\n".join(_run(drives, stripes, ops)))


if __name__ == "__main__":
    main()
