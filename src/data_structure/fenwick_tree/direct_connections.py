import bisect
import sys

MOD = 1000000007


class Fenwick:
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (n + 1)

    def add(self, i, delta):
        n = self.n
        tree = self.tree
        delta %= MOD
        while i <= n:
            tree[i] = (tree[i] + delta) % MOD
            i += i & -i

    def query(self, i):
        s = 0
        tree = self.tree
        while i > 0:
            s = (s + tree[i]) % MOD
            i -= i & -i
        return s

    def query_range(self, l, r):
        if l > r:
            return 0
        res = (self.query(r) - self.query(l - 1)) % MOD
        return res


def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    t = int(tokens[0])
    idx = 1
    out = []
    for _ in range(t):
        n = int(tokens[idx])
        idx += 1
        xs = [int(tokens[idx + i]) for i in range(n)]
        idx += n
        ps = [int(tokens[idx + i]) for i in range(n)]
        idx += n

        coords = sorted(set(xs))
        m = len(coords)

        # cities: list of tuples (p, x, rank)
        # rank is 1-based index in coords
        cities = []
        for i in range(n):
            x = xs[i]
            p = ps[i]
            r = bisect.bisect_left(coords, x) + 1
            cities.append((p, x, r))

        cities.sort(key=lambda item: item[0])

        count_bit = Fenwick(m)
        sum_bit = Fenwick(m)
        total_cost = 0

        for p, x, r in cities:
            p_mod = p % MOD
            x_mod = x % MOD

            count_left = count_bit.query(r - 1)
            sum_left = sum_bit.query(r - 1)

            count_right = count_bit.query_range(r + 1, m)
            sum_right = sum_bit.query_range(r + 1, m)

            left_contrib = (count_left * x_mod - sum_left) % MOD
            right_contrib = (sum_right - count_right * x_mod) % MOD

            cost = ((left_contrib + right_contrib) % MOD * p_mod) % MOD
            total_cost = (total_cost + cost) % MOD

            count_bit.add(r, 1)
            sum_bit.add(r, x_mod)

        out.append(str(total_cost))

    sys.stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
