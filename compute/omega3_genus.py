"""A RIGOROUS LOWER BOUND ON THE GEOMETRIC GENUS of a plane curve (entries 102-103).

For an absolutely irreducible Phi(t, x) = 0 (bidegree (dg, dh) in P^1 x P^1),
project to the t-line: degree dh.  Riemann-Hurwitz for the normalization:
    2g - 2 = -2 dh + sum_P (e_P - 1),
and over a value b the ramification is dh - #{points of the normalization over
b} >= dh - sum_{Q over b} m_Q, because a point Q of multiplicity m_Q carries at
most m_Q branches.  Writing I_Q for the intersection multiplicity of the
vertical line with the curve at Q (the root multiplicity of x_Q in Phi(b, x),
including x = infinity), sum_Q I_Q = dh, so the contribution over b is at least
sum_Q (I_Q - m_Q) >= 0, nonzero only at roots b of the discriminant or of the
leading coefficient, or at b = infinity.  Hence
    g >= 1 - dh + (1/2) sum_b sum_{Q over b} (I_Q - m_Q),
computed EXACTLY: the branch values are grouped by the irreducible factors q of
Disc_x(Phi) * lc_x(Phi) over Q; over a root of q the fiber is factored in the
number field K = Q[a]/(q~) -- q~ the MONIC INTEGRAL polynomial c^{n-1} q(a/c)
of the scaled root c*b (PARI's factor over a non-monic modulus silently changes
the generator; nffactor against nfinit(q~) keeps every object in one
presentation -- the entry-103 fix) -- each factor h of multiplicity I giving
deg(h) conjugate points; the multiplicity m of those points is the least k for
which some order-k partial derivative of Phi, evaluated at t = b, is not
divisible by h in K[x].  The point x = infinity and the value b = infinity are
handled in the charts x -> 1/x, t -> 1/t.  Factors q of degree above a cap are
skipped (their contribution is >= 0, so skipping keeps the bound valid).  The
bound is taken for both projections.

ABSOLUTE IRREDUCIBILITY (needed for the genus to be the genus of one curve): Phi
irreducible over F_p with a smooth F_p-point is absolutely irreducible (Frobenius
permutes the absolute components transitively and a smooth rational point lies
on exactly one).  If Phi is irreducible over Q but not absolutely irreducible,
every rational point lies on all the conjugate components at once, i.e. in a
finite set -- finiteness holds anyway.

A bound g >= 2 with a certificate of absolute irreducibility makes the
component Faltings-finite: 'finite' (not yet effective).
"""
from __future__ import annotations
import re
import subprocess
import sympy as sp

from compute.omega3 import tg, th
from compute.pari_genus1 import GP

X, Tt = sp.symbols("x t")


def _gp(script, timeout=600):
    try:
        cp = subprocess.run([GP, "-q", "-f"], input='default(parisize,"1G");\n' + script, capture_output=True, text=True, timeout=timeout)
    except (subprocess.TimeoutExpired, OSError) as e:
        return "", repr(e)
    return cp.stdout, cp.stderr


def _pari_poly(phi, swap=False):
    """phi(tg, th) as a PARI string in variables t (= tg) and x (= th); swap
    exchanges the roles (project to the th-line instead)."""
    if swap:
        e = phi.subs({tg: X, th: Tt}, simultaneous=True)
    else:
        e = phi.subs({tg: Tt, th: X}, simultaneous=True)
    return str(sp.expand(e)).replace("**", "^")


PARI_FIELD = r"""
monicfield(q) = { my(n = poldegree(q, a), c = pollead(q, a), qm);
  qm = subst(q, a, a / c) * c^(n - 1); qm = qm / content(qm) * denominator(content(qm));
  if(pollead(qm, a) != 1, qm = qm / pollead(qm, a));
  [qm, c] };
fieldfactor(nfq, P) = { my(F, v = variable(nfq.pol));
  F = nffactor(nfq, P);
  for(i = 1, #F~, F[i,1] = subst(lift(F[i,1]), v, Mod(v, nfq.pol)));
  F };
"""


def ramification_bound(phi, dg, dh, swap=False, degmax=40, timeout=900, nf_seconds=0):
    """Lower bound R_lb on the ramification of the projection to the t-line;
    returns (R_lb, details) or (None, error).  nf_seconds > 0 puts an alarm on
    each branch-value field's nfinit: a field that takes longer is SKIPPED,
    which only lowers the bound (entry 104: (2,1,1) branch fields reach degree
    36 with 300-bit discriminants, minutes each)."""
    if swap:
        dg, dh = dh, dg
    s = _pari_poly(phi, swap)
    script = "x; t; a;\n" + PARI_FIELD + f"""
phi = {s};
dg = {dg}; dh = {dh}; DEGMAX = {degmax}; NFSEC = {nf_seconds};
mult(P, A, h) = {{ my(k = 0, ok = 1, d);
  while(ok, k++; ok = 1;
    for(i = 0, k, d = P; for(u = 1, i, d = deriv(d, t)); for(u = 1, k - i, d = deriv(d, x));
      d = subst(d, t, A); if(d != 0 && (d % h) != 0, ok = 0)));
  k }};
contrib(P, A, nfq) = {{ my(PK, F, R = 0, mI, h, m, degx, Pst);
  PK = subst(P, t, A);
  if(PK == 0, return([-1, "fiber vanishes"]));
  degx = poldegree(PK, x);
  if(degx > 0, F = if(nfq == 0, factor(PK), fieldfactor(nfq, PK));
    for(i = 1, #F~, h = F[i,1]; mI = F[i,2]; m = mult(P, A, h); R += poldegree(h, x) * (mI - m)));
  if(degx < dh,
    Pst = numerator(subst(P, x, 1/x) * x^dh); mI = dh - degx; m = mult(Pst, A, x); R += (mI - m));
  [R, ""] }};
{{
R = 0; skipped = 0; notes = "";
D = poldisc(phi, x); L = pollead(phi, x);
F = factor(D * L);
for(i = 1, #F~, q = F[i,1]; if(poldegree(q, t) <= 0, next); if(poldegree(q, t) > DEGMAX, skipped++; next);
  qa = subst(q, t, a);
  if(poldegree(qa, a) == 1, A = -polcoeff(qa, 0, a) / polcoeff(qa, 1, a); nfq = 0,
    mf = monicfield(qa);
    nfq = if(NFSEC > 0, alarm(NFSEC, nfinit(mf[1])), nfinit(mf[1]));
    if(type(nfq) == "t_ERROR", skipped++; next);
    A = Mod(a, mf[1]) / mf[2]);
  c = contrib(phi, A, nfq); if(c[1] < 0, notes = concat(notes, c[2]); next);
  R += poldegree(qa, a) * c[1]);
phi2 = numerator(subst(phi, t, 1/t) * t^dg);
c = contrib(phi2, 0, 0); if(c[1] >= 0, R += c[1], notes = concat(notes, c[2]));
print("RES ", R, " ", skipped, " ", notes);
}}
"""
    out, err = _gp(script, timeout)
    m = re.search(r"RES\s+(-?\d+)\s+(\d+)\s*(.*)", out)
    if not m:
        return None, (out[-300:] + " | " + err[-300:])
    return int(m.group(1)), {"skipped_factors": int(m.group(2)), "notes": m.group(3).strip()}


def genus_lower_bound(phi, dg, dh, degmax=40, timeout=900, nf_seconds=0):
    """max over the two projections of ceil((2 - 2 deg + R_lb)/2)."""
    best, info = None, {}
    for swap in (False, True):
        d = dg if swap else dh
        R, det = ramification_bound(phi, dg, dh, swap=swap, degmax=degmax, timeout=timeout, nf_seconds=nf_seconds)
        if R is None:
            info["swap" if swap else "direct"] = {"error": str(det)[:200]}
            continue
        g = -(-(2 - 2 * d + R) // 2)          # ceil
        info["swap" if swap else "direct"] = {"deg": d, "R_lb": R, "g_lb": g, **det}
        if best is None or g > best:
            best = g
    return best, info


def absolutely_irreducible(phi, primes=(101, 103, 107, 109, 113), timeout=300):
    """Certificate: irreducible mod p and a smooth F_p-point, for some p."""
    s = _pari_poly(phi)
    script = "x; t;\nphi = " + s + ";\n"
    script += "for(k = 1, %d, p = [%s][k]; F = factor(phi * Mod(1, p)); if(#F~ != 1 || F[1,2] != 1, next);" % (len(primes), ",".join(map(str, primes)))
    script += (" found = 0; for(u = 0, p-1, for(v = 0, p-1, if(subst(subst(phi, t, u), x, v) % p == 0,"
               " if(subst(subst(deriv(phi, t), t, u), x, v) % p != 0 || subst(subst(deriv(phi, x), t, u), x, v) % p != 0, found = 1; break(2)))));"
               " if(found, print(\"RES \", p); break));\n")
    out, err = _gp(script, timeout)
    m = re.search(r"RES\s+(\d+)", out)
    return (int(m.group(1)) if m else None)
