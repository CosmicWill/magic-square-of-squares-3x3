"""Mechanical verification for docs/foundations/F5-local-solubility.md."""

from ..framework import check, require
from ..targets import (FP_EXCEPTIONS_BELOW_1000, FP_WITNESSES, LINES_3,
                       MOD2N_WITNESS, is_magic, lucas_entries)

DOC = "docs/foundations/F5-local-solubility.md"


def sqrt_mod_2n(a, n):
    assert a % 8 == 1
    x = 1
    for k in range(3, n):
        if (x * x - a) % (1 << (k + 1)) != 0:
            x += 1 << (k - 1)
    return x % (1 << n)


def hensel_sqrt(a, p, k):
    """x with x^2 == a mod p^k for odd p, given a is a nonzero QR mod p."""
    x = next(t for t in range(1, p) if (t * t - a) % p == 0)
    pk = p
    for _ in range(k - 1):
        # x_{new} = x + t*pk with t = (a - x^2)/pk * (2x)^{-1} mod p
        t = ((a - x * x) // pk) * pow(2 * x, p - 2, p) % p
        x += t * pk
        pk *= p
    assert (x * x - a) % pk == 0
    return x


@check("f5.bare_congruence", DOC)
def _(ctx):
    """F5.1: (c,u,v) = (1,0,0) solves the bare congruence system mod every n
    (spot-checked for all n <= bound, which suffices: the entries are all
    literally 1)."""
    bound = ctx.bound(full=500, fast=100)
    for n in range(2, bound + 1):
        sq = {x * x % n for x in range(n)}
        ents = lucas_entries(1, 0, 0, mod=n)
        require(all(e in sq for e in ents), f"n={n}")
        require(is_magic(lucas_entries(1, 0, 0), LINES_3))


@check("f5.zp_witness", DOC)
def _(ctx):
    """F5.2: for every odd prime p <= bound, the triple (1, p, 3p) has nine
    distinct entries, all squares mod p^5 (explicit Hensel roots verified);
    2-adically, (1, 8, 24) has entries == 1 (mod 8), roots verified mod 2^20."""
    bound = ctx.bound(full=300, fast=60)
    # distinctness product for (u0,v0)=(1,3): u v (u-v)(u+v)(u-2v)(u+2v)(2u-v)(2u+v)
    u0, v0 = 1, 3
    prod = (u0 * v0 * (u0 - v0) * (u0 + v0) * (u0 - 2 * v0) * (u0 + 2 * v0)
            * (2 * u0 - v0) * (2 * u0 + v0))
    require(prod != 0)
    p = 3
    while p <= bound:
        if all(p % q for q in range(2, int(p ** 0.5) + 1)):
            ents = lucas_entries(1, p * u0, p * v0)
            require(len(set(ents)) == 9)
            p5 = p ** 5
            for e in ents:
                x = hensel_sqrt(e % p5, p, 5)
                require((x * x - e) % p5 == 0, f"root failed p={p}")
        p += 2
    ents = lucas_entries(1, 8, 24)
    require(len(set(ents)) == 9)
    for e in ents:
        require(e % 8 == 1)
        x = sqrt_mod_2n(e % (1 << 20), 20)
        require((x * x - e) % (1 << 20) == 0)
    ctx.note("Z_p witnesses verified to p^5, Z_2 witness to 2^20")


@check("f5.fp_scan", DOC)
def _(ctx):
    """F5.3: recompute which primes p < bound admit a magic square of nine
    distinct nonzero squares over F_p (WLOG c = 1), and compare with the
    stored exceptional list."""
    bound = ctx.bound(full=1000, fast=130)

    def admits(p):
        qr = bytearray(p)
        for x in range(1, p):
            qr[x * x % p] = 1
        for u in range(1, p):
            if not (qr[(1 + u) % p] and qr[(1 - u) % p]):
                continue
            for v in range(1, p):
                e = lucas_entries(1, u, v, mod=p)
                if len(set(e)) == 9 and all(x and qr[x] for x in e):
                    return True
        return False

    exceptions = []
    for p in range(5, bound):
        if not all(p % q for q in range(2, int(p ** 0.5) + 1)):
            continue
        if not admits(p):
            exceptions.append(p)
    expected = [p for p in FP_EXCEPTIONS_BELOW_1000 if p < bound]
    require(exceptions == expected,
            f"exceptional primes {exceptions} != stored {expected}")
    # pinned witnesses really work:
    for p, (c, u, v) in FP_WITNESSES.items():
        qr = {x * x % p for x in range(1, p)}
        e = lucas_entries(c, u, v, mod=p)
        require(len(set(e)) == 9 and all(x in qr for x in e), f"witness p={p}")
        require(all(sum(e[i] for i in line) % p == (3 * c) % p
                    for line in LINES_3), f"witness p={p} not magic")
    ctx.note(f"exceptional primes below {bound}: {exceptions}")


@check("f5.mod2n", DOC)
def _(ctx):
    """F5.4: the stored mod-2^32 witness is genuine, and the deterministic
    generator reproduces it."""
    W = MOD2N_WITNESS
    mod = 1 << W["N"]
    ents = lucas_entries(W["c"], W["u"], W["v"], mod=mod)
    require(ents == W["entries"], "entries mismatch")
    require(len(set(ents)) == 9, "entries not distinct")
    for e, x in zip(W["entries"], W["roots"]):
        require((x * x - e) % mod == 0, "root fails")
        require(e % 8 == 1)
    from compute.mod2n_lift import C, U, V, sqrt_mod_2n as gen_sqrt
    require((C, U, V) == (W["c"], W["u"], W["v"]), "generator drifted")
    require(gen_sqrt(W["entries"][0]) == W["roots"][0], "generator root drifted")
