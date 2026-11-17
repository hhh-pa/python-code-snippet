import sys

FREQ = [
    8.2,
    1.5,
    2.8,
    4.3,
    13.0,
    2.2,
    2.0,
    6.1,
    7.0,
    0.15,
    0.77,
    4.0,
    2.4,
    6.7,
    7.5,
    1.9,
    0.095,
    6.0,
    6.3,
    9.1,
    2.8,
    0.98,
    2.4,
    0.15,
    2.0,
    0.074,
]


def _caesar(text, shift):
    out = []
    for c in text:
        if "A" <= c <= "Z":
            out.append(chr((ord(c) - 65 + shift) % 26 + 65))
        elif "a" <= c <= "z":
            out.append(chr((ord(c) - 97 + shift) % 26 + 97))
        else:
            out.append(c)
    return "".join(out)


def _vigenere(text, key, decode):
    ks = [(ord(k.upper()) - 65) % 26 for k in key if k.isalpha()]
    out, j = [], 0
    for c in text:
        if c.isalpha():
            s = ks[j % len(ks)]
            if decode:
                s = -s
            base = 65 if c.isupper() else 97
            out.append(chr((ord(c) - base + s) % 26 + base))
            j += 1
        else:
            out.append(c)
    return "".join(out)


def _break(text):
    letters = [c.upper() for c in text if c.isalpha()]
    n = len(letters)
    best, bests = None, 0
    for shift in range(26):
        pt = _caesar("".join(letters), -shift)
        obs = [0] * 26
        for c in pt:
            obs[ord(c) - 65] += 1
        chi = sum((o - n * f / 100) ** 2 / (n * f / 100) for o, f in zip(obs, FREQ))
        if best is None or chi < best:
            best, bests = chi, shift
    return f"{bests} {_caesar(text, -bests)}"


def main():
    data = sys.stdin.read()
    if not data.strip():
        return
    head = data.strip().split(None, 1)
    op = head[0]
    rest = head[1] if len(head) > 1 else ""
    if op == "BREAK":
        sys.stdout.write(_break(rest))
    else:
        arg_rest = rest.split(None, 1)
        arg, text = arg_rest[0], arg_rest[1] if len(arg_rest) > 1 else ""
        if op == "CAESAR_ENC":
            sys.stdout.write(_caesar(text, int(arg)))
        elif op == "CAESAR_DEC":
            sys.stdout.write(_caesar(text, -int(arg)))
        elif op == "VIGENERE_ENC":
            sys.stdout.write(_vigenere(text, arg, False))
        else:
            sys.stdout.write(_vigenere(text, arg, True))


if __name__ == "__main__":
    main()
