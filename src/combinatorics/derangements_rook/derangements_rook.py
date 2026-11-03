import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    mode = tokens[0]
    if mode == "D":
        n = int(tokens[1])
        if n == 0:
            sys.stdout.write("1\n")
            return
        if n == 1:
            sys.stdout.write("0\n")
            return
        d0, d1 = 1, 0
        for i in range(2, n + 1):
            d0, d1 = d1, (i - 1) * (d1 + d0)
        sys.stdout.write(str(d1) + "\n")
    else:
        rows = int(tokens[1])
        cols = int(tokens[2])
        idx = 3
        b = []
        for _ in range(rows):
            row = [int(tokens[idx + j]) for j in range(cols)]
            idx += cols
            b.append(row)
            
        dp = [0] * (1 << cols)
        dp[0] = 1
        for i in range(rows):
            ndp = list(dp)
            row = b[i]
            avail_cols = [j for j in range(cols) if row[j]]
            if not avail_cols:
                continue
            for mask in range(1 << cols):
                cnt = dp[mask]
                if not cnt:
                    continue
                for j in avail_cols:
                    bit = 1 << j
                    if not (mask & bit):
                        ndp[mask | bit] += cnt
            dp = ndp
            
        m = min(rows, cols)
        r = [0] * (m + 1)
        for mask in range(1 << cols):
            c = bin(mask).count('1')
            r[c] += dp[mask]
            
        sys.stdout.write(" ".join(map(str, r)) + "\n")

if __name__ == "__main__":
    main()
