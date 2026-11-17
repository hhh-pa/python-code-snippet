import sys

MASK26 = (1 << 26) - 1


def _poly_tag(key, msg):
    r = int.from_bytes(key[:16], "little") & 0x0FFFFFFC0FFFFFFC0FFFFFFC0FFFFFFF
    s = int.from_bytes(key[16:], "little")
    r0, r1 = r & MASK26, (r >> 26) & MASK26
    r2, r3 = (r >> 52) & MASK26, (r >> 78) & MASK26
    r4 = (r >> 104) & MASK26
    s1, s2, s3, s4 = r1 * 5, r2 * 5, r3 * 5, r4 * 5
    h0 = h1 = h2 = h3 = h4 = 0
    for off in range(0, len(msg), 16):
        block = msg[off : off + 16]
        n = int.from_bytes(block, "little") | (1 << (8 * len(block)))
        h0 += n & MASK26
        h1 += (n >> 26) & MASK26
        h2 += (n >> 52) & MASK26
        h3 += (n >> 78) & MASK26
        h4 += (n >> 104) & MASK26
        d0 = h0 * r0 + h1 * s4 + h2 * s3 + h3 * s2 + h4 * s1
        d1 = h0 * r1 + h1 * r0 + h2 * s4 + h3 * s3 + h4 * s2
        d2 = h0 * r2 + h1 * r1 + h2 * r0 + h3 * s4 + h4 * s3
        d3 = h0 * r3 + h1 * r2 + h2 * r1 + h3 * r0 + h4 * s4
        d4 = h0 * r4 + h1 * r3 + h2 * r2 + h3 * r1 + h4 * r0
        c = d0 >> 26
        h0 = d0 & MASK26
        d1 += c
        c = d1 >> 26
        h1 = d1 & MASK26
        d2 += c
        c = d2 >> 26
        h2 = d2 & MASK26
        d3 += c
        c = d3 >> 26
        h3 = d3 & MASK26
        d4 += c
        c = d4 >> 26
        h4 = d4 & MASK26
        h0 += c * 5
        c = h0 >> 26
        h0 &= MASK26
        h1 += c
    # Freeze: h -= p iff h >= p (borrow chain over p = 2^130 - 5).
    p = [0x3FFFFFB, MASK26, MASK26, MASK26, MASK26]
    h = [h0, h1, h2, h3, h4]
    g, borrow = [], 0
    for i in range(5):
        v = h[i] - p[i] - borrow
        if v < 0:
            v += 1 << 26
            borrow = 1
        else:
            borrow = 0
        g.append(v)
    if borrow == 0:
        h = g
    # Serialize low 130 bits little-endian, add s mod 2^128 byte-wise.
    out = [0] * 17
    acc, bits, idx = 0, 0, 0
    for limb in h:
        acc |= limb << bits
        bits += 26
        while bits >= 8:
            out[idx] = acc & 0xFF
            acc >>= 8
            bits -= 8
            idx += 1
    sb = s.to_bytes(16, "little")
    carry = 0
    for i in range(16):
        v = out[i] + sb[i] + carry
        out[i] = v & 0xFF
        carry = v >> 8
    return bytes(out[:16]).hex()


def main():
    toks = sys.stdin.read().split()
    if len(toks) < 1:
        return
    key = bytes.fromhex(toks[0])
    msg = bytes.fromhex(toks[1]) if len(toks) > 1 else b""
    sys.stdout.write(_poly_tag(key, msg))


if __name__ == "__main__":
    main()
