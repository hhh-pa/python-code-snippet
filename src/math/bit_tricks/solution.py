"""Integer bit tricks (exact arithmetic on values < 2^62)."""

import sys


def _solve(op, args):
    if op == "POPCOUNT":
        return bin(args[0]).count("1")
    if op == "PARITY":
        return bin(args[0]).count("1") & 1
    if op == "ISPOW2":
        return 1 if args[0] > 0 and args[0] & (args[0] - 1) == 0 else 0
    if op == "CTZ":
        x = args[0]
        return 64 if x == 0 else (x & -x).bit_length() - 1
    if op == "REVERSE":
        x, w = args
        r = 0
        for i in range(w):
            r |= ((x >> i) & 1) << (w - 1 - i)
        return r
    if op == "NEXTPOW2":
        x = args[0]
        if x <= 1:
            return 1
        return 1 << (x - 1).bit_length()
    raise ValueError(op)


def main():
    lines = sys.stdin.read().splitlines()
    if not lines:
        return
    q = int(lines[0].split()[0])
    out = []
    for i in range(1, min(q + 1, len(lines))):
        toks = lines[i].split()
        out.append(str(_solve(toks[0], [int(v) for v in toks[1:]])))
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()
