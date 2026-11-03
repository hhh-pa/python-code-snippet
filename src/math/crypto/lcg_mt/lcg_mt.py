import sys

class MT:
    def __init__(self, seed):
        self.mt = [0] * 624
        self.idx = 624
        self.mt[0] = seed & 0xFFFFFFFF
        for i in range(1, 624):
            prev = self.mt[i - 1]
            self.mt[i] = (1812433253 * (prev ^ (prev >> 30)) + i) & 0xFFFFFFFF

    def twist(self):
        for i in range(624):
            y = (self.mt[i] & 0x80000000) | (self.mt[(i + 1) % 624] & 0x7FFFFFFF)
            self.mt[i] = self.mt[(i + 397) % 624] ^ (y >> 1)
            if y & 1:
                self.mt[i] ^= 0x9908B0DF
        self.idx = 0

    def next(self):
        if self.idx >= 624:
            self.twist()
        y = self.mt[self.idx]
        self.idx += 1
        y ^= (y >> 11)
        y ^= ((y << 7) & 0x9D2C5680)
        y ^= ((y << 15) & 0xEFC60000)
        y ^= (y >> 18)
        return y & 0xFFFFFFFF

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    mode = tokens[0]
    if mode == "L":
        a = int(tokens[1])
        c = int(tokens[2])
        m = int(tokens[3])
        seed = int(tokens[4])
        n = int(tokens[5])
        x = seed
        res = []
        for _ in range(n):
            x = (a * x + c) % m
            res.append(str(x))
        print(" ".join(res))
    else:
        seed = int(tokens[1])
        n = int(tokens[2])
        mt = MT(seed)
        res = []
        for _ in range(n):
            res.append(str(mt.next()))
        print(" ".join(res))

if __name__ == '__main__':
    main()
