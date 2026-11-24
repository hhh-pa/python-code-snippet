# Pseudo-DES hashing (NR 7.2).
import sys

C1 = [0xbaa96887, 0x1e17d32c, 0x03bcdc3c, 0x0f33d1b2]
C2 = [0x4b0f3b58, 0xe874f0c3, 0x6955c5a6, 0x55a7ca46]
M32 = 0xFFFFFFFF


def psdes(lword, rword):
    for i in range(2):
        iswap = rword
        ia = iswap ^ C1[i]
        itmpl = ia & 0xFFFF
        itmph = ia >> 16
        ib = (itmpl * itmpl + (~(itmph * itmph) & M32)) & M32
        ia = (ib >> 16) | ((ib & 0xFFFF) << 16)
        rword = lword ^ (((ia ^ C2[i]) + itmpl * itmph) & M32)
        lword = iswap
    return lword, rword


def hashall(arr):
    m = len(arr)
    if m < 2:
        return arr
    n = m - 1
    n |= n >> 1
    n |= n >> 2
    n |= n >> 4
    n |= n >> 8
    n |= n >> 16
    n += 1
    nb = n
    nb2 = n >> 1
    while nb > 1:
        jb = 0
        while jb < n - nb + 1:
            for j in range(nb2):
                if jb + j + nb2 < m:
                    arr[jb + j], arr[jb + j + nb2] = psdes(arr[jb + j], arr[jb + j + nb2])
            jb += nb
        nb = nb2
        nb2 >>= 1
    nb2 = n >> 1
    if m != n:
        for j in range(nb2, m):
            arr[j], arr[j - nb2] = psdes(arr[j], arr[j - nb2])
    return arr


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    op = toks[0]
    if op == "PSDES":
        l, r = psdes(int(toks[1]), int(toks[2]))
        sys.stdout.write("%d %d\n" % (l, r))
    elif op == "HASHALL":
        m = int(toks[1])
        arr = [int(w) for w in toks[2:2 + m]]
        sys.stdout.write(" ".join(map(str, hashall(arr))) + "\n")


main()
