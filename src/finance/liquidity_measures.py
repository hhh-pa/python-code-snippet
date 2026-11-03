import math
import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    B = int(tokens[0])
    idx = 1
    O, H, L, C, V = [], [], [], [], []
    for _ in range(B):
        O.append(float(tokens[idx]))
        H.append(float(tokens[idx + 1]))
        L.append(float(tokens[idx + 2]))
        C.append(float(tokens[idx + 3]))
        V.append(float(tokens[idx + 4]))
        idx += 5
        
    # Roll
    roll = 0.0
    if B >= 3:
        n = B - 2
        d1 = [C[t] - C[t - 1] for t in range(1, B - 1)]
        d2 = [C[t + 1] - C[t] for t in range(1, B - 1)]
        m1 = sum(d1) / n
        m2 = sum(d2) / n
        cv = sum((d1[i] - m1) * (d2[i] - m2) for i in range(n)) / n
        if cv < 0:
            roll = 2.0 * math.sqrt(-cv)
            
    # Corwin-Schultz
    cs = 0.0
    if B >= 2:
        s = 0.0
        cnt = 0
        denom = 3.0 - 2.0 * math.sqrt(2.0)
        for t in range(B - 1):
            b0 = math.log(H[t] / L[t])
            b1 = math.log(H[t + 1] / L[t + 1])
            beta = b0 * b0 + b1 * b1
            g = math.log(max(H[t], H[t + 1]) / min(L[t], L[t + 1]))
            gamma = g * g
            alpha = (math.sqrt(2.0 * beta) - math.sqrt(beta)) / denom - math.sqrt(gamma / denom)
            stt = 2.0 * (math.exp(alpha) - 1.0) / (1.0 + math.exp(alpha))
            if stt < 0:
                stt = 0.0
            s += stt
            cnt += 1
        cs = s / cnt
        
    # signs (tick rule)
    sg = [1] * B
    for t in range(1, B):
        if C[t] > C[t - 1]:
            sg[t] = 1
        elif C[t] < C[t - 1]:
            sg[t] = -1
        else:
            sg[t] = sg[t - 1]
            
    # Kyle lambda
    kyle = 0.0
    if B >= 2:
        n = B - 1
        xs = [sg[t] * V[t] for t in range(1, B)]
        rs = [C[t] / C[t - 1] - 1.0 for t in range(1, B)]
        mx = sum(xs) / n
        mr = sum(rs) / n
        cv = sum((xs[i] - mx) * (rs[i] - mr) for i in range(n))
        vv = sum((xs[i] - mx) ** 2 for i in range(n))
        if vv > 0:
            kyle = cv / vv
            
    # Amihud
    am = 0.0
    an = 0
    for t in range(1, B):
        dv = C[t] * V[t]
        if dv > 0:
            am += abs(C[t] / C[t - 1] - 1.0) / dv
            an += 1
    amihud = am / an if an > 0 else 0.0
    
    # VPIN
    tot = sum(V)
    nb = min(50, B)
    if nb < 1:
        nb = 1
    vb = tot / nb
    vpin = 0.0
    fill = 0.0
    buy = 0.0
    sell = 0.0
    for t in range(B):
        rem = V[t]
        while rem > 1e-12:
            take = min(rem, vb - fill)
            if sg[t] > 0:
                buy += take
            else:
                sell += take
            fill += take
            rem -= take
            if fill >= vb - 1e-12:
                vpin += abs(buy - sell)
                fill = 0.0
                buy = 0.0
                sell = 0.0
    if fill > 1e-12:
        vpin += abs(buy - sell)
    vpin = vpin / tot if tot > 0 else 0.0
    
    sys.stdout.write(f"ROLL: {roll:.6f}\n")
    sys.stdout.write(f"CS: {cs:.6f}\n")
    sys.stdout.write(f"KYLE: {kyle:.6f}\n")
    sys.stdout.write(f"AMIHUD: {amihud:.6f}\n")
    sys.stdout.write(f"VPIN: {vpin:.6f}\n")

if __name__ == "__main__":
    main()
