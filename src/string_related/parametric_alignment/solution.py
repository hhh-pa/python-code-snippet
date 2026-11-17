import sys
from fractions import Fraction

NEG = float("-inf")


def _constrained_dp(s1, s2, match, mismatch):
    n, m = len(s1), len(s2)
    dp = [[[NEG] * (n + m + 1) for _ in range(m + 1)] for _ in range(n + 1)]
    par = [[[None] * (n + m + 1) for _ in range(m + 1)] for _ in range(n + 1)]
    dp[0][0][0] = 0
    for i in range(1, n + 1):
        dp[i][0][i] = 0
        par[i][0][i] = "u"
    for j in range(1, m + 1):
        dp[0][j][j] = 0
        par[0][j][j] = "l"
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            _fill_cell(dp, par, s1, s2, match, mismatch, i, j, n + m)
    return dp, par


def _fill_cell(dp, par, s1, s2, match, mismatch, i, j, kmax):
    sub = match if s1[i - 1] == s2[j - 1] else mismatch
    for k in range(kmax + 1):
        best, bp = NEG, None
        if dp[i - 1][j - 1][k] != NEG:
            best, bp = dp[i - 1][j - 1][k] + sub, "d"
        if k > 0 and dp[i - 1][j][k - 1] != NEG and dp[i - 1][j][k - 1] > best:
            best, bp = dp[i - 1][j][k - 1], "u"
        if k > 0 and dp[i][j - 1][k - 1] != NEG and dp[i][j - 1][k - 1] > best:
            best, bp = dp[i][j - 1][k - 1], "l"
        dp[i][j][k] = best
        par[i][j][k] = bp


def _trace_sig(par, s1, s2, n, m, s):
    mt = ms = 0
    i, j, k = n, m, s
    while i > 0 or j > 0:
        p = par[i][j][k]
        if p == "d":
            if s1[i - 1] == s2[j - 1]:
                mt += 1
            else:
                ms += 1
            i -= 1
            j -= 1
        elif p == "u":
            i -= 1
            k -= 1
        else:
            j -= 1
            k -= 1
    return mt, ms


def _slope_lines(dp, par, s1, s2, match, mismatch):
    n, m = len(s1), len(s2)
    lines = []
    for s in range(n + m + 1):
        c = dp[n][m][s]
        if c == NEG:
            continue
        mt, ms = _trace_sig(par, s1, s2, n, m, s)
        lines.append((-s, c, mt, ms, s))
    seen = set()
    uniq = []
    for ln in lines:
        if (ln[0], ln[1]) not in seen:
            seen.add((ln[0], ln[1]))
            uniq.append(ln)
    return sorted(uniq, key=lambda ln: ln[4], reverse=True)


def _segments(lines, g0, g1):
    def ix(a, b):
        return Fraction(b[1] - a[1], a[0] - b[0])

    hull = []
    for ln in lines:
        while len(hull) >= 2 and ix(hull[-2], hull[-1]) >= ix(hull[-1], ln):
            hull.pop()
        hull.append(ln)
    out = []
    for i, ln in enumerate(hull):
        lo = g0 if i == 0 else ix(hull[i - 1], ln)
        hi = g1 if i == len(hull) - 1 else ix(ln, hull[i + 1])
        lo, hi = max(lo, g0), min(hi, g1)
        if lo < hi:
            out.append((lo, hi, ln[2], ln[3], ln[4]))
    if not out:
        best = max(hull, key=lambda ln: ln[1] + ln[0] * g0)
        out = [(g0, g1, best[2], best[3], best[4])]
    return out


def _fmt(fr):
    if fr.denominator == 1:
        return str(fr.numerator)
    return f"{fr.numerator}/{fr.denominator}"


def main():
    toks = sys.stdin.read().split()
    if len(toks) < 7:
        return
    match, mismatch = int(toks[1]), int(toks[2])
    g0, g1 = Fraction(toks[3]), Fraction(toks[4])
    s1, s2 = toks[5], toks[6]
    dp, par = _constrained_dp(s1, s2, match, mismatch)
    lines = _slope_lines(dp, par, s1, s2, match, mismatch)
    segs = _segments(lines, g0, g1)
    sys.stdout.write(
        "\n".join(f"{_fmt(lo)} {_fmt(hi)} {mt} {ms} {s}" for lo, hi, mt, ms, s in segs)
    )


if __name__ == "__main__":
    main()
