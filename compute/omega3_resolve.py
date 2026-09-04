"""THE EXACT GENUS by resolution of singularities (entry 103).

For an absolutely irreducible plane curve Phi(t, x) = 0 of bidegree (dg, dh)
in P^1 x P^1, g = p_a - sum_Q delta_Q with p_a = (dg-1)(dh-1) and, for each
singular point Q, delta_Q = sum over the infinitely near points P of
m_P (m_P - 1)/2 -- the points reached by blowing up until every point is
smooth.  The same process counts the branches: r_Q = the number of smooth
terminal points.  Blow-up at a point of multiplicity m with tangent cone C
(the homogeneous part of degree m of the local equation F(T, X)): the
directions X = lam T are the roots of C(1, lam); for each, the strict transform
F(T, T(X + lam)) / T^m at (0, 0); the direction T = 0 is present when C is
divisible by T (deg_X C < m), with strict transform F(X T, X) / X^m.  An
irreducible factor of degree e > 1 of C(1, lam) over the current field gives e
conjugate directions with identical local structure: the field is EXTENDED by
the factor (PARI rnfequation -> an absolute monic field; every coefficient is
transported by the embedding of the old generator), one direction is resolved
there and counted e times.  The singular points themselves are found in the
four charts of P^1 x P^1 as the common zeros of Phi and its two partials
(gcd of resultants over Q, factored; the x-coordinate factored over the field
of the t-value); a point with coordinates in an extension is handled by the
same extension mechanism and counted with its conjugates.  Every field is built
from a MONIC INTEGRAL polynomial and factored with nffactor against that same
field (PARI's factor over a non-monic modulus changes the generator).

CROSS-CHECK.  With r_Q known, Riemann-Hurwitz for the t-projection is exact:
R = R_lb + sum_{Q sing} (m_Q - r_Q), R_lb the multiplicity bound of
compute.omega3_genus (which used r_Q <= m_Q); so 2g = 2 - 2 dh + R must equal
2 (p_a - sum delta_Q).  Both are computed; agreement is required.
"""
from __future__ import annotations
import re
import subprocess
import sympy as sp

from compute.omega3 import tg, th
from compute.omega3_genus import _pari_poly, ramification_bound, PARI_FIELD
from compute.pari_genus1 import GP


def _gp(script, timeout=900):
    try:
        cp = subprocess.run([GP, "-q", "-f"], input='default(parisize,"1G");\n' + script, capture_output=True, text=True, timeout=timeout)
    except (subprocess.TimeoutExpired, OSError) as e:
        return "", repr(e)
    return cp.stdout, cp.stderr


# variable priorities (creation order): x > t > w4 > w3 > w2 > w1 > a
PARI_LIB = r"""
x; t; w4; w3; w2; w1; a;
WV = [w1, w2, w3, w4];
mult(F) = { my(m = 10^9, cT); if(F == 0, return(-1));
  for(i = 0, poldegree(F, t), cT = polcoeff(F, i, t); if(cT == 0, next);
    for(j = 0, poldegree(cT, x), if(polcoeff(cT, j, x) != 0, m = min(m, i + j))));
  m };
hompart(F, m) = { my(C = 0, cT); for(i = 0, m, cT = polcoeff(F, i, t); if(cT == 0, next);
  if(poldegree(cT, x) >= m - i, C += polcoeff(cT, m - i, x) * t^i * x^(m - i))); C };
monicint(q, v) = { my(D = 1, n = poldegree(q, v), c, qm);
  for(i = 0, n, D = lcm(D, denominator(polcoeff(q, i, v))));
  qm = q * D; c = pollead(qm, v);
  qm = subst(qm, v, v / c) * c^(n - 1);
  [qm, c] };
extend(fld, f) = { my(nfK, v, lvl, wv, fw, RE, absP, alpha, k, nfL, lam, mf, Dn);
  v = fld[1]; lvl = fld[3]; nfK = fld[2];
  if(lvl >= 4, error("extension depth"));
  wv = WV[lvl + 1];
  fw = subst(lift(f), x, wv);
  if(nfK == 0,
    mf = monicint(fw, wv); absP = mf[1]; alpha = 0; lam = Mod(wv, absP) / mf[2],
    fw = fw / pollead(fw, wv);
    RE = rnfequation(nfK, fw, 1); absP = RE[1]; alpha = RE[2]; k = RE[3];
    mf = monicint(absP, wv); Dn = mf[2];
    absP = mf[1];
    alpha = Mod(subst(lift(alpha), wv, wv / Dn), absP);
    lam = Mod(wv, absP) / Dn - k * alpha);
  if(pollead(absP, wv) != 1 || denominator(content(absP)) != 1, error("non-monic absolute field"));
  nfL = nfinit(absP);
  [[wv, nfL, lvl + 1], lam, alpha] };
tr(e, fld, alpha) = if(fld[2] == 0, e, subst(lift(e), fld[1], alpha));
rootfactor(fld, Cl) = { my(F); if(fld[2] == 0, factor(Cl), fieldfactor(fld[2], Cl)) };
resolve(F, fld, depth) = { my(m, C, Cl, Fl, delta, r, e, lam, F1, F2, res, degx, f, ex, F0, fld2);
  if(depth > 16, error("resolution depth"));
  m = mult(F);
  if(m <= 0, error("bad local equation"));
  if(m == 1, return([0, 1]));
  delta = m * (m - 1) / 2; r = 0;
  C = hompart(F, m);
  Cl = subst(C, t, 1);
  degx = poldegree(Cl, x);
  if(degx > 0, Fl = rootfactor(fld, Cl);
    for(i = 1, #Fl~, f = Fl[i,1]; e = poldegree(f, x);
      if(e == 1,
        lam = -polcoeff(f, 0, x) / polcoeff(f, 1, x);
        F1 = subst(F, x, t * (x + lam)) / t^m;
        if(type(F1) != "t_POL", error("inexact strict transform"));
        res = resolve(F1, fld, depth + 1); delta += res[1]; r += res[2],
        ex = extend(fld, f); fld2 = ex[1]; lam = ex[2];
        F0 = tr(F, fld, ex[3]);
        F1 = subst(F0, x, t * (x + lam)) / t^m;
        if(type(F1) != "t_POL", error("inexact strict transform (ext)"));
        res = resolve(F1, fld2, depth + 1); delta += e * res[1]; r += e * res[2])));
  if(degx < m,
    F2 = subst(F, t, x * t) / x^m;
    if(type(F2) != "t_POL", error("inexact strict transform (vertical)"));
    res = resolve(F2, fld, depth + 1); delta += res[1]; r += res[2]);
  [delta, r] };
singular_x(P, A) = gcd(gcd(subst(P, t, A), subst(deriv(P, x), t, A)), subst(deriv(P, t), t, A));
"""


def exact_genus(phi, dg, dh, timeout=900):
    """(g, details): g = p_a - sum delta over all singular points (with conjugates),
    details = the singular points (chart, t-factor, x-factor degree, m, delta, r,
    conjugates) and the branch correction sum conj*(m - r)."""
    s = _pari_poly(phi)
    charts = [("tx", "phi"), ("Tx", f"numerator(subst(phi, t, 1/t) * t^{dg})"),
              ("tX", f"numerator(subst(phi, x, 1/x) * x^{dh})"),
              ("TX", f"numerator(subst(subst(phi, t, 1/t), x, 1/x) * t^{dg} * x^{dh})")]
    script = PARI_LIB + PARI_FIELD + f"\nphi = {s}; dg = {dg}; dh = {dh};\n" + "{\n"
    script += "total = 0; corr = 0;\n"
    for name, expr in charts:
        only_t0 = "T" in name
        only_x0 = "X" in name
        script += f"P = {expr};\n"
        script += "r1 = polresultant(P, deriv(P, x), x); r2 = polresultant(P, deriv(P, t), x); g = gcd(r1, r2);\n"
        script += "if(poldegree(g, t) > 0, Fq = factor(g), Fq = matrix(0, 2));\n"
        script += "for(i = 1, #Fq~, q = Fq[i,1]; if(poldegree(q, t) == 0, next);\n"
        if only_t0:
            script += "  if(q != t, next);\n"
        script += "  qa = subst(q, t, a); cq = poldegree(qa, a);\n"
        script += "  if(cq == 1, A = -polcoeff(qa, 0, a) / polcoeff(qa, 1, a); fld = [a, 0, 0],\n"
        script += "    mf = monicfield(qa); nfq = nfinit(mf[1]); A = Mod(a, mf[1]) / mf[2]; fld = [a, nfq, 0]);\n"
        script += "  h = singular_x(P, A); if(type(h) != \"t_POL\" || poldegree(h, x) <= 0, next);\n"
        script += "  Fh = rootfactor(fld, h);\n"
        script += "  for(j = 1, #Fh~, f = Fh[j,1]; ex_ = poldegree(f, x);\n"
        script += "    if(ex_ == 1, x0 = -polcoeff(f, 0, x) / polcoeff(f, 1, x); fldp = fld; Pp = P; Ap = A,\n"
        script += "      ex = extend(fld, f); fldp = ex[1]; x0 = ex[2]; Pp = P; Ap = tr(A, fld, ex[3]));\n"
        if only_x0:
            script += "    if(x0 != 0, next);\n"
        script += "    F = subst(subst(Pp, t, t + Ap), x, x + x0);\n"
        script += "    m = mult(F); res = resolve(F, fldp, 0);\n"
        script += f"    print(\"SING {name} | \", q, \" | \", ex_, \" \", m, \" \", res[1], \" \", res[2], \" \", cq);\n"
        script += "    total += cq * ex_ * res[1]; corr += cq * ex_ * (m - res[2])));\n"
    script += "print(\"RES \", total, \" \", corr);\n}\n"
    out, err = _gp(script, timeout)
    m = re.search(r"RES\s+(-?\d+)\s+(-?\d+)", out)
    sings = [dict(chart=a, tfactor=b.strip(), xdeg=int(c), m=int(d), delta=int(e), r=int(f), conj=int(g))
             for a, b, c, d, e, f, g in re.findall(r"SING\s+(\S+)\s+\|\s+(.*?)\s+\|\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)", out)]
    if not m:
        return None, {"error": (out[-300:] + " | " + err[-400:]).strip(), "singular": sings}
    total_delta, corr = int(m.group(1)), int(m.group(2))
    pa = (dg - 1) * (dh - 1)
    return pa - total_delta, {"p_a": pa, "sum_delta": total_delta, "branch_correction": corr, "singular": sings}


def pullback_genera(phi, dg, dh, timeout=900):
    """For a component of genus <= 1: the Pythagorean pullback Psi(tau_g, tau_h) =
    numer(Phi(2tg/(1-tg^2), 2th/(1-th^2))) factored over Q in PARI, and the exact
    genus (with the cross-check) and absolute-irreducibility certificate of every
    factor.  A rational point of Phi that is a Pythagorean frame pair lifts to a
    rational point of some factor, so if every factor has genus >= 2 the component
    has finitely many frame pairs.  Returns a list of factor records."""
    from compute.omega3_genus import absolutely_irreducible
    s = _pari_poly(phi)
    script = ("x; t;\nphi = " + s + ";\n{\npb = numerator(subst(subst(phi, t, 2*t/(1-t^2)), x, 2*x/(1-x^2)));\n"
              "F = factor(pb);\nfor(i = 1, #F~, f = F[i,1]; if(poldegree(f, t) > 0 && poldegree(f, x) > 0, "
              "print(\"FAC \", F[i,2], \" | \", f)));\n}\n")
    out, err = _gp(script, timeout)
    facs = []
    for line in out.splitlines():
        if not line.startswith("FAC "):
            continue
        mult, body = line[4:].split("|", 1)
        fe = sp.expand(sp.sympify(body.strip().replace("^", "**"), locals={"t": tg, "x": th}))
        P = sp.Poly(fe, tg, th)
        eg, eh = P.degree(tg), P.degree(th)
        g, det = exact_genus_checked(fe, eg, eh)
        facs.append({"deg": (eg, eh), "mult": int(mult), "genus": g, "consistent": det.get("consistent"),
                     "abs_irred_p": absolutely_irreducible(fe), "error": det.get("error")})
    return facs


def exact_genus_checked(phi, dg, dh, degmax=400):
    """Exact genus with the Riemann-Hurwitz cross-check; returns (g, details).
    The cross-check needs every discriminant factor (cap 400: the (8,8)
    components have one factor of degree between 40 and 400)."""
    g, det = exact_genus(phi, dg, dh)
    if g is None:
        return None, det
    R, info = ramification_bound(phi, dg, dh, swap=False, degmax=degmax)
    det["rh"] = {"R_lb": R, "info": info}
    if R is not None and info.get("skipped_factors", 0) == 0:
        two_g = 2 - 2 * dh + R + det["branch_correction"]
        det["rh"]["two_g"] = two_g
        det["consistent"] = (two_g == 2 * g)
    else:
        det["consistent"] = None
    return g, det
