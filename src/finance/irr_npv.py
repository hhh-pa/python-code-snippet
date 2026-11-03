import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    rate = float(tokens[0])
    m = int(tokens[1])
    cf = [float(tokens[2 + i]) for i in range(m)]
    idx = 2 + m
    tax = float(tokens[idx])
    we = float(tokens[idx + 1])
    re = float(tokens[idx + 2])
    wd = float(tokens[idx + 3])
    rd = float(tokens[idx + 4])
    
    def npv(r):
        return sum(cf[t] * ((1.0 + r) ** (-t)) for t in range(m))
        
    N = npv(rate)
    lo = -0.9999
    hi = 10.0
    flo = npv(lo)
    fhi = npv(hi)
    has = (flo == 0 or fhi == 0 or (flo < 0) != (fhi < 0))
    irr = 0.0
    if has:
        if flo == 0:
            irr = lo
        elif fhi == 0:
            irr = hi
        else:
            for _ in range(200):
                mid = (lo + hi) / 2.0
                fm = npv(mid)
                if fm == 0:
                    lo = hi = mid
                    break
                if (fm < 0) != (flo < 0):
                    hi = mid
                    fhi = fm
                else:
                    lo = mid
                    flo = fm
            irr = (lo + hi) / 2.0
            
    wacc = we * re + wd * rd * (1.0 - tax)
    
    sys.stdout.write(f"NPV: {N:.6f}\n")
    if has:
        sys.stdout.write(f"IRR: {irr:.6f}\n")
    else:
        sys.stdout.write("IRR: NONE\n")
    sys.stdout.write(f"WACC: {wacc:.6f}\n")

if __name__ == "__main__":
    main()
