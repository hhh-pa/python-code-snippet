import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    y = [float(tokens[1 + i]) for i in range(n)]
    
    df = [0.0] * n
    for j in range(n):
        cp = y[j] * 50.0
        acc = sum(cp * df[k] for k in range(j))
        df[j] = (100.0 - acc) / (100.0 + cp)
        
    zeros = [2.0 * ((df[j] ** (-1.0 / (j + 1))) - 1.0) for j in range(n)]
    forwards = [2.0 * (df[j - 1] / df[j] - 1.0) for j in range(1, n)]
    
    zeros_str = " ".join(f"{v:.6f}" for v in zeros)
    forwards_str = " ".join(f"{v:.6f}" for v in forwards)
    sys.stdout.write(f"ZEROS: {zeros_str}\n")
    sys.stdout.write(f"FORWARDS: {forwards_str}\n" if forwards else "FORWARDS:\n")

if __name__ == "__main__":
    main()
