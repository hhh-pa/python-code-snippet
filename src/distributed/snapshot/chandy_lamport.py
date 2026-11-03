import collections
import sys

class Process:
    def __init__(self, id_, balance):
        self.id = id_
        self.balance = balance
        self.recorded = False
        self.recorded_balance = 0

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    try:
        n_procs = int(next(it))
        n_events = int(next(it))
    except StopIteration:
        return

    procs = [Process(i, int(next(it))) for i in range(n_procs)]
    channels = [[collections.deque() for _ in range(n_procs)] for _ in range(n_procs)]
    recorded_channels = [[[] for _ in range(n_procs)] for _ in range(n_procs)]
    is_recording = [[False] * n_procs for _ in range(n_procs)]

    for _ in range(n_events):
        event_type = next(it)
        if event_type == "TRANSFER":
            u = int(next(it))
            v = int(next(it))
            amt = int(next(it))
            procs[u].balance -= amt
            channels[u][v].append((u, v, str(amt)))
        elif event_type == "RECEIVE":
            u = int(next(it))
            v = int(next(it))
            if channels[u][v]:
                msg = channels[u][v].popleft()
                if msg[2] == "MARKER":
                    if not procs[v].recorded:
                        procs[v].recorded = True
                        procs[v].recorded_balance = procs[v].balance
                        for k in range(n_procs):
                            if k != v and k != u:
                                is_recording[k][v] = True
                        for k in range(n_procs):
                            if k != v:
                                channels[v][k].append((v, k, "MARKER"))
                    else:
                        is_recording[u][v] = False
                else:
                    amt = int(msg[2])
                    procs[v].balance += amt
                    if is_recording[u][v]:
                        recorded_channels[u][v].append(msg[2])
        elif event_type == "SNAPSHOT_INIT":
            init_p = int(next(it))
            if not procs[init_p].recorded:
                procs[init_p].recorded = True
                procs[init_p].recorded_balance = procs[init_p].balance
                for k in range(n_procs):
                    if k != init_p:
                        is_recording[k][init_p] = True
                        channels[init_p][k].append((init_p, k, "MARKER"))

    out = []
    total_snapshot_money = 0
    for i in range(n_procs):
        out.append(f"P{i}: {procs[i].recorded_balance}")
        total_snapshot_money += procs[i].recorded_balance

    for u in range(n_procs):
        for v in range(n_procs):
            for msg_text in recorded_channels[u][v]:
                out.append(f"CHANNEL {u}->{v}: {msg_text}")
                total_snapshot_money += int(msg_text)

    out.append(f"TOTAL: {total_snapshot_money}")
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
