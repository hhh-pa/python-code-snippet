import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    try:
        head = int(next(it))
        maxc = int(next(it))
        n = int(next(it))
    except StopIteration:
        return

    req = [int(next(it)) for _ in range(n)]

    # FCFS
    tot = 0
    h = head
    for x in req:
        tot += abs(x - h)
        h = x
    out = ["FCFS", str(tot)] + [str(x) for x in req]
    print(" ".join(out))

    # SSTF
    done = [False] * n
    tot = 0
    h = head
    ord_sstf = []
    for _ in range(n):
        pick = -1
        for i in range(n):
            if done[i]:
                continue
            if (pick == -1 or
                abs(req[i] - h) < abs(req[pick] - h) or
                (abs(req[i] - h) == abs(req[pick] - h) and
                 (req[i] < req[pick] or (req[i] == req[pick] and i < pick)))):
                pick = i
        tot += abs(req[pick] - h)
        h = req[pick]
        done[pick] = True
        ord_sstf.append(req[pick])
    out = ["SSTF", str(tot)] + [str(x) for x in ord_sstf]
    print(" ".join(out))

    up = sorted([x for x in req if x >= head])
    down = sorted([x for x in req if x < head])

    # SCAN
    tot = maxc - head
    if down:
        tot += maxc - down[0]
    scan_ord = up + list(reversed(down))
    out = ["SCAN", str(tot)] + [str(x) for x in scan_ord]
    print(" ".join(out))

    # CSCAN
    tot = (maxc - head) + maxc
    if down:
        tot += down[-1]
    cscan_ord = up + down
    out = ["CSCAN", str(tot)] + [str(x) for x in cscan_ord]
    print(" ".join(out))

    # LOOK
    tot = 0
    if up and down:
        tot = (up[-1] - head) + (up[-1] - down[0])
    elif up:
        tot = up[-1] - head
    elif down:
        tot = head - down[0]
    look_ord = up + list(reversed(down))
    out = ["LOOK", str(tot)] + [str(x) for x in look_ord]
    print(" ".join(out))

    # CLOOK
    tot = 0
    if up and down:
        tot = (up[-1] - head) + (up[-1] - down[0]) + (down[-1] - down[0])
    elif up:
        tot = up[-1] - head
    elif down:
        tot = (head - down[0]) + (down[-1] - down[0])
    clook_ord = up + down
    out = ["CLOOK", str(tot)] + [str(x) for x in clook_ord]
    print(" ".join(out))

if __name__ == "__main__":
    main()
