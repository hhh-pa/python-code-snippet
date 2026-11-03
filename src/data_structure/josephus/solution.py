import sys


class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, i, d):
        n = self.n
        while i <= n:
            self.bit[i] += d
            i += i & -i

    def kth(self, k):
        i = 0
        step = 1
        while step * 2 <= self.n:
            step *= 2
        while step > 0:
            j = i + step
            if j <= self.n and self.bit[j] < k:
                k -= self.bit[j]
                i = j
            step //= 2
        return i + 1


def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    m = int(tokens[1])
    fw = Fenwick(n)
    for i in range(1, n + 1):
        fw.add(i, 1)

    pos = 0
    rem = n
    res = []
    while rem > 0:
        pos = (pos + m - 1) % rem
        idx = fw.kth(pos + 1)
        res.append(str(idx))
        fw.add(idx, -1)
        rem -= 1

    sys.stdout.write(" ".join(res) + "\n")


if __name__ == "__main__":
    main()
