import sys

def npar(k):
    p = 0
    while (1 << p) < k + p + 1:
        p += 1
    return p

def ispow2(x):
    return x > 0 and (x & (x - 1)) == 0

def encode(data):
    k = len(data)
    p = npar(k)
    hlen = k + p
    h = [0] * (hlen + 1)
    di = 0
    for i in range(1, hlen + 1):
        if not ispow2(i):
            h[i] = 1 if data[di] == '1' else 0
            di += 1
    for b in range(p):
        s = 0
        for i in range(1, hlen + 1):
            if i & (1 << b):
                s ^= h[i]
        h[1 << b] = s
    p0 = 0
    for i in range(1, hlen + 1):
        p0 ^= h[i]
    out = ('1' if p0 else '0') + "".join('1' if h[i] else '0' for i in range(1, hlen + 1))
    return out

def decode(code):
    hlen = len(code) - 1
    h = [0] * (hlen + 1)
    p0 = 1 if code[0] == '1' else 0
    for i in range(1, hlen + 1):
        h[i] = 1 if code[i] == '1' else 0
    p = 0
    while (1 << p) <= hlen:
        p += 1
    syn = 0
    for b in range(p):
        s = 0
        for i in range(1, hlen + 1):
            if i & (1 << b):
                s ^= h[i]
        if s:
            syn |= (1 << b)
    tot = p0
    for i in range(1, hlen + 1):
        tot ^= h[i]
    if syn == 0 and tot == 0:
        status = "OK"
    elif syn == 0:
        status = "FIXED"
        p0 ^= 1
    elif tot != 0:
        status = "FIXED"
        h[syn] ^= 1
    else:
        status = "DED"
    data = "".join('1' if h[i] else '0' for i in range(1, hlen + 1) if not ispow2(i))
    return data, status

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    try:
        q = int(next(it))
    except StopIteration:
        return

    for _ in range(q):
        op = next(it)
        w = next(it)
        if op == 'E':
            print(encode(w))
        else:
            d, s = decode(w)
            print(f"{d} {s}")

if __name__ == "__main__":
    main()
