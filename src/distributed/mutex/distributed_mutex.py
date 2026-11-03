import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    try:
        mode = next(it)
        n = int(next(it))
    except StopIteration:
        return

    if mode == "ra":
        R = int(next(it))
        order = []
        for _ in range(R):
            c = int(next(it))
            g = [int(next(it)) for _ in range(c)]
            g.sort()
            order.extend(g)

        ord_str = " ".join(map(str, order))
        line1 = f"ORDER: {ord_str}" if ord_str else "ORDER:"
        line2 = f"MSGS: {2 * (n - 1) * len(order)}"
        sys.stdout.write(f"{line1}\n{line2}\n")
    else:
        holder = int(next(it))
        Q = int(next(it))
        req = [int(next(it)) for _ in range(Q)]
        order = []
        ln = [0] * n
        rn = [[0] * n for _ in range(n)]
        queue = []
        qhead = 0
        hops = 0

        for i in req:
            rn[i][i] += 1
            for t in range(n):
                rn[t][i] = rn[i][i]
            if i == holder:
                order.append(i)
                ln[i] = rn[i][i]
                continue
            queue.append(i)
            while qhead < len(queue):
                j = queue[qhead]
                qhead += 1
                if rn[holder][j] <= ln[j]:
                    continue
                ln[j] = rn[holder][j]
                for t in range(n):
                    if rn[holder][t] > rn[j][t]:
                        rn[j][t] = rn[holder][t]
                holder = j
                hops += 1
                order.append(j)

        ord_str = " ".join(map(str, order))
        line1 = f"ORDER: {ord_str}" if ord_str else "ORDER:"
        line2 = f"HOPS: {hops}"
        line3 = f"MSGS: {(n - 1) * Q + hops}"
        sys.stdout.write(f"{line1}\n{line2}\n{line3}\n")

if __name__ == "__main__":
    main()
