r"""Entry 131: is C_c: y^2 = x^5 - 4x^4 + 6x^3 + 12x^2 + x isomorphic over Q to the LMFDB curve 1408.b.180224.2,
y^2 = 2x^5 - 4x^3 - x^2 + 2x + 1?  Both have exactly three rational Weierstrass points (C_c: 0, -1, inf; LMFDB: -1, 1, inf),
so a Q-isomorphism induces a Moebius map matching them; try the six bijections, solve for the map, and check that the
transformed binary sextic is a rational square multiple of the target.  Also compare Igusa-Clebsch invariants."""
R.<x> = QQ[]
S.<X, Z> = QQ[]
fA = x^5 - 4*x^4 + 6*x^3 + 12*x^2 + x
fB = 2*x^5 - 4*x^3 - x^2 + 2*x + 1
def sextic(f):
    return sum(QQ(f[k]) * X^k * Z^(6 - k) for k in range(7))
FA, FB = sextic(fA), sextic(fB)
HA, HB = HyperellipticCurve(fA), HyperellipticCurve(fB)
print("Igusa-Clebsch A:", HA.igusa_clebsch_invariants())
print("Igusa-Clebsch B:", HB.igusa_clebsch_invariants())
print("absolute Igusa (Wamelen) A:", HA.absolute_igusa_invariants_wamelen())
print("absolute Igusa (Wamelen) B:", HB.absolute_igusa_invariants_wamelen())
# Weierstrass points as (X:Z)
WA = [(QQ(0), QQ(1)), (QQ(-1), QQ(1)), (QQ(1), QQ(0))]
WB = [(QQ(-1), QQ(1)), (QQ(1), QQ(1)), (QQ(1), QQ(0))]
from itertools import permutations
found = None
for perm in permutations(range(3)):
    # find M in GL2(Q) with M * WA[i] ~ WB[perm[i]]: linear conditions (M v) x w = 0
    rows = []
    for i in range(3):
        v, w = WA[i], WB[perm[i]]
        rows.append([v[0]*w[1], v[1]*w[1], -v[0]*w[0], -v[1]*w[0]])
    K = matrix(QQ, rows).right_kernel()
    if K.dimension() != 1:
        continue
    a, b, c, d = K.basis()[0]
    M = matrix(QQ, [[a, b], [c, d]])
    if M.det() == 0:
        continue
    # pull back FB along M: FB(M (X,Z)) should be lambda * FA
    G = FB(a*X + b*Z, c*X + d*Z)
    # proportional?
    ratio = None; ok = True
    for mono in FA.monomials():
        cA = FA.monomial_coefficient(mono); cB = G.monomial_coefficient(mono)
        if cA == 0:
            if cB != 0:
                ok = False; break
            continue
        r = cB / cA
        if ratio is None:
            ratio = r
        elif r != ratio:
            ok = False; break
    if ok and (G - ratio * FA) == 0:
        print("perm", perm, "M =", [a, b, c, d], "FB(M.) = lambda FA with lambda =", ratio, "| square?", ratio.is_square(), "| squarefree part", ratio.squarefree_part())
        found = (perm, M, ratio)
print("RESULT:", "Q-isomorphic (lambda a square)" if found and found[2].is_square() else ("quadratic twist by " + str(found[2].squarefree_part()) if found else "no matching Moebius map"))
