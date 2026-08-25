"""Mechanical verification for docs/foundations/F4-congruences-mod-72.md."""

from math import gcd

from ..framework import check, require
from ..targets import AB1, AB1_LUCAS, congrua, proper_decompositions

DOC = "docs/foundations/F4-congruences-mod-72.md"


def small_primes(bound):
    sieve = bytearray([1]) * (bound + 1)
    sieve[0:2] = b"\x00\x00"
    for i in range(2, int(bound ** 0.5) + 1):
        if sieve[i]:
            sieve[i * i:: i] = bytearray(len(sieve[i * i:: i]))
    return [i for i in range(bound + 1) if sieve[i]]


@check("f4.mod72", DOC)
def _(ctx):
    """Complete enumeration proving F4.1's finite core: every
    (c,u,v) in (Z/72)^3 whose nine Lucas entries are squares mod 72,
    excluding the all-entries-div-4 and all-entries-div-9 shadows of
    imprimitivity, has all entries == 1 (mod 24) and 3c == 3 (mod 72)."""
    squares72 = {x * x % 72 for x in range(72)}
    survivors = 0
    for c in range(72):
        for u in range(72):
            for v in range(72):
                entries = [c % 72, (c + u) % 72, (c - u) % 72,
                           (c + v) % 72, (c - v) % 72,
                           (c + u + v) % 72, (c - u - v) % 72,
                           (c + u - v) % 72, (c - u + v) % 72]
                if any(e not in squares72 for e in entries):
                    continue
                if all(e % 4 == 0 for e in entries):
                    continue
                if all(e % 9 == 0 for e in entries):
                    continue
                survivors += 1
                for e in entries:
                    require(e % 24 == 1, f"survivor (c,u,v)=({c},{u},{v}) entry {e}")
                require((3 * c) % 72 == 3, f"survivor c={c} has 3c != 3 mod 72")
    require(survivors > 0, "enumeration found no admissible residue triples")
    ctx.note(f"{survivors} admissible residue triples, all == 1 (mod 24)")


@check("f4.ap_prime_lemma", DOC)
def _(ctx):
    """F4.2(1) at the AP level, against data: for every 3-AP of squares
    (p^2, m^2, q^2), every prime l == 3,5 (mod 8) dividing p*q divides m."""
    bound = ctx.bound(full=800, fast=200)
    for m in range(1, bound + 1):
        for (e, f) in proper_decompositions(m):
            for root in (f - e, f + e):
                n = root
                l = 3
                while l * l <= n:
                    if n % l == 0:
                        while n % l == 0:
                            n //= l
                        if l % 8 in (3, 5):
                            require(m % l == 0, f"l={l} | {root}, l does not | m={m}")
                    l += 2
                if n > 1 and n % 8 in (3, 5):
                    require(m % n == 0, f"l={n} | {root}, l does not | m={m}")
    ctx.note("every 3,5 (mod 8) prime of an AP endpoint divides the center root")


@check("f4.qr_criteria", DOC)
def _(ctx):
    """The three QR criteria against Euler's criterion, all odd primes <= bound:
    -1 QR iff l==1 (4); 2 QR iff l==+-1 (8); -2 QR iff l==1,3 (8)."""
    bound = ctx.bound(full=10000, fast=2000)
    for l in small_primes(bound):
        if l == 2:
            continue
        e = (l - 1) // 2
        qr_m1 = pow(l - 1, e, l) == 1
        qr_2 = pow(2, e, l) == 1
        qr_m2 = pow(l - 2, e, l) == 1
        require(qr_m1 == (l % 4 == 1), f"-1 criterion at {l}")
        require(qr_2 == (l % 8 in (1, 7)), f"2 criterion at {l}")
        require(qr_m2 == (l % 8 in (1, 3)), f"-2 criterion at {l}")


@check("f4.offsets_24", DOC)
def _(ctx):
    """Corollary: congrua of odd m are == 0 (mod 24)."""
    bound = ctx.bound(full=1500, fast=400)
    for m in range(1, bound + 1, 2):
        for d in congrua(m):
            require(d % 24 == 0, f"congruum {d} of odd m={m} not divisible by 24")


@check("f4.ab1_consistency", DOC)
def _(ctx):
    """AB1 sits in the F4.1 residue class: all nine entries == 1 (mod 24),
    all four offsets == 0 (mod 24), magic sum == 3 (mod 72)."""
    require(all(x % 24 == 1 for x in AB1), "AB1 entry residue")
    u, v = AB1_LUCAS["u"], AB1_LUCAS["v"]
    require(all(w % 24 == 0 for w in (u, v, u + v, u - v)), "AB1 offset residue")
    require(sum(AB1[:3]) % 72 == 3, "AB1 magic sum residue")
