import sys
import heapq

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    idx = 0
    try:
        n = int(tokens[idx])
        k_regs = int(tokens[idx + 1])
    except (ValueError, IndexError):
        return
    idx += 2

    intervals = []
    for _ in range(n):
        if idx >= len(tokens):
            return
        iid = int(tokens[idx])
        s = int(tokens[idx + 1])
        e = int(tokens[idx + 2])
        idx += 3
        intervals.append((iid, s, e))

    sorted_intervals = sorted(intervals, key=lambda x: (x[1], x[2]))

    free_regs = list(range(k_regs))
    heapq.heapify(free_regs)

    active = []  # list of [end, id, reg]
    assigned_reg = [-1] * n
    is_spilled = [False] * n

    for iid, s, e in sorted_intervals:
        new_active = []
        for act in active:
            if act[0] < s:
                heapq.heappush(free_regs, act[2])
            else:
                new_active.append(act)
        active = new_active

        if len(active) == k_regs:
            # find latest ending in active
            # in C++ max_element with < returns first maximum
            latest_idx = 0
            for i in range(1, len(active)):
                if active[i][0] > active[latest_idx][0]:
                    latest_idx = i

            if active[latest_idx][0] > e:
                spilled = active.pop(latest_idx)
                is_spilled[spilled[1]] = True
                assigned_reg[spilled[1]] = -1

                assigned_reg[iid] = spilled[2]
                active.append([e, iid, spilled[2]])
            else:
                is_spilled[iid] = True
        else:
            reg = heapq.heappop(free_regs)
            assigned_reg[iid] = reg
            active.append([e, iid, reg])

        active.sort(key=lambda x: x[0])

    allocated_cnt = 0
    spilled_cnt = 0
    out = []
    for i in range(n):
        if is_spilled[i]:
            out.append(f"v{i}: SPILL")
            spilled_cnt += 1
        else:
            out.append(f"v{i}: R{assigned_reg[i]}")
            allocated_cnt += 1

    out.append(f"Allocated: {allocated_cnt} Spilled: {spilled_cnt}")
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
