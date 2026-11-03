import sys
import math

def main():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    it = iter(input_data)
    
    try:
        T_str = next(it)
    except StopIteration:
        return
    T = int(T_str)
    
    out = []
    for _ in range(T):
        N = int(next(it))
        F = int(next(it))
        H = int(next(it))
        E = int(next(it))
        
        X = []
        Y = []
        for _ in range(N):
            row = [int(next(it)) for _ in range(F)]
            y = int(next(it))
            X.append(row)
            Y.append(y)
            
        out.append("BACKPROP")
        
        # Perceptron
        w = [0] * F
        b = 0
        for _ in range(E):
            for i in range(N):
                y = 1 if Y[i] == 1 else -1
                act = b
                for f in range(F):
                    act += w[f] * X[i][f]
                if y * act <= 0:
                    for f in range(F):
                        w[f] += y * X[i][f]
                    b += y
        p_row = ["P"]
        for f in range(F):
            p_row.append(str(w[f]))
        p_row.append(str(b))
        for i in range(N):
            act = b
            for f in range(F):
                act += w[f] * X[i][f]
            p_row.append("1" if act > 0 else "0")
        out.append(" ".join(p_row))
        
        # Logistic regression
        wl = [0.0] * F
        bl = 0.0
        for _ in range(E):
            for i in range(N):
                z = bl
                for f in range(F):
                    z += wl[f] * X[i][f]
                p = 1.0 / (1.0 + math.exp(-z))
                err = float(Y[i]) - p
                for f in range(F):
                    wl[f] += 0.5 * err * X[i][f]
                bl += 0.5 * err
        l_row = ["L"]
        for f in range(F):
            l_row.append(f"{wl[f]:.6f}")
        l_row.append(f"{bl:.6f}")
        for i in range(N):
            z = bl
            for f in range(F):
                z += wl[f] * X[i][f]
            p = 1.0 / (1.0 + math.exp(-z))
            l_row.append("1" if p >= 0.5 else "0")
        out.append(" ".join(l_row))
        
        # MLP backprop
        w1 = [[0.05 * (h + f + 1) for f in range(F)] for h in range(H)]
        b1 = [0.0] * H
        w2 = [0.05 * (h + 1) for h in range(H)]
        b2 = 0.0
        
        for _ in range(E):
            for i in range(N):
                a1 = [0.0] * H
                for h in range(H):
                    z = b1[h]
                    for f in range(F):
                        z += w1[h][f] * X[i][f]
                    a1[h] = math.tanh(z)
                z2 = b2
                for h in range(H):
                    z2 += w2[h] * a1[h]
                p = 1.0 / (1.0 + math.exp(-z2))
                d2 = (p - float(Y[i])) * p * (1.0 - p)
                for h in range(H):
                    d1 = d2 * w2[h] * (1.0 - a1[h] * a1[h])
                    for f in range(F):
                        w1[h][f] -= 0.1 * d1 * X[i][f]
                    b1[h] -= 0.1 * d1
                for h in range(H):
                    w2[h] -= 0.1 * d2 * a1[h]
                b2 -= 0.1 * d2
                
        m_row = ["M"]
        loss = 0.0
        for i in range(N):
            a1 = [0.0] * H
            for h in range(H):
                z = b1[h]
                for f in range(F):
                    z += w1[h][f] * X[i][f]
                a1[h] = math.tanh(z)
            z2 = b2
            for h in range(H):
                z2 += w2[h] * a1[h]
            p = 1.0 / (1.0 + math.exp(-z2))
            diff = float(Y[i]) - p
            loss += 0.5 * diff * diff
            m_row.append("1" if p >= 0.5 else "0")
        loss /= N
        m_row.append(f"{loss:.6f}")
        out.append(" ".join(m_row))
        
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
