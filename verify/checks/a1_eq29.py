"""A1 formal re-audit of Hill, arXiv:2510.08286v3 — the eq.-(29) endgame.

Verifies the three pillars of docs/attacks/A1-hill-audit.md §7:

1. ``a1.eq29_identity`` — Hill's equation (29) is *correctly derived*: as
   polynomials in his own variables, LHS(29) - RHS(29) equals the explicit
   positive cofactor 4 N2^2 N3^2 b1d^2 b2d^2 d^2 times the (denominator-
   cleared) spacing constraint 4E/t^2 of his Lemma 3.2.  Hence (29) is
   *equivalent* to the single real-algebraic constraint E = 0 and carries no
   Diophantine content.  Also verifies his (30)-factorization
   RHS(29) = 4 N2^2 N3^2 b2n b2d (b1d - b1n)(b1n n^2 - b1d d^2) and the
   printed form of the (30) bracket after the eq.-(12) substitution.

2. ``a1.eq29_witness`` — the executable counterexample to the final step:
   two genuine *integer* AP pairs (2,58,82), (46,74,94) with common sum
   (congruum) 3360, third pair forced over the reals by the spacing
   constraint.  Every quantity Hill's step needs is well-defined and
   positive, eq. (29) holds exactly (by check 1 + E = 0), both sides equal
   4 N2^2 N3^2 b2n b2d (b1d - b1n)(b1n n^2 - b1d d^2) != 0, and
   beta1^2 = 36/25 != 1.  Hill's inference "(29) => beta1 = 1" is therefore
   a non-sequitur; his proof of Theorem 3.1 is invalid.

3. ``a1.hill_grid`` — structure theorem: Hill's constraint set (three
   equal-sum AP pairs + Lemma 3.2 spacing) is *equivalent* to nine squares
   in a 3x3 additive grid M + i*D + j*F, which is exactly the Lucas magic
   structure.  So his reduction is faithful and complete — and *no* integer
   hypothesis-level counterexample can exist (it would be a magic square of
   squares); the only possible flaw was inferential, and check 2 locates it.
   The witness's nine values form the grid (4, 3360, 2112): a genuine magic
   square (sum 16428, center 74^2) with SIX perfect-square entries.

Variable dictionary (matching the audit doc): n = alpha_1n, d = alpha_1d,
N2, N3 = Hill's per-pair N for pairs 2, 3; b1n = beta_1n^2 = a2n/a1n,
b1d = beta_1d^2 = a2d/a1d, b2n = beta_2n^2 = a3n/a2n, b2d = beta_2d^2 =
a3d/a2d (all beta's enter (29) squared, so the b's are honest variables).
"""

from fractions import Fraction
from math import gcd, isqrt

from ..framework import check, require
from ..targets import is_square

DOC = "docs/attacks/A1-hill-audit.md"

# ---------------------------------------------------------------------------
# tiny exact multivariate polynomial arithmetic:
# monomial = 8-tuple of exponents in (n, d, N2, N3, b1n, b1d, b2n, b2d),
# polynomial = dict{monomial: int}.
# ---------------------------------------------------------------------------

NVARS = 8
VN, VD, VN2, VN3, VB1N, VB1D, VB2N, VB2D = range(NVARS)


def mono(coef=1, **exps):
    e = [0] * NVARS
    names = {"n": VN, "d": VD, "N2": VN2, "N3": VN3,
             "b1n": VB1N, "b1d": VB1D, "b2n": VB2N, "b2d": VB2D}
    for k, v in exps.items():
        e[names[k]] = v
    return {tuple(e): coef}


def padd(*polys):
    out = {}
    for p in polys:
        for m, c in p.items():
            c2 = out.get(m, 0) + c
            if c2:
                out[m] = c2
            elif m in out:
                del out[m]
    return out


def pneg(p):
    return {m: -c for m, c in p.items()}


def pmul(a, b):
    out = {}
    for ma, ca in a.items():
        for mb, cb in b.items():
            m = tuple(x + y for x, y in zip(ma, mb))
            c2 = out.get(m, 0) + ca * cb
            if c2:
                out[m] = c2
            elif m in out:
                del out[m]
    return out


def psq(a):
    return pmul(a, a)


def pscale(a, k):
    return {m: c * k for m, c in a.items()} if k else {}


ONE = mono()


@check("a1.eq29_identity", DOC)
def _(ctx):
    """Hill (29) == [4 N2^2 N3^2 b1d^2 b2d^2 d^2] * [4E/t^2], exactly, as
    polynomials — his equation is the Lemma-3.2 constraint in costume; the
    derivation through (30) is sound and purely real-algebraic."""
    # representation data: a2d = b1d*d, a3d = b2d*b1d*d, a2n = b1n*n
    a2d = mono(b1d=1, d=1)
    a3d = mono(b2d=1, b1d=1, d=1)
    # X_i := 8 a_id^2 - N_i^2  (so that s_i = X_i / (2 N_i), eq. (11)-(12))
    X2 = padd(pscale(psq(a2d), 8), pneg(mono(N2=2)))
    X3 = padd(pscale(psq(a3d), 8), pneg(mono(N3=2)))

    # the four terms of 4E/t^2 = T1 - T2 - T3 + T4 as exact fractions
    # (numerator, denominator), denominators monomial-times-integer:
    #   T1 = 4 p2^2/t^2 = (b2n/b2d) * s2^2 / a2d^2,  s2^2 = X2^2/(4 N2^2)
    #   T2 = 4 q1^2/t^2 = (b1n b2n)/(b1d b2d) * (n - d)^2 / d^2
    #   T3 = 4 p3^2/t^2 = s3^2 / a3d^2,              s3^2 = X3^2/(4 N3^2)
    #   T4 = 4 q2^2/t^2 = (b2n/b2d) * (b1n n - b1d d)^2 / a2d^2
    n_minus_d = padd(mono(n=1), pneg(mono(d=1)))
    a2n_minus_a2d = padd(mono(b1n=1, n=1), pneg(mono(b1d=1, d=1)))
    T = [
        (pmul(mono(b2n=1), psq(X2)),
         pscale(pmul(mono(b2d=1, N2=2), psq(a2d)), 4)),
        (pmul(mono(b1n=1, b2n=1), psq(n_minus_d)),
         mono(b1d=1, b2d=1, d=2)),
        (psq(X3), pscale(pmul(mono(N3=2), psq(a3d)), 4)),
        (pmul(mono(b2n=1), psq(a2n_minus_a2d)),
         pmul(mono(b2d=1), psq(a2d))),
    ]
    signs = [1, -1, -1, 1]
    # sum the four fractions: common denominator = product of the four
    dens = [t[1] for t in T]
    E_den = ONE
    for dpoly in dens:
        E_den = pmul(E_den, dpoly)
    E_num = {}
    for i, (npoly, _) in enumerate(T):
        cross = npoly
        for j, dpoly in enumerate(dens):
            if j != i:
                cross = pmul(cross, dpoly)
        E_num = padd(E_num, pscale(cross, signs[i]))

    # Hill's (29), literally as printed (v3, p.6):
    lhs29 = padd(
        pmul(pmul(mono(N3=2, b2n=1, b2d=1), ONE),
             psq(padd(mono(b1d=2, d=2, coef=8), pneg(mono(N2=2))))),
        pneg(pmul(mono(N2=2),
                  psq(padd(mono(b2d=2, b1d=2, d=2, coef=8),
                           pneg(mono(N3=2)))))),
    )
    rhs29 = padd(
        pscale(pmul(mono(N2=2, N3=2, b1n=1, b1d=1, b2n=1, b2d=1),
                    psq(n_minus_d)), 4),
        pneg(pscale(pmul(mono(N2=2, N3=2, b2n=1, b2d=1),
                         psq(a2n_minus_a2d)), 4)),
    )
    P = padd(lhs29, pneg(rhs29))

    # identity:  P * E_den == K0 * E_num,  K0 = 4 N2^2 N3^2 b1d^2 b2d^2 d^2
    K0 = mono(N2=2, N3=2, b1d=2, b2d=2, d=2, coef=4)
    diff = padd(pmul(P, E_den), pneg(pmul(K0, E_num)))
    require(diff == {}, "eq. (29) is NOT the K0-multiple of the spacing "
                        "constraint — identity fails")

    # (30)-factorization of the RHS:
    #   RHS29 == 4 N2^2 N3^2 b2n b2d (b1d - b1n)(b1n n^2 - b1d d^2)
    fact = pmul(
        mono(N2=2, N3=2, b2n=1, b2d=1, coef=4),
        pmul(padd(mono(b1d=1), pneg(mono(b1n=1))),
             padd(mono(b1n=1, n=2), pneg(mono(b1d=1, d=2)))),
    )
    require(padd(rhs29, pneg(fact)) == {},
            "RHS(29) factorization (b1d-b1n)(b1n n^2 - b1d d^2) fails")

    # Hill's printed (30) bracket: substituting eq. (12) for pair 1,
    # n = (8 d^2 + 6 d N1 + N1^2)/(2 N1), the second factor becomes his
    # bracket.  Verified in Q[d, N1, b1n, b1d] after clearing 4 N1^2
    # (monomials here: reuse slots n->N1):
    def m1(coef=1, **e):  # variables (N1, d, b1n, b1d) packed into slots
        return mono(coef, n=e.get("N1", 0), d=e.get("d", 0),
                    b1n=e.get("b1n", 0), b1d=e.get("b1d", 0))
    a1n_2N1 = padd(m1(d=2, coef=8), m1(N1=1, d=1, coef=6), m1(N1=2))
    lhs30 = padd(pmul(m1(b1n=1), psq(a1n_2N1)),
                 pneg(m1(N1=2, b1d=1, d=2, coef=4)))
    rhs30 = padd(m1(b1n=1, d=4, coef=64), m1(b1n=1, N1=1, d=3, coef=96),
                 m1(b1n=1, N1=2, d=2, coef=52),
                 pneg(m1(b1d=1, N1=2, d=2, coef=4)),
                 m1(b1n=1, N1=3, d=1, coef=12), m1(b1n=1, N1=4))
    require(padd(lhs30, pneg(rhs30)) == {}, "printed (30) bracket mismatch")

    ctx.note("(29) == 4 N2^2 N3^2 b1d^2 b2d^2 d^2 * (Lemma-3.2 constraint): "
             "correctly derived, and EQUIVALENT to it — no Diophantine "
             "content; (30) printed correctly too")


# ---------------------------------------------------------------------------
# exact arithmetic in Q(g), g = sqrt(105961): elements a + b g, Fractions.
# ---------------------------------------------------------------------------

G = 105961  # = 17 * 23 * 271;  325^2 = 105625 < G < 106276 = 326^2


def qg(a, b=0):
    return (Fraction(a), Fraction(b))


def qg_add(x, y):
    return (x[0] + y[0], x[1] + y[1])


def qg_sub(x, y):
    return (x[0] - y[0], x[1] - y[1])


def qg_mul(x, y):
    return (x[0] * y[0] + x[1] * y[1] * G, x[0] * y[1] + x[1] * y[0])


def qg_scale(x, k):
    return (x[0] * k, x[1] * k)


def qg_pos(x):
    """Certified x > 0 using 325 < g < 326 (fails => needs finer bounds)."""
    a, b = x
    if b >= 0:
        return a + 325 * b > 0 or (b > 0 and a + 325 * b >= 0)
    return a + 326 * b > 0


@check("a1.eq29_witness", DOC)
def _(ctx):
    """The counterexample to Hill's final step: integer pairs (2,58,82) and
    (46,74,94) (congruum 3360) + the spacing-forced real third pair satisfy
    every hypothesis and positivity requirement of the (29) -> beta1 = 1
    inference, with beta1^2 = 36/25 != 1 and both sides of (29) nonzero."""
    D = 3360
    P1, P2 = (2, 58, 82), (46, 74, 94)
    for (p, q, r) in (P1, P2):
        require(q * q - p * p == D and r * r - q * q == D, "congruum")
    require(P1 != P2, "pairs distinct")

    def pair_data(p, q, r):
        n1, n2 = q - p, r - q
        kap = Fraction(n1, n2)
        alpha = kap * (kap + 1) / (kap - 1)
        an, ad = alpha.numerator, alpha.denominator
        disc = (an - 3 * ad) ** 2 - 8 * ad * ad
        require(disc >= 0 and is_square(disc), "discriminant square")
        s = isqrt(disc)
        N, Nother = an - 3 * ad - s, an - 3 * ad + s
        require(gcd(an, ad) == 1, "coprime rep (Hill's WLOG)")
        require(N > 0 and N * Nother == 8 * ad * ad, "N roots")
        # eq. (12) for both roots; kappa via (13) and (14):
        for NN in (N, Nother):
            require(Fraction(an) == Fraction(4 * ad * ad, NN) + 3 * ad
                    + Fraction(NN, 2), "eq. (12)")
        require(kap == Fraction(4 * ad + Nother, Nother)
                == Fraction(2 * ad + N, 2 * ad), "eqs. (13)/(14)")
        # offset identities: p = n2 s/(2 ad), q = n2 (alpha-1)/2
        require(Fraction(n2 * s, 2 * ad) == p, "p-identity")
        require(Fraction(n2, 2) * (alpha - 1) == q, "q-identity")
        return n2, an, ad, s, N

    n2_1, a1n, a1d, s1, N1 = pair_data(*P1)
    n2_2, a2n, a2d, s2, N2 = pair_data(*P2)
    require((a1n, a1d, s1, N1) == (35, 6, 1, 16), "pair-1 data")
    require((a2n, a2d, s2, N2) == (42, 5, 23, 4), "pair-2 data")

    b1n, b1d = Fraction(a2n, a1n), Fraction(a2d, a1d)
    require(b1n == Fraction(6, 5) and b1d == Fraction(5, 6))
    require(Fraction(n2_1, n2_2) ** 2 == b1n / b1d, "beta1^2 consistency")
    prefactor = b1d - b1n
    require(prefactor == Fraction(-11, 30) and prefactor != 0,
            "prefactor beta1d^2 - beta1n^2 nonzero")
    second = b1n * a1n ** 2 - b1d * a1d ** 2
    require(second == 1440 and second != 0, "second RHS factor nonzero")

    # pair 3, forced by the Lemma-3.2 spacing constraint E = 0:
    p3sq = 74 ** 2 + 46 ** 2 - 58 ** 2
    q3sq, r3sq = p3sq + D, p3sq + 2 * D
    require((p3sq, q3sq, r3sq) == (4228, 7588, 10948))
    require((46 ** 2 - 58 ** 2) - (p3sq - 74 ** 2) == 0, "E = 0 (integers)")
    require(not any(is_square(x) for x in (p3sq, q3sq, r3sq)),
            "pair 3 is genuinely non-integral (else we found an MSS3...)")

    # t := r3 - q3 (> 0), t^2 = 18536 - 56 g in Q(g):
    require(q3sq * r3sq == 83073424 == 784 * G, "sqrt(q3^2 r3^2) = 28 g")
    t2 = qg(q3sq + r3sq, -56)
    require(t2 == qg(18536, -56) and qg_pos(t2), "t^2 = 18536 - 56g > 0")
    # alpha3 = 3360/t^2  == (2317 + 7g)/420  (exact):
    alpha3 = (Fraction(2317, 420), Fraction(7, 420))
    require(qg_mul(alpha3, t2) == qg(3360), "alpha3 * t^2 = 3360")
    # b2n = 5 alpha3 / 42, b2d = 1 (choice a3d := 5); (n2_2/t)^2 = b2n:
    b2n = qg_scale(alpha3, Fraction(5, 42))
    require(qg_mul(b2n, t2) == qg(n2_2 ** 2), "b2n t^2 = n2_2^2 = 400")
    require(qg_pos(b2n), "b2n > 0")
    # s3^2 = (5 alpha3 - 15)^2 - 200 = 1057(331 + g)/504 > 0, real s3:
    fivea15 = qg_sub(qg_scale(alpha3, 5), qg(15))
    require(qg_pos(fivea15), "5 alpha3 - 15 > 0")
    s3sq = qg_sub(qg_mul(fivea15, fivea15), qg(200))
    require(s3sq == (Fraction(1057 * 331, 504), Fraction(1057, 504)),
            "s3^2 closed form")
    require(qg_pos(s3sq), "s3 real")
    # ... and consistent with p3: s3^2 t^2 = (2 a3d p3)^2 = 100 p3^2:
    require(qg_mul(s3sq, t2) == qg(100 * p3sq), "s3 = 10 p3 / t")
    # N3 = (5 alpha3 - 15) - s3: real; product of the two N3-roots is
    # 8 a3d^2 = 200 != 0, and (5a3-15)^2 - s3^2 = 200 > 0 with 5a3-15 > 0
    # forces N3 > 0.  Every positivity Hill's step invokes therefore holds.
    require(qg_sub(qg_mul(fivea15, fivea15), s3sq) == qg(200), "N3 roots")

    # Hill's own interleaving trichotomy, case (c), in offsets (P^1 = 2p...):
    require(2 * 46 < 2 * 58, "P2^1 < P1^2")
    require(4 * p3sq < (2 * 74) ** 2, "P3^1 < P2^2")
    require(4 * p3sq <= (2 * 94 - 2) ** 2, "P3 <|| P2")
    require(2 * 46 <= 2 * 82 - 2, "P2 <|| P1")

    # Conclusion: by a1.eq29_identity, (29) = K0 * (constraint) with
    # K0 != 0 here (N2 = 4, N3 != 0, b1d, b2d, d != 0) and constraint = 0,
    # so (29) HOLDS at this witness; RHS(29) = 4 N2^2 N3^2 b2n b2d *
    # (b1d - b1n)(b1n n^2 - b1d d^2) has every factor nonzero, so both
    # sides are NONZERO; and beta1^2 = 36/25 != 1.
    ctx.note("(29) holds, both sides nonzero, beta1 = 6/5 != 1: the step "
             "'(29) & positivity => beta1 = 1' is a non-sequitur — the "
             "claimed proof of Thm 3.1 (arXiv:2510.08286v3) is invalid")


@check("a1.hill_grid", DOC)
def _(ctx):
    """Hill's constraint set == 3x3 additive grid == Lucas magic structure
    (so no integer hypothesis-level counterexample exists — his encoding is
    the full problem); the eq29 witness IS a magic square, six entries
    square."""
    # (i) chain => grid: b_i - a_i = c_i - b_i = D, a2 - b1 = a3 - b2 = E
    # forces value(i,j) = a1 + i*D + j*(D+E) for the 3x3 array of nine
    # values (i = position in pair, j = pair index).  Symbolic over the
    # lattice Z<a1, D, E>: represent values as coefficient triples.
    def v(ca, cd, ce):
        return (ca, cd, ce)
    pairs = [[v(1, i, 0) for i in range(3)]]
    for j in (1, 2):
        prev = pairs[-1]
        a_next = (prev[1][0], prev[1][1], prev[1][2] + 1)   # a_{j+1}=b_j+E
        pairs.append([(a_next[0], a_next[1] + i, a_next[2])
                      for i in range(3)])
    for j, pr in enumerate(pairs):
        for i, val in enumerate(pr):
            require(val == (1, i + j, j), "grid form a1 + (i+j)D + jE")
    # rewritten with F := D + E: value(i,j) = M + i*D + j*F ; over the
    # basis (M, D, F) that is (1, i, j) — the 3x3 additive grid.

    # (ii) grid => magic arrangement (Lucas): the standard placement uses a
    # pair of orthogonal Latin squares in the (i, j) grid coordinates:
    ARR = [[(2, 1), (0, 0), (1, 2)],
           [(0, 2), (1, 1), (2, 0)],
           [(1, 0), (2, 2), (0, 1)]]
    lines = [[ARR[k][0], ARR[k][1], ARR[k][2]] for k in range(3)]
    lines += [[ARR[0][k], ARR[1][k], ARR[2][k]] for k in range(3)]
    lines += [[ARR[0][0], ARR[1][1], ARR[2][2]],
              [ARR[0][2], ARR[1][1], ARR[2][0]]]
    for line in lines:
        require(sum(i for i, _ in line) == 3 and
                sum(j for _, j in line) == 3, "each line sums to 3M+3D+3F")
    cells = {c for row in ARR for c in row}
    require(cells == {(i, j) for i in range(3) for j in range(3)},
            "arrangement is a bijection onto the grid")

    # (iii) the eq29 witness as the grid (M, D, F) = (4, 3360, 2112):
    M, Dv, Fv = 4, 3360, 2112
    grid = {(i, j): M + i * Dv + j * Fv for i in range(3) for j in range(3)}
    vals = sorted(grid.values())
    require(len(set(vals)) == 9, "nine distinct values")
    require([grid[(i, 0)] for i in range(3)] == [4, 3364, 6724])      # pair 1
    require([grid[(i, 1)] for i in range(3)] == [2116, 5476, 8836])   # pair 2
    require([grid[(i, 2)] for i in range(3)] == [4228, 7588, 10948])  # pair 3
    square_count = sum(1 for x in vals if is_square(x))
    require(square_count == 6, "six perfect-square entries")
    magic = [[grid[c] for c in row] for row in ARR]
    sums = [sum(row) for row in magic]
    sums += [sum(magic[k][c] for k in range(3)) for c in range(3)]
    sums += [magic[0][0] + magic[1][1] + magic[2][2],
             magic[0][2] + magic[1][1] + magic[2][0]]
    require(all(s == 16428 for s in sums), "magic sum 16428")
    require(magic[1][1] == 74 ** 2, "center 74^2")
    ctx.note("Hill's encoding == the full Lucas grid (faithful; no integer "
             "counterexample possible) — witness is a real magic square of "
             "squares with 6/9 integer squares, magic sum 16428")
