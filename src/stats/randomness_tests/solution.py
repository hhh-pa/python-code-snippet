import sys


def main():
    bits = sys.stdin.read().strip()
    n = len(bits)
    if n == 0:
        return
    ones = bits.count("1")
    nibs = [0] * 16
    for i in range(0, n, 4):
        nibs[int(bits[i : i + 4], 2)] += 1
    runs, cur, longrun, curlen = 1, bits[0], 0, 1
    for b in bits[1:]:
        if b == cur:
            curlen += 1
        else:
            if cur == "1":
                longrun = max(longrun, curlen)
            runs += 1
            cur, curlen = b, 1
    if cur == "1":
        longrun = max(longrun, curlen)
    bcount = [0] * 256
    for i in range(0, n, 8):
        bcount[int(bits[i : i + 8], 2)] += 1
    poker_sq = sum(v * v for v in nibs)
    byte_sq = sum(v * v for v in bcount)
    sys.stdout.write(f"{n} {ones} {poker_sq} {runs} {longrun} {byte_sq}")


if __name__ == "__main__":
    main()
