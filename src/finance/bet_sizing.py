import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    d = float(tokens[1])
    pr = [float(tokens[2 + i]) for i in range(n)]
    
    s = [2 * p - 1 for p in pr]
    sizes_str = " ".join(f"{x:.6f}" for x in s)
    sys.stdout.write(f"SIZES: {sizes_str}\n")
    
    pos = 0.0
    active = []
    for x in s:
        pos = d * pos + (1 - d) * x
        pos = max(-1.0, min(1.0, pos))
        active.append(pos)
    active_str = " ".join(f"{x:.6f}" for x in active)
    sys.stdout.write(f"ACTIVE: {active_str}\n")

if __name__ == "__main__":
    main()
