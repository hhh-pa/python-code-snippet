import collections
import sys

TIMEOUT = 4

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    try:
        policy = int(next(it))
        W = int(next(it))
    except StopIteration:
        return

    if policy == 0:
        W = 1
    N = int(next(it))
    L = int(next(it))
    floss = collections.defaultdict(int)
    aloss = collections.defaultdict(int)
    for _ in range(L):
        t = next(it)
        s = int(next(it))
        if t == 'F':
            floss[s] += 1
        else:
            aloss[s] += 1

    base = 0
    next_to_send = 0
    sent = [-1000000] * N
    acked = [0] * N
    expected = 0
    buffered = [0] * N
    farr = collections.defaultdict(list)
    aarr = collections.defaultdict(list)
    frame_tx = 0
    ack_tx = 0

    def send_frame(j, now):
        nonlocal frame_tx
        frame_tx += 1
        sent[j] = now
        if floss[j] > 0:
            floss[j] -= 1
            return
        farr[now + 1].append(j)

    def send_ack(j, now):
        nonlocal ack_tx
        ack_tx += 1
        if aloss[j] > 0:
            aloss[j] -= 1
            return
        aarr[now + 1].append(j)

    for now in range(90000):
        if now in farr:
            for j in farr[now]:
                if j < 0 or j >= N:
                    continue
                if policy == 2:
                    if j == expected:
                        expected += 1
                        while expected < N and buffered[expected]:
                            buffered[expected] = 0
                            expected += 1
                    elif expected < j < expected + W:
                        buffered[j] = 1
                    send_ack(j, now)
                else:
                    if j == expected:
                        expected += 1
                    if expected > 0:
                        send_ack(expected - 1, now)
            del farr[now]

        if now in aarr:
            for j in aarr[now]:
                if policy == 2:
                    if 0 <= j < N:
                        acked[j] = 1
                else:
                    for k in range(base, min(j, N - 1) + 1):
                        acked[k] = 1
            del aarr[now]

        while base < N and acked[base]:
            base += 1
        if base >= N:
            break

        if policy == 2:
            for j in range(base, next_to_send):
                if not acked[j] and now - sent[j] >= TIMEOUT:
                    send_frame(j, now)
        else:
            if base < next_to_send and now - sent[base] >= TIMEOUT:
                next_to_send = base

        while next_to_send < base + W and next_to_send < N:
            send_frame(next_to_send, now)
            next_to_send += 1

    print(f"{frame_tx} {ack_tx}")

if __name__ == "__main__":
    main()
