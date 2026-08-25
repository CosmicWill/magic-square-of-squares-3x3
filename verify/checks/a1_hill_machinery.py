"""Mechanical verification for docs/attacks/A1-hill-audit.md."""

from math import gcd

from ..framework import check, require
from ..targets import EULER4, LINES_4, congrua, is_square

DOC = "docs/attacks/A1-hill-audit.md"


def odd_interval_sum(p, q):
    """Sum of the odd numbers from 2p+1 to 2q-1 (0 <= p < q)."""
    return sum(range(2 * p + 1, 2 * q, 2))


@check("a1.dictionary", DOC)
def _(ctx):
    """The odd-interval encoding: sum of odds in [2p+1, 2q-1] = q^2 - p^2;
    equal-sum consecutive pairs pivoting at m == congrua of m (the F2
    layer); Euler's 4x4 satisfies every line-level interval identity."""
    bound = ctx.bound(full=120, fast=50)
    for p in range(bound):
        for q in range(p + 1, bound):
            require(odd_interval_sum(p, q) == q * q - p * p, f"({p},{q})")
            # exact identities: (#terms) x (mean)
            require(q * q - p * p == (q - p) * (q + p))
    # equal-sum consecutive pairs at pivot m <-> congrua of m
    for m in range(1, ctx.bound(full=300, fast=80)):
        pairs = set()
        for p in range(m):
            d = m * m - p * p
            # partner interval [2m+1, 2q-1] with the same sum: q^2 = m^2 + d
            if is_square(m * m + d):
                pairs.add(d)
        require(pairs == congrua(m), f"pair set mismatch at m={m}")
    # Euler line-level identities: each line of squares is a disjoint union
    # of initial segments with the common total sum
    from math import isqrt
    for line in LINES_4:
        total = sum(EULER4[i] for i in line)
        require(total == sum(odd_interval_sum(0, isqrt(EULER4[i]))
                             for i in line))
        require(total == 8515)
    ctx.note("interval language == F2 layer; 4x4 satisfies line identities")


@check("a1.pseudo_solutions", DOC)
def _(ctx):
    """Theorem A1.1 witnesses: for several moduli N, explicit positive,
    distinct, ordered root tuples satisfying ALL MSS3 relations mod N (and
    all order constraints exactly) without being an MSS3."""
    for N in (72, 3 ** 5, 2 ** 20, 24 * 625):
        base = 1
        # roots: m and (p_i < m < q_i) all == 1 (mod lcm(N,24)), distinct
        L = N if N % 24 == 0 else N * 24 // gcd(N, 24)
        m = base + 40 * L
        ps = [base + k * L for k in (2, 5, 11, 17)]
        qs = [base + k * L for k in (57, 61, 71, 83)]
        roots = ps + [m] + qs
        require(len(set(roots)) == 9 and all(r > 0 for r in roots))
        require(all(ps[i] < m < qs[i] for i in range(4)), "order pattern")
        require(all(r % 24 == 1 for r in roots), "root congruence class")
        deltas = [q * q - m * m for q in qs]
        # all defining relations hold mod N:
        for p, q in zip(ps, qs):
            require((p * p + q * q - 2 * m * m) % N == 0, "AP relation mod N")
        require((deltas[2] - deltas[0] - deltas[1]) % N == 0, "sum relation")
        require((deltas[3] - (deltas[0] - deltas[1])) % N == 0, "diff relation")
        # ... and yet this is nowhere near an MSS3 (exact relations fail):
        exact = [p * p + q * q == 2 * m * m for p, q in zip(ps, qs)]
        require(not any(exact), "pseudo-solution accidentally exact")
    ctx.note("pseudo-solutions exist for every tested modulus => "
             "congruence+order endgames cannot prove nonexistence")
