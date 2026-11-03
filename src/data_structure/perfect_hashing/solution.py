import sys

P = 1000003


def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    keys = [int(tokens[1 + i]) for i in range(n)]
    idx = 1 + n
    q = int(tokens[idx])
    idx += 1
    queries = [int(tokens[idx + i]) for i in range(q)]

    m = n if n > 0 else 1

    best_a = 1
    best_b = 0
    best_sum = -1

    for a in range(1, 501):
        for b in range(501):
            cnt = [0] * m
            for k in keys:
                cnt[((a * k + b) % P) % m] += 1
            s = sum(c * c for c in cnt)
            if best_sum == -1 or s < best_sum:
                best_sum = s
                best_a = a
                best_b = b

    buckets = [[] for _ in range(m)]
    for k in keys:
        buckets[((best_a * k + best_b) % P) % m].append(k)

    a2 = [1] * m
    b2 = [0] * m
    m2 = [1] * m
    slots = [[] for _ in range(m)]
    total_slots = 0

    for j in range(m):
        nj = len(buckets[j])
        mj = nj * nj if nj > 1 else 1
        m2[j] = mj
        total_slots += mj

        ba = 1
        bb = 0
        bc = nj + 1
        for a in range(1, 501):
            found_zero = False
            for b in range(501):
                seen = [False] * mj
                col = 0
                for k in buckets[j]:
                    s = ((a * k + b) % P) % mj
                    if seen[s]:
                        col += 1
                    else:
                        seen[s] = True
                if col < bc:
                    bc = col
                    ba = a
                    bb = b
                    if bc == 0:
                        found_zero = True
                        break
            if found_zero:
                break

        a2[j] = ba
        b2[j] = bb
        bucket_slots = [[] for _ in range(mj)]
        for k in buckets[j]:
            bucket_slots[((ba * k + bb) % P) % mj].append(k)
        slots[j] = bucket_slots

    out = [str(total_slots)]
    for x in queries:
        j = ((best_a * x + best_b) % P) % m
        s = ((a2[j] * x + b2[j]) % P) % m2[j]
        ok = any(k == x for k in slots[j][s])
        out.append("YES" if ok else "NO")

    sys.stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
