import sys

class Acceptor:
    def __init__(self, id_):
        self.id = id_
        self.promised_n = 0
        self.accepted_n = 0
        self.accepted_val = ""

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    try:
        n_acceptors = int(next(it))
        n_ops = int(next(it))
    except StopIteration:
        return

    acceptors = [Acceptor(i) for i in range(n_acceptors)]
    majority = n_acceptors // 2 + 1
    out = []

    for _ in range(n_ops):
        op = next(it)
        if op == "PREPARE":
            n_prop = int(next(it))
            promises = 0
            max_acc_n = 0
            val_for_max = ""
            for acc in acceptors:
                if n_prop > acc.promised_n:
                    acc.promised_n = n_prop
                    promises += 1
                    if acc.accepted_n > max_acc_n:
                        max_acc_n = acc.accepted_n
                        val_for_max = acc.accepted_val
            if promises >= majority:
                if max_acc_n > 0:
                    out.append(f"PROMISED {n_prop} PREV {max_acc_n} {val_for_max}")
                else:
                    out.append(f"PROMISED {n_prop} NONE")
            else:
                out.append(f"PREPARE REJECTED {n_prop}")
        elif op == "PROPOSE":
            n_prop = int(next(it))
            val = next(it)
            accepted_cnt = 0
            for acc in acceptors:
                if n_prop >= acc.promised_n:
                    acc.promised_n = n_prop
                    acc.accepted_n = n_prop
                    acc.accepted_val = val
                    accepted_cnt += 1
            if accepted_cnt >= majority:
                out.append(f"CHOSEN {n_prop} {val}")
            else:
                out.append(f"PROPOSE REJECTED {n_prop}")

    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
