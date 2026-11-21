import sys


def _qr(a, b, c, d):
    m = 0xFFFFFFFF
    a = (a + b) & m
    d ^= a
    d = ((d << 16) | (d >> 16)) & m
    c = (c + d) & m
    b ^= c
    b = ((b << 12) | (b >> 20)) & m
    a = (a + b) & m
    d ^= a
    d = ((d << 8) | (d >> 24)) & m
    c = (c + d) & m
    b ^= c
    b = ((b << 7) | (b >> 25)) & m
    return a, b, c, d


def _block(key, counter, nonce):
    st = [0x61707865, 0x3320646E, 0x79622D32, 0x6B206574]
    st += [int.from_bytes(key[i : i + 4], "little") for i in range(0, 32, 4)]
    st += [counter] + [
        int.from_bytes(nonce[i : i + 4], "little") for i in range(0, 12, 4)
    ]
    w = list(st)
    for _ in range(10):
        w[0], w[4], w[8], w[12] = _qr(w[0], w[4], w[8], w[12])
        w[1], w[5], w[9], w[13] = _qr(w[1], w[5], w[9], w[13])
        w[2], w[6], w[10], w[14] = _qr(w[2], w[6], w[10], w[14])
        w[3], w[7], w[11], w[15] = _qr(w[3], w[7], w[11], w[15])
        w[0], w[5], w[10], w[15] = _qr(w[0], w[5], w[10], w[15])
        w[1], w[6], w[11], w[12] = _qr(w[1], w[6], w[11], w[12])
        w[2], w[7], w[8], w[13] = _qr(w[2], w[7], w[8], w[13])
        w[3], w[4], w[9], w[14] = _qr(w[3], w[4], w[9], w[14])
    out = b""
    for i in range(16):
        out += ((w[i] + st[i]) & 0xFFFFFFFF).to_bytes(4, "little")
    return out


def main():
    toks = sys.stdin.read().split()
    if len(toks) < 3:
        return
    key = bytes.fromhex(toks[0])
    nonce = bytes.fromhex(toks[1])
    counter = int(toks[2])
    msg = bytes.fromhex(toks[3]) if len(toks) > 3 else b""
    out = b""
    for blk in range((len(msg) + 63) // 64):
        ks = _block(key, (counter + blk) % 2**32, nonce)
        chunk = msg[blk * 64 : (blk + 1) * 64]
        out += bytes(c ^ k for c, k in zip(chunk, ks))
    sys.stdout.write(out.hex())


if __name__ == "__main__":
    main()
