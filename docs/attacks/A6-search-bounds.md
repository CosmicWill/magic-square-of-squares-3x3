# A6 — Search bounds: what is verified, by whom, and how to push further

**Status:** the repository's own bounds **VERIFIED** (reproducible,
cross-validated by independent implementations); the literature bound
**CITED**; sieve design recorded; large-scale sieve left as an open
engineering task. Verification: `python3 -m verify --only a6`.

## 1. The bound ladder

| bound (on the MSS3 center $c = m^2$) | source | provenance |
|---|---|---|
| no MSS3 with $m \le 8{,}000$ | `compute/small_bound_search.py` — direct decomposition enumeration | first-party, VERIFIED, independent implementation |
| no MSS3 with $m \le 300{,}000$ (so $c \le 9\times10^{10}$, magic sum $\le 2.7\times10^{11}$) | the additive desert sweep, [A3.3](A3-simultaneous-congrua.md) — indeed not even *three* of the four APs can be realized | first-party, VERIFIED |
| no MSS3 (and no 8-square square) with $c \le 10^6$, center square or not | the taxonomy sweep, [A4](A4-eight-squares.md) | first-party, VERIFIED, third implementation |
| all entries of any MSS3 exceed $10^{14}$ | L. Morgenstern 2007, multimagie.com | CITED (SUMMARY-ONLY) |

The three first-party implementations use different enumeration
strategies (direct $e$-loops; the primitive-triple sieve; the
$\widetilde D(c)$ $q$-loops) and agree on their overlaps — that
cross-validation is checked mechanically (`a6.cross_validation`).

Note the *shape* of the first-party bounds: they exclude far more than
"no solution below the bound" — below $3\times10^5$ the additive
structure never even reaches three realized APs (A3.3), and below $10^6$
no center of any kind supports eight squares (A4). Any eventual solution
is not merely large; the entire additive mechanism it needs has no small
prototypes.

## 2. What a serious sieve would look like (design, for a future push)

The congruence layer ([F4](../foundations/F4-congruences-mod-72.md))
gives a clean wheel: in a primitive MSS3, all roots are $\equiv \pm 1
\pmod 6$ (coprime to 6), the center root $m$ satisfies the same, offsets
are $\equiv 0 \pmod{24}$ automatically, and $m$ must carry
$\prod_{p \equiv 1 (4)} (2a_p + 1) \ge 9$ ([F2.7](../foundations/F2-aps-and-pythagorean.md))
— so a sieve enumerates only $m$ divisible by two distinct primes
$\equiv 1 \pmod 4$ (or $p^4$), computes $D(m)$ by the Gaussian
factorization of $m$ (fast: factor $m$, multiply out the
$\prod(2a_i+1)$ decompositions), and tests additive closure with a hash
set — exactly `compute/congrua_search.py`'s inner loop, which does
$3\times10^5$ in ~40 s of pure Python. A compiled implementation (Rust/C,
$D(m)$ via factorization sieve) should reach $m \sim 10^8$–$10^9$ on a
single machine — i.e. centers $\sim 10^{16}$–$10^{18}$, beyond the cited
Morgenstern frontier, *and* would simultaneously push the A3.3 desert
and the class-E kill. **Open engineering task A6-T1** (deliberately not
attempted here: the mathematical program takes precedence, and a bound
alone cannot settle the problem — [F5](../foundations/F5-local-solubility.md)).

## 3. Honesty notes

- The Morgenstern $10^{14}$ entry bound could not be verified at source
  (fetch-blocked environment); we treat it as a search fact only and
  never build proofs on it.
- Our bounds are *center* bounds; the literature's are *entry* bounds.
  For comparison: center $\le 9\times10^{10}$ corresponds to entries
  $\le 1.8\times10^{11}$ on the largest cell — smaller than the cited
  frontier, but fully reproducible from this repository in under a
  minute, with three independent implementations.

## 4. What the verify script proves mechanically

`verify/checks/a6_bounds.py`: `small_bound_search` re-run to its FULL
bound; agreement of the three implementations on overlapping ranges (the
congrua sets themselves compared elementwise for a sample of $m$); and
the wheel facts used by the sieve design (roots coprime to 6, offsets
$\equiv 0 \bmod 24$) re-asserted against F4's checks.
