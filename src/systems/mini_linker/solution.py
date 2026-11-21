"""Mini static linker (CS:APP ch 7: resolution + relocation)."""

import sys


def _layout(files):
    text_base, data_base = [], []
    addr = 0
    for ts, _, _, _ in files:
        text_base.append(addr)
        addr += ts
    text_size = addr
    for _, ds, _, _ in files:
        data_base.append(addr)
        addr += ds
    return text_base, data_base, text_size, addr - text_size


def _resolve(files, text_base, data_base):
    defs = {}
    for fi, (_, _, dd, _) in enumerate(files):
        for name, sec, off, _size, strong in dd:
            base = text_base[fi] if sec == "TEXT" else data_base[fi]
            defs.setdefault(name, []).append((strong, fi, base + off))
    needed = set()
    for _, _, _, rr in files:
        for _, _, name, _ in rr:
            needed.add(name)
    syms = {}
    for name in sorted(set(defs) | needed):
        ds = defs.get(name, [])
        if not ds:
            return None, f"ERROR undefined {name}"
        strong = [d for d in ds if d[0] == 1]
        if len(strong) > 1:
            return None, f"ERROR multiply-defined {name}"
        syms[name] = strong[0][2] if strong else sorted(ds, key=lambda d: d[1])[0][2]
    return syms, None


def _run(files):
    text_base, data_base, text_size, data_size = _layout(files)
    syms, err = _resolve(files, text_base, data_base)
    if err is not None:
        return [err]
    out = [f"TEXT 0 {text_size}", f"DATA {text_size} {data_size}"]
    for name in sorted(syms):
        out.append(f"SYM {name} {syms[name]}")
    for fi, (_, _, _, rr) in enumerate(files):
        for sec, off, name, kind in rr:
            base = text_base[fi] if sec == "TEXT" else data_base[fi]
            place = base + off
            val = syms[name] if kind == "ABS" else syms[name] - (place + 4)
            out.append(f"PATCH {fi} {sec} {off} {val}")
    return out


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    m = int(toks[0])
    files = []
    i = 1
    for _ in range(m):
        ts, ds = int(toks[i]), int(toks[i + 1])
        nd = int(toks[i + 2])
        i += 3
        dd = []
        for _ in range(nd):
            dd.append(
                (
                    toks[i],
                    toks[i + 1],
                    int(toks[i + 2]),
                    int(toks[i + 3]),
                    int(toks[i + 4]),
                )
            )
            i += 5
        nr = int(toks[i])
        i += 1
        rr = []
        for _ in range(nr):
            rr.append((toks[i], int(toks[i + 1]), toks[i + 2], toks[i + 3]))
            i += 4
        files.append((ts, ds, dd, rr))
    sys.stdout.write("\n".join(_run(files)))


if __name__ == "__main__":
    main()
