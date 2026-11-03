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

    srtt = 0
    rttvar = 0
    rto = 1000
    have_sample = False

    for _ in range(q):
        e = next(it)
        if e == 'S':
            r = int(next(it))
            ret = int(next(it))
            if ret == 0:
                if not have_sample:
                    have_sample = True
                    srtt = r
                    rttvar = r // 2
                else:
                    rttvar = (3 * rttvar + abs(srtt - r)) // 4
                    srtt = (7 * srtt + r) // 8
                x = 4 * rttvar
                if x < 1:
                    x = 1
                rto = srtt + x
                if rto < 1:
                    rto = 1
                if rto > 60000:
                    rto = 60000
        elif e == 'T':
            rto *= 2
            if rto > 60000:
                rto = 60000
        print(f"{srtt} {rttvar} {rto}")

if __name__ == "__main__":
    main()
