import sys

def build_sa(s):
    n = len(s)
    sa = list(range(n))
    rnk = [ord(c) for c in s]
    tmp = [0] * n

    k = 1
    while k < n:
        shift = 20
        keys = [(rnk[x] << shift) | (rnk[x + k] + 1 if x + k < n else 0) for x in range(n)]
        sa.sort(key=keys.__getitem__)
        tmp[sa[0]] = 0
        prev_k = keys[sa[0]]
        for i in range(1, n):
            cur_k = keys[sa[i]]
            tmp[sa[i]] = tmp[sa[i - 1]] + (1 if cur_k != prev_k else 0)
            prev_k = cur_k
        rnk = tmp[:]
        if rnk[sa[-1]] == n - 1:
            break
        k *= 2

    return sa

def build_lcp(s, sa):
    n = len(s)
    rnk = [0] * n
    for i in range(n):
        rnk[sa[i]] = i
    lcp = [0] * n
    h = 0
    for i in range(n):
        if rnk[i] == 0:
            continue
        j = sa[rnk[i] - 1]
        while i + h < n and j + h < n and s[i + h] == s[j + h]:
            h += 1
        lcp[rnk[i]] = h
        if h > 0:
            h -= 1
    return lcp

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    s = tokens[0]
    n = len(s)
    if n == 0:
        print("\n")
        return

    sa = build_sa(s)
    lcp = build_lcp(s, sa)

    print(" ".join(str(x) for x in sa))
    print(" ".join(str(x) for x in lcp))

if __name__ == "__main__":
    main()
