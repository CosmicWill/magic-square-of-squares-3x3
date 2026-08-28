# The state of the program

*A standing honest assessment: what has genuinely been achieved, what it
means, and what it does not mean. Updated at milestones (last:
2026-08-28, after Theorem A8.18 and the A9-T1 fourth layer). Every claim
below carries the repository's provenance tags and is enforced by the
verification suite (`python3 -m verify`, currently 108 checks); the
[README ledger](../README.md#claims-ledger) is the row-by-row
record.*

## The one-sentence truth

**The existence question is untouched — by us and by everyone — but this
program has built, on two independent fronts, a detailed structural map
of *why* the problem is hard, and several pieces of that map are new
mathematics about a well-studied object.**

The repository's standing banner applies to every line of this memo: the
open problem remains open, and nothing here claims otherwise.

## Front 1: the surface (A5/A7/A8)

The moduli space of the problem is a surface $X \subset \mathbb{P}^8$
(a complete intersection of 6 quadrics, degree 64, with 256 nodes),
which Bruin–Thomas–Várilly-Alvarado (2022) proved *algebraically
quasi-hyperbolic*: it carries only finitely many curves of genus
$\le 1$. Their proof is abstract; they wrote that computing the
symmetric differentials that drive it is "out of range of current
computational techniques", and no one had enumerated the low-genus
curves or made the finiteness explicit for $X$. That gap is where this
program worked, via descent along the $(\mathbb{Z}/2)^8$ cover of the
Lucas plane (Theorem A8.1). The results, in ascending order of
consequence — all first-party, machine-verified, and unconditional
unless flagged:

1. **The spectrum is computed.** $h^0$ of symmetric differentials on
   the open surface, all 256 characters, degrees through 8; on the
   *resolution*, degree 4 has exactly **one** section $\eta_\star$
   (PROVEN), and **Theorem A8.18** closes the invariant ladder with no
   gaps: $4 \to 1,\ 5 \to 0,\ 6 \to 0,\ 7 \to 0,\ 8 \to 1$ — every
   invariant section through degree 8 is a power of $\eta_\star$
   (PROVEN by sandwich; the $m = 8$ lower bound $\eta_\star^2$ is
   re-certified exactly on every suite run). The abstract finiteness
   theorem now has one explicit object carrying it — and the
   cuboid-style *two-section* finiteness shortcut is provably
   unavailable at these degrees.

2. **The structure theory of rational curves.** Every complete genus-0
   curve on $X$ passes through nodes over $\ge 3$ distinct triple
   points of the branch arrangement, and 3 is sharp (Theorems
   A8.8/A8.14/A8.15, PROVEN, exact certificates); any such curve whose
   node pattern spans a $\ge 2$-dimensional extension space *is* one of
   the 128 classical degenerate AP components (Theorem A8.16, PROVEN);
   everything else must be an integral curve of the single web
   $\eta_\star$, of degree $\ge 3$, and the web's line and conic levels
   are closed with nothing new (Theorem A8.17 + the A7.6/M10-B budget).
   **Any hypothetical new 1-parameter family of near-solutions is
   cornered into one explicit, finitely-checkable system.** This is,
   to the best of our (reachable-literature) knowledge, the analogue
   for $X$ of what Stoll–Testa did for the perfect-cuboid surface —
   and $X$ had nothing like it before.

3. **No local obstruction** (F5, long established here): the system is
   solvable modulo every prime power — whatever excludes magic squares
   of squares, it is not a congruence.

*The frontier on this front:* the web's cubic level (M11-J-2), then the
arithmetic endgame (Picard lattice as Galois module, Brauer–Manin — the
cuboid template exists in the acquired literature).

## Front 2: the discrete spheres (A9)

The owner's geometric picture — the square as lattice points on spheres
— made exact and pushed into class-group territory:

1. **The dictionary (PROVEN).** A magic square of squares with center
   $m^2$ is 8 points of the single sphere $\mathcal{S}(3m^2)$ glued by
   shared coordinates; the through-center slice *is* A3's congrua set;
   the whole family lives in one field, $\mathbb{Q}(\sqrt{-3})$, with
   $r_3^*(3m^2) = 24\,h(-3m^2)$.

2. **The three-sieve pair desert (each sieve PROVEN necessary; the
   annihilation VERIFIED to $m \le 1200$).** Positivity, genus-character
   coherence (Theorem A9.3, via the gluing law A9.1: each line's Gauss
   class represents its entries' co-norms), and single-class
   representation kill **every** ordered congrua pair for **every**
   center $m \le 1200$ — 1782 pairs: 1608/152/22, zero remain. The A3
   desert, previously a search fact, now has named arithmetic causes.

3. **The anatomy (the deepest finding on this front).** Of the 57 line
   kills behind the final sieve: 21 are *provably local* (certified
   against an exhaustively validated representability criterion), and
   **36 are provably beyond every congruence and character condition**
   — they occur inside single genera, i.e. inside cosets of
   $\mathrm{Cl}^2$ (Gauss's principal genus theorem is machine-verified
   here). At $m = 725$ the desert exists *only* for this reason.

*The frontier on this front:* the law governing representing classes
inside a genus — Gauss composition / spinor structure (the P8
acquisitions now have a precise question to answer), and the fourth
sieve where the three sieves first fail beyond 1200.

## The convergence — the program's central structural finding

The two fronts were built independently and say the same thing: **the
obstruction to a 3×3 magic square of squares is genuinely global
arithmetic.** No congruence excludes it (F5, and the 36 beyond-genus
kills); what excludes candidate configurations in every range we can
reach is class-group structure (sphere side) and the rigidity of one
global differential (surface side). This is the signature of the
hardest class of Diophantine problems — and it is now located, not just
suspected.

## Honest calibration — what none of this does

- **Rational curves are not rational points.** The surface theorems
  constrain *families*; a single magic square of squares would be one
  rational point, and no result here excludes one. Even a complete
  M11-J would yield "no new families" plus — *conditionally on
  Bombieri–Lang* — "at most finitely many squares". Finitely many is
  not zero.
- **Range-verified is not proven-for-all-$m$**: the slice confinement,
  the pair desert ($m \le 1200$), and the sieve anatomy are exact
  within their stated ranges and conjectural beyond them; the spectral
  rigidity is through degree 8, trivial character (nontrivial
  characters at $m \in \{6,7,8\}$: partial, scope-noted).
- **Novelty is claimed only relative to the literature we could
  reach** (citation databases unreachable from this environment; the
  searches are documented). Everything is machine-verified; nothing is
  peer-reviewed.
- The multi-hour mod-$p$ computations are recorded artifacts with
  pinned system shapes; the suite re-verifies exactly what is cheap
  enough to re-verify (including the $\eta_\star^2$ certification,
  live, in exact arithmetic).

## What an actual resolution would still require

Three known-shaped paths, all hard, none with a visible finish line:
**(i)** the arithmetic endgame on $X$ — Picard/Galois module, then a
Brauer–Manin-type global obstruction (deep, but the cuboid literature
provides the template); **(ii)** upgrading the sphere sieves from
range-verified to all-$m$ theorems via composition/spinor theory;
**(iii)** something genuinely new. In the other direction, existence
would need a construction or a search far beyond current bounds — the
structure found here is evidence *against* accessible solutions and
proof of nothing asymptotic.

## Reproducing the state

```sh
python3 -m verify            # 108 checks, FULL bounds
python3 -m verify --only a8  # the surface front
python3 -m verify --only a9  # the sphere front
```

Attack documents: [A8](attacks/A8-descent-differentials.md) (surface),
[A9](attacks/A9-discrete-spheres.md) (spheres), with A1–A7 and the
foundations F1–F6 linked from the [README](../README.md).
[RESEARCH_LOG.md](../RESEARCH_LOG.md) is the dated narrative,
entries 1–27.
