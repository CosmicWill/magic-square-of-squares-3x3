"""Front A step 2 (ROADMAP R.6-A): the mechanical ENDPOINT EXTRACTOR for
the (a,b) ladder -- what the hand-trees of A3.8/A3.9/A3.10 did by hand,
done once for every pattern.

Setting (two split primes; the engine's conventions).  A pattern is a
signed relation  sum_i c_i Im(sigma^{j_i} tau^{k_i}) = 0  and its
cleared form is  sum_i c_i p^{2(J-|j_i|)} q^{2(K-|k_i|)} Im(l^{2j_i} w^{2k_i})
with l = pi^2 = c1 + i s1, w = rho^2 = c2 + i s2, negative exponents
meaning conjugates.  Three facts drive the extractor:

  (1) COLLAPSE.  For any two terms the sum-to-product identity holds
      EXACTLY with the cleared weights:  the pair collapses to
      +-2 p^{2a} q^{2b} Trig1(D) Trig2(M)  with D, M the half-difference /
      half-sum monomials (Trig in {Re, Im}).  We do not trust the sign
      conventions: every collapse is found by exact polynomial identity
      over Z[c1,s1,c2,s2].
  (2) UNITS.  A trig-monomial involving l (x != 0) is a p-unit and one
      involving w is a q-unit (pi divides one of the two conjugate
      products, never both).  Only a PURE-w monomial can absorb a power
      of p, only a pure-l one a power of q.
  (3) LEVER.  After collapsing the pair of minimal weight at a prime P,
      the third term's surplus weight P^e must divide the product; by
      (2) it must land on a pure factor of the other prime, else the
      pattern is DEAD.  What remains is the ENDPOINT:
          P^e | Trig(pure monomial)   and   the residual product equation,
      which after absorption is a coincidence between trig-monomials of
      the two primes -- the Lucas-coincidence family (the rigidity lemma
      is  Re(w^4) = +-p^2 Re(l^2)).
"""
from __future__ import annotations

from compute.two_prime_additive import (gauss_pow, p4add, p4mul, ELL, W,
                                        P2, Q2)


def _neg(P):
    return {k: -v for k, v in P.items()}


def trig(kind, x, y):
    """Re/Im of l^x w^y in Z[c1,s1,c2,s2]; negative exponents = conjugates."""
    Rl, Il = gauss_pow(*ELL, abs(x))
    if x < 0:
        Il = _neg(Il)
    Rw, Iw = gauss_pow(*W, abs(y))
    if y < 0:
        Iw = _neg(Iw)
    R = p4add(p4mul(Rl, Rw), p4mul(Il, Iw), -1)
    I = p4add(p4mul(Rl, Iw), p4mul(Il, Rw))
    return R if kind == "Re" else I


def scale(P, c):
    return {k: c * v for k, v in P.items()} if c != 1 else dict(P)


def times_pq(P, a, b):
    for _ in range(a):
        P = p4mul(P, P2)
    for _ in range(b):
        P = p4mul(P, Q2)
    return P


def cleared_terms(pattern):
    """[(c, wp, wq, (2j, 2k), poly)] with poly = c p^{2wp} q^{2wq} Im(l^{2j} w^{2k})."""
    J = max(abs(j) for (j, k), c in pattern)
    K = max(abs(k) for (j, k), c in pattern)
    out = []
    for (j, k), c in pattern:
        T = trig("Im", 2 * j, 2 * k)
        wp, wq = J - abs(j), K - abs(k)
        out.append((c, wp, wq, (2 * j, 2 * k), scale(times_pq(T, wp, wq), c)))
    return out


def deg_pq(P):
    """(degree in (c1,s1), degree in (c2,s2)) of a homogeneous-per-prime poly."""
    return (max(a + b for a, b, c, d in P), max(c + d for a, b, c, d in P))


def find_collapse(ta, tb):
    """Exact identity  ta.poly + tb.poly == s * 2 * p^{2a} q^{2b} Trig1(D) Trig2(M)
    for D, M in the natural half-sum/half-difference candidates.  Returns
    (s, a, b, kind1, D, kind2, M) or None."""
    ca, wpa, wqa, ea, Pa = ta
    cb, wpb, wqb, eb, Pb = tb
    S = p4add(Pa, Pb)
    if not S:
        return None
    dS = deg_pq(S)
    (x1, y1), (x2, y2) = ea, eb
    cands = set()
    for sx in (1, -1):
        for sy in (1, -1):
            # half-sum and half-difference with sign variants (conjugation freedom)
            hs = ((x1 + sx * x2) // 2, (y1 + sy * y2) // 2)
            hd = ((x1 - sx * x2) // 2, (y1 - sy * y2) // 2)
            if (x1 + sx * x2) % 2 or (y1 + sy * y2) % 2:
                continue
            for D, M in ((hd, hs), (hs, hd)):
                for D2 in (D, (-D[0], D[1]), (D[0], -D[1]), (-D[0], -D[1])):
                    for M2 in (M, (-M[0], M[1]), (M[0], -M[1]), (-M[0], -M[1])):
                        cands.add((D2, M2))
    for D, M in cands:
        for k1 in ("Re", "Im"):
            for k2 in ("Re", "Im"):
                T = p4mul(trig(k1, *D), trig(k2, *M))
                T = scale(T, 2)
                if not T:
                    continue
                dT = deg_pq(T)
                a2, b2 = dS[0] - dT[0], dS[1] - dT[1]
                if a2 < 0 or b2 < 0 or a2 % 2 or b2 % 2:
                    continue
                T = times_pq(T, a2 // 2, b2 // 2)
                if T == S:
                    return (1, a2 // 2, b2 // 2, k1, D, k2, M)
                if _neg(T) == S:
                    return (-1, a2 // 2, b2 // 2, k1, D, k2, M)
    return None


def is_pure_w(m):
    return m[0] == 0 and m[1] != 0


def is_pure_l(m):
    return m[1] == 0 and m[0] != 0


def extract(pattern):
    """The endpoint of one OPEN pattern.  Returns a dict with
    'status' in {'DEAD-no-pure-factor', 'ENDPOINT', 'NO-LEVER', 'NO-COLLAPSE'}."""
    terms = cleared_terms(pattern)
    n = len(terms)
    if n != 3:
        return {"status": "NOT-3-TERMS"}
    results = []
    for prime in ("p", "q"):
        wi = 1 if prime == "p" else 2
        ws = [t[wi] for t in terms]
        m = min(ws)
        low = [i for i in range(3) if ws[i] == m]
        if len(low) != 2:
            continue                      # no lever at this prime (all equal or single min: pruned)
        a, b = low
        c = ({0, 1, 2} - {a, b}).pop()
        col = find_collapse(terms[a], terms[b])
        if col is None:
            results.append({"prime": prime, "status": "NO-COLLAPSE"})
            continue
        s, ap, bq, k1, D, k2, M = col
        # relation:  s*2*p^{2ap} q^{2bq} T1(D) T2(M) = -term_c
        cc, wpc, wqc, ec, Pc = terms[c]
        ep, eq = wpc - ap, wqc - bq          # surplus of the third term (may be negative)
        # which side must absorb which power
        absorb = {}
        dead = False
        for P, e, pure in (("p", ep, is_pure_w), ("q", eq, is_pure_l)):
            if e > 0:
                fac = [("D", D, k1) if pure(D) else None, ("M", M, k2) if pure(M) else None]
                fac = [f for f in fac if f]
                if not fac:
                    dead = True
                absorb[P] = ("product", 2 * e, fac)
            elif e < 0:
                if not pure(ec):
                    dead = True
                absorb[P] = ("third", -2 * e, ("C", ec, "Im"))
        results.append({"prime": prime, "status": "DEAD-no-pure-factor" if dead else "ENDPOINT",
                        "pair": (a, b), "third": c, "sign": s, "kinds": (k1, k2), "D": D, "M": M,
                        "C": ec, "coeff_c": cc, "absorb": absorb})
    if not results:
        return {"status": "NO-LEVER"}
    if any(r["status"] == "DEAD-no-pure-factor" for r in results):
        return {"status": "DEAD-no-pure-factor", "detail": results}
    if all(r["status"] == "NO-COLLAPSE" for r in results):
        return {"status": "NO-COLLAPSE", "detail": results}
    return {"status": "ENDPOINT", "detail": [r for r in results if r["status"] == "ENDPOINT"]}


# ---------------------------------------------------------------- the chase
#
# Lucas values: U_y = Re(w^y), V_y = Im(w^y), C_x = Re(l^x), S_x = Im(l^x)
# (y, x >= 1).  Facts used by the chase, all classical for primitive
# Gaussian powers:  gcd(U_y, V_y) = 1 = gcd(C_x, S_x);  U_y, C_x odd and
# V_y, S_x even;  U_y, V_y are p-units and C_x, S_x are q-units;
# U_{2y} = U_y^2 - V_y^2, V_{2y} = 2 U_y V_y (same for C, S).
#
# An endpoint  s*2*T1(D)*T2(M) = -c * p^{2ep} q^{2eq} * Im(C)  is turned
# into a polynomial identity in the Lucas symbols of ONE w-exponent and
# ONE l-exponent (after double-angle reduction), verified as an exact
# identity in Z[c1,s1,c2,s2].  Then the chase collects the symbol shared
# by both sides into a product form and applies the coprimality rules.

import sympy as _sp

_c1, _s1, _c2, _s2 = _sp.symbols("c1 s1 c2 s2")
_P, _Q = _sp.symbols("p q", positive=True)


def _poly_expr(P):
    return sum(v * _c1**a * _s1**b * _c2**c * _s2**d for (a, b, c, d), v in P.items())


def lucas_expr(kind, x, y):
    """Trig(l^x w^y) written in the symbols U_|y|, V_|y|, C_|x|, S_|x|
    (conjugation = sign flip of the Im part), as a sympy expression."""
    Ux, Vx = _sp.Symbol(f"C{abs(x)}"), _sp.Symbol(f"S{abs(x)}")
    Uy, Vy = _sp.Symbol(f"U{abs(y)}"), _sp.Symbol(f"V{abs(y)}")
    if x == 0:
        Ux, Vx = _sp.Integer(1), _sp.Integer(0)
    if y == 0:
        Uy, Vy = _sp.Integer(1), _sp.Integer(0)
    if x < 0:
        Vx = -Vx
    if y < 0:
        Vy = -Vy
    re = Ux * Uy - Vx * Vy
    im = Ux * Vy + Vx * Uy
    return re if kind == "Re" else im


def lucas_value(sym):
    """The polynomial (as sympy expr in c1,s1,c2,s2) of a Lucas symbol."""
    name, n = sym.name[0], int(sym.name[1:])
    kind = "Re" if name in "UC" else "Im"
    if name in "UV":
        return _poly_expr(trig(kind, 0, n))
    return _poly_expr(trig(kind, n, 0))


def _multiple_angle(Cg, Sg, k):
    """(Re, Im) of (Cg + i Sg)^k as polynomials in the symbols Cg, Sg."""
    R, I = _sp.Integer(1), _sp.Integer(0)
    for _ in range(k):
        R, I = _sp.expand(R * Cg - I * Sg), _sp.expand(R * Sg + I * Cg)
    return R, I


def reduce_to_base(expr, y0, x0):
    """Rewrite every w-side symbol U_n, V_n through the base exponent y0
    (n a multiple of y0) by the multiple-angle polynomials of
    (U_{y0} + i V_{y0})^{n/y0}, and every l-side symbol C_n, S_n through
    x0 likewise.  Callers pass y0 = gcd of the w-exponents present and
    x0 = gcd of the l-exponents present, so every symbol reduces."""
    from math import gcd
    subs = {}
    for sy in expr.free_symbols:
        nm = str(sy)
        if nm[0] not in "UVCS":
            continue
        n = int(nm[1:])
        base = y0 if nm[0] in "UV" else x0
        if base == 0 or n == base or n % base:
            continue
        if nm[0] in "UV":
            R, I = _multiple_angle(_sp.Symbol(f"U{base}"), _sp.Symbol(f"V{base}"), n // base)
            subs[sy] = R if nm[0] == "U" else I
        else:
            R, I = _multiple_angle(_sp.Symbol(f"C{base}"), _sp.Symbol(f"S{base}"), n // base)
            subs[sy] = R if nm[0] == "C" else I
    return _sp.expand(expr.subs(subs))


def endpoint_identity(pattern, detail):
    """The endpoint as  LHS - RHS = 0  in Lucas symbols, plus the base
    exponents (y0, x0) and the verification that the identity holds
    exactly in Z[c1,s1,c2,s2].  Returns (expr, y0, x0, ep, eq, ok)."""
    terms = cleared_terms(pattern)
    a, b = detail["pair"]
    c = detail["third"]
    s = detail["sign"]
    k1, k2 = detail["kinds"]
    D, M, C = detail["D"], detail["M"], detail["C"]
    # weights of the collapsed pair (min) and of the third term
    ap, bq = min(terms[a][1], terms[b][1]), min(terms[a][2], terms[b][2])
    cc, wpc, wqc = terms[c][0], terms[c][1], terms[c][2]
    ep, eq = wpc - ap, wqc - bq
    lhs = s * 2 * lucas_expr(k1, *D) * lucas_expr(k2, *M)
    rhs = -cc * lucas_expr("Im", *C)
    if ep >= 0:
        rhs = rhs * _P**(2 * ep)
    else:
        lhs = lhs * _P**(-2 * ep)
    if eq >= 0:
        rhs = rhs * _Q**(2 * eq)
    else:
        lhs = lhs * _Q**(-2 * eq)
    expr = _sp.expand(lhs - rhs)
    # base exponents: the gcd of the w- and of the l-exponents present
    from math import gcd
    from functools import reduce
    ys = {int(str(sy)[1:]) for sy in expr.free_symbols if str(sy)[0] in "UV"}
    xs = {int(str(sy)[1:]) for sy in expr.free_symbols if str(sy)[0] in "CS"}
    y0 = reduce(gcd, ys) if ys else 0
    x0 = reduce(gcd, xs) if xs else 0
    red = reduce_to_base(expr, y0, x0) if (y0 or x0) else expr
    # verify exactly: the symbol expression is the EQUATION (not an
    # identity); substituting the Lucas polynomials and p^2 = c1^2+s1^2,
    # q^2 = c2^2+s2^2 it must reproduce the cleared relation divided by
    # the common weight p^{2 mp} q^{2 mq}.
    check = red
    for sy in list(red.free_symbols):
        nm = str(sy)
        if nm[0] in "UVCS":
            check = check.subs(sy, lucas_value(sy))
    check = _sp.expand(check.subs({_P**2: _c1**2 + _s1**2, _Q**2: _c2**2 + _s2**2}))
    mp, mq = min(t[1] for t in terms), min(t[2] for t in terms)
    rel = _sp.Integer(0)
    for t in terms:
        rel += _poly_expr(t[4])
    lhs_full = _sp.expand(check * (_c1**2 + _s1**2)**mp * (_c2**2 + _s2**2)**mq)
    ok = _sp.expand(lhs_full - rel) == 0
    return red, y0, x0, ep, eq, ok


def _side_of(sym):
    n = str(sym)
    return "w" if n[0] in "UV" else ("l" if n[0] in "CS" else n)


def _coprime(A, B, facts):
    """Known-coprime oracle for atoms (symbols, p, q, or binomials)."""
    if A == B:
        return False
    a, b = str(A), str(B)
    if (A, B) in facts or (B, A) in facts:
        return True
    # Pythagorean legs of the same power are coprime
    if a[0] in "UV" and b[0] in "UV" and a[1:] == b[1:] and a[0] != b[0]:
        return True
    if a[0] in "CS" and b[0] in "CS" and a[1:] == b[1:] and a[0] != b[0]:
        return True
    # unit-ness (STRUCTURAL): l-side values C_x, S_x are p-units (pi divides
    # one conjugate power, never both); w-side values U_y, V_y are q-units.
    # A p-power dividing a w-side value is CONTENT (a lever), never assumed.
    if (a == "p" and b[0] in "CS") or (b == "p" and a[0] in "CS"):
        return True
    if (a == "q" and b[0] in "UV") or (b == "q" and a[0] in "UV"):
        return True
    if {a, b} == {"p", "q"}:
        return True
    return False


def _atoms(factors):
    out = {}
    for f in factors:
        if f.is_number:
            out["const"] = out.get("const", 1) * int(f)
            continue
        base, e = (f.base, int(f.exp)) if f.is_Pow else (f, 1)
        out[base] = out.get(base, 0) + e
    return out


def _binomial_facts(binom, facts):
    """Coprimality facts for a polynomial atom:  gcd(aX + bY, X) =
    gcd(bY, X); and mod a prime P dividing one of two terms it is the
    other term."""
    for s in binom.free_symbols:
        rest = _sp.expand(binom.subs(s, 0))
        if rest == 0:
            continue
        rat = _atoms(_sp.Mul.make_args(_sp.factor(rest)))
        ok = True
        for a in rat:
            if a == "const":
                if abs(rat[a]) % 2 == 0 and str(s)[0] not in "UC":
                    ok = False              # only U, C are known odd
                continue
            if not _coprime(a, s, facts):
                ok = False
        if ok:
            facts.add((binom, s))
    parts = _sp.Add.make_args(binom)
    if len(parts) == 2:
        for P_ in (_P, _Q):
            has = [P_ in t.free_symbols for t in parts]
            if has.count(True) == 1:
                other = parts[has.index(False)]
                oat = _atoms(_sp.Mul.make_args(_sp.factor(other)))
                if all(_coprime(a, P_, facts) for a in oat if a != "const"):
                    facts.add((binom, P_))


def _closure(Lat, Rat, facts):
    """Per-atom divisibilities and the closure lemma, exactly:
    X | P^e Y  (Y the only non-coprime atom besides the prime, exponent 1),
    Y | X  (X the only atom on the other side not coprime to Y),
    P^e | X  (X the only atom not coprime to P),  gcd(P, Y) = 1
        ==>  X = +-P^e Y.   Without a prime:  X | Y and Y | X  ==>  X = +-Y."""
    divs = {}
    for side, other in ((Lat, Rat), (Rat, Lat)):
        for A, e in side.items():
            if A == "const":
                continue
            divs[A] = ({B: f for B, f in other.items()
                        if B != "const" and not _coprime(A, B, facts)}, e)
    eqs = []
    for X, (tgt, e) in divs.items():
        if e != 1 or X in (_P, _Q):
            continue
        Ps = {B: f for B, f in tgt.items() if B in (_P, _Q)}
        Ys = {B: f for B, f in tgt.items() if B not in (_P, _Q)}
        if len(Ys) != 1 or len(Ps) > 1:
            continue
        (Y, fy), = Ys.items()
        if fy != 1:
            continue
        backY, eY = divs.get(Y, ({}, 0))
        if eY != 1 or set(backY) != {X}:
            continue
        if Ps:
            (P_, pe), = Ps.items()
            backP, _ = divs.get(P_, ({}, 0))
            if set(backP) != {X} or not _coprime(P_, Y, facts):
                continue
            eqs.append((X, P_**pe * Y))
        else:
            eqs.append((X, Y))
    return divs, eqs


def _pyth_subs(expr):
    """The Pythagorean rewrites available for the symbols in expr:
    U_y^2 -> q^{2y} - V_y^2 etc.  Yields (label, rewritten expr)."""
    yield "id", expr
    for sy in sorted(expr.free_symbols, key=str):
        nm = str(sy)
        if nm[0] not in "UVCS":
            continue
        n = int(nm[1:])
        if nm[0] == "U":
            other, norm = _sp.Symbol(f"V{n}"), _Q**(2 * n)
        elif nm[0] == "V":
            other, norm = _sp.Symbol(f"U{n}"), _Q**(2 * n)
        elif nm[0] == "C":
            other, norm = _sp.Symbol(f"S{n}"), _P**(2 * n)
        else:
            other, norm = _sp.Symbol(f"C{n}"), _P**(2 * n)
        if _sp.degree(expr, sy) >= 2:
            yield f"{nm}^2->", _sp.expand(expr.subs(sy**2, norm - other**2))


def chase(expr, max_terms=6):
    """The divisibility chase on a Lucas equation with up to max_terms
    terms.  Every split of the terms into two sides is tried (after each
    available Pythagorean rewrite); each side is factored into atoms
    (symbols, p, q, polynomial factors), kept only if each side carries at
    most one polynomial atom; divisibilities follow from the coprimality
    oracle and close into equalities X = +-P^e Y (the coincidences);
    each equality is substituted back to give the residual equation.
    Returns the list of (product form, equalities, residuals)."""
    from itertools import combinations
    expr = _sp.expand(expr)
    base_terms = list(_sp.Add.make_args(expr))
    if len(base_terms) > max_terms:
        return {"status": f"{len(base_terms)}-terms", "results": []}
    results = []
    seen = set()
    for label, e2 in _pyth_subs(expr):
        terms = list(_sp.Add.make_args(_sp.expand(e2)))
        n = len(terms)
        if n < 2 or n > max_terms:
            continue
        idx = list(range(n))
        for k in range(1, n // 2 + 1):
            for GL in combinations(idx, k):
                if k * 2 == n and 0 not in GL:
                    continue                      # complementary duplicate
                GR = [j for j in idx if j not in GL]
                left = sum(terms[i] for i in GL)
                right = -sum(terms[j] for j in GR)
                FL, FR = _sp.factor(left), _sp.factor(right)
                Lat, Rat = _atoms(_sp.Mul.make_args(FL)), _atoms(_sp.Mul.make_args(FR))
                polys = [A for A in list(Lat) + list(Rat) if A != "const" and not A.is_Symbol]
                if len(polys) > 2 or any(len(_sp.Add.make_args(A)) > 3 for A in polys):
                    continue
                key = (label, tuple(sorted(str(a) for a in Lat)), tuple(sorted(str(a) for a in Rat)))
                if key in seen:
                    continue
                seen.add(key)
                facts = set()
                for A in list(Lat) + list(Rat):
                    if A != "const" and not A.is_Symbol:
                        _binomial_facts(A, facts)
                divs, eqs = _closure(Lat, Rat, facts)
                if not eqs:
                    continue
                residuals = []
                for X, val in eqs:
                    for sgn in (1, -1):
                        res = _sp.factor(_sp.expand(e2.subs(X, sgn * val)))
                        residuals.append((X, sgn, val, res))
                results.append({"rewrite": label, "L": Lat, "R": Rat, "facts": facts,
                                "divs": divs, "equalities": eqs, "residuals": residuals})
    return {"status": "product-form" if results else "no-equality", "results": results}


def all_collapses(pattern):
    """The collapse identity for EVERY pair of terms (all three hold),
    with the lever bookkeeping relative to that pair.  Returns a list of
    detail dicts in the format of extract()['detail'][0]."""
    terms = cleared_terms(pattern)
    if len(terms) != 3:
        return []
    out = []
    for a, b in ((0, 1), (0, 2), (1, 2)):
        c = ({0, 1, 2} - {a, b}).pop()
        col = find_collapse(terms[a], terms[b])
        if col is None:
            continue
        s, ap, bq, k1, D, k2, M = col
        cc, wpc, wqc, ec, Pc = terms[c]
        ep, eq = wpc - ap, wqc - bq
        absorb = {}
        dead = False
        for P, e, pure in (("p", ep, is_pure_w), ("q", eq, is_pure_l)):
            if e > 0:
                fac = [f for f in (("D", D, k1) if pure(D) else None,
                                   ("M", M, k2) if pure(M) else None) if f]
                if not fac:
                    dead = True
                absorb[P] = ("product", 2 * e, fac)
            elif e < 0:
                if not pure(ec):
                    dead = True
                absorb[P] = ("third", -2 * e, ("C", ec, "Im"))
        out.append({"pair": (a, b), "third": c, "sign": s, "kinds": (k1, k2),
                    "D": D, "M": M, "C": ec, "coeff_c": cc, "absorb": absorb,
                    "dead": dead})
    return out


def classify_equality(X, val):
    """'parity-dead' (odd = even), 'unit-collapse' (X = +-P^e),
    'coincidence-weighted' (X = +-P^e Y), 'coincidence' (X = +-Y),
    or 'rearrangement' (polynomial right-hand side)."""
    def parity(sym):
        n = str(sym)
        return "odd" if n[0] in "UC" else ("even" if n[0] in "VS" else None)
    if not X.is_Symbol:
        return "rearrangement"
    if _sp.expand(val - X) == 0 or _sp.expand(val + X) == 0:
        return "trivial"
    f = _sp.factor(val)
    at = _atoms(_sp.Mul.make_args(f))
    syms = [A for A in at if A != "const" and A not in (_P, _Q)]
    if any(not A.is_Symbol for A in syms):
        return "rearrangement"
    pw = [A for A in at if A in (_P, _Q)]
    if not syms:
        return "unit-collapse"
    if len(syms) == 1:
        Y = syms[0]
        px, py = parity(X), parity(Y)
        if px and py and px != py:
            return "parity-dead"
        return "coincidence-weighted" if pw else "coincidence"
    return "rearrangement"


def _parity_poly(expr):
    """Parity of a polynomial in Lucas symbols and p, q: 'odd' (hence
    nonzero), 'even', or None (undetermined).  U, C, p, q are odd; V, S
    are even; a monomial is odd iff its coefficient is odd and it has no
    V/S factor."""
    expr = _sp.expand(expr)
    odd_count = 0
    for term in _sp.Add.make_args(expr):
        coeff, rest = term.as_coeff_Mul()
        if not coeff.is_integer:
            return None
        if int(coeff) % 2 == 0:
            continue
        has_even = any(str(s)[0] in "VS" for s in rest.free_symbols)
        if not has_even:
            odd_count += 1
    return "odd" if odd_count % 2 == 1 else "even"


def factor_nonzero(f):
    """True if the factor f is provably nonzero: a Lucas symbol (values of
    primitive Gaussian powers never vanish), p, q, a nonzero constant,
    or a polynomial that is odd (hence not 0)."""
    if f.is_number:
        return f != 0
    if f.is_Symbol:
        return True
    return _parity_poly(f) == "odd"


def residual_branches(pattern, coincidences, equations, max_terms=6):
    """For each coincidence X = +-val and each sign, substitute into every
    collapse equation and factor: the branch is DEAD if some equation's
    residual has all factors provably nonzero.  Returns
    {(X, val): {+1: 'dead'|'open', -1: ...}} and the open residuals."""
    out, open_res = {}, {}
    for (X, val) in coincidences:
        if not X.is_Symbol:
            continue
        out[(X, val)] = {}
        for sgn in (1, -1):
            dead = False
            res_list = []
            for e in equations:
                if X not in e.free_symbols:
                    continue
                r = _sp.expand(e.subs(X, sgn * val))
                if r == 0:
                    continue
                fac = _sp.factor(r)
                factors = [f for f in _sp.Mul.make_args(fac)]
                bases = [(f.base if f.is_Pow else f) for f in factors]
                if all(factor_nonzero(b) for b in bases):
                    dead = True
                    break
                res_list.append(fac)
            out[(X, val)][sgn] = "dead" if dead else "open"
            if not dead:
                open_res[(X, val, sgn)] = res_list
    return out, open_res


def run_chase(pattern, max_terms=6):
    """Extract every collapse of the pattern, build each Lucas equation
    (verified against the cleared relation), chase each, and union the
    equalities.  Returns dict: verified count, equalities by class."""
    from collections import Counter
    eqs = {}
    nver = 0
    equations = []
    for d in all_collapses(pattern):
        if d["dead"]:
            return {"status": "DEAD-no-pure-factor", "equalities": {}, "classes": Counter()}
        red, y0, x0, ep, eq, ok = endpoint_identity(pattern, d)
        if not ok:
            continue
        nver += 1
        equations.append(red)
        r = chase(red, max_terms=max_terms)
        for res in r["results"]:
            for X, val in res["equalities"]:
                eqs[(X, val)] = classify_equality(X, val)
    # depth-1 substitution: each derived equality (both signs) into the
    # OTHER collapse equations, then chase again (the hand-proofs'
    # "substitute and re-derive")
    for (X, val), cls in list(eqs.items()):
        if not X.is_Symbol:
            continue
        for sgn in (1, -1):
            for e2 in equations:
                if X not in e2.free_symbols:
                    continue
                e3 = _sp.expand(e2.subs(X, sgn * val))
                if e3 == 0:
                    continue
                r = chase(e3, max_terms=max_terms)
                for res in r["results"]:
                    for X2, val2 in res["equalities"]:
                        if (X2, val2) not in eqs:
                            eqs[(X2, val2)] = classify_equality(X2, val2)
    eqs = {k: v for k, v in eqs.items() if v != "trivial"}
    classes = Counter(eqs.values())
    coincidences = [k for k, v in eqs.items() if v.startswith("coincidence")]
    branches, open_res = residual_branches(pattern, coincidences, equations, max_terms) if coincidences else ({}, {})
    residual_dead = any(all(b[s] == "dead" for s in (1, -1)) for b in branches.values())
    if "parity-dead" in classes:
        status = "DEAD-parity"
    elif residual_dead:
        status = "DEAD-residual"
    elif "unit-collapse" in classes:
        status = "UNIT-COLLAPSE"
    elif coincidences:
        status = "COINCIDENCE"
    elif eqs:
        status = "REARRANGEMENT-ONLY"
    else:
        status = "NO-EQUALITY"
    return {"status": status, "verified": nver, "equalities": eqs, "classes": classes,
            "branches": branches, "open_residuals": open_res}


# ------------------------------------------------- the valuation layer
#
# Every collapse identity is an equality of PRODUCTS,
#     2 p^{2ap} q^{2bq} Trig1(D) Trig2(M) = -c p^{2wpc} q^{2wqc} Im(C),
# so the p-adic and q-adic valuations balance term by term.  Mixed
# monomials are units at both primes; a pure-l monomial is a p-unit and
# a pure-w one a q-unit; and the q-adic valuations of ALL the l-side
# Lucas values are governed by one unknown, the rank of apparition
# r = ord(l/lbar mod rho) (a divisor of q-1), through the lifting-the-
# exponent lemma:
#     v_q(S_n) = v0 + v_q(n/r)      if r | n,  else 0,
#     v_q(C_n) = v0 + v_q(2n/r)     if r | 2n and r !| n,  else 0,
# with v0 = v_q(S_r) >= 1 (S_n = Im l^n, C_n = Re l^n); likewise the
# w-side at p with (r', v0').  The finitely many (r, r') cases give
# linear systems in (v0, v0'); no solution = DEAD by valuation.

def _vsmall(k, P):
    """v_P(k) for a small positive integer k and a specific prime P, or 0
    for a 'generic' prime (P larger than every exponent in play)."""
    if P is None or k <= 0:
        return 0
    v = 0
    while k % P == 0:
        k //= P
        v += 1
    return v


def _lucas_val(kind, n, r, v0, P):
    """Valuation at the OTHER prime of Trig(l^n) with rank of apparition
    r (None = no divisibility at all), base valuation v0 (a symbol or
    int), and specific prime P (None = generic)."""
    if r is None:
        return 0
    n = abs(n)
    if kind == "Im":
        return v0 + _vsmall(n // r, P) if n % r == 0 else 0
    # Re: divisible iff r | 2n and r !| n
    if (2 * n) % r == 0 and n % r != 0:
        return v0 + _vsmall(2 * n // r, P)
    return 0


def collapse_products(pattern):
    """For each pair: (D, k1, M, k2, C, ap, bq, wpc, wqc) -- the product
    identity  +-2 p^{2ap} q^{2bq} T1(D) T2(M) = -c p^{2wpc} q^{2wqc} Im(C)."""
    terms = cleared_terms(pattern)
    out = []
    if len(terms) == 2:
        # doubled pattern: c_a p^.. q^.. Im(A) + c_b p^.. q^.. Im(B) = 0 is a
        # product equality already
        (ca, wpa, wqa, ea, _), (cb, wpb, wqb, eb, _) = terms
        out.append(("doubled", ea, "Im", None, None, eb, wpa, wqa, wpb, wqb))
        return out
    for a, b in ((0, 1), (0, 2), (1, 2)):
        c = ({0, 1, 2} - {a, b}).pop()
        col = find_collapse(terms[a], terms[b])
        if col is None:
            continue
        s, ap, bq, k1, D, k2, M = col
        cc, wpc, wqc, ec, _ = terms[c]
        out.append(("triple", D, k1, M, k2, ec, ap, bq, wpc, wqc))
    return out


def valuation_layer(pattern, max_r=None, specific=(5, 7, 11, 13, 17, 19, 23)):
    """The valuation balance over all (rank, prime-case) configurations.
    Returns {'status': 'DEAD-valuation' | 'SURVIVES', 'survivors': [...]}
    where each survivor is (r_q, q_case, r_p, p_case, v0q, v0p)."""
    prods = collapse_products(pattern)
    if not prods:
        return {"status": "NO-COLLAPSE", "survivors": []}
    exps_l = {abs(m[0]) for pr in prods for m in (pr[1], pr[3], pr[5]) if m is not None and m[0]}
    exps_w = {abs(m[1]) for pr in prods for m in (pr[1], pr[3], pr[5]) if m is not None and m[1]}
    NL = 2 * max(exps_l) if exps_l else 1
    NW = 2 * max(exps_w) if exps_w else 1
    if max_r:
        NL, NW = min(NL, max_r), min(NW, max_r)
    v0q, v0p = _sp.symbols("v0q v0p")

    def val(m, kind, side, r, v0, P):
        """valuation of Trig(monomial m) at prime 'side' ('p' or 'q')."""
        x, y = m
        if side == "p":
            if x != 0:
                return 0                       # involves l: p-unit
            return _lucas_val(kind, y, r, v0, P)
        if y != 0:
            return 0                           # involves w: q-unit
        return _lucas_val(kind, x, r, v0, P)

    survivors = []
    r_cases_l = [None] + list(range(1, NL + 1))
    r_cases_w = [None] + list(range(1, NW + 1))
    q_cases = [None] + [P for P in specific if P <= NL]
    p_cases = [None] + [P for P in specific if P <= NW]
    for rq in r_cases_l:
        for qc in q_cases:
            if rq is not None and qc is not None and (qc - 1) % rq:
                continue                       # r | q - 1
            for rp in r_cases_w:
                for pc in p_cases:
                    if rp is not None and pc is not None and (pc - 1) % rp:
                        continue
                    if qc is not None and pc is not None and qc == pc:
                        continue
                    eqs = []
                    for pr in prods:
                        kind_, D, k1, M, k2, C, ap, bq, wpc, wqc = pr
                        for side, r, v0, P, wl, wr in (("p", rp, v0p, pc, ap, wpc),
                                                       ("q", rq, v0q, qc, bq, wqc)):
                            if kind_ == "doubled":
                                lhs = 2 * wl + val(D, "Im", side, r, v0, P)
                                rhs = 2 * wr + val(C, "Im", side, r, v0, P)
                            else:
                                lhs = 2 * wl + val(D, k1, side, r, v0, P) + val(M, k2, side, r, v0, P)
                                rhs = 2 * wr + val(C, "Im", side, r, v0, P)
                            eqs.append(_sp.expand(lhs - rhs))
                    unknowns = [u for u, r in ((v0q, rq), (v0p, rp)) if r is not None]
                    consts = [e for e in eqs if not e.free_symbols]
                    if any(c != 0 for c in consts):
                        continue
                    lin = [e for e in eqs if e.free_symbols]
                    if not lin:
                        survivors.append((rq, qc, rp, pc, None, None))
                        continue
                    sol = _sp.linsolve(lin, unknowns) if unknowns else None
                    if sol is None or sol == _sp.S.EmptySet:
                        continue
                    ok_sol = None
                    for s in sol:
                        vals = dict(zip(unknowns, s))
                        good = True
                        for u in unknowns:
                            v = vals[u]
                            if v.free_symbols:
                                continue               # free: unconstrained (>= 1 possible)
                            if not (v.is_integer and v >= 1):
                                good = False
                        if good:
                            ok_sol = vals
                    if ok_sol is None:
                        continue
                    survivors.append((rq, qc, rp, pc,
                                      ok_sol.get(v0q) if rq is not None else None,
                                      ok_sol.get(v0p) if rp is not None else None))
    return {"status": "SURVIVES" if survivors else "DEAD-valuation", "survivors": survivors}


def box_classes(a, b):
    return [(j, k) for j in range(0, a + 1) for k in range(-b, b + 1)
            if (j, k) != (0, 0) and (j > 0 or k > 0)]


def survey_box(a, b, mods=(16, 32, 64, 9, 5, 7, 11, 13, 8, 3)):
    """The engine's general layers (valuation -> tan-half factorization ->
    congruence) with the complete enumeration and canon_full dedup.
    Returns (verdict counts, list of OPEN (pattern, kind))."""
    from collections import Counter
    from compute.two_prime_additive import (
        candidates_for_box, enumerate_patterns_complete, canon_full,
        valuation_pruned, relation_poly, peel_general, is_constant,
        residual_cs_form, congruence_kill)
    cls = box_classes(a, b)
    cands = candidates_for_box(a, b)
    seen, verdict, opens = set(), Counter(), []
    for pattern, kind in enumerate_patterns_complete(cls):
        key = canon_full(pattern)
        if key in seen:
            continue
        seen.add(key)
        if valuation_pruned(pattern):
            verdict["VALUATION"] += 1
            continue
        N = relation_poly(pattern)
        if not N:
            verdict["ZERO"] += 1
            continue
        factors, residual = peel_general(N, cands)
        if is_constant(residual):
            verdict["FACTORED"] += 1
            continue
        G = residual_cs_form(residual)
        if any(congruence_kill(G, M) for M in mods):
            verdict["CONGRUENCE"] += 1
            continue
        verdict["OPEN"] += 1
        opens.append((pattern, kind))
    return verdict, opens


def shape(m):
    return "w" if is_pure_w(m) else ("l" if is_pure_l(m) else "mixed")


def type_census(opens):
    """Run the extractor on the distinct OPEN patterns; returns
    (status counts, family signature counts, shape-type counts)."""
    from collections import Counter
    st, fams, types = Counter(), Counter(), Counter()
    for pattern, kind in opens:
        if kind != "distinct":
            continue
        r = extract(tuple(pattern))
        st[r["status"]] += 1
        if r["status"] != "ENDPOINT":
            continue
        d = r["detail"][0]
        fams[endpoint_signature(r)] += 1
        types[(shape(d["D"]), shape(d["M"]), shape(d["C"]),
               tuple(sorted(d["absorb"])))] += 1
    return st, fams, types


def endpoint_signature(r):
    """A hashable family signature for an ENDPOINT record."""
    d = r["detail"][0]
    ab = tuple(sorted((P, v[0], v[1], tuple(f[0] for f in v[2]) if v[0] == "product" else v[2][0])
                      for P, v in d["absorb"].items()))
    return (d["kinds"], d["D"], d["M"], d["C"], ab)
