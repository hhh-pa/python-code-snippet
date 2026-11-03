import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    h = float(tokens[0])
    M = int(tokens[1])
    px = [float(tokens[2 + i]) for i in range(M)]
    
    mu = sum(px) / M
    sp = 0.0
    sn = 0.0
    ev = []
    for i, p in enumerate(px):
        y = p - mu
        sp += y
        if sp < 0:
            sp = 0.0
        sn += y
        if sn > 0:
            sn = 0.0
        if sp > h or sn < -h:
            ev.append(i)
            sp = 0.0
            sn = 0.0
            
    if ev:
        sys.stdout.write(f"EVENTS: {' '.join(str(e) for e in ev)}\n")
    else:
        sys.stdout.write("EVENTS:\n")
    sys.stdout.write(f"COUNT: {len(ev)}\n")

if __name__ == "__main__":
    main()
