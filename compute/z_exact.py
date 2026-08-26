"""A8-T3: the EXACT special-curve locus — upgrading Certificate A8.7
from mod-p to Q-bar, making Theorem A8.8 (node passage) unconditional.

Strategy.  Z is contained in V(R_12) and V(R_34) for the pairwise
resultants R_ab = Res_(dc:dv)(F_a, F_b) in Z[c, v] (disjoint index
pairs).  Therefore every curve component of Z divides
gcd(R_12, R_34).  We prove that gcd is supported on the nine entry
lines:

  1. compute R_12 and R_34 EXACTLY: interpolate the 8x8 Sylvester
     determinant on a 113 x 113 grid modulo enough 30-bit primes and
     CRT.  Exactness is PROVEN, not sampled: every coefficient of an
     8x8 determinant of polynomial entries is bounded in absolute
     value by prod_rows (l1-norm of the row polynomials) — the
     permutation expansion gives |coeff| <= sum_sigma prod_i
     l1(M_[i, sigma(i)]) <= prod_i sum_j l1(M_ij) =: B — and the
     prime product exceeds 2B.  (Belt-and-braces, the module also
     re-checks R at random integer points against exact integer
     Sylvester determinants.)
  2. peel the entry-line factors exactly: synthetic division by the
     monic-in-c linear forms l_(a,b) = c + a + b v over Z, recording
     the exact multiplicity e_(a,b) of each line in each resultant;
  3. certify the two peeled cofactors COPRIME over Q, in the sound
     direction: a common factor H with deg_v H >= 1 would survive
     reduction mod a prime p that keeps the v-leading coefficient
     alive (lc_v(H) divides lc_v(cof) in Z[c], so p not dividing
     lc_v(cof) keeps deg_v H), forcing Res_v(cof1, cof2) = 0 mod p;
     exhibiting a point c0 with lc's alive and Res_v(c0) != 0 mod p
     kills it.  Common factors with deg_v = 0 lie in the gcd of the
     v-contents, computed exactly over Q.

Then gcd(R_12, R_34) = prod l^(min e) x constant, so the curve part
of Z is contained in the nine entry lines — over Q-bar, no mod-p
caveat.  With Lemma A8.6 this proves Theorem A8.8 outright.

The exact resultants are stored in compute/data_z_resultants.json
(sparse {(i, j): int} with ~40-digit coefficients); the verify check
re-derives everything in FULL profile and re-verifies the stored data
in FAST.

Run:  python3 -m compute.z_exact
"""

import json
import os
from fractions import Fraction as F
from functools import reduce
from math import gcd

from compute.special_locus import DEG_BOUND, M, numerator_forms

DATA = os.path.join(os.path.dirname(__file__), "data_z_resultants.json")
PAIRS = ((0, 1), (2, 3))  # disjoint pairs: Z is inside both V(R)
GRIDN = 113  # interpolation grid; covers bidegree (112, 112) >= 8 x 14


# ---------------------------------------------------------------------------
# integer forms

def integral_forms():
    """The six direction-quartics with integer, content-free
    coefficient dicts [B_0..B_4] (scaling is harmless: it rescales
    resultants by nonzero constants, which V() ignores)."""
    out = []
    for Ns in numerator_forms():
        dens = [v.denominator for N in Ns for v in N.values() if v]
        L = reduce(lambda a, b: a * b // gcd(a, b), dens, 1)
        ints = [{ij: int(v * L) for ij, v in N.items() if v}
                for N in Ns]
        g = reduce(gcd, (abs(x) for N in ints for x in N.values()), 0)
        out.append([{ij: x // g for ij, x in N.items()}
                    for N in ints])
    return out


def l1(poly):
    return sum(abs(x) for x in poly.values())


def resultant_bound(fa, fb):
    """Rigorous sup-norm bound for the coefficients of
    Res_(4,4)(F_a, F_b): prod over the 8 Sylvester rows of the row's
    total l1-norm (each row holds the 5 coefficient polynomials of one
    form)."""
    ra, rb = sum(l1(N) for N in fa), sum(l1(N) for N in fb)
    return ra ** 4 * rb ** 4


# ---------------------------------------------------------------------------
# primes (deterministic Miller-Rabin, valid far beyond 2^64)

def _is_prime(n):
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d, s = d // 2, s + 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def primes_exceeding(target):
    """Descending 30-bit primes whose product exceeds `target`."""
    ps, prod, n = [], 1, 2 ** 30
    while prod <= target:
        n -= 1
        if _is_prime(n):
            ps.append(n)
            prod *= n
    return ps


# ---------------------------------------------------------------------------
# modular grid interpolation of the resultant

def _det_mod(mat, p):
    m = [row[:] for row in mat]
    n, det = len(m), 1
    for col in range(n):
        piv = next((r for r in range(col, n) if m[r][col]), None)
        if piv is None:
            return 0
        if piv != col:
            m[col], m[piv] = m[piv], m[col]
            det = -det % p
        det = det * m[col][col] % p
        inv = pow(m[col][col], p - 2, p)
        for r in range(col + 1, n):
            if m[r][col]:
                f = m[r][col] * inv % p
                for cc in range(col, n):
                    m[r][cc] = (m[r][cc] - f * m[col][cc]) % p
    return det


def _res44_vals(fvals, gvals, p):
    A, B = fvals[::-1], gvals[::-1]
    rows = [[0] * s + A + [0] * (3 - s) for s in range(4)]
    rows += [[0] * s + B + [0] * (3 - s) for s in range(4)]
    return _det_mod(rows, p)


def _interp1(ys, p, inv_cache={}):
    """Interpolate through (i, ys[i]), i = 0..n-1, mod p (Newton)."""
    n = len(ys)
    key = (p, n)
    if key not in inv_cache:
        inv_cache[key] = [0] + [pow(i, p - 2, p) for i in range(1, n)]
    inv = inv_cache[key]
    coef = ys[:]
    for j in range(1, n):
        for i in range(n - 1, j - 1, -1):
            coef[i] = (coef[i] - coef[i - 1]) * inv[j] % p
    poly = [coef[n - 1]]
    for k in range(n - 2, -1, -1):
        new = [0] * (len(poly) + 1)
        for i, x in enumerate(poly):
            new[i + 1] = (new[i + 1] + x) % p
            new[i] = (new[i] - x * k) % p
        new[0] = (new[0] + coef[k]) % p
        poly = new
    return poly


def resultant_modp(fa, fb, p, gridn=GRIDN):
    """R_ab mod p as a dense c-major coefficient table
    tab[i][j] = coeff of c^i v^j, via grid evaluation + row/column
    Newton interpolation."""
    # per-form, per-k: restriction c -> c0 as v-polynomial, then Horner
    def vpoly(N, c0):
        out = [0] * (DEG_BOUND + 1)
        cp = [pow(c0, i, p) for i in range(DEG_BOUND + 1)]
        for (i, j), val in N.items():
            out[j] = (out[j] + val * cp[i]) % p
        return out

    vals = []  # vals[ci][vj] = det
    for ci in range(gridn):
        fap = [vpoly(N, ci) for N in fa]
        fbp = [vpoly(N, ci) for N in fb]
        row = []
        for vj in range(gridn):
            fv = [0] * 5
            gv = [0] * 5
            for k in range(5):
                acc = 0
                for cc in reversed(fap[k]):
                    acc = (acc * vj + cc) % p
                fv[k] = acc
                acc = 0
                for cc in reversed(fbp[k]):
                    acc = (acc * vj + cc) % p
                gv[k] = acc
            row.append(_res44_vals(fv, gv, p))
        vals.append(row)
    # interpolate in v (rows), then in c (columns)
    rows = [_interp1(r, p) for r in vals]
    width = max(len(r) for r in rows)
    tab = []
    for j in range(width):
        col = [(r[j] if j < len(r) else 0) for r in rows]
        tab.append(_interp1(col, p))
    # tab[j][i] = coeff c^i v^j -> transpose to {(i,j)}
    out = {}
    for j, col in enumerate(tab):
        for i, x in enumerate(col):
            if x:
                out[(i, j)] = x
    return out


def crt_resultant(fa, fb, verbose=False):
    """The EXACT resultant in Z[c, v]: CRT over descending 30-bit
    primes whose product provably exceeds twice the l1 bound."""
    B = resultant_bound(fa, fb)
    ps = primes_exceeding(2 * B)
    if verbose:
        print(f"  bound B ~ 10^{len(str(B)) - 1}, "
              f"{len(ps)} primes of 30 bits")
    acc, mod = {}, 1
    for p in ps:
        tab = resultant_modp(fa, fb, p)
        if not acc:
            acc = {ij: v % p for ij, v in tab.items()}
            mod = p
        else:
            new = {}
            inv = pow(mod, p - 2, p)
            for ij in set(acc) | set(tab):
                a = acc.get(ij, 0)
                t = (tab.get(ij, 0) - a) * inv % p
                new[ij] = a + mod * t
            acc, mod = new, mod * p
    # symmetric lift
    out = {}
    for ij, v in acc.items():
        if v > mod // 2:
            v -= mod
        if v:
            out[ij] = v
    return out, len(ps)


# ---------------------------------------------------------------------------
# exact spot verification (independent of the interpolation code path)

def det_exact(mat):
    """Fraction-free-enough exact determinant of a small integer
    matrix (fraction Gaussian elimination)."""
    m = [[F(x) for x in row] for row in mat]
    n, det = len(m), F(1)
    for col in range(n):
        piv = next((r for r in range(col, n) if m[r][col]), None)
        if piv is None:
            return 0
        if piv != col:
            m[col], m[piv] = m[piv], m[col]
            det = -det
        det *= m[col][col]
        for r in range(col + 1, n):
            if m[r][col]:
                f = m[r][col] / m[col][col]
                for cc in range(col, n):
                    m[r][cc] -= f * m[col][cc]
    assert det.denominator == 1
    return det.numerator


def spot_check(R, fa, fb, points):
    """R(c0, v0) == exact integer Sylvester determinant at each
    point."""
    for (c0, v0) in points:
        fv = [sum(val * c0 ** i * v0 ** j for (i, j), val in N.items())
              for N in fa]
        gv = [sum(val * c0 ** i * v0 ** j for (i, j), val in N.items())
              for N in fb]
        A, Bv = fv[::-1], gv[::-1]
        rows = [[0] * s + A + [0] * (3 - s) for s in range(4)]
        rows += [[0] * s + Bv + [0] * (3 - s) for s in range(4)]
        want = det_exact(rows)
        got = sum(val * c0 ** i * v0 ** j for (i, j), val in R.items())
        assert got == want, f"spot check FAILED at {(c0, v0)}"
    return True


# ---------------------------------------------------------------------------
# exact line-peeling over Z

def _to_cmajor(R):
    """{(i,j): int} -> list over c-degree of {v-deg: int}."""
    dc = max(i for (i, _) in R)
    out = [dict() for _ in range(dc + 1)]
    for (i, j), v in R.items():
        out[i][j] = v
    return out


def _from_cmajor(lst):
    return {(i, j): v for i, d in enumerate(lst)
            for j, v in d.items() if v}


def _vp_mul(d, a, b):
    """d(v) * (-a - b v) for integer a, b."""
    out = {}
    for j, x in d.items():
        if a:
            out[j] = out.get(j, 0) - a * x
        if b:
            out[j + 1] = out.get(j + 1, 0) - b * x
    return {j: x for j, x in out.items() if x}


def _vp_add(d, e):
    out = dict(d)
    for j, x in e.items():
        out[j] = out.get(j, 0) + x
        if not out[j]:
            del out[j]
    return out


def divide_line(R, a, b):
    """Exact division of R by l = c + a + b v (monic in c): returns
    (quotient, remainder_v_poly); remainder == {} iff l | R."""
    cm = _to_cmajor(R)
    d = len(cm) - 1
    quot = [dict() for _ in range(d)]
    carry = {}
    for i in range(d, 0, -1):
        cur = _vp_add(cm[i], carry)
        quot[i - 1] = cur
        carry = _vp_mul(cur, a, b)  # (-a - b v) * cur
    rem = _vp_add(cm[0], carry)
    return _from_cmajor(quot), rem


def peel_lines(R):
    """Divide out each entry line to its exact multiplicity.
    Returns ({(a, b): e}, cofactor)."""
    from compute.descent_differentials import GRID
    exps = {}
    for (a, b) in sorted(GRID):
        e = 0
        while True:
            q, rem = divide_line(R, a, b)
            if rem:
                break
            R, e = q, e + 1
        exps[(a, b)] = e
    return exps, R


def content(R):
    return reduce(gcd, (abs(v) for v in R.values()), 0)


# ---------------------------------------------------------------------------
# coprimality of the cofactors (sound direction)

def _vdeg(R):
    return max(j for (_, j) in R)


def _lc_v(R):
    """Leading coefficient w.r.t. v: {c-deg: int}."""
    dv = _vdeg(R)
    return {i: v for (i, j), v in R.items() if j == dv}


def _vcontent_gcd(R1, R2):
    """gcd over Q of the two v-contents (gcd of v-coefficient
    c-polynomials): [1] means no common deg_v = 0 factor."""
    from compute.special_locus import poly_gcd_1var

    def cpolys(R):
        by_j = {}
        for (i, j), v in R.items():
            by_j.setdefault(j, {})[i] = v
        out = []
        for j, d in by_j.items():
            out.append([d.get(i, 0) for i in range(max(d) + 1)])
        return out

    g = None
    for lst in cpolys(R1) + cpolys(R2):
        g = lst if g is None else poly_gcd_1var(g, lst)
        if len(g) == 1 and g[0] != 0:
            return [1]
    return g


def coprime_witness(R1, R2, prime):
    """Certify gcd_Q(R1, R2) is constant.  Returns the witness dict or
    raises.  Sound direction only: a common factor H (primitive, in
    Z[c,v]) with deg_v H >= 1 satisfies lc_v(H) | lc_v(R_i) in Z[c];
    since p does not kill lc_v(R1) (checked), deg_v of H mod p is
    preserved, so H mod p would be a positive-v-degree common factor
    of the reductions — impossible once Res_v(R1, R2) mod p is shown
    nonzero by ONE evaluation c = c0 where neither lc_v vanishes.
    deg_v = 0 common factors are excluded by the exact v-content gcd
    over Q."""
    p = prime
    lc1, lc2 = _lc_v(R1), _lc_v(R2)
    assert any(v % p for v in lc1.values()), "p kills lc_v(R1)"
    assert any(v % p for v in lc2.values()), "p kills lc_v(R2)"
    vc = _vcontent_gcd(R1, R2)
    assert len(vc) == 1 and vc[0] != 0, "common v-free factor!"

    def vpolys_at(R, c0):
        dv = _vdeg(R)
        out = [0] * (dv + 1)
        for (i, j), v in R.items():
            out[j] = (out[j] + v * pow(c0, i, p)) % p
        return out

    def lc_at(lc, c0):
        return sum(v * pow(c0, i, p) for i, v in lc.items()) % p

    for c0 in range(2, 200):
        if lc_at(lc1, c0) == 0 or lc_at(lc2, c0) == 0:
            continue
        f, g = vpolys_at(R1, c0), vpolys_at(R2, c0)
        n1, n2 = len(f) - 1, len(g) - 1
        rows = [[0] * s + f[::-1] + [0] * (n2 - 1 - s)
                for s in range(n2)]
        rows += [[0] * s + g[::-1] + [0] * (n1 - 1 - s)
                 for s in range(n1)]
        d = _det_mod(rows, p)
        if d:
            return {"prime": p, "c0": c0, "resv_mod": d,
                    "vdeg": (n1, n2)}
    raise AssertionError("no coprimality witness found — investigate")


# ---------------------------------------------------------------------------
# orchestration

def compute_certificate(verbose=True, spots=6):
    forms = integral_forms()
    cert = {"pairs": [], "primes_used": {}, "coprime": None}
    Rs = []
    for (a, b) in PAIRS:
        if verbose:
            print(f"pair ({a + 1},{b + 1}): exact resultant ...")
        R, np_ = crt_resultant(forms[a], forms[b], verbose)
        pts = [(3, 5), (-7, 2), (11, -4), (-1, -9), (13, 8),
               (-15, 17)][:spots]
        spot_check(R, forms[a], forms[b], pts)
        c = content(R)
        R = {ij: v // c for ij, v in R.items()}
        exps, cof = peel_lines(R)
        Rs.append((R, exps, cof))
        cert["pairs"].append({
            "pair": (a + 1, b + 1), "n_primes": np_,
            "total_deg": max(i + j for (i, j) in R),
            "n_terms": len(R),
            "max_digits": max(len(str(abs(v))) for v in R.values()),
            "line_exponents": {str(k): e for k, e in exps.items()},
            "cofactor_deg": max(i + j for (i, j) in cof),
            "cofactor_vdeg": _vdeg(cof),
        })
        if verbose:
            pr = cert["pairs"][-1]
            print(f"  deg {pr['total_deg']}, {pr['n_terms']} terms, "
                  f"<= {pr['max_digits']} digits; exponents "
                  f"{sorted(set(exps.values()))}; cofactor deg "
                  f"{pr['cofactor_deg']}")
    (R1, e1, cof1), (R2, e2, cof2) = Rs
    cert["coprime"] = coprime_witness(cof1, cof2, 999999937)
    if verbose:
        print("cofactor coprimality witness:", cert["coprime"])
    gcd_exps = {k: min(e1[k], e2[k]) for k in e1}
    cert["gcd_exponents"] = {str(k): v for k, v in gcd_exps.items()}
    cert["ok"] = all(v >= 1 for v in gcd_exps.values())
    return cert, Rs


def save(cert, Rs):
    payload = {"certificate": cert,
               "R": [{f"{i},{j}": str(v) for (i, j), v in R.items()}
                     for (R, _, _) in Rs]}
    with open(DATA, "w") as fh:
        json.dump(payload, fh)
    return os.path.getsize(DATA)


def load():
    with open(DATA) as fh:
        payload = json.load(fh)
    Rs = []
    for d in payload["R"]:
        R = {}
        for k, v in d.items():
            i, j = k.split(",")
            R[(int(i), int(j))] = int(v)
        Rs.append(R)
    return payload["certificate"], Rs


def main():
    cert, Rs = compute_certificate()
    size = save(cert, Rs)
    print(f"stored {DATA} ({size // 1024} KiB)")
    if cert["ok"]:
        print("EXACT: gcd(R_12, R_34) = prod l^e x const with all "
              "e >= 1 and coprime cofactors")
        print("=> the curve part of Z is contained in the nine entry "
              "lines, over Q-bar.")
        print("=> Theorem A8.8 (node passage) is UNCONDITIONAL.")
    else:
        print("STRUCTURE CHANGED — investigate before claiming "
              "anything!")


if __name__ == "__main__":
    main()
