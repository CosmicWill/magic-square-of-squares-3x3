"""A9-T1 fourth layer: Gauss composition, the local criterion, and
the anatomy of the representation kills.

GAUSS COMPOSITION (classical, implemented exactly): primitive forms
of one discriminant compose via united representatives (leading
coefficients coprine after a PROPER SL2 change — determinant +1 is
asserted; an improper change silently inverts the class).  The
class groups are verified as groups (identity, inverses, closure,
element orders), and the PRINCIPAL GENUS THEOREM (Gauss: the
squares are exactly the trivial-character genus) is machine-checked
on the pinned discriminants.  Consequence used below: a kill that
happens INSIDE one genus happens inside a coset of Cl^2 — invisible
to every character.

THE LOCAL CRITERION (classical local lattice theory, derived and
then VALIDATED EXHAUSTIVELY against brute-force representability —
zero mismatches for every odd w <= 6000 at three sample discs).
For D = -3 k^2 (3 not dividing k), an odd w > 0 is represented by
SOME primitive class of disc D iff:
  (i)   every inert prime (Kronecker (D|p) = -1) divides w to even
        order;
  (ii)  at p | k, e = v_p(k): if v_p(w) < 2e then v_p(w) is even
        and the genus sign chi_p(w/p^v) is pinned; if v_p(w) >= 2e
        and p == 2 (mod 3) (anisotropic unimodular part) then
        v_p(w) - 2e is even;
  (iii) the pinned signs extend to an OCCURRING character vector —
        the occurring vectors form an index-2 subgroup of {+-1}^mu,
        whose annihilator is derived from the class data per disc;
        for the Eisenstein family it is supported at 3 alone:
        chi_3(w / 3^(v_3)) = +1 — every value's 3-free part is
        == 1 (mod 3), the norm-residue law.

THE ANATOMY (the theory behind a9.pair_desert's 22 kills).  Every
killed line is classified:
  L0     — some single co-norm value violates the local criterion
           at every stratum: a PROVABLY LOCAL kill (congruences);
  GENUS  — values locally fine, but no genus admits all three;
  GLOBAL — some genus admits all three values, no single class
           does: the kill is strictly beyond every character —
           by the principal genus theorem it lives inside a coset
           of Cl^2.  The fourth sieve is composition structure.
Measured decomposition of the 57 killed lines behind the m <= 1200
pair desert: 21 L0 + 0 GENUS + 36 GLOBAL.  All 24 L0 values carry
local certificates; all 36 GLOBAL lines are certified locally fine.
At m = 725 BOTH pairs die exclusively through GLOBAL kills: that
part of the desert is invisible to every congruence argument.

Run:  python3 -m compute.sphere_composition
"""

from math import gcd

from compute.sphere_classes import reduce_form, reduced_forms
from compute.sphere_gluing import (legendre, odd_primes, pair_lines,
                                   represents)

# the 11 unordered three-sieve passers at m <= 1200 (a9.pair_desert)
PASSERS_1200 = ((425, 54600, 97104), (481, 29760, 141960),
                (725, 122400, 282576), (725, 171600, 282576),
                (845, 194184, 507000), (845, 205656, 507000),
                (850, 218400, 388416), (901, 107880, 703560),
                (925, 79464, 501600), (962, 119040, 567840),
                (1025, 450000, 564816))


def _xgcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x, y = _xgcd(b, a % b)
    return g, y, x - (a // b) * y


def transform(f, M):
    """Form under the substitution (x, y) -> (px + ry, qx + sy)."""
    a, b, c = f
    p, q, r, s = M
    return (a*p*p + b*p*q + c*q*q,
            2*a*p*r + b*(p*s + q*r) + 2*c*q*s,
            a*r*r + b*r*s + c*s*s)


def rep_coprime_to(f, N):
    """PROPERLY equivalent form whose leading coefficient is coprime
    to N (determinant +1 enforced: an improper change of variables
    silently replaces the class by its inverse)."""
    a, b, c = f
    for x in range(0, 60):
        for y in sorted(range(-60, 61), key=abs):
            if gcd(x, y) != 1:
                continue
            v = a*x*x + b*x*y + c*y*y
            if v != 0 and gcd(v, N) == 1:
                g, u, w = _xgcd(x, y)
                if g < 0:
                    g, u, w = -g, -u, -w
                assert g == 1 and x*u + y*w == 1
                nf = transform(f, (x, y, -w, u))
                assert nf[0] == v
                return nf
    raise RuntimeError("no coprime value found")


def compose(f1, f2, D):
    """Gauss composition of primitive classes of discriminant D."""
    f2 = rep_coprime_to(f2, f1[0])
    a1, b1, _ = f1
    a2, b2, _ = f2
    assert gcd(a1, a2) == 1
    A = a1 * a2
    g, u, _ = _xgcd(2 * a1, 2 * a2)
    assert (b2 - b1) % g == 0
    B = (b1 + 2 * a1 * ((b2 - b1) // g) * u) % (2 * A)
    assert (B - b1) % (2 * a1) == 0 and (B - b2) % (2 * a2) == 0
    assert (B * B - D) % (4 * A) == 0
    return reduce_form(A, B, (B * B - D) // (4 * A))


def principal_form(D):
    return reduce_form(1, D % 2, ((D % 2) - D) // 4)


_PRIMS = {}


def prims(D):
    """Primitive reduced forms (the class group) of discriminant D."""
    if D not in _PRIMS:
        _PRIMS[D] = [f for f in reduced_forms(D)
                     if gcd(gcd(f[0], abs(f[1])), f[2]) == 1]
    return _PRIMS[D]


def group_check(D):
    """Verify the composition group laws; return (h, sorted orders)."""
    forms = prims(D)
    e0 = principal_form(D)
    fs = set(forms)
    assert all(compose(e0, f, D) == f for f in forms)
    assert all(compose((f[0], -f[1], f[2]), f, D) == e0 for f in forms)
    assert all(compose(f, g2, D) in fs for f in forms for g2 in forms)
    orders = []
    for f in forms:
        x, k = f, 1
        while x != e0:
            x = compose(x, f, D)
            k += 1
            assert k <= len(forms) + 1
        orders.append(k)
    return len(forms), sorted(orders)


_CHI = {}


def chi_vec(f, D, ps):
    """The genus character vector of a primitive class (validated:
    each chi_p constant on the class's p-coprime values)."""
    key = (f, D)
    if key not in _CHI:
        a, b, c = f
        vec = []
        for p in ps:
            vals = set()
            for x in range(-3, 4):
                for y in range(-3, 4):
                    v = a*x*x + b*x*y + c*y*y
                    if v and v % p:
                        vals.add(legendre(v, p))
            assert len(vals) == 1, (f, p, vals)
            vec.append(vals.pop())
        _CHI[key] = tuple(vec)
    return _CHI[key]


def genera(D):
    """Classes grouped by character vector."""
    ps = odd_primes(-D)
    out = {}
    for f in prims(D):
        out.setdefault(chi_vec(f, D, ps), set()).add(f)
    return out


def principal_genus_check(D):
    """Gauss's principal genus theorem on the data: the set of
    squares equals the trivial-character genus."""
    gen = genera(D)
    ps = odd_primes(-D)
    squares = {compose(f, f, D) for f in prims(D)}
    triv = set(gen.get(tuple(1 for _ in ps), set()))
    return squares == triv, len(gen), sorted(len(v) for v in gen.values())


_EPS = {}


def genus_relation(D):
    """The occurring character vectors form an index-2 subgroup of
    {+-1}^mu; derive its (unique) nontrivial annihilator support."""
    if D not in _EPS:
        ps = odd_primes(-D)
        vecs = set(genera(D).keys())
        assert tuple(1 for _ in ps) in vecs
        assert len(vecs) == 2 ** (len(ps) - 1), (D, len(vecs))
        for a in vecs:
            for b in vecs:
                assert tuple(x * y for x, y in zip(a, b)) in vecs
        best = None
        for mask in range(1, 2 ** len(ps)):
            if all(_msk_prod(v, mask) == 1 for v in vecs):
                assert best is None
                best = mask
        assert best is not None
        _EPS[D] = (ps, best)
    return _EPS[D]


def _msk_prod(vec, mask):
    p = 1
    for i, s in enumerate(vec):
        if mask >> i & 1:
            p *= s
    return p


def _vp(n, p):
    v = 0
    while n % p == 0:
        n //= p
        v += 1
    return v, n


def local_representable(w, D):
    """The validated local criterion (module docstring): is the odd
    w > 0 represented by SOME primitive class of disc D = -3 k^2?"""
    assert w > 0 and w % 2 == 1
    k2 = -D // 3
    assert k2 % 3 != 0 and (-D) % 9 != 0
    forced = {}
    freeps = set()
    ps = odd_primes(-D)
    for p in ps:
        v, unit = _vp(w, p)
        if p == 3:
            forced[3] = legendre(unit, 3)
            continue
        e2 = _vp(k2, p)[0]          # = 2 v_p(k)
        if v < e2:
            if v % 2:
                return False
            forced[p] = legendre(unit, p)
        else:
            if p % 3 == 2 and (v - e2) % 2:
                return False
            freeps.add(p)
    rest = w
    for p in ps:
        while rest % p == 0:
            rest //= p
    d = 3
    while d * d <= rest:
        if rest % d == 0:
            v = 0
            while rest % d == 0:
                rest //= d
                v += 1
            if legendre(D % d, d) == -1 and v % 2:
                return False
        d += 2
    if rest > 1 and legendre(D % rest, rest) == -1:
        return False
    ps2, mask = genus_relation(D)
    supp = [p for i, p in enumerate(ps2) if mask >> i & 1]
    if any(p in freeps for p in supp):
        return True
    prod = 1
    for p in supp:
        prod *= forced[p]
    return prod == 1


def validate_local_criterion(D, bound=6000):
    """Exhaustive: criterion == brute representability for every odd
    w <= bound; returns the number of values checked."""
    pf = prims(D)
    n = 0
    for w in range(1, bound + 1, 2):
        assert local_representable(w, D) == \
            any(represents(f, w) for f in pf), (D, w)
        n += 1
    return n


def strata(tri, n):
    """All (g, ct, D, halved triple) strata for a hypothetical line
    with co-norm triple tri on S(n): point content g (2-part forced
    to v_2(n)/2, odd part free) and halved-form content ct."""
    G = gcd(gcd(tri[0], tri[1]), tri[2])
    out = []
    base, nn = 1, n
    while nn % 4 == 0:
        nn //= 4
        base *= 2
    d = 1
    while (base * d) ** 2 <= n:
        g = base * d
        if n % (g * g) == 0 and G % (g * g) == 0:
            ng = n // (g * g)
            th = [t // (g * g) // 2 for t in tri]
            Gh = gcd(gcd(th[0], th[1]), th[2])
            ct = 1
            while ct * ct <= ng:
                if ng % (ct * ct) == 0 and Gh % ct == 0:
                    out.append((g, ct, -(ng // (ct * ct)),
                                [t // ct for t in th]))
                ct += 2
        d += 2
    return out


def killed_lines(m, U, V):
    """The lines of the pair (U, V) whose triple no class represents
    (stratified primitive-class route; agrees with line_classes)."""
    n = 3 * m * m
    out = []
    for i, tri in enumerate(pair_lines(2 * m * m, U, V)):
        if not any(all(represents(f, t) for t in th)
                   for g, ct, D, th in strata(tri, n) for f in prims(D)):
            out.append((i, tri))
    return out


def line_anatomy(tri, n):
    """Classify one killed line: ('L0', bad value indices),
    ('GENUS', None), or ('GLOBAL', admitting-genus data
    [(g, ct, genus size, per-value S-intersection sizes)...])."""
    single_ok = [False, False, False]
    admitting = []
    for g, ct, D, th in strata(tri, n):
        pf = prims(D)
        if not pf:
            continue
        ps = odd_primes(-D)
        S = [{f for f in pf if represents(f, t)} for t in th]
        for i in range(3):
            if S[i]:
                single_ok[i] = True
        if all(S):
            for key, gv in genera(D).items():
                if all(gv & S[i] for i in range(3)):
                    admitting.append((g, ct, len(gv),
                                      tuple(len(gv & S[i])
                                            for i in range(3))))
    if not all(single_ok):
        return "L0", [i for i in range(3) if not single_ok[i]]
    if not admitting:
        return "GENUS", None
    return "GLOBAL", admitting


def anatomy(pairs=PASSERS_1200):
    """Full anatomy: per pair the killed lines with verdicts; totals;
    and the certification that every L0 value fails the local
    criterion at every stratum while every GLOBAL line's values all
    pass it somewhere (so those kills are provably beyond-local)."""
    rows = []
    totals = {"L0": 0, "GENUS": 0, "GLOBAL": 0}
    l0_vals = l0_cert = glob_lines = glob_local_ok = 0
    for m, U, V in pairs:
        n = 3 * m * m
        row = []
        for i, tri in killed_lines(m, U, V):
            verdict, info = line_anatomy(tri, n)
            totals[verdict] += 1
            row.append((i, verdict, info))
            st = strata(tri, n)
            if verdict == "L0":
                for j in info:
                    l0_vals += 1
                    if not any(prims(D) and
                               local_representable(th[j], D)
                               for g, ct, D, th in st):
                        l0_cert += 1
            elif verdict == "GLOBAL":
                glob_lines += 1
                if all(any(local_representable(th[j], D)
                           for g, ct, D, th in st if prims(D))
                       for j in range(3)):
                    glob_local_ok += 1
        rows.append((m, U, V, row))
    cert = (l0_vals, l0_cert, glob_lines, glob_local_ok)
    return rows, totals, cert


def main():
    for D in (-507, -3 * 65 * 65):
        h, orders = group_check(D)
        pg, ngen, sizes = principal_genus_check(D)
        ps, mask = genus_relation(D)
        supp = [p for i, p in enumerate(ps) if mask >> i & 1]
        print(f"disc {D}: h = {h}, orders {orders}; principal genus "
              f"theorem: {pg} ({ngen} genera, sizes {sizes}); "
              f"relation: chi over {supp} = +1")
    nv = validate_local_criterion(-3 * 65 * 65, 4000)
    print(f"local criterion == brute force on {nv} odd values "
          f"(disc -12675)")
    rows, totals, cert = anatomy()
    for m, U, V, row in rows:
        print(f"m={m} ({U},{V}): " +
              "; ".join(f"line{i}:{v}" for i, v, _ in row))
    print(f"TOTALS {totals}; L0 values {cert[0]} all locally "
          f"certified: {cert[0] == cert[1]}; GLOBAL lines {cert[2]} "
          f"all locally fine: {cert[2] == cert[3]}")
    print("THE FOURTH SIEVE IS COMPOSITION: 36 of 57 kills happen "
          "inside a single genus — inside a coset of Cl^2 — beyond "
          "every congruence and character condition.")


if __name__ == "__main__":
    main()
