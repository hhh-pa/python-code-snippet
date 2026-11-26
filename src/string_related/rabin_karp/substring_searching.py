import sys

BASE = 256
MOD = 1000000007


def rabin_karp(text, pat):
    n, m = len(text), len(pat)
    if m == 0:
        return True
    if m > n:
        return False
    pw = pow(BASE, m - 1, MOD)
    ph = 0
    th = 0
    for ch in pat:
        ph = (ph * BASE + ord(ch)) % MOD
    for ch in text[:m]:
        th = (th * BASE + ord(ch)) % MOD
    for i in range(n - m + 1):
        if ph == th and text[i : i + m] == pat:
            return True
        if i + m < n:
            th = (th - ord(text[i]) * pw) % MOD
            th = (th * BASE + ord(text[i + m])) % MOD
    return False


def main():
    lines = sys.stdin.read().split("\n")
    if not lines or not lines[0].strip():
        return
    t = int(lines[0].strip())
    rest = lines[1:]
    out = []
    for i in range(t):
        text = rest[2 * i] if 2 * i < len(rest) else ""
        pat = rest[2 * i + 1] if 2 * i + 1 < len(rest) else ""
        out.append("YES" if rabin_karp(text, pat) else "NO")
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()
