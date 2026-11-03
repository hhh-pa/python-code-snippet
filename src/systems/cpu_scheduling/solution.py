import collections
import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    try:
        policy = int(next(it))
    except StopIteration:
        return
    quantum = 1
    if policy == 2:
        quantum = int(next(it))
    n = int(next(it))
    arr = [0] * n
    burst = [0] * n
    for i in range(n):
        arr[i] = int(next(it))
        burst[i] = int(next(it))

    order = []
    comp = [-1] * n
    idx = sorted(range(n), key=lambda i: (arr[i], i))

    if policy == 0:
        now = 0
        for i in idx:
            if now < arr[i]:
                now = arr[i]
            now += burst[i]
            comp[i] = now
            order.append(i)
    elif policy == 1:
        done = [False] * n
        now = 0
        left = n
        while left > 0:
            pick = -1
            for i in range(n):
                if done[i] or arr[i] > now:
                    continue
                if pick == -1 or burst[i] < burst[pick] or \
                   (burst[i] == burst[pick] and (arr[i] < arr[pick] or (arr[i] == arr[pick] and i < pick))):
                    pick = i
            if pick == -1:
                now = min(arr[i] for i in range(n) if not done[i])
                continue
            now += burst[pick]
            comp[pick] = now
            done[pick] = True
            order.append(pick)
            left -= 1
    else:
        rem = list(burst)
        ready = collections.deque()
        now = 0
        ap = 0
        left = n
        while left > 0:
            while ap < len(idx) and arr[idx[ap]] <= now:
                ready.append(idx[ap])
                ap += 1
            if not ready:
                now = arr[idx[ap]]
                continue
            id_ = ready.popleft()
            run = min(rem[id_], quantum)
            now += run
            rem[id_] -= run
            while ap < len(idx) and arr[idx[ap]] <= now:
                ready.append(idx[ap])
                ap += 1
            if rem[id_] > 0:
                ready.append(id_)
            else:
                comp[id_] = now
                order.append(id_)
                left -= 1

    print(" ".join(map(str, order)))
    tot = sum(comp[i] - arr[i] - burst[i] for i in range(n))
    print(tot)

if __name__ == "__main__":
    main()
