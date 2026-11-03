import math
import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    M = int(tokens[0])
    r0 = float(tokens[1])
    y = [float(tokens[2 + i]) for i in range(M)]
    
    emin = int(r0 * M) - 1
    if emin < 3:
        emin = 3
        
    sadf = -1e100
    arg = emin
    for e in range(emin, M):
        nobs = e
        my = sum(y[t - 1] for t in range(1, e + 1)) / nobs
        md = sum(y[t] - y[t - 1] for t in range(1, e + 1)) / nobs
        sxx = 0.0
        sxy = 0.0
        for t in range(1, e + 1):
            dx = y[t - 1] - my
            dy = (y[t] - y[t - 1]) - md
            sxx += dx * dx
            sxy += dx * dy
            
        tst = 0.0
        if sxx > 0 and nobs > 2:
            b = sxy / sxx
            a = md - b * my
            sse = 0.0
            for t in range(1, e + 1):
                r = (y[t] - y[t - 1]) - a - b * y[t - 1]
                sse += r * r
            s2 = sse / (nobs - 2)
            if s2 > 0:
                tst = b / math.sqrt(s2 / sxx)
                
        if tst > sadf:
            sadf = tst
            arg = e
            
    sys.stdout.write(f"SADF: {sadf:.6f}\n")
    sys.stdout.write(f"ARGMAX: {arg}\n")

if __name__ == "__main__":
    main()
