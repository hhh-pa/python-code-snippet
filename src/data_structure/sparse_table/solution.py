import math
import sys


def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    q = int(tokens[1])
    a = [int(tokens[2 + i]) for i in range(n)]

    lg = [0] * (n + 1)
    for i in range(2, n + 1):
        lg[i] = lg[i // 2] + 1

    max_k = lg[n] + 1

    st_min = [[0] * n for _ in range(max_k)]
    st_max = [[0] * n for _ in range(max_k)]
    st_gcd = [[0] * n for _ in range(max_k)]

    for i in range(n):
        st_min[0][i] = a[i]
        st_max[0][i] = a[i]
        st_gcd[0][i] = a[i]

    for j in range(1, max_k):
        length = 1 << j
        half = 1 << (j - 1)
        prev_min = st_min[j - 1]
        prev_max = st_max[j - 1]
        prev_gcd = st_gcd[j - 1]
        cur_min = st_min[j]
        cur_max = st_max[j]
        cur_gcd = st_gcd[j]
        for i in range(n - length + 1):
            i_half = i + half
            cur_min[i] = min(prev_min[i], prev_min[i_half])
            cur_max[i] = max(prev_max[i], prev_max[i_half])
            cur_gcd[i] = math.gcd(prev_gcd[i], prev_gcd[i_half])

    idx = 2 + n
    out = []
    for _ in range(q):
        t = int(tokens[idx])
        l = int(tokens[idx + 1])
        r = int(tokens[idx + 2])
        idx += 3
        span = r - l + 1
        k = lg[span]
        right_start = r + 1 - (1 << k)
        if t == 1:
            out.append(str(min(st_min[k][l], st_min[k][right_start])))
        elif t == 2:
            out.append(str(max(st_max[k][l], st_max[k][right_start])))
        elif t == 3:
            out.append(str(math.gcd(st_gcd[k][l], st_gcd[k][right_start])))

    sys.stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
