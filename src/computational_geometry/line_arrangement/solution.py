import sys
import math

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    idx = 1
    A = []
    B = []
    C = []
    for _ in range(n):
        A.append(int(tokens[idx]))
        B.append(int(tokens[idx + 1]))
        C.append(int(tokens[idx + 2]))
        idx += 3

    verts = []
    for i in range(n):
        for j in range(i + 1, n):
            det = A[i] * B[j] - A[j] * B[i]
            if det == 0:
                continue
            xn = C[i] * B[j] - C[j] * B[i]
            yn = A[i] * C[j] - A[j] * C[i]
            gx = math.gcd(xn, det)
            gy = math.gcd(yn, det)
            xd = -det if det < 0 else det
            xn2 = (-xn if det < 0 else xn) // gx
            xd2 = xd // gx
            yn2 = (-yn if det < 0 else yn) // gy
            yd2 = xd // gy
            verts.append((xn2, xd2, yn2, yd2))

    from functools import cmp_to_key
    def cmp_v(a, b):
        l = a[0] * b[1]
        r = b[0] * a[1]
        if l != r:
            return -1 if l < r else 1
        l2 = a[2] * b[3]
        r2 = b[2] * a[3]
        if l2 != r2:
            return -1 if l2 < r2 else 1
        return 0

    verts.sort(key=cmp_to_key(cmp_v))

    Vv = len(verts)
    out = [str(Vv)]
    for v in verts:
        out.append(f"{v[0]}/{v[1]} {v[2]}/{v[3]}")
    out.append(f"{n + 2 * Vv} {n + Vv + 1}")
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
