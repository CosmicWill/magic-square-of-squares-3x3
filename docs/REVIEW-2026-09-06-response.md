# Response to the independent review of 2026-09-06

*(Entry 117, 2026-09-06.  The review is `docs/REVIEW-2026-09-06.md`; this file records what was verified, what was accepted, what was corrected, and what is deferred.)*

## Finding 1 — discarded non-square constants: CONFIRMED, the most important item

The reviewer's control reproduces exactly: `decide_component` on `8425 th² − 11664 (tg⁴ + 1)` returned *dead* through the model y² = t⁴ + 1 although (4/3, 12/5) is an admissible point; the squareclass 337 had been dropped.  Three sites had the pattern: `_disc_model` (the constant of the discriminant's factorization), `gp_model` (division by the coefficients' gcd), `omega3_towers.int_coeffs` (denominators cleared with a non-square lcm, gcd divided out).  All three are repaired (`squarefree_part`, `square_part_of_gcd`); the control now yields the model y² = 337(t⁴ + 1) of rank 2 and the verdict *finite* through the pullback route.

The audit went beyond the reviewer's sample.  Every engine kill of both boxes was re-run with the two routines instrumented to record every discarded non-square constant, and every flagged kill, every tower kill (entry 100), every quotient kill (entry 105), every two-step kill (entry 106) and every entry-108 attack kill was re-decided with the repaired code.  Result: (1,1,1) — 206 of 1376 engine kills had discarded a non-square constant and every one of them survives with the correct twist; the 72 quotient and 36 two-step kills survive; 8 of the 296 tower kills are void (4 of those classes stay dead by the free-frame reduction of entry 116); the box's tally moves from {'dead': 1492, 'finite': 1452} to {'dead': 1484, 'finite': 1460}.  (2,1,1) — 4581 of 12132 engine kills flagged, 0 kills lost; tally {'dead': 16032, 'finite': 63336} → {'dead': 16032, 'finite': 63336}.  No finiteness statement changes (a lost kill reverts a class to Faltings-finite); the count of dead classes does.  The control case is now a permanent check (`a3.omega3_twist`).

## Finding 2 — the provisional-verdict cache: ACCEPTED, repaired

`exact_genus_verdict`'s memo key now includes the decision policy and the computation settings, so a provisional verdict cached under `PROVISIONAL_FINITE` cannot be served in strict mode.  No recorded verdict depended on the defect: the rigorous pass (entries 113–114) re-resolved every provisional component outside the cache.

## Finding 3 — what a green run certifies: ACCEPTED in part, partly deferred

Accepted and done: PARI/GP is discovered through `MSS3_GP`, then `PATH`, then the portable install (the hardcoded path was the last resort).  Accepted and deferred (architecture, R.11): separate statuses for artifact consistency, sampled recomputation and complete certificate verification; a pinned certification environment in which a missing tool makes certification incomplete rather than a passing note; the enumerator's classes required to equal the certificate set; mechanism-specific positive controls (the twist control is the first); the gauntlet's predicate coverage.  The `--fast` profile has grown past its advertised budget and needs a genuinely bounded smoke profile — noted, not yet done.

## Finding 4 — the mathematical summaries: ACCEPTED, corrected

(a) Conjecture A3.C (no additive triple) *implies* nonexistence, so it is stronger, not weaker; corrected in A3 §2.  (b) R.11's "base-locus half done" now states the exception (both relations trinomial-type).  (c) The superelliptic curve of Conjecture R_J has genus 3J − 2 (J odd) / 3J − 3 (J even); J − 1 is its quadratic quotient, and the squareclass condition for the lift is retained; corrected in §2.44.  (d) Full 2-torsion gives a Legendre curve only up to a quadratic twist; corrected in §2.42.  (e) PROGRESS.md and README refreshed.

## The bielliptic descent for 𝒞₂: ACCEPTED as the route for the sixteen classes

Reproduced: gcd(F, G) ∈ {1, 8, 25, 200} on all coprime pairs to 80, both forms positive, so a square coordinate on 𝒞₂ forces a rational point on one of the two genus-2 bielliptic curves G_δ: z² = δ(25t⁶ − 29t⁴ + 11t² + 1), δ ∈ {1, 2}, whose elliptic quotients are 1840d1, 184b1, 7360r1, 1472a1, all of rank 1 (PARI, twist constants kept).  Bounded searches: G₁ has (0, ±1) and two points at infinity, G₂ has (±1, ±4).  This replaces the generic genus-2 curve of 2.45 by two curves in the setting of bielliptic quadratic Chabauty (Bianchi–Padurariu), with Sage code available — a concrete next computation for objective P-C, still needing a good prime, generators, local heights and a completeness argument.  The acceptance criterion in the review is adopted verbatim.

## The proposed workstreams

They coincide with R.11 (P-A the uniform finiteness theorem with the trinomial exception stated, P-E the weighted free-frame relation, the arbitrary-support experiment for goal G) and add the surface program as a separate objective; the architecture proposal (a certified-curve module owning model maps, twist constants, exceptional fibers and completeness; an immutable settings/provenance ledger) is the right shape for the next refactor and is recorded in R.11.
