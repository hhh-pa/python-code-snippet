import sys


def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    s = int(tokens[1])
    if n <= 0 or s < 0 or s >= n:
        return

    nxt = [int(tokens[2 + i]) for i in range(n)]

    tortoise = s
    hare = s
    has_cycle = False

    while True:
        if hare == -1 or nxt[hare] == -1:
            has_cycle = False
            break
        next_hare = nxt[hare]
        if nxt[next_hare] == -1:
            has_cycle = False
            break
        tortoise = nxt[tortoise]
        hare = nxt[next_hare]
        if tortoise == hare:
            has_cycle = True
            break

    if not has_cycle:
        steps = 0
        cur = s
        while cur != -1:
            cur = nxt[cur]
            steps += 1
        sys.stdout.write(f"NO CYCLE {steps}\n")
        return

    mu = 0
    tortoise = s
    while tortoise != hare:
        tortoise = nxt[tortoise]
        hare = nxt[hare]
        mu += 1
    entry_node = tortoise

    lam = 1
    hare = nxt[tortoise]
    while tortoise != hare:
        hare = nxt[hare]
        lam += 1

    sys.stdout.write(f"CYCLE {mu} {lam} {entry_node}\n")


if __name__ == "__main__":
    main()
