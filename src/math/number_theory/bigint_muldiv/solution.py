import sys

# Grade-school below this many digits; Karatsuba above it.
KARAT_THRESHOLD = 16


def _strip(d):
    while len(d) > 1 and d[-1] == 0:
        d.pop()
    return d


def _cmp(a, b):
    if len(a) != len(b):
        return -1 if len(a) < len(b) else 1
    for x, y in zip(reversed(a), reversed(b)):
        if x != y:
            return -1 if x < y else 1
    return 0


def _add(a, b):
    out, carry = [], 0
    for i in range(max(len(a), len(b))):
        v = (a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0) + carry
        out.append(v % 10)
        carry = v // 10
    if carry:
        out.append(carry)
    return _strip(out)


def _sub(a, b):
    # Requires a >= b.
    out, borrow = [], 0
    for i in range(len(a)):
        v = a[i] - (b[i] if i < len(b) else 0) - borrow
        if v < 0:
            v += 10
            borrow = 1
        else:
            borrow = 0
        out.append(v)
    return _strip(out)


def _mul_school(a, b):
    out = [0] * (len(a) + len(b))
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    carry = 0
    for i in range(len(out)):
        v = out[i] + carry
        out[i] = v % 10
        carry = v // 10
    while carry:
        out.append(carry % 10)
        carry //= 10
    return _strip(out)


def _mul(a, b):
    if len(a) < len(b):
        a, b = b, a
    if len(b) < KARAT_THRESHOLD:
        return _mul_school(a, b)
    m = len(a) // 2
    a0, a1 = a[:m], a[m:]
    b0, b1 = b[:m], b[m:] if len(b) > m else [0]
    z0 = _mul(a0, b0)
    z2 = _mul(a1, b1)
    z1 = _sub(_sub(_mul(_add(a0, a1), _add(b0, b1)), z0), z2)
    return _strip(_add(_add([0] * (2 * m) + z2, [0] * m + z1), z0))


def _divmod(a, b):
    # Long division; a, b LSB-first digit lists, b != 0.
    if _cmp(a, b) < 0:
        return ([0], list(a))
    quot = [0] * len(a)
    rem = []
    for i in range(len(a) - 1, -1, -1):
        rem = _strip([a[i], *rem])
        q = 9
        while q > 0 and _cmp(_mul_school(b, [q]), rem) > 0:
            q -= 1
        quot[i] = q
        rem = _sub(rem, _mul_school(b, [q]))
    return (_strip(quot), _strip(rem))


def _parse(s):
    return _strip([ord(c) - 48 for c in reversed(s.strip())])


def _show(d):
    return "".join(chr(48 + x) for x in reversed(d))


def main():
    toks = sys.stdin.read().split()
    if len(toks) < 3:
        return
    op, a, b = toks[0], _parse(toks[1]), _parse(toks[2])
    if op == "MUL":
        sys.stdout.write(_show(_mul(a, b)))
    else:
        q, r = _divmod(a, b)
        sys.stdout.write(_show(q) + " " + _show(r))


if __name__ == "__main__":
    main()
