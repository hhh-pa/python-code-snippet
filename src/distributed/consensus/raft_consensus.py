import sys

class RaftNode:
    def __init__(self, id_):
        self.id = id_
        self.role = "FOLLOWER"
        self.current_term = 0
        self.voted_for = -1
        self.log = []
        self.commit_index = -1

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    try:
        n_nodes = int(next(it))
        n_events = int(next(it))
    except StopIteration:
        return

    cluster = [RaftNode(i) for i in range(n_nodes)]
    majority = n_nodes // 2 + 1
    out = []

    for _ in range(n_events):
        event_type = next(it)
        if event_type == "START_ELECTION":
            candidate_id = int(next(it))
            cand = cluster[candidate_id]
            cand.role = "CANDIDATE"
            cand.current_term += 1
            cand.voted_for = candidate_id
            votes = 1
            for i in range(n_nodes):
                if i == candidate_id:
                    continue
                peer = cluster[i]
                if peer.current_term < cand.current_term:
                    peer.current_term = cand.current_term
                    peer.role = "FOLLOWER"
                    peer.voted_for = candidate_id
                    votes += 1
            if votes >= majority:
                cand.role = "LEADER"
                out.append(f"LEADER ELECTED: {candidate_id} TERM: {cand.current_term}")
            else:
                cand.role = "FOLLOWER"
                out.append(f"ELECTION FAILED: {candidate_id}")
        elif event_type == "APPEND_ENTRY":
            leader_id = int(next(it))
            cmd = next(it)
            leader = cluster[leader_id]
            if leader.role != "LEADER":
                out.append("REJECT NOT LEADER")
                continue
            leader.log.append((leader.current_term, cmd))
            replicated = 1
            for i in range(n_nodes):
                if i == leader_id:
                    continue
                peer = cluster[i]
                peer.current_term = leader.current_term
                peer.role = "FOLLOWER"
                peer.log.append((leader.current_term, cmd))
                replicated += 1
            if replicated >= majority:
                leader.commit_index = len(leader.log) - 1
                for i in range(n_nodes):
                    cluster[i].commit_index = leader.commit_index
                out.append(f"COMMITTED {cmd} AT INDEX {leader.commit_index}")
        elif event_type == "PRINT_STATE":
            node_id = int(next(it))
            node = cluster[node_id]
            out.append(f"NODE {node_id} ROLE {node.role} TERM {node.current_term} COMMITTED {node.commit_index}")

    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
