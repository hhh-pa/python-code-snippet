import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    try:
        q = int(next(it))
    except StopIteration:
        return

    cwnd = 1
    ssthresh = 64
    ack_count = 0
    out = []

    for _ in range(q):
        e = next(it)
        if e == 'A':
            if cwnd < ssthresh:
                cwnd += 1
            else:
                ack_count += 1
                if ack_count >= cwnd:
                    cwnd += 1
                    ack_count = 0
        elif e == 'D':
            ssthresh = cwnd // 2
            if ssthresh < 1:
                ssthresh = 1
            cwnd = ssthresh
            ack_count = 0
        elif e == 'T':
            ssthresh = cwnd // 2
            if ssthresh < 1:
                ssthresh = 1
            cwnd = 1
            ack_count = 0
        out.append(f"{cwnd} {ssthresh}")

    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
