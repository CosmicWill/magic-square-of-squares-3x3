"""Standalone verification of the refutation of arXiv:2510.08286v3 (Hill),
"On Arithmetic Progressions and a Proof of the Nonexistence of Magic
Squares of Squares".  Requires only sympy.  Run:  python verify_refutation.py

Variables: n = alpha_1n, d = alpha_1d, N2, N3 = the paper's per-pair N for
pairs 2 and 3; b1n = beta_1n^2, b1d = beta_1d^2, b2n = beta_2n^2,
b2d = beta_2d^2 (every beta enters eq. (29) squared).
"""
import sympy as sp

n, d, N2, N3, b1n, b1d, b2n, b2d = sp.symbols(
    'n d N2 N3 b1n b1d b2n b2d', positive=True)

# ---- the paper's eq. (29), literally as printed (v3, p. 6) ----
LHS = N3**2*b2n*b2d*(8*b1d**2*d**2 - N2**2)**2 \
    - N2**2*(8*b2d**2*b1d**2*d**2 - N3**2)**2
RHS = 4*N2**2*N3**2*b1n*b1d*b2n*b2d*(n - d)**2 \
    - 4*N2**2*N3**2*b2n*b2d*(b1n*n - b1d*d)**2

# ---- the Lemma-3.2 spacing constraint, in the same variables ----
# For a pair (p, q, r): q = n2(alpha-1)/2 (paper's (8)), p = n2*s/(2 ad)
# (equivalent to (7)), s = (8 ad^2 - N^2)/(2N) (from (11)-(12));
# alpha_2* = b1* alpha_1*, alpha_3* = b2* alpha_2*;  n2 ratios via betas.
a2d, a3d = b1d*d, b2d*b1d*d
T1 = (b2n/b2d) * (8*a2d**2 - N2**2)**2/(4*N2**2) / a2d**2   # 4 p2^2 / t^2
T2 = (b1n*b2n/(b1d*b2d)) * (n - d)**2 / d**2                # 4 q1^2 / t^2
T3 = (8*a3d**2 - N3**2)**2/(4*N3**2) / a3d**2               # 4 p3^2 / t^2
T4 = (b2n/b2d) * (b1n*n - b1d*d)**2 / a2d**2                # 4 q2^2 / t^2
E4 = T1 - T2 - T3 + T4      # = 4[(p2^2-q1^2) - (p3^2-q2^2)] / t^2

# ---- THEOREM 1: (29) is the constraint times a positive cofactor ----
assert sp.simplify((LHS - RHS) - 4*N2**2*N3**2*b1d**2*b2d**2*d**2*E4) == 0
print("Theorem 1: LHS(29)-RHS(29) == 4 N2^2 N3^2 b1d^2 b2d^2 d^2 * (4E/t^2)  [OK]")

# ---- THEOREM 2: the witness ----
# Pairs (2,58,82) and (46,74,94): congruum 3360, alpha = 35/6 and 42/5,
# (s, N) = (1, 16) and (23, 4).  Third pair forced by the constraint:
# (sqrt(4228), sqrt(7588), sqrt(10948)); representation alpha_3d := 5.
t2 = 18536 - 56*sp.sqrt(105961)          # exact (r3 - q3)^2
alpha3 = sp.Rational(3360, 1)/t2
vals = {n: 35, d: 6, N2: 4,
        b1n: sp.Rational(6, 5), b1d: sp.Rational(5, 6),
        b2n: 5*alpha3/42, b2d: 1,
        N3: (5*alpha3 - 15) - sp.sqrt((5*alpha3 - 15)**2 - 200)}
lhs_v, rhs_v = LHS.subs(vals), RHS.subs(vals)
assert sp.simplify(lhs_v - rhs_v) == 0        # eq. (29) HOLDS at the witness
assert abs(sp.N(lhs_v, 30)) > 1               # ... with both sides NONZERO
print("Theorem 2: at the witness, (29) holds; both sides =",
      sp.N(lhs_v, 30))
print("           beta1^2 =", sp.nsimplify(vals[b1n]/vals[b1d]),
      "!= 1;  prefactor b1d - b1n =",
      sp.nsimplify(vals[b1d] - vals[b1n]), "!= 0")
# The paper's final step concludes beta1 = 1 (and hence both sides 0)
# from exactly these hypotheses.  It is therefore invalid.
