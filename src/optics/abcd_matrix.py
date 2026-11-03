import sys

def mul(X, Y):
    # X = (a, b, c, d), Y = (a, b, c, d)
    return (
        X[0]*Y[0] + X[1]*Y[2],
        X[0]*Y[1] + X[1]*Y[3],
        X[2]*Y[0] + X[3]*Y[2],
        X[2]*Y[1] + X[3]*Y[3],
    )

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    
    m = int(tokens[0])
    idx = 1
    sys_mat = (1.0, 0.0, 0.0, 1.0)
    for _ in range(m):
        kind = tokens[idx]
        idx += 1
        if kind == "free":
            dist = float(tokens[idx])
            idx += 1
            e = (1.0, dist, 0.0, 1.0)
        elif kind == "lens":
            f = float(tokens[idx])
            idx += 1
            e = (1.0, 0.0, -1.0 / f, 1.0)
        elif kind == "mirror":
            f = float(tokens[idx])
            idx += 1
            e = (1.0, 0.0, -1.0 / f, 1.0)
        elif kind == "refract":
            n1 = float(tokens[idx])
            n2 = float(tokens[idx+1])
            R = float(tokens[idx+2])
            idx += 3
            e = (1.0, 0.0, (n1 - n2) / (n2 * R), n1 / n2)
        else:
            raise ValueError(f"Unknown kind {kind}")
        sys_mat = mul(e, sys_mat)
        
    y0 = float(tokens[idx])
    theta0 = float(tokens[idx+1])
    y1 = sys_mat[0] * y0 + sys_mat[1] * theta0
    th1 = sys_mat[2] * y0 + sys_mat[3] * theta0
    
    sys.stdout.write(f"{sys_mat[0]:.6f} {sys_mat[1]:.6f} {sys_mat[2]:.6f} {sys_mat[3]:.6f}\n")
    sys.stdout.write(f"{y1:.6f} {th1:.6f}\n")

if __name__ == "__main__":
    main()
