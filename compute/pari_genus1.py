"""PARI/GP driver for genus-1 quartic models y^2 = f(t) (entry 97).

Jacobian via ellfromeqn; rank bounds via ellrank (2-descent + Cassels-Tate);
torsion via elltors; rational points up to height H via hyperellratpoints.

THE FINITENESS ARGUMENT.  If the Jacobian E has rank 0 then E(Q) = E_tors is
finite, and C: y^2 = f(t) is either empty or a torsor under E(Q), so |C(Q)| =
|E_tors| exactly when C(Q) is nonempty.  Hence a height search that finds
|E_tors| points (the two points at infinity included when the leading
coefficient is a nonzero square) has found ALL rational points: the record is
then 'complete' and can be used as a certificate.  Fewer points found is
inconclusive (never a kill).
"""
from __future__ import annotations
import os
import re
import subprocess

GP = r"C:\Users\Will\pari-2.17.4\gp.exe"


def gp_available():
    return os.path.isfile(GP)


def quartic_points(coeffs, H=3000, timeout=300):
    """coeffs: integer coefficients of f (highest degree first), deg f in {3, 4}."""
    poly = " + ".join(f"({c})*t^{len(coeffs)-1-i}" for i, c in enumerate(coeffs))
    script = f"""
default(parisize, "256M");
f = {poly};
E = ellinit(ellfromeqn(y^2 - f));
r = ellrank(E);
T = elltors(E);
L = hyperellratpoints(f, {H});
print("RES ", r[1], " ", r[2], " ", T[1], " ", T[2], " | ", L);
"""
    try:
        cp = subprocess.run([GP, "-q", "-f"], input=script, capture_output=True, text=True, timeout=timeout)
    except (subprocess.TimeoutExpired, OSError) as e:
        return {"error": repr(e)[:80]}
    out = cp.stdout + cp.stderr
    m = re.search(r"RES\s+(\d+)\s+(\d+)\s+(\d+)\s+(\[[^\]]*\])\s+\|\s+(.*)", out, re.S)
    if not m:
        return {"error": out[-300:]}
    rank_lo, rank_hi, tors = int(m.group(1)), int(m.group(2)), int(m.group(3))
    pts = re.findall(r"\[\s*(-?\d+(?:/\d+)?)\s*,\s*(-?\d+(?:/\d+)?)\s*\]", m.group(5))
    tvals = sorted({p[0] for p in pts})
    lc = coeffs[0]
    r0 = int(round(abs(lc) ** 0.5))
    n_inf = 2 if (lc > 0 and r0 * r0 == lc and len(coeffs) == 5) else 0
    return {"rank_lo": rank_lo, "rank_hi": rank_hi, "torsion_order": tors, "torsion": m.group(4),
            "points": pts, "tvals": tvals, "n_points": len(pts), "n_inf": n_inf,
            "complete": (rank_hi == 0 and len(pts) + n_inf == tors)}
