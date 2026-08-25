"""Exhaustive search for magic squares of squares over F_q[t]
(docs/attacks/A2-function-field.md, section 5).

Method (complete by Prop. A2.1): every MSS3 over F_q[t] with nonconstant
entries has a nonconstant center root M, and its four offsets lie in the
congrua set D(M) = {2ef : e^2 + f^2 = M^2}.  So for each monic nonconstant
M up to a degree bound we compute D(M) and test whether it contains an
additive quadruple u, v, u+v, u-v obeying the F1.3 distinctness factors.

Congrua enumeration:
* q == 3 (mod 4): -1 is not a square, so e^2 + f^2 has no leading
  cancellation and deg e, deg f <= deg M — brute force over e.
* q == 1 (mod 4): i = sqrt(-1) lies in F_q, so e^2+f^2 = (e+if)(e-if)
  and decompositions correspond to divisor splittings M^2 = h * h' with
  e = (h+h')/2, f = (h-h')/(2i) — enumerate divisors of M^2.

Polynomials are coefficient tuples, low degree first, no trailing zeros.

Run:  python3 -m compute.ff_search
"""

from itertools import product

# ---------------------------------------------------------------------------
# F_q[t] arithmetic


def trim(c):
    c = list(c)
    while c and c[-1] == 0:
        c.pop()
    return tuple(c)


def deg(a):
    return len(a) - 1  # deg(0) = -1


def add(a, b, q):
    n = max(len(a), len(b))
    return trim([( (a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0) ) % q
                 for i in range(n)])


def neg(a, q):
    return tuple((-x) % q for x in a)


def sub(a, b, q):
    return add(a, neg(b, q), q)


def mul(a, b, q):
    if not a or not b:
        return ()
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                out[i + j] = (out[i + j] + x * y) % q
    return trim(out)


def scale(a, s, q):
    return trim([(x * s) % q for x in a])


def divmod_poly(a, b, q):
    assert b
    a = list(a)
    binv = pow(b[-1], q - 2, q)
    out = [0] * max(0, len(a) - len(b) + 1)
    while len(a) >= len(b) and trim(a):
        if len(a) < len(b):
            break
        c = (a[-1] * binv) % q
        k = len(a) - len(b)
        out[k] = c
        for i in range(len(b)):
            a[k + i] = (a[k + i] - c * b[i]) % q
        a = list(trim(a))
        if not a:
            break
    return trim(out), trim(a)


def gcd_poly(a, b, q):
    while b:
        a, b = b, divmod_poly(a, b, q)[1]
    return a


def monic_polys(q, d):
    """All monic polynomials of exact degree d."""
    for lower in product(range(q), repeat=d):
        yield trim(list(lower) + [1])


def all_polys(q, d):
    """All polynomials of degree <= d (including 0)."""
    for c in product(range(q), repeat=d + 1):
        yield trim(c)


def irreducibles(q, dmax):
    irr = []
    for d in range(1, dmax + 1):
        for f in monic_polys(q, d):
            if all(divmod_poly(f, g, q)[1] for g in irr if 2 * deg(g) <= d):
                irr.append(f)
    return irr


def factor_monic(M, q, irr):
    out = {}
    rest = M
    for g in irr:
        while True:
            quo, rem = divmod_poly(rest, g, q)
            if rem:
                break
            out[g] = out.get(g, 0) + 1
            rest = quo
        if deg(rest) == 0:
            break
    assert deg(rest) == 0 and rest == (1,), "incomplete factorization"
    return out


def monic_divisors(fact, q):
    divs = [(1,)]
    for g, e in fact.items():
        new = []
        p = (1,)
        for k in range(e + 1):
            for d0 in divs:
                new.append(mul(d0, p, q))
            p = mul(p, g, q)
        divs = new
    return divs


# ---------------------------------------------------------------------------
# congrua over F_q[t]


def sqrt_of_minus_one(q):
    for i in range(2, q):
        if (i * i + 1) % q == 0:
            return i
    return None


def congrua_ff(M, q, irr, squares=None):
    """D(M) = {2ef : e^2+f^2 = M^2, ef != 0}, closed under negation."""
    M2 = mul(M, M, q)
    D = set()
    if q % 4 == 3:
        # no cancellation possible: deg e, deg f <= deg M
        assert squares is not None
        for e in all_polys(q, deg(M)):
            if not e:
                continue
            f2 = sub(M2, mul(e, e, q), q)
            f = squares.get(f2)
            if f is not None and f:
                D.add(scale(mul(e, f, q), 2, q))
    else:
        i0 = sqrt_of_minus_one(q)
        inv2 = pow(2, q - 2, q)
        inv2i = pow((2 * i0) % q, q - 2, q)
        fact = factor_monic(M2, q, irr)
        for h in monic_divisors(fact, q):
            hprime = divmod_poly(M2, h, q)[0]
            for lam in range(1, q):
                hh = scale(h, lam, q)
                hp = scale(hprime, pow(lam, q - 2, q), q)
                e = scale(add(hh, hp, q), inv2, q)
                f = scale(sub(hh, hp, q), inv2i, q)
                if e and f:
                    D.add(scale(mul(e, f, q), 2, q))
    return D | {neg(d, q) for d in D}


def square_table(q, dmax):
    """{g^2: g} for deg g <= dmax (keeps one root per square)."""
    table = {}
    for g in all_polys(q, dmax):
        table.setdefault(mul(g, g, q), g)
    return table


# ---------------------------------------------------------------------------
# the search


def distinct_ok(u, v, q):
    """F1.3: u v (u-v)(u+v)(u-2v)(u+2v)(2u-v)(2u+v) != 0 in F_q[t]."""
    two = 2 % q
    vals = [u, v, sub(u, v, q), add(u, v, q),
            sub(u, scale(v, two, q), q), add(u, scale(v, two, q), q),
            sub(scale(u, two, q), v, q), add(scale(u, two, q), v, q)]
    return all(x for x in vals)


def search(q, dmax):
    """Yield (M, u, v) for every MSS3 with nonconstant monic center root M,
    deg M <= dmax.  Exhaustive for that range (Prop. A2.1)."""
    irr = irreducibles(q, dmax)
    squares = square_table(q, dmax) if q % 4 == 3 else None
    hits = []
    for d in range(1, dmax + 1):
        for M in monic_polys(q, d):
            D = congrua_ff(M, q, irr, squares)
            for u in D:
                for v in D:
                    if add(u, v, q) in D and sub(u, v, q) in D \
                            and distinct_ok(u, v, q):
                        hits.append((M, u, v))
    return hits


def main():
    for q, dmax in [(3, 3), (5, 3), (7, 2), (11, 2), (13, 2)]:
        hits = search(q, dmax)
        print(f"q={q:2d}, deg M <= {dmax}: "
              f"{'NO MSS3' if not hits else f'FOUND {hits[:3]} ...'}")


if __name__ == "__main__":
    main()
