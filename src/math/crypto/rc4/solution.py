import sys


def _rc4(key, data):
    s = list(range(256))
    j = 0
    for i in range(256):
        j = (j + s[i] + key[i % len(key)]) % 256
        s[i], s[j] = s[j], s[i]
    i = j = 0
    out = bytearray()
    for b in data:
        i = (i + 1) % 256
        j = (j + s[i]) % 256
        s[i], s[j] = s[j], s[i]
        out.append(b ^ s[(s[i] + s[j]) % 256])
    return bytes(out)


def main():
    toks = sys.stdin.read().split()
    if len(toks) < 2:
        return
    key = bytes.fromhex(toks[0])
    msg = bytes.fromhex(toks[1]) if len(toks) > 1 else b""
    sys.stdout.write(_rc4(key, msg).hex())


if __name__ == "__main__":
    main()
