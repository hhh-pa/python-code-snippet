"""Wildcard matching with ? and * (O(n*m) DP, full match)."""

import sys


def _match(text, pat):
    n, m = len(text), len(pat)
    dp = [False] * (m + 1)
    dp[0] = True
    for j in range(1, m + 1):
        dp[j] = dp[j - 1] and pat[j - 1] == "*"
    for i in range(1, n + 1):
        ndp = [False] * (m + 1)
        for j in range(1, m + 1):
            c = pat[j - 1]
            if c == "*":
                ndp[j] = ndp[j - 1] or dp[j]
            elif c == "?" or c == text[i - 1]:
                ndp[j] = dp[j - 1]
        dp = ndp
    return dp[m]


def main():
    parts = sys.stdin.read().split("\n")
    if not parts or not parts[0].strip():
        return
    q = int(parts[0].strip())
    lines = parts[1:] + [""] * (2 * q)
    out = []
    for i in range(q):
        text = lines[2 * i].rstrip("\r")
        pat = lines[2 * i + 1].rstrip("\r") if 2 * i + 1 < len(lines) else ""
        out.append("YES" if _match(text, pat) else "NO")
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()
