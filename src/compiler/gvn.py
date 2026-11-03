import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    idx = 0
    try:
        n_inst = int(tokens[idx])
    except (ValueError, IndexError):
        return
    idx += 1

    insts = []
    for _ in range(n_inst):
        if idx >= len(tokens):
            return
        dest = tokens[idx]
        # eq = tokens[idx + 1]
        opcode = tokens[idx + 2]
        idx += 3
        if opcode == "CONST":
            val = tokens[idx]
            idx += 1
            insts.append((dest, opcode, val, ""))
        elif opcode == "COPY":
            src = tokens[idx]
            idx += 1
            insts.append((dest, opcode, src, ""))
        else:
            a1 = tokens[idx]
            a2 = tokens[idx + 1]
            idx += 2
            insts.append((dest, opcode, a1, a2))

    var_to_vn = {}
    vn_to_rep = {}
    expr_to_vn = {}
    const_to_vn = {}

    next_vn = 1
    redundant_count = 0

    def get_var_vn(v):
        nonlocal next_vn
        if v in var_to_vn:
            return var_to_vn[v]
        vn = next_vn
        next_vn += 1
        var_to_vn[v] = vn
        vn_to_rep[vn] = v
        return vn

    out = []
    for dest, opcode, arg1, arg2 in insts:
        if opcode == "CONST":
            val = int(arg1)
            if val in const_to_vn:
                vn = const_to_vn[val]
                var_to_vn[dest] = vn
                redundant_count += 1
                out.append(f"{dest} = {vn_to_rep[vn]} (VN{vn} REDUNDANT)")
            else:
                vn = next_vn
                next_vn += 1
                const_to_vn[val] = vn
                var_to_vn[dest] = vn
                vn_to_rep[vn] = dest
                out.append(f"{dest} = CONST {val} (VN{vn})")
        elif opcode == "COPY":
            src_vn = get_var_vn(arg1)
            var_to_vn[dest] = src_vn
            redundant_count += 1
            out.append(f"{dest} = {vn_to_rep[src_vn]} (VN{src_vn} REDUNDANT)")
        elif opcode == "PHI":
            vn1 = get_var_vn(arg1)
            vn2 = get_var_vn(arg2)
            if vn1 == vn2:
                var_to_vn[dest] = vn1
                redundant_count += 1
                out.append(f"{dest} = {vn_to_rep[vn1]} (VN{vn1} REDUNDANT PHI)")
            else:
                if vn1 > vn2:
                    vn1, vn2 = vn2, vn1
                expr_key = ("PHI", vn1, vn2)
                if expr_key in expr_to_vn:
                    vn = expr_to_vn[expr_key]
                    var_to_vn[dest] = vn
                    redundant_count += 1
                    out.append(f"{dest} = {vn_to_rep[vn]} (VN{vn} REDUNDANT)")
                else:
                    vn = next_vn
                    next_vn += 1
                    expr_to_vn[expr_key] = vn
                    var_to_vn[dest] = vn
                    vn_to_rep[vn] = dest
                    out.append(f"{dest} = PHI VN{vn1} VN{vn2} (VN{vn})")
        else:
            vn1 = get_var_vn(arg1)
            vn2 = get_var_vn(arg2)
            op = opcode
            if op in ("ADD", "MUL") and vn1 > vn2:
                vn1, vn2 = vn2, vn1
            expr_key = (op, vn1, vn2)
            if expr_key in expr_to_vn:
                vn = expr_to_vn[expr_key]
                var_to_vn[dest] = vn
                redundant_count += 1
                out.append(f"{dest} = {vn_to_rep[vn]} (VN{vn} REDUNDANT)")
            else:
                vn = next_vn
                next_vn += 1
                expr_to_vn[expr_key] = vn
                var_to_vn[dest] = vn
                vn_to_rep[vn] = dest
                out.append(f"{dest} = {op} VN{vn1} VN{vn2} (VN{vn})")

    out.append(f"Total unique VNs: {next_vn - 1}")
    out.append(f"Redundant instructions eliminated: {redundant_count}")
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
