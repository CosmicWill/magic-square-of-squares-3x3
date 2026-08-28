"""Adversarial controls for the A1 re-audit (A1 §7.5) — implement Hill
arXiv:2510.08286v3's definitions LITERALLY, from raw data, independent of
the derived formulas used by ``verify/checks/a1_eq29.py``, guarding against
any misinterpretation of the paper on our side.  Requires mpmath (ships
with sympy); 60-digit working precision, tolerance 1e-35.  Run:
``python compute/hill_literal_controls.py`` — all controls assert.

Controls:

A. the witness: all his per-pair machinery, Lemma 3.2 case (c) literally,
   eq. (29) exactly as printed -> holds?  both sides nonzero?  beta1 != 1?
B. the (30) decomposition at the witness: the 'odd part' he claims must
   vanish -- what does it actually equal?
C. perturbation control: break the spacing constraint by 1 -> (29) must
   FAIL if (29) really is the constraint in costume.
D. 500 random real grids (M, D, F): (29) should hold on every one (it is
   real-algebra), with beta1 != 1 generically.
E. rep-choice control: alpha_3d = 1 instead of 5 -> (29) still holds.
"""
from mpmath import mp, mpf, sqrt, fabs
from fractions import Fraction
import random

mp.dps = 60
TOL = mpf(10) ** -35


class Pair:
    """An AP pair from a square triple (a, b, c) = (p^2, q^2, r^2), roots
    possibly irrational.  alpha_rep: None -> lowest terms (rational kappa
    only), or an explicit positive denominator choice."""

    def __init__(self, a, b, c, alpha_d=None):
        self.p, self.q, self.r = sqrt(mpf(a)), sqrt(mpf(b)), sqrt(mpf(c))
        self.sum = mpf(b) - mpf(a)          # = Sigma P (must equal c - b)
        assert fabs((mpf(c) - mpf(b)) - self.sum) < TOL
        self.n1 = self.q - self.p           # P^{n1}
        self.n2 = self.r - self.q           # P^{n2}
        self.off1 = 2 * self.p              # P^1
        self.off2 = self.off1 + 2 * self.n1  # P^2  (= 2q)
        self.off3 = self.off2 + 2 * (self.n2 - 1)  # P^3 (= 2r - 2)
        self.kappa = self.n1 / self.n2
        self.alpha = self.kappa * (self.kappa + 1) / (self.kappa - 1)
        if alpha_d is None:
            fr = Fraction(int(round(self.n1)), int(round(self.n2)))
            k = Fraction(fr)
            al = k * (k + 1) / (k - 1)
            self.an, self.ad = mpf(al.numerator), mpf(al.denominator)
        else:
            self.ad = mpf(alpha_d)
            self.an = self.alpha * self.ad
        disc = (self.an - 3 * self.ad) ** 2 - 8 * self.ad ** 2
        assert disc > -TOL, "discriminant negative"
        self.s = sqrt(fabs(disc))
        self.N = (self.an - 3 * self.ad) - self.s   # N(N+Q) = 8 ad^2, Q = 2s
        # his (11), (12), (13), (14) as literal consistency checks:
        assert fabs(self.N * (self.N + 2 * self.s) - 8 * self.ad ** 2) < TOL
        assert fabs(self.an - (4 * self.ad ** 2 / self.N + 3 * self.ad
                               + self.N / 2)) < TOL, "(12) fails"
        Nplus = (self.an - 3 * self.ad) + self.s
        k13 = (4 * self.ad + Nplus) / Nplus          # his (13)
        k14 = (2 * self.ad + self.N) / (2 * self.ad)  # his (14)
        assert fabs(k13 - self.kappa) < TOL and fabs(k14 - self.kappa) < TOL
        # his (7) and (8) — the offset formulas cited as inputs to (29):
        k = self.kappa
        assert fabs(self.off1 - self.n2 * ((k + 1) / (k - 1) - k)) < TOL, \
            "(7) fails"
        assert fabs(self.off2 - self.n2 * (k * (k + 1) / (k - 1) - 1)) < TOL, \
            "(8) fails"
        # his (6): Sigma P = (P^{n2})^2 kappa (kappa+1)/(kappa-1):
        assert fabs(self.sum - self.n2 ** 2 * k * (k + 1) / (k - 1)) < TOL, \
            "(6) fails"


def ap_sum(offset, nterms):
    """His eq. (2): Sigma p = n (n + offset)."""
    return nterms * (nterms + offset)


def eq29(P1, P2, P3):
    """Eq. (29) EXACTLY as printed; returns (LHS, RHS, beta pieces)."""
    b1n = sqrt(P2.an / P1.an)
    b1d = sqrt(P2.ad / P1.ad)
    b2n = sqrt(P3.an / P2.an)
    b2d = sqrt(P3.ad / P2.ad)
    a1n, a1d, N2, N3 = P1.an, P1.ad, P2.N, P3.N
    LHS = (N3 ** 2 * b2n ** 2 * b2d ** 2
           * (8 * b1d ** 4 * a1d ** 2 - N2 ** 2) ** 2
           - N2 ** 2 * (8 * b2d ** 4 * b1d ** 4 * a1d ** 2 - N3 ** 2) ** 2)
    RHS = (4 * N2 ** 2 * N3 ** 2 * b1n ** 2 * b1d ** 2 * b2n ** 2 * b2d ** 2
           * (a1n - a1d) ** 2
           - 4 * N2 ** 2 * N3 ** 2 * b2n ** 2 * b2d ** 2
           * (b1n ** 2 * a1n - b1d ** 2 * a1d) ** 2)
    return LHS, RHS, (b1n, b1d, b2n, b2d)


def check_config(vals, reps=(None, None, 5), label="", verbose=False):
    """vals = nine grid values as three triples (pair1, pair2, pair3)."""
    (a1, b1, c1), (a2, b2, c2), (a3, b3, c3) = vals
    P1 = Pair(a1, b1, c1, reps[0])
    P2 = Pair(a2, b2, c2, reps[1])
    P3 = Pair(a3, b3, c3, reps[2])
    # equal sums (his (20)):
    assert fabs(P1.sum - P2.sum) < TOL and fabs(P2.sum - P3.sum) < TOL
    # beta1 per his (21) both ways:
    beta1 = P1.n2 / P2.n2
    assert fabs(beta1 - sqrt(P2.alpha / P1.alpha)) < TOL, "(21) fails"
    LHS, RHS, (b1n_, b1d_, b2n_, b2d_) = eq29(P1, P2, P3)
    holds = fabs(LHS - RHS) < TOL * max(1, fabs(LHS))
    if verbose:
        print(f"[{label}] beta1 = {beta1}")
        print(f"  LHS(29) = {LHS}")
        print(f"  RHS(29) = {RHS}")
        print(f"  |LHS-RHS| = {fabs(LHS - RHS)}  -> (29) holds: {holds}")
        print(f"  prefactor b1d^2-b1n^2 = {b1d_**2 - b1n_**2}")
    return holds, beta1, LHS, RHS, (P1, P2, P3)


# ---------------- A. the witness, literally ----------------
W = [(4, 3364, 6724), (2116, 5476, 8836), (4228, 7588, 10948)]
holds, beta1, LHS, RHS, (P1, P2, P3) = check_config(
    W, label="witness a3d=5", verbose=True)
assert holds and fabs(beta1 - mpf(6) / 5) < TOL
assert fabs(LHS) > 1, "LHS should be nonzero"

# Lemma 3.2 case (c) LITERALLY: pA(P2^1, (P1^2 - P2^1)/2),
# pB(P3^1, (P2^2 - P3^1)/2), sums via his eq. (2):
assert P2.off1 < P1.off2 and P3.off1 < P2.off2, "case (c) inequalities"
SpA = ap_sum(P2.off1, (P1.off2 - P2.off1) / 2)
SpB = ap_sum(P3.off1, (P2.off2 - P3.off1) / 2)
print(f"[Lemma 3.2(c)] Sigma pA = {SpA},  Sigma pB = {SpB},  "
      f"equal: {fabs(SpA - SpB) < TOL}")
assert fabs(SpA - SpB) < TOL
# interleaving legality (his <|| relations):
assert P3.off1 <= P2.off3 and P2.off1 <= P1.off3

# ---------------- B. the 'odd part' of (30) at the witness ----------------
b1n2 = P2.an / P1.an           # beta_1n^2
b1d2 = P2.ad / P1.ad
b2n2 = P3.an / P2.an
b2d2 = P3.ad / P2.ad
a1d, N1, N2, N3 = P1.ad, P1.N, P2.N, P3.N
pref = 4 * N2 ** 2 * N3 ** 2 * b2n2 * b2d2 * (b1d2 - b1n2)
bracket_even = (16 / N1 ** 2 * b1n2 * a1d ** 4
                + (13 * b1n2 - b1d2) * a1d ** 2 + N1 ** 2 / 4 * b1n2)
bracket_odd = 24 / N1 * b1n2 * a1d ** 3 + 3 * N1 * b1n2 * a1d
print(f"[(30) at witness] prefactor x odd-part = {pref * bracket_odd}"
      f"   (his step claims this MUST be 0)")
print(f"  RHS(30) = prefactor x (even+odd) = {pref * (bracket_even + bracket_odd)}"
      f"  == RHS(29): {fabs(pref * (bracket_even + bracket_odd) - RHS) < TOL}")
assert fabs(pref * (bracket_even + bracket_odd) - RHS) < TOL
assert fabs(pref * bracket_odd) > 1

# ---------------- C. perturbation control ----------------
Wbad = [(4, 3364, 6724), (2116, 5476, 8836), (4229, 7589, 10949)]
holds_bad, _, LHSb, RHSb, _ = check_config(Wbad, label="perturbed", verbose=True)
assert not holds_bad, "(29) held on a broken configuration?!"

# ---------------- D. random real grids ----------------
random.seed(20260828)
n_ok, beta1s = 0, []
for _ in range(500):
    D = mpf(random.randint(50, 10 ** 6))
    F = mpf(random.randint(50, 10 ** 6))
    if fabs(D - F) < 5 or fabs(2 * D - F) < 5 or fabs(D - 2 * F) < 5:
        continue
    M = mpf(random.randint(1, 10 ** 6))
    vals = [[M + i * D + j * F for i in range(3)] for j in range(3)]
    # pairs must be square triples in increasing AP with positive sums: sort
    trip = [tuple(sorted(v)) for v in vals]
    try:
        h, b1, L, R, _ = check_config(trip, reps=(1, 1, 1))
    except AssertionError:
        continue
    n_ok += 1
    beta1s.append(b1)
    assert h, f"(29) failed on a random real grid: {trip}"
print(f"[random grids] (29) held on all {n_ok} sampled real grids; "
      f"beta1 range [{min(beta1s)}, {max(beta1s)}]  "
      f"(beta1 = 1 on none: {all(fabs(b - 1) > mpf(10)**-6 for b in beta1s)})")

# ---------------- E. rep-choice control ----------------
holds_e, beta1_e, LHS_e, RHS_e, _ = check_config(
    W, reps=(None, None, 1), label="witness a3d=1", verbose=True)
assert holds_e and fabs(beta1_e - mpf(6) / 5) < TOL and fabs(LHS_e) > 1

print("\nALL CONTROLS PASS: (29) is the constraint (holds on-grid, fails "
      "off-grid, any rep), beta1 != 1 throughout, odd part nonzero.")
