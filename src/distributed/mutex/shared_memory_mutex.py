import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    try:
        algo = next(it)
        n = int(next(it))
        T = int(next(it))
    except StopIteration:
        return

    region = [0] * n
    pc = [0] * n
    aux = [0] * n
    entries = [0] * n
    flag = [0] * n
    level = [0] * n
    choosing = [0] * n
    b = [1] * n
    c = [1] * n
    number = [0] * n
    victim = [0] * n
    turn = 0
    k = 0

    def step(i):
        nonlocal turn, k
        j = (i + 1) % n
        if region[i] == 0:
            region[i] = 1
            pc[i] = 0
            aux[i] = 0
            return
        if region[i] == 2:
            region[i] = 3
            pc[i] = 0
            return
        if region[i] == 3:
            if algo == "peterson2":
                flag[i] = 0
                region[i] = 0
            elif algo == "filter":
                level[i] = 0
                region[i] = 0
            elif algo == "bakery":
                number[i] = 0
                region[i] = 0
            elif algo == "dijkstra":
                if pc[i] == 0:
                    c[i] = 1
                    pc[i] = 1
                else:
                    b[i] = 1
                    region[i] = 0
            elif algo == "burns":
                flag[i] = 0
                region[i] = 0
            return

        # region[i] == 1
        if algo == "peterson2":
            if pc[i] == 0:
                flag[i] = 1
                pc[i] = 1
            elif pc[i] == 1:
                turn = j
                pc[i] = 2
            else:
                if flag[j] == 1 and turn == j:
                    pass
                else:
                    region[i] = 2
                    entries[i] += 1
        elif algo == "filter":
            L = pc[i] // 3
            sub = pc[i] % 3
            if sub == 0:
                level[i] = L + 1
                pc[i] += 1
            elif sub == 1:
                victim[L + 1] = i
                pc[i] += 1
            else:
                blocked = False
                for t in range(n):
                    if t != i and level[t] >= L + 1:
                        blocked = True
                        break
                if blocked and victim[L + 1] == i:
                    pass
                elif L + 1 == n - 1:
                    region[i] = 2
                    entries[i] += 1
                else:
                    pc[i] += 1
        elif algo == "bakery":
            if pc[i] == 0:
                choosing[i] = 1
                pc[i] = 1
            elif pc[i] == 1:
                mx = max(number)
                number[i] = mx + 1
                pc[i] = 2
            elif pc[i] == 2:
                choosing[i] = 0
                pc[i] = 3
                aux[i] = 0
            else:
                t = aux[i]
                if t == i:
                    aux[i] += 1
                elif t >= n:
                    region[i] = 2
                    entries[i] += 1
                elif choosing[t] == 1:
                    pass
                elif number[t] != 0 and (number[t] < number[i] or (number[t] == number[i] and t < i)):
                    pass
                else:
                    aux[i] += 1
        elif algo == "dijkstra":
            if pc[i] == 0:
                b[i] = 0
                pc[i] = 1
            elif pc[i] == 1:
                pc[i] = 2 if k != i else 4
            elif pc[i] == 2:
                c[i] = 1
                pc[i] = 3
            elif pc[i] == 3:
                if b[k] == 1:
                    k = i
                pc[i] = 1
            elif pc[i] == 4:
                c[i] = 0
                pc[i] = 5
            else:
                fail = False
                for t in range(n):
                    if t != i and c[t] == 0:
                        fail = True
                        break
                if fail:
                    pc[i] = 1
                else:
                    region[i] = 2
                    entries[i] += 1
        elif algo == "burns":
            if pc[i] == 0:
                flag[i] = 0
                pc[i] = 1
            elif pc[i] == 1:
                flag[i] = 1
                pc[i] = 2
                aux[i] = 0
            elif pc[i] == 2:
                t = aux[i]
                if t >= i:
                    aux[i] = i + 1
                    pc[i] = 3
                elif flag[t] == 1:
                    pc[i] = 4
                else:
                    aux[i] += 1
            elif pc[i] == 4:
                flag[i] = 0
                pc[i] = 5
            elif pc[i] == 5:
                if flag[aux[i]] == 1:
                    pass
                else:
                    pc[i] = 1
                    aux[i] = 0
            else:
                t = aux[i]
                if t >= n:
                    region[i] = 2
                    entries[i] += 1
                elif flag[t] == 1:
                    pass
                else:
                    aux[i] += 1

    maxconc = 0
    for s in range(T):
        i = s % n
        step(i)
        cc = sum(1 for x in region if x == 2)
        if cc > maxconc:
            maxconc = cc

    out = []
    for i in range(n):
        out.append(f"P{i}: entries={entries[i]}")
    out.append(f"MAXCONCURRENT: {maxconc}")
    out.append(f"STEPS: {T}")
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
