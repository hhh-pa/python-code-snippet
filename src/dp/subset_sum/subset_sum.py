import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    target = int(tokens[1])
    v = [int(tokens[2 + i]) for i in range(n)]

    def poss(t):
        if t < 0:
            return False
        # Bitset representation of reachable subset sums
        dp = 1
        for x in v:
            if x < 0 or x > t:
                continue
            dp |= (dp << x)
        return bool((dp >> t) & 1)

    tot = sum(v)
    ans1 = "YES" if poss(target) else "NO"
    ans2 = "YES" if (tot % 2 == 0 and poss(tot // 2)) else "NO"
    print(ans1)
    print(ans2)

if __name__ == '__main__':
    main()
