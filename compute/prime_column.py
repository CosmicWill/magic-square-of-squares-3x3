"""THE PRIME-COLUMN LEMMA (entry 120; proposed by the independent review of 2026-09-06,
docs/PROOF-DIRECTIONS-2026-09-06.md section 2; re-derived in docs/attacks/A3-simultaneous-congrua.md 2.49).

Setting.  A class of the box p_1^{a_1} p_2^{a_2} p_3^{a_3} is four labels (A, B, C, D), each a vector
(e_1, e_2, e_3) with |e_j| <= a_j, and four signs; the offsets of the additive quadruple are
d_X = eps_X * elem_box(X) with d_C = d_A + d_B and d_D = d_A - d_B (the relations R1, R2 of omega3.relations),
where  elem_box(X) = prod_j p_j^{2(a_j - |e_{X,j}|)} * Im(prod_j l_j^{2 e_{X,j}})  with l_j = pi_j^2 the frame
of p_j (a negative exponent means the conjugate power).

Lemma (Theorem A3.PC).  For every prime column j in which some label is nonzero, the maximum of
|e_{A,j}|, |e_{B,j}|, |e_{C,j}|, |e_{D,j}| is attained by at least THREE of the four labels.

Proof.  (Additive half)  For an odd prime p and nonzero U, V, U+V, U-V, the minimum of their p-adic
valuations is attained at least three times: if v(U) < v(V) then v(U+V) = v(U-V) = v(U); symmetrically
if v(U) > v(V); if v(U) = v(V) = k, write U = p^k u, V = p^k v with units u, v -- u+v and u-v cannot both
be divisible by p (their sum 2u is a unit), so at least one of U+V, U-V has valuation k.
(Gaussian half)  Let z = prod_k l_k^{2 e_{X,k}}.  If e_{X,j} != 0, exactly one of z and its conjugate is
divisible by pi_j (the other frames are units at pi_j, and pi_j does not divide pi_j-bar), so z - z-bar is a
unit at pi_j; 2i is a unit too, hence Im z = (z - z-bar)/(2i) is a unit at pi_j, and being a rational
integer it is prime to p_j.  Therefore v_{p_j}(d_X) = 2(a_j - |e_{X,j}|) exactly when e_{X,j} != 0, and
v_{p_j}(d_X) >= 2 a_j when e_{X,j} = 0.  With M_j = max_X |e_{X,j}| > 0 the minimum valuation among the
four offsets is 2(a_j - M_j), attained exactly by the labels with |e_{X,j}| = M_j; the additive half
says there are at least three of them.  QED

Consequences.  A frame appearing in exactly one label ("free frame", entry 116) is impossible outright.
Every class whose certificate below is not None is dead, uniformly in the exponents and the primes.
"""
from collections import Counter


def column_certificate(labels):
    """None when the four labels satisfy the lemma in every prime column; otherwise the certificate
    of the first failing column: {'column': j, 'abs_exponents': [|e_{A,j}|, ..., |e_{D,j}|],
    'max': M_j, 'count': #labels attaining M_j (< 3)}."""
    labels = [tuple(int(x) for x in lab) for lab in labels]
    for j in range(len(labels[0])):
        mags = [abs(lab[j]) for lab in labels]
        M = max(mags)
        if M == 0:
            continue
        n = mags.count(M)
        if n < 3:
            return {"column": j, "abs_exponents": mags, "max": M, "count": n}
    return None


def excluded(labels):
    return column_certificate(labels) is not None


def zero_columns(labels):
    """The prime columns in which every label is zero (the prime does not enter the offsets: the
    configuration is a scaled square of a smaller box)."""
    labels = [tuple(int(x) for x in lab) for lab in labels]
    return [j for j in range(len(labels[0])) if all(lab[j] == 0 for lab in labels)]


def valuation(n, p):
    n = abs(int(n))
    if n == 0:
        return None
    v = 0
    while n % p == 0:
        n //= p
        v += 1
    return v


def additive_minimum_rule(U, V, p):
    """The valuations of (U, V, U+V, U-V) and whether their minimum is attained at least three times."""
    vals = [valuation(x, p) for x in (U, V, U + V, U - V)]
    if None in vals:
        return vals, None
    return vals, vals.count(min(vals)) >= 3


# frames l = pi^2 as (c, s) with c^2 + s^2 = p^2: 5 = N(2+i), (2+i)^2 = 3+4i; 13: (3+2i)^2 = 5+12i;
# 17: (4+i)^2 = 15+8i; 29: (5+2i)^2 = 21+20i; 37: (6+i)^2 = 35+12i; 41: (5+4i)^2 = 9+40i
FRAMES = {5: (3, 4), 13: (5, 12), 17: (15, 8), 29: (21, 20), 37: (35, 12), 41: (9, 40)}


def offset_valuations(lab, exps, primes):
    """The p_j-adic valuations of the ledger's element elem_box(lab, exps) evaluated at the frames of the
    given primes (exact integers), against the lemma's prediction 2(a_j - |e_j|) (e_j != 0) or >= 2 a_j."""
    from compute import omega3 as O
    sub = {}
    for (c, s), p in zip(O.FR, primes):
        sub[c], sub[s] = FRAMES[p]
    d = int(O.elem_box(lab, exps).subs(sub))
    out = []
    for e, a, p in zip(lab, exps, primes):
        v = valuation(d, p)
        out.append((v, 2 * (a - abs(e)) if e != 0 else None, (v == 2 * (a - abs(e))) if e != 0 else (v is None or v >= 2 * a)))
    return d, out


def census(classes, verdict_key="verdict"):
    """Counts of (verdict, excluded/survives) over a list of class records."""
    t = Counter()
    for r in classes:
        t[(r[verdict_key], "excluded" if excluded(r["cand"][:4]) else "survives")] += 1
    return dict(t)


if __name__ == "__main__":
    import gzip, json, os
    base = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base, "data_omega3_box111.json"), encoding="utf-8") as fh:
        print("(1,1,1):", census(json.load(fh)["classes"], "verdict"))
    with gzip.open(os.path.join(base, "data_omega3_box211.json.gz"), "rt", encoding="utf-8") as fh:
        print("(2,1,1):", census(json.load(fh)["classes"], "v"))
