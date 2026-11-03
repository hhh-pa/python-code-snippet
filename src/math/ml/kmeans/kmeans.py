import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    d = int(tokens[1])
    k = int(tokens[2])
    iters = int(tokens[3])

    idx = 4
    pts = []
    for _ in range(n):
        pts.append([float(x) for x in tokens[idx : idx + d]])
        idx += d

    c = [[pts[cc][j] for j in range(d)] for cc in range(k)]
    asg = [0] * n

    for _ in range(iters):
        for i in range(n):
            pt = pts[i]
            best = -1.0
            bi = 0
            for cc in range(k):
                center = c[cc]
                dd = 0.0
                for j in range(d):
                    diff = pt[j] - center[j]
                    dd += diff * diff
                if best < 0 or dd < best:
                    best = dd
                    bi = cc
            asg[i] = bi

        for cc in range(k):
            s = [0.0] * d
            cnt = 0
            for i in range(n):
                if asg[i] == cc:
                    pt = pts[i]
                    for j in range(d):
                        s[j] += pt[j]
                    cnt += 1
            if cnt > 0:
                for j in range(d):
                    c[cc][j] = s[j] / cnt

    print(*(asg))
    out = []
    for cc in range(k):
        out.append(" ".join(f"{c[cc][j] + 0.0:.4f}" for j in range(d)))
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == '__main__':
    main()
