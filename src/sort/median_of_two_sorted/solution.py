import sys

def find_median(a, b):
    if len(a) > len(b):
        return find_median(b, a)
    m, n = len(a), len(b)
    if m == 0 and n == 0:
        return 0.0
    if m == 0:
        mid = n // 2
        if n % 2 == 1:
            return float(b[mid])
        return (b[mid - 1] + b[mid]) / 2.0
    
    lo, hi = 0, m
    total = m + n
    INF = 10**18
    while lo <= hi:
        cut_a = (lo + hi) // 2
        cut_b = (total + 1) // 2 - cut_a
        max_left_a = -INF if cut_a == 0 else a[cut_a - 1]
        min_right_a = INF if cut_a == m else a[cut_a]
        max_left_b = -INF if cut_b == 0 else b[cut_b - 1]
        min_right_b = INF if cut_b == n else b[cut_b]
        
        if max_left_a <= min_right_b and max_left_b <= min_right_a:
            if total % 2 == 1:
                return float(max(max_left_a, max_left_b))
            return (max(max_left_a, max_left_b) + min(min_right_a, min_right_b)) / 2.0
        elif max_left_a > min_right_b:
            hi = cut_a - 1
        else:
            lo = cut_a + 1
    return 0.0

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    m = int(tokens[0])
    n = int(tokens[1])
    idx = 2
    a = [int(tokens[idx + i]) for i in range(m)]
    idx += m
    b = [int(tokens[idx + i]) for i in range(n)]
    a.sort()
    b.sort()
    ans = find_median(a, b)
    if ans == int(ans):
        print(int(ans))
    else:
        print(ans)

if __name__ == "__main__":
    main()
