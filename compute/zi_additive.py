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


# ---------------------------------------------------------------------------
# A3-S1b: the degenerate-subsum classification, and
# A3-S2 (omega = 1): the single-split-prime theorem
# ---------------------------------------------------------------------------

def gaussian_prime_over(p):
    """(e, f) with e^2 + f^2 = p, e > f > 0 (p = 1 mod 4)."""
    for f in range(1, p):
        if 2 * f * f >= p:
            break
        e2 = p - f * f
        e = int(e2 ** 0.5)
        while e * e < e2:
            e += 1
        if e * e == e2:
            return (e, f)
    raise ValueError(f"{p} is not a split prime")


def _gmul(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def _gpow(a, n):
    r = (1, 0)
    for _ in range(n):
        r = _gmul(r, a)
    return r


def split_structure(m):
    """(twos, inert_part, [(p, a) split primes]) with
    m = 2^twos * inert_part * prod p^a; inert primes are = 3 mod 4."""
    twos = 0
    while m % 2 == 0:
        m //= 2
        twos += 1
    inert, split = 1, []
    d = 3
    while d * d <= m:
        if m % d == 0:
            a = 0
            while m % d == 0:
                m //= d
                a += 1
            if d % 4 == 1:
                split.append((d, a))
            else:
                inert *= d ** a
        d += 2
    if m > 1:
        if m % 4 == 1:
            split.append((m, 1))
        else:
            inert *= m
    return twos, inert, split


def omega1_D_predicted(m):
    """For single-split m = 2^s r p^a: the predicted congrua set
    { m^2 |Im sigma^k| : 1 <= k <= a } with sigma = lambda^4 / p^2,
    computed exactly: d_k = (m/p^k)^2 * |Im(lambda^{4k})| / p^{2k} *
    p^{2k} ... concretely d_k = 4^s r^2 p^{2a-2k} |Im(lambda^{4k})|."""
    s, r, split = split_structure(m)
    if len(split) != 1:
        raise ValueError("not single-split")
    p, a = split[0]
    lam = gaussian_prime_over(p)
    out = set()
    for k in range(1, a + 1):
        l4k = _gpow(lam, 4 * k)
        d = (4 ** s) * (r * r) * (p ** (2 * (a - k))) * abs(l4k[1])
        if d:
            out.add(d)
    return out


def omega1_relation_scan(p, amax):
    """Exact instance verification of the omega = 1 theorem: for all
    1 <= k1 <= k2 <= k3 <= amax (not all equal in the cancelling way)
    and all sign patterns, the six-term sum
    sum eps_j (sigma^{k_j} - sigma^{-k_j}) is NONZERO — evaluated
    exactly in Z[i] after multiplying by p^{2 k3}.  Returns the number
    of (k, eps) instances checked (all nonzero) — raises on a zero."""
    lam = gaussian_prime_over(p)
    lam4 = _gpow(lam, 4)
    lam4c = (lam4[0], -lam4[1])
    pows = {k: _gpow(lam4, k) for k in range(0, amax + 1)}
    powsc = {k: (pows[k][0], -pows[k][1]) for k in pows}
    checked = 0
    for k3 in range(1, amax + 1):
        for k2 in range(1, k3 + 1):
            for k1 in range(1, k2 + 1):
                for eps in ((1, 1, -1), (1, -1, 1), (-1, 1, 1),
                            (1, 1, 1)):
                    tot_im = 0
                    for e, k in zip(eps, (k1, k2, k3)):
                        scale = p ** (2 * (k3 - k))
                        # p^{2k3}(sigma^k - sigma^{-k})
                        #   = p^{2(k3-k)} (lam^{4k} - conj)
                        tot_im += e * scale * (pows[k][1] - powsc[k][1])
                    # relation eps1 d1 + eps2 d2 + eps3 d3 = 0 with
                    # d_k proportional to |Im sigma^k| > 0: a zero of
                    # tot_im for SOME sign pattern is the relation;
                    # positivity kills (1,1,1) trivially but we assert
                    # nonvanishing anyway (the theorem is signed)
                    if tot_im == 0:
                        raise AssertionError((p, (k1, k2, k3), eps))
                    checked += 1
    return checked


def subsum_scan(m, max_points=8):
    """Enumerate vanishing proper subsums of the six-term sum over
    ordered point triples (repeats allowed) and all eps patterns.
    Returns (n_configs, n_vanishing, classifications) where every
    vanishing subsum must classify as size 2 or 4 with paired equal
    |Im| values (the degenerate lemma)."""
    pts = circle_squares(m)[:max_points]
    n_cfg = n_van = 0
    bad = []
    m4 = m ** 4
    for wi, di in pts:
        for wj, dj in pts:
            for wk, dk in pts:
                ws = (wi, wj, wk)
                ds = (di, dj, dk)
                for eps in ((1, 1, -1), (1, -1, 1), (-1, 1, 1),
                            (1, 1, 1)):
                    n_cfg += 1
                    # the six terms, exactly, common denom w1 w2 w3:
                    # term_j = eps_j w_j ; term_{j+3} = -eps_j conj w_j
                    terms = []
                    for e, w in zip(eps, ws):
                        terms.append((e * w[0], e * w[1]))
                    for e, w in zip(eps, ws):
                        terms.append((-e * w[0], e * w[1]))
                    for mask in range(1, 63):
                        tot = (0, 0)
                        size = 0
                        dvals = []
                        for b in range(6):
                            if mask >> b & 1:
                                tot = (tot[0] + terms[b][0],
                                       tot[1] + terms[b][1])
                                size += 1
                                dvals.append(ds[b % 3])
                        if tot == (0, 0):
                            n_van += 1
                            ok = size in (2, 4) and \
                                sorted(dvals)[:size // 2] == \
                                sorted(dvals)[size // 2:]
                            if not ok:
                                bad.append((m, ds, eps, mask, size))
    return n_cfg, n_van, bad
