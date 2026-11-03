import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    s = [0] * n
    f = [0] * n
    w = [0] * n
    idx = 1
    for i in range(n):
        s[i] = int(tokens[idx])
        f[i] = int(tokens[idx + 1])
        w[i] = int(tokens[idx + 2])
        idx += 3

    o = list(range(n))
    o.sort(key=lambda i: (f[i], s[i], i))

    p = [-1] * n
    for j in range(n):
        lo = 0
        hi = j - 1
        ans = -1
        sj = s[o[j]]
        while lo <= hi:
            mid = (lo + hi) // 2
            if f[o[mid]] <= sj:
                ans = mid
                lo = mid + 1
            else:
                hi = mid - 1
        p[j] = ans

    M = [0] * n
    for j in range(n):
        incl = w[o[j]] + (M[p[j]] if p[j] >= 0 else 0)
        excl = M[j - 1] if j > 0 else 0
        M[j] = incl if incl > excl else excl

    sel = []
    j = n - 1
    while j >= 0:
        incl = w[o[j]] + (M[p[j]] if p[j] >= 0 else 0)
        excl = M[j - 1] if j > 0 else 0
        if incl > excl:
            sel.append(o[j])
            j = p[j]
        else:
            j -= 1

    sel.sort()
    print(M[n - 1] if n else 0)
    print(*(sel))

if __name__ == '__main__':
    main()
