"""Top-level workers for parallel quadruple-box processing (Windows spawn
needs importable functions).  Used by the omega=2 extension runner."""
from compute.lucas_endpoints import kill_pattern
from compute.quadruple import pooled_kill, joint_residual_kill


def _to_pat(rows):
    return tuple((tuple(jk), c) for jk, c in rows)


def open_or_none(rows):
    """Return the pattern (as rows) if it survives the full machine, else None."""
    pat = _to_pat(rows)
    try:
        v, _c = kill_pattern(pat)
    except Exception:
        return rows            # conservative: treat as open (will be inspected)
    return None if v.startswith("DEAD") else rows


def kill_pair(pair):
    """(rows1, rows2) -> verdict string: 'pincer' / 'joint' / 'OPEN:<reason>'."""
    T1 = _to_pat(pair[0])
    T2 = _to_pat(pair[1])
    try:
        ok, info = pooled_kill(T1, T2)
        if ok:
            return "pincer"
        jr = joint_residual_kill(T1, T2)
        return "joint" if jr.get("kills") else ("OPEN:" + str(jr))
    except Exception as e:
        return "ERR:" + repr(e)[:80]
