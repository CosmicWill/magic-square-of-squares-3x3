"""THE MINOR FORMULA: the quadruple curves as pullbacks of the circle (entry 105;
ROADMAP R.9 attempt C, first step).

In the frame f to eliminate, every element of the (1,1,1) box is LINEAR in
    (X, Y, N) = (2 c_f s_f, c_f^2 - s_f^2, c_f^2 + s_f^2),      X^2 + Y^2 = N^2
(an element with |l| = 1 is Im((Y +- iX) Z) = Y Im Z +- X Re Z, one with l = 0 is
N Im Z', Z and Z' monomials in the other two frames), so the two relations are
    R1 = a1 X + b1 Y + c1 N,    R2 = a2 X + b2 Y + c2 N,
a_i, b_i, c_i bihomogeneous forms of bidegree <= (2,2) in the frames g, h.  With
R_i = A_i c_f^2 + B_i c_f s_f + C_i s_f^2 one has (a_i, b_i, c_i) = (B_i/2, (A_i - C_i)/2,
(A_i + C_i)/2), and the classical resultant of two binary quadratics,
Res = (A1 C2 - A2 C1)^2 - (A1 B2 - A2 B1)(B1 C2 - B2 C1), is EXACTLY
    Res_{s_f}(R1, R2) = 4 (D_X^2 + D_Y^2 - D_N^2),   (D_X, D_Y, D_N) = (a1,b1,c1) x (a2,b2,c2).
THEOREM.  Every quadruple curve Phi_f is a component of the pullback of the circle
X^2 + Y^2 = N^2 under the minor map m = (D_X : D_Y : D_N) of bidegree <= (4,4).
Consequences: bidegree <= (8,8); the singular points are the BASE POINTS of m
(D_X = D_Y = D_N = 0: the two relations proportional, the third frame free on a
line meeting the circle twice -- a node) or tangency points of m with the circle,
which on the whole box lie only over t in {0, +-1, +-i, tan(+-22.5 deg)}; and the
third frame in closed form: (X : Y : N) = (D_X : D_Y : D_N), t_f = D_X / (D_N + D_Y),
Pythagorean condition 2 D_N (D_N + D_Y) = square on Phi_f.
"""
from __future__ import annotations
import re
import subprocess
import sympy as sp

from compute.omega3 import reduced_relations, FR, tg, th
from compute.omega3_genus import _pari_poly, PARI_FIELD
from compute.pari_genus1 import GP


def minor_rows(cand, f):
    """The two rows (a_i, b_i, c_i) of the relations in (X, Y, N), as forms in the
    other two frames, and the reduced relations."""
    R1, R2, common = reduced_relations(cand)
    cf, sf = FR[f]
    rows = []
    for R in (R1, R2):
        P = sp.Poly(R, cf, sf)
        A, B, C = P.coeff_monomial(cf ** 2), P.coeff_monomial(cf * sf), P.coeff_monomial(sf ** 2)
        if sp.expand(R - (A * cf ** 2 + B * cf * sf + C * sf ** 2)) != 0:
            raise ValueError("a relation is not a quadratic form in the eliminated frame")
        rows.append([sp.expand(B / 2), sp.expand((A - C) / 2), sp.expand((A + C) / 2)])
    return rows, (R1, R2)


def minors(cand, f, ratio=True):
    """(D_X, D_Y, D_N) = row1 x row2; in the ratio form (c_g = c_h = 1, s = t) when
    ratio is True."""
    rows, _ = minor_rows(cand, f)
    (a1, b1, c1), (a2, b2, c2) = rows
    DX, DY, DN = sp.expand(b1 * c2 - b2 * c1), sp.expand(c1 * a2 - c2 * a1), sp.expand(a1 * b2 - a2 * b1)
    if not ratio:
        return DX, DY, DN
    g, h = [i for i in range(3) if i != f]
    (cg, sg), (ch, sh) = FR[g], FR[h]
    sub = {sg: tg, sh: th, cg: 1, ch: 1}
    return tuple(sp.expand(m.subs(sub, simultaneous=True)) for m in (DX, DY, DN))


def resultant_identity(cand, f):
    """Res_{s_f}(R1, R2) == 4 (D_X^2 + D_Y^2 - D_N^2) as polynomials (c_f = 1)."""
    rows, (R1, R2) = minor_rows(cand, f)
    cf, sf = FR[f]
    Res = sp.resultant(sp.Poly(R1.subs(cf, 1), sf), sp.Poly(R2.subs(cf, 1), sf))
    DX, DY, DN = minors(cand, f, ratio=False)
    return sp.expand(Res - 4 * (DX ** 2 + DY ** 2 - DN ** 2)) == 0


def singular_on_base_locus(phi, mins, tfactors, timeout=600):
    """For each singular t-factor q (affine chart) of the component phi: do the
    three minors vanish on the singular points over the roots of q?  Exact, over
    the branch-value field (PARI): the singular x-coordinates are the roots of
    h = gcd(phi(A, x), d/dx phi(A, x), d/dt phi(A, x)); the test is h | D(A, x)
    for each minor.  Returns [(q, 'on' | 'OFF' | 'nosing')]."""
    DX, DY, DN = mins
    script = "x; t; a;\n" + PARI_FIELD + "phi = " + _pari_poly(phi) + ";\n"
    script += "MX = " + _pari_poly(DX) + ";\nMY = " + _pari_poly(DY) + ";\nMN = " + _pari_poly(DN) + ";\n{\n"
    for q in tfactors:
        script += "q = " + q.replace("**", "^") + "; qa = subst(q, t, a);\n"
        script += "if(poldegree(qa, a) == 1, A = -polcoeff(qa, 0, a) / polcoeff(qa, 1, a), mf = monicfield(qa); A = Mod(a, mf[1]) / mf[2]);\n"
        script += "PK = subst(phi, t, A); h = gcd(gcd(PK, deriv(PK, x)), subst(deriv(phi, t), t, A));\n"
        script += "if(type(h) != \"t_POL\" || poldegree(h, x) <= 0, print(\"SING \", q, \" | nosing\"),\n"
        script += "  ok = 1; for(i = 1, 3, M = [MX, MY, MN][i]; MK = subst(M, t, A); if(MK != 0 && (MK % h) != 0, ok = 0));\n"
        script += "  print(\"SING \", q, \" | \", if(ok, \"on\", \"OFF\")));\n"
    script += "}\n"
    cp = subprocess.run([GP, "-q", "-f"], input='default(parisize,"512M");\n' + script, capture_output=True, text=True, timeout=timeout)
    return re.findall(r"SING\s+(.*?)\s+\|\s+(\w+)", cp.stdout)
