import sys

def main():
    lines = sys.stdin.read().splitlines()
    if not lines:
        return
    idx = 0
    while idx < len(lines) and not lines[idx].strip():
        idx += 1
    if idx >= len(lines):
        return
    try:
        n = int(lines[idx].strip())
    except ValueError:
        return
    idx += 1

    scopes = [{}]
    chain = [0]
    nextid = 1
    declares = 0
    errors = 0
    out = []

    commands_processed = 0
    while idx < len(lines) and commands_processed < n:
        line = lines[idx].strip()
        idx += 1
        if not line:
            continue
        commands_processed += 1
        t = line.split()
        cmd = t[0]

        if cmd == "ENTER":
            scopes.append({})
            chain.append(nextid)
            nextid += 1
            out.append(f"ENTER {len(scopes) - 1}")
        elif cmd == "EXIT":
            if len(scopes) <= 1:
                out.append("EXIT UNDERFLOW")
                errors += 1
            else:
                scopes.pop()
                chain.pop()
                out.append(f"EXIT {len(scopes) - 1}")
        elif cmd == "DECLARE" and len(t) >= 3:
            name, typ = t[1], t[2]
            if name in scopes[-1]:
                out.append(f"DECLARE {name} {typ} REDECLARED")
                errors += 1
            else:
                scopes[-1][name] = typ
                out.append(f"DECLARE {name} {typ} OK")
                declares += 1
        elif cmd == "LOOKUP" and len(t) >= 2:
            name = t[1]
            found = False
            for d in range(len(scopes) - 1, -1, -1):
                if name in scopes[d]:
                    out.append(f"LOOKUP {name} {scopes[d][name]} {d}")
                    found = True
                    break
            if not found:
                out.append(f"LOOKUP {name} UNDECLARED")
                errors += 1
        elif cmd == "ASSIGN" and len(t) >= 2:
            name = t[1]
            found = False
            for d in range(len(scopes) - 1, -1, -1):
                if name in scopes[d]:
                    out.append(f"ASSIGN {name} OK {d}")
                    found = True
                    break
            if not found:
                out.append(f"ASSIGN {name} UNDECLARED")
                errors += 1
        elif cmd == "DISPLAY":
            disp = " ".join(f"{d}:{chain[d]}" for d in range(len(chain)))
            out.append(f"DISPLAY {disp}")

    out.append(f"SYMTAB declares={declares} errors={errors}")
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
