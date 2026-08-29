"""A3-S1: the Z[i] reformulation of the additive layer (ROADMAP W10).

D(m) is exactly the set of nonzero |Im(z^2)| over Gaussian integers z
of norm m^2 (z = e + if with e^2 + f^2 = m^2 gives Im(z^2) = 2ef —
definitional, but pinned both ways against congrua_sets).  Writing
w_j = z_j^2, every w_j lies on the circle |w| = m^2, so its conjugate
is bar(w_j) = m^4 / w_j, and a signed additive triple
eps_1 d_1 + eps_2 d_2 + eps_3 d_3 = 0 (d_j = Im w_j after orienting
Im w_j > 0) is equivalent to

    eps_1 w_1 + eps_2 w_2 + eps_3 w_3  being REAL,

i.e. to the six-term vanishing sum

    sum_j eps_j (w_j - m^4 / w_j) = 0,

an S-unit-equation-shaped condition on the norm-m^4 torus of Q(i).
Multiplying by w_1 w_2 w_3 keeps everything in Z[i]; the functions
below work exactly.

The additive desert (zero triples to 10^7) therefore says: this
six-term sum never vanishes nondegenerately on square points of the
torus.  W10's A3-S2 attacks small omega(m) unconditionally.
"""

from __future__ import annotations

from .congrua_search import congrua_sets


def circle_squares(m):
    """[(w, d)] with w = z^2 for z = e + if, e > f > 0, e^2 + f^2 =
    m^2; w as an exact pair (re, im), d = Im w = 2ef > 0."""
    out = []
    e = 1
    while 2 * e * e < m * m:
        f2 = m * m - e * e
        f = int(f2 ** 0.5)
        while f * f < f2:
            f += 1
        if f * f == f2 and f > e > 0:
            re, im = f * f - e * e, 2 * e * f  # (f + ie)^2, im > 0
            out.append(((re, im), im))
        e += 1
    return out


def D_from_zi(m):
    """The congrua of m via the Z[i] parametrization."""
    return {d for _, d in circle_squares(m)}


def six_term_is_zero(ws, eps, R):
    """Exact test of sum_j eps_j (w_j - R/w_j) = 0 in Q(i), where R
    is the common squared radius |w_j|^2 (R = m^4 in the congrua
    application): multiplied through by w_1 w_2 w_3 (nonzero), so
    everything stays in Z[i]."""
    def mul(a, b):
        return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])

    w1, w2, w3 = ws
    m4 = R
    for w in ws:
        # conj(w) * w == R  <=>  |w|^2 = R (the torus identity)
        assert w[0] * w[0] + w[1] * w[1] == m4, "point off the torus"
    w23, w13, w12 = mul(w2, w3), mul(w1, w3), mul(w1, w2)
    tot = (0, 0)
    for e, w, wother in zip(eps, ws, (w23, w13, w12)):
        # e * (w - m^4/w) * w1 w2 w3 = e * (w*wother*w/w ... ) —
        # concretely: (w - m^4/w) * (w1 w2 w3) = w^2 * wother/w * ...
        # simplest exact route: (w*w - (m4, 0)) * wother / w * ... is
        # fractional; instead use (w - m4/w)*w1w2w3 = (w*w - m4)*wother
        ww = mul(w, w)
        term = mul((ww[0] - m4, ww[1]), wother)
        tot = (tot[0] + e * term[0], tot[1] + e * term[1])
    return tot == (0, 0)


def triples_via_zi(m):
    """All signed additive triples of D(m), found through the
    six-term criterion (should be empty in the desert)."""
    pts = circle_squares(m)
    hits = []
    n = len(pts)
    for i in range(n):
        for j in range(i, n):
            for k in range(j, n):
                if len({i, j, k}) < 2:
                    continue
                ws = (pts[i][0], pts[j][0], pts[k][0])
                for eps in ((1, 1, -1), (1, -1, 1), (-1, 1, 1),
                            (1, -1, -1)):
                    if six_term_is_zero(ws, eps, m ** 4):
                        hits.append((pts[i][1], pts[j][1], pts[k][1],
                                     eps))
    return hits


def triples_direct(m):
    """Control: additive triples straight from D(m)."""
    D = sorted(D_from_zi(m))
    hits = []
    for i, d1 in enumerate(D):
        for d2 in D[i:]:
            if d1 + d2 in D:
                hits.append((d1, d2, d1 + d2))
    return hits
