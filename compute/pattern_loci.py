"""Singleton-pattern exclusion (M11-G): every complete genus-0 curve
on X meets nodes over at least TWO distinct triple points.

By the pattern dichotomy (Theorem A8.13), a complete genus-0 curve C
whose nodes all sit over ONE triple point P has Lucas image a common
integral curve of the 4-dimensional extension subspace V_P =
V_{tau >= 4}(P) — and the image, being the image of a curve meeting
no other node, must also avoid the other seven triple points (their
pi-fibres consist of nodes).  This module certifies, for EACH of the
eight triple points, that the special locus of the subsystem V_P has
curve part contained in the nine entry lines, by the exact machinery
of Theorem A8.7': for a pair of basis-pair resultants
R = Res(F_i, F_j) in Z[c, v] (provably exact CRT; independently
spot-verified), peel the entry lines exactly and witness the two
peeled cofactors COPRIME over Q.  Then

    curve part of Z(V_P)  <=  V(gcd(R_1, R_2))  =  the entry lines,

and since genus-0 curves have no entry-line images (Theorem A7.3:
the only genus-0 line images are u = 0 and v = 0, whose components
visit three triple points each), singleton patterns are impossible:

    THEOREM A8.14.  Every complete curve of geometric genus 0 on X
    meets nodes over >= 2 distinct triple points of the arrangement;
    in particular it passes through >= 2 distinct nodes.

(The bases of the three B-point subspaces come from the transpose
transfer V(B) = {x : M_sigma^T x in V(A)} — Lemma A8.9's tau is
preserved by the linear automorphism sigma, which maps the
(B, pencil) configuration to the (A, pencil) configuration and the
invariant 6-space to itself.  The certificates below run directly on
those bases, so they need only that the transfer produces a spanning
set, which the exact in-span solve of M_sigma establishes.)

Run:  python3 -m compute.pattern_loci
"""

from fractions import Fraction as F
from functools import reduce
from itertools import combinations
from math import gcd

from compute.node_extension import (ALL_TAGS, extension_spaces,
                                    intersect)
from compute.special_locus import numerator_forms
from compute.z_exact import (content, coprime_witness, crt_resultant,
                             peel_lines, spot_check)

M = 4
SPOTS = ((3, 5), (-7, 2), (11, -4))


def combo_int(vec, forms=None):
    """Integer, content-free numerators of sum_a vec[a] eta_a."""
    forms = forms or numerator_forms()
    out = [dict() for _ in range(M + 1)]
    for a, Ns in enumerate(forms):
        if vec[a] == 0:
            continue
        for k in range(M + 1):
            for ij, v in Ns[k].items():
                out[k][ij] = out[k].get(ij, F(0)) + vec[a] * v
    out = [{ij: v for ij, v in c.items() if v} for c in out]
    dens = [v.denominator for c in out for v in c.values()]
    L = reduce(lambda a, b: a * b // gcd(a, b), dens, 1)
    ints = [{ij: int(v * L) for ij, v in c.items()} for c in out]
    g = reduce(gcd, (abs(x) for c in ints for x in c.values()), 0)
    return [{ij: x // g for ij, x in c.items()} for c in ints]


def _peeled_resultant(fa, fb):
    R, n_primes = crt_resultant(fa, fb)
    assert R, "identically zero pair resultant"
    spot_check(R, fa, fb, list(SPOTS))
    c = content(R)
    R = {ij: v // c for ij, v in R.items()}
    exps, cof = peel_lines(R)
    return n_primes, exps, cof


def singleton_certificate(tag, spaces=None, witness_prime=999999937):
    """The exact certificate that Z(V_P) has curve part inside the
    nine entry lines, for the triple point `tag`: two basis-pair
    resultants whose peeled cofactors are coprime over Q.  Tries
    basis pairs in a fixed order until a coprime cofactor pair is
    witnessed.  Returns a summary dict (raises if none found)."""
    spaces = spaces or extension_spaces()
    forms = numerator_forms()
    basis = [combo_int(b, forms) for b in spaces[tag]]
    assert len(basis) == 4, f"V({tag}) is not 4-dimensional?"
    done = {}
    order = list(combinations(range(4), 2))
    for pair in order:
        done[pair] = _peeled_resultant(basis[pair[0]], basis[pair[1]])
        for p1, p2 in combinations(done, 2):
            (_, e1, cof1), (_, e2, cof2) = done[p1], done[p2]
            try:
                w = coprime_witness(cof1, cof2, witness_prime)
            except AssertionError:
                continue
            assert all(v >= 8 for v in e1.values())
            assert all(v >= 8 for v in e2.values())
            return {
                "tag": tag, "pairs": (p1, p2),
                "line_exps": ({str(k): v for k, v in e1.items()},
                              {str(k): v for k, v in e2.items()}),
                "cof_degs": (max((i + j for (i, j) in cof1), default=0),
                             max((i + j for (i, j) in cof2), default=0)),
                "witness": w,
                "n_resultants_computed": len(done),
            }
    raise AssertionError(
        f"no coprime cofactor pair at {tag}: shared curve factors — "
        "the singleton exclusion needs the deeper component analysis")


def all_singletons(tags=ALL_TAGS):
    """Certificates for every requested triple point; the full run
    over all eight proves Theorem A8.14."""
    spaces = extension_spaces()
    return {tag: singleton_certificate(tag, spaces) for tag in tags}


# ---------------------------------------------------------------------------
# the |S| = 2 layer (M11-H): excluding two-point node patterns
#
# A genus-0 curve with node pattern S = {P, Q} has image containing P
# and Q, avoiding the other six triple points, integral for the
# subsystem V_S (dim 2 or 3), and not an entry line (A7.3).  For a
# 2-dimensional pencil, Z(V_S) = V(Res) EXACTLY, so the image is an
# entry line (excluded) or a component of the peeled cofactor that
# passes the battery: contains P and Q, avoids the rest, and is
# tangent (integral).  The flow below needs no factorization in
# practice: either the cofactor already misses P or Q (no component
# through both a fortiori), or the unique line PQ divides it — the
# line is tested directly (it always hits a third triple point in
# these configurations) and divided out, after which the quotient
# misses P or Q.

# triple points: (affine chart-u coords or None, projective (c:u:v))
TRIPLE_POINTS = {
    "A0": ((F(0), F(0)), (0, 1, 0)),
    "A+": ((F(-1), F(0)), (1, -1, 0)),
    "A-": ((F(1), F(0)), (1, 1, 0)),
    "B0": (None, (0, 0, 1)),
    "B+": (None, (1, 0, -1)),
    "B-": (None, (1, 0, 1)),
    "D+": ((F(0), F(-1)), (0, 1, -1)),
    "D-": ((F(0), F(1)), (0, 1, 1)),
}


def eval_proj(poly, tag):
    """poly (dict over Z/Q, chart u = 1) homogenized to its total
    degree, evaluated at the projective triple point `tag`; for
    affine points this is a nonzero multiple of the affine value."""
    d = max(i + j for (i, j) in poly)
    (Pc, Pu, Pv) = TRIPLE_POINTS[tag][1]
    return sum(val * F(Pc) ** i * F(Pv) ** j * F(Pu) ** (d - i - j)
               for (i, j), val in poly.items())


def line_through(tagP, tagQ):
    """The unique line through two triple points, as (alpha, beta,
    gamma) with alpha c + beta u + gamma v = 0 (integer, primitive)."""
    (c1, u1, v1) = TRIPLE_POINTS[tagP][1]
    (c2, u2, v2) = TRIPLE_POINTS[tagQ][1]
    a = u1 * v2 - v1 * u2
    b = v1 * c2 - c1 * v2
    g = c1 * u2 - u1 * c2
    d = reduce(gcd, (abs(a), abs(b), abs(g)))
    return (a // d, b // d, g // d)


def divide_affine_line(R, line):
    """Exact division of R (chart u = 1) by alpha c + beta + gamma v;
    returns (quotient, remainder-poly).  For alpha != 0 this is
    synthetic division in c; for alpha = 0, in v."""
    (al, be, ga) = line
    if al != 0:
        # monic-ize in c: c = (-be - ga v)/al ; divide by (c - root)
        from compute.z_exact import _to_cmajor, _from_cmajor, _vp_add
        cm = _to_cmajor(R)
        quot, carry = [dict() for _ in range(len(cm) - 1)], {}
        for i in range(len(cm) - 1, 0, -1):
            cur = _vp_add(cm[i], carry)
            quot[i - 1] = cur
            carry = {}
            for j, x in cur.items():
                if be:
                    carry[j] = carry.get(j, 0) - F(be, al) * x
                if ga:
                    carry[j + 1] = carry.get(j + 1, 0) - F(ga, al) * x
            carry = {j: x for j, x in carry.items() if x}
        rem = _vp_add(cm[0], carry)
        return _from_cmajor(quot), rem
    # alpha = 0: line is v = -be/ga (ga != 0 since primitive)
    root = F(-be, ga)
    by_i = {}
    for (i, j), val in R.items():
        by_i.setdefault(i, {})[j] = val
    quot, rem = {}, {}
    for i, d in by_i.items():
        n = max(d)
        q = [0] * n
        acc = 0
        for j in range(n, 0, -1):
            acc = acc * root + d.get(j, 0)
            q[j - 1] = acc
        r0 = acc * root + d.get(0, 0)
        for j, x in enumerate(q):
            if x:
                quot[(i, j)] = x
        if r0:
            rem[(i, 0)] = r0
    return quot, rem


def _prem_zero_modp(G, H, p):
    """True iff the v-pseudo-remainder of G by H vanishes mod p
    (requires lc_v(H) alive mod p — asserted).  A NONZERO result
    proves H does not divide G over Q (sound exclusion)."""
    def vmax(P):
        return max(j for (_, j) in P)

    def tolists(P):
        out = {}
        for (i, j), val in P.items():
            out.setdefault(j, {})[i] = val % p
        return out

    g, h = tolists(G), tolists(H)
    dh = vmax(H)
    lc = h[dh]
    assert any(x % p for x in lc.values()), "lc_v(H) dead mod p"

    def cmul(a, b):
        out = {}
        for i, x in a.items():
            for k, y in b.items():
                out[i + k] = (out.get(i + k, 0) + x * y) % p
        return {i: x for i, x in out.items() if x}

    while g:
        dg = max(g)
        if dg < dh:
            break
        top = g.pop(dg)
        # g <- lc * g - top * H * v^(dg - dh)
        new = {}
        for j, coef in g.items():
            new[j] = cmul(coef, lc)
        for j, coef in h.items():
            jj = j + dg - dh
            if jj == dg:
                continue
            t = cmul(coef, top)
            tgt = new.get(jj, {})
            for i, x in t.items():
                tgt[i] = (tgt.get(i, 0) - x) % p
            new[jj] = {i: x for i, x in tgt.items() if x}
        g = {j: cc for j, cc in new.items() if cc}
    return not g


def is_integral_modp(basis_forms, H, primes=(999999937, 1000003919)):
    """Sound-direction integrality test of the curve V(H) for the
    system: H | F_i(c, v; H_v, -H_c) must hold over Q for every basis
    form; a nonzero pseudo-remainder mod p refutes it.  Returns False
    (proven non-integral) or True (not refuted at these primes)."""
    from compute.node_extension import pmul, padd, pscal, dpoly
    Hf = {ij: F(x) for ij, x in H.items()}
    Hc, Hv = dpoly(Hf)
    if not Hv:  # v-free H: swap roles (curve v' direction)
        return is_integral_modp(
            [[c for c in reversed(B)] for B in basis_forms],
            {(j, i): x for (i, j), x in H.items()}, primes)
    negHc = pscal(Hc, F(-1)) if Hc else {}
    pows_v = [{(0, 0): F(1)}]
    for _ in range(M):
        pows_v.append(pmul(pows_v[-1], Hv))
    pows_c = [{(0, 0): F(1)}]
    for _ in range(M):
        pows_c.append(pmul(pows_c[-1], negHc) if negHc else {})
    Hint = {ij: int(x) for ij, x in Hf.items()}
    for B in basis_forms:
        G = {}
        for k in range(M + 1):
            piece = pmul(pows_v[k], pows_c[M - k])
            if not piece:
                continue
            G = padd(G, pmul({ij: F(x) for ij, x in B[k].items()},
                             piece))
        if not G:
            continue
        Gden = reduce(lambda a, b: a * b // gcd(a, b),
                      (x.denominator for x in G.values()), 1)
        Gint = {ij: int(x * Gden) for ij, x in G.items()}
        for p in primes:
            if not _prem_zero_modp(Gint, Hint, p):
                return False
    return True


def _restrict_to_line(poly, p0=(F(1, 3), F(2, 7)),
                      dirv=(F(1), F(5, 11))):
    """Exact ascending t-list of poly along p0 + t dir."""
    (c0, v0), (dc, dv) = p0, dirv
    deg = max(i + j for (i, j) in poly)

    def powers(x0, dx):
        tab = [[F(1)]]
        for _ in range(deg):
            last = tab[-1]
            new = [x0 * x for x in last] + [F(0)]
            for i, x in enumerate(last):
                new[i + 1] += dx * x
            tab.append(new)
        return tab

    cp, vp = powers(F(c0), F(dc)), powers(F(v0), F(dv))
    out = [F(0)] * (deg + 1)
    for (i, j), val in poly.items():
        for a, x in enumerate(cp[i]):
            if x:
                for b, y in enumerate(vp[j]):
                    if y:
                        out[a + b] += val * x * y
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def _ddf_degrees(f, p):
    """Degrees (with multiplicity 1; f must be squarefree mod p) of
    the irreducible factors of the univariate f mod p."""
    f = [x % p for x in f]

    def trim(a):
        while len(a) > 1 and a[-1] == 0:
            a.pop()
        return a

    def pmod_(a, b):
        a = trim(a[:])
        while a != [0] and len(a) >= len(b):
            fac = a[-1] * pow(b[-1], p - 2, p) % p
            off = len(a) - len(b)
            for i in range(len(b)):
                a[off + i] = (a[off + i] - fac * b[i]) % p
            trim(a)
        return a

    def pgcd(a, b):
        a, b = trim(a[:]), trim(b[:])
        while b != [0]:
            a, b = b, pmod_(a, b)
        inv = pow(a[-1], p - 2, p)
        return [x * inv % p for x in a]

    def pmulmod(a, b, m):
        out = [0] * (len(a) + len(b) - 1)
        for i, x in enumerate(a):
            if x:
                for j, y in enumerate(b):
                    out[i + j] = (out[i + j] + x * y) % p
        return pmod_(out, m)

    df = trim([i * f[i] % p for i in range(1, len(f))] or [0])
    g = pgcd(f, df)
    assert len(g) == 1, "restriction not squarefree mod p — skip prime"
    degs, rest, k = [], f[:], 0
    h = [0, 1]  # x
    while len(rest) - 1 > 0:
        k += 1
        if 2 * k > len(rest) - 1:
            degs.append(len(rest) - 1)
            break
        # h <- h^p mod rest
        e, base, acc = p, h[:], [1]
        while e:
            if e & 1:
                acc = pmulmod(acc, base, rest)
            base = pmulmod(base, base, rest)
            e >>= 1
        h = acc
        gk = pgcd(rest, trim([(x - (1 if i == 1 else 0)) % p
                              for i, x in enumerate(h)] or [0]))
        d = len(gk) - 1
        if d:
            degs += [k] * (d // k)
            # rest <- rest / gk (exact division mod p)
            q = []
            r = rest[:]
            while len(r) >= len(gk) and trim(r[:]) != [0]:
                fac = r[-1] * pow(gk[-1], p - 2, p) % p
                q.append(fac)
                off = len(r) - len(gk)
                for i in range(len(gk)):
                    r[off + i] = (r[off + i] - fac * gk[i]) % p
                r.pop()
            rest = trim(list(reversed(q)) or [1])
            h = pmod_(h, rest)
    return degs


LINES3 = (((F(1, 3), F(2, 7)), (F(1), F(5, 11))),
          ((F(-2, 5), F(3)), (F(1), F(-7, 3))),
          ((F(7, 2), F(-1, 9)), (F(1), F(13, 4))))
PRIMES8 = (999999937, 1000003919, 999999893, 999999883, 2000000011,
           1999999973, 999999797, 999999761)


def irreducible_over_Q(H, lines=LINES3, primes=PRIMES8):
    """PROVEN irreducibility of the bivariate H over Q: restrict to
    rational lines preserving the total degree, check each
    restriction squarefree over Q, and intersect the proper
    subset-sums of the mod-p factor-degree multisets across all
    (line, prime) pairs — an empty intersection leaves no possible
    total degree for a proper factor.  (A factorization H = H1 H2
    restricts with full degrees along a degree-preserving line and
    reduces with full degrees mod a leading-coefficient-preserving
    prime, so deg H1 is a proper subset-sum at EVERY line and prime;
    a single irreducible restriction mod one prime finishes at
    once.)"""
    from compute.special_locus import poly_gcd_1var
    d = max(i + j for (i, j) in H)
    possible = None
    for (p0, dirv) in lines:
        f = _restrict_to_line({ij: F(x) for ij, x in H.items()},
                              p0, dirv)
        if len(f) - 1 != d:
            continue
        den = reduce(lambda a, b: a * b // gcd(a, b),
                     (x.denominator for x in f), 1)
        fint = [int(x * den) for x in f]
        g = poly_gcd_1var(fint,
                          [i * fint[i] for i in range(1, len(fint))])
        if len(g) != 1:
            continue  # restriction not squarefree over Q: skip line
        for p in primes:
            if fint[-1] % p == 0:
                continue
            try:
                degs = _ddf_degrees(fint, p)
            except AssertionError:
                continue
            acc = {0}
            for dd in degs:
                acc |= {s + dd for s in acc}
            sums = {s for s in acc if 0 < s < d}
            possible = sums if possible is None else (possible & sums)
            if possible is not None and not possible:
                return True
    return possible is not None and not possible


def pair_certificate(tagS, spaces=None, witness_prime=999999937):
    """The exclusion certificate for the node pattern S = {P, Q}.
    Returns a dict with 'excluded' True/False and the reason chain."""
    spaces = spaces or extension_spaces()
    forms = numerator_forms()
    vecs = intersect(spaces, list(tagS))
    basis = [combo_int(b, forms) for b in vecs]
    dim = len(basis)
    out = {"tags": tagS, "dim": dim, "steps": []}
    cofs = []
    if dim >= 3:
        done = []
        for (i, j) in combinations(range(dim), 2):
            _, exps, cof = _peeled_resultant(basis[i], basis[j])
            assert all(e >= 1 for e in exps.values())
            done.append(cof)
            for other in done[:-1]:
                try:
                    coprime_witness(other, cof, witness_prime)
                    out["steps"].append("coprime cofactors: Z(V_S) "
                                        "curve part = entry lines")
                    out["excluded"] = True
                    out["survivors"] = []
                    return out
                except AssertionError:
                    pass
        cofs = done
    else:
        _, exps, cof = _peeled_resultant(basis[0], basis[1])
        assert all(e >= 1 for e in exps.values())
        cofs = [cof]
    cof = dict(cofs[0])
    P, Q = tagS
    survivors = []
    for _round in range(30):
        if not cof or max(i + j for (i, j) in cof) == 0:
            out["steps"].append("cofactor exhausted (constant)")
            break
        if eval_proj(cof, P) != 0 or eval_proj(cof, Q) != 0:
            out["steps"].append("remaining cofactor misses P or Q: "
                                "no component through both")
            break
        line = line_through(P, Q)
        # affine form: alpha c + beta u + gamma v at u = 1
        quot, rem = divide_affine_line(cof, line)
        if rem:
            # non-line component(s) through both P and Q: if the
            # remaining cofactor is IRREDUCIBLE over Q (certified) and
            # hits an outside triple point, its single component is
            # excluded and nothing else is left
            hits = [t for t in TRIPLE_POINTS
                    if t not in tagS and eval_proj(cof, t) == 0]
            if hits and irreducible_over_Q(cof):
                out["steps"].append(
                    f"remaining cofactor (deg "
                    f"{max(i + j for (i, j) in cof)}) is IRREDUCIBLE "
                    f"over Q (certified) and hits outside triple "
                    f"point(s) {hits}: excluded")
                break
            out["steps"].append(f"non-line component(s); cofactor "
                                f"vanishes at outside points {hits}")
            survivors.append({"cof_deg": max(i + j for (i, j) in cof),
                              "note": "needs factorization"})
            break
        # the PQ-line divides: analyze the line itself
        outside = [t for t in TRIPLE_POINTS if t not in tagS
                   and eval_proj({(1, 0): line[0], (0, 0): line[1],
                                  (0, 1): line[2]}, t) == 0]
        if outside:
            out["steps"].append(f"line PQ = {line} divides; hits "
                                f"outside triple point(s) {outside}: "
                                "excluded, divided out")
        else:
            ok = is_integral_modp(basis, {(1, 0): line[0],
                                          (0, 0): line[1],
                                          (0, 1): line[2]})
            if ok:
                survivors.append({"line": line,
                                  "note": "PQ-line not refuted"})
                out["steps"].append(f"line PQ = {line} divides and "
                                    "was NOT refuted — survivor")
            else:
                out["steps"].append(f"line PQ = {line} divides; "
                                    "proven non-integral: excluded, "
                                    "divided out")
        cof = {ij: x for ij, x in quot.items() if x}
    out["survivors"] = survivors
    out["excluded"] = not survivors
    return out


def all_pairs(tags=None):
    """Certificates for every 2-element pattern; all excluded proves
    Theorem A8.15 (|S| >= 3)."""
    spaces = extension_spaces()
    pairs = list(combinations(ALL_TAGS, 2)) if tags is None else tags
    return {tagS: pair_certificate(tagS, spaces) for tagS in pairs}


def main():
    certs = all_singletons()
    for tag, c in certs.items():
        print(f"{tag}: pairs {c['pairs']}, cofactor degs "
              f"{c['cof_degs']}, witness Res_v != 0 at "
              f"c0 = {c['witness']['c0']} mod {c['witness']['prime']} "
              f"({c['n_resultants_computed']} resultants computed)")
    print("ALL EIGHT SINGLETON PATTERNS EXCLUDED:")
    print("  Theorem A8.14 — every complete genus-0 curve on X meets")
    print("  nodes over >= 2 distinct triple points (>= 2 nodes).")
    print()
    pcs = all_pairs()
    bad = 0
    for tagS, cert in pcs.items():
        status = "EXCLUDED" if cert["excluded"] else "SURVIVORS!"
        print(f"{tagS} (dim {cert['dim']}): {status}")
        for s in cert["steps"]:
            print(f"    {s}")
        bad += 0 if cert["excluded"] else 1
    if bad == 0:
        print("ALL 28 TWO-POINT PATTERNS EXCLUDED:")
        print("  Theorem A8.15 — every complete genus-0 curve on X")
        print("  meets nodes over >= 3 distinct triple points.")
    else:
        print(f"{bad} pattern(s) with surviving candidates — "
              "deeper analysis required before any |S| >= 3 claim.")


if __name__ == "__main__":
    main()
