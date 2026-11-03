import sys

def edit_distance(a, b):
    m = len(a)
    n = len(b)
    dp0 = list(range(m + 1))
    dp1 = [0] * (m + 1)
    for i in range(1, n + 1):
        dp1[0] = i
        bi = b[i - 1]
        for j in range(1, m + 1):
            if a[j - 1] == bi:
                dp1[j] = dp0[j - 1]
            else:
                dp1[j] = 1 + min(dp0[j], dp1[j - 1], dp0[j - 1])
        dp0, dp1 = dp1, dp0
    return dp0[m]

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    idx = 1
    out = []
    for _ in range(n):
        a = tokens[idx]
        b = tokens[idx + 1]
        idx += 2
        out.append(str(edit_distance(a, b)))
    print("\n".join(out))

if __name__ == '__main__':
    main()
