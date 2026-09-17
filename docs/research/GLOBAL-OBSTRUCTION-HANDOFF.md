# Global-obstruction checkpoint, 2026-09-14

Source: main `a719b635e7ca969ef62a805d85c0a9d6b5fbc17e`, through entry 140.
Branch: `research/proof-alternatives`. Calculations ran locally; primary
literature was consulted online. Other agents' files and campaign ledgers
were not changed, and no messages were sent to other people or agents.

## Results to review

- GB.1--2: entry-monomial quaternion classes pull back to constants, and
  the original square cover has trivial twist label at every full rational
  square configuration. These do not furnish the proposed separation.
- GB.3: **CITED consequence of Harari's formal lemma**, with all hypotheses
  verified for the normalized surface: any finite B in Br(U) has nonempty
  U(A_Q)^B, even allowing ramification along deleted degeneracies. The
  proof handles almost-all integrality, not just a product of local sets.
- GB.4: a concrete root-dependent quaternion is nontrivial but regular at
  the all-equal rational point; stronger fourth-power local controls exist.
- GB.5--6: the homogeneous direction covers have a rational-boundary trap.
  One/two-line twists always have a smooth rational boundary point; the
  three-line locally soluble case reduces to Hasse--Minkowski. Four-line
  direction boundaries give 70 subsets and 11 geometric genus-one types,
  but any rationally realizable direction again supplies a boundary point.
- GB.7: the degree-eight root-sum cover
  34 z1^2=A+B, 178 z2^2=B+C, 3026 z3^2=C+A is geometrically integral,
  locally soluble at every place, and has no rational signed all-equal
  fiber. Its v=0 AP boundary has no rational lift (real sign selection,
  then a complete 3-adic obstruction).
- GB.8: **CITED deduction from Tunnell's unconditional theorem:** the u=0
  genus-three boundary has no rational points, including projective and
  exceptional fibers. It maps to y^2=89(1-t^4). A nonexceptional point
  gives a rational right triangle of area 89, but the complete ternary
  counts are N8=48 and N32=20, contradicting N8=2*N32. No BSD assumption.
- GB.8: the selected cover has a smooth proper compactification with
  **no rational boundary points**. The proof uses the morphism to the
  projective base to cover infinity, zero entries, all degeneracy lines,
  normalization and exceptional divisors. Surface resolution and the
  four-square AP theorem remain CITED inputs. An explicit blowup sequence
  and a Brauer-group computation have not been carried out.
- An explicit row quartic and the five additional square conditions needed
  to recover the full cover are recorded at the end of GB.8. PARI/GP 2.17.4
  independently gives rank zero and torsion order two for the decisive
  elliptic quotient; the exclusion proof does not depend on that computation.

Full proofs, status distinctions, sources, and maps are in
[global-obstructions.md](global-obstructions.md). All labels are local
to this research note, not replacements for the repository's A-series.

## Universal reduction continuation

The owner asked to make the universal reduction the lead question.
[universal-twist-reduction.md](universal-twist-reduction.md) records:

- UT.1, **PROVEN:** the exact eight-element root-sign orbit of the product
  class T. The four noncentral frames account for D4 symmetry.
- UT.2, **PROVEN:** every hypothetical MSS3 reaches a cover with signed
  odd squarefree q_i, sum(q_i)=3 mod 8, and z_i 2-adic units. There are
  16 residue triples, but infinitely many numerical labels. Every triple
  in this family has full admissible local lifts at 2; the normalization
  does not create a new local obstruction.
- UT.3, **PROVEN:** the triple gcd of the labels divides the squarefree
  center; pairwise shared primes come from the center or gcd(U,V); center
  primes 5 mod 8 occur in all labels or none according to center parity.
  More precisely q1*q2*q3=m*H times a rational square, with H supported
  only on primitive-direction differences. Once that direction is fixed,
  H has finitely many possibilities independently of m and gcd(U,V).
- UT.4, **PROVEN:** a full admissible Q_401 configuration has nonsquare
  product class in all four frames and all eight sign choices. Thus the
  earlier product-one restriction is not forced locally or algebraically
  by the square equations and symmetries. This does not refute a possible
  additional global theorem solely about rational admissible points.

## Next concrete task

The [coupled-cycle continuation](coupled-cycle-descent.md) proves:

- CC.1: four even-cycle parameters are signed odd squarefree and 1 mod 8;
  their support depends only on the primitive direction, independently of
  m and G. The first two labels have gcd dividing 5.
- CC.2: the corner-cycle class is (ai+cg)/(2m^2); four independent divisor
  valuations certify that the combined cover has geometric degree 16.
  A full Q_97 point has nonsquare corner class under every sign and D4 choice.
- CC.3: every single corner double cover has a smooth rational boundary
  point on an explicit blowup chart, regardless of its coefficient.
- CC.4: an infinite subfamily of the simultaneous permitted covers has
  smooth rational boundary too. The first explicit tuple is
  (-119,-15,1,-7), with direction (1,8). By GB.3, unrestricted finite
  ordinary Brauer tests cannot exclude these twists. This does not settle
  the canonical 2-adic subdomain or another justified integral restriction.

The [finite-descent audit](finite-descent-barrier.md) then establishes:

- FD.1, CITED: Demeio's Theorem 3.2.1, frozen arXiv:2112.00843v3, lifts a
  rational boundary point to a smooth model of some twist of any finite
  torsor. The paper and its proof, credited to Wittenberg, were read.
- FD.2, CITED deduction: some twist retains nonempty finite-Brauer adelic
  sets even with canonical roots at 2. This extends to finite collections
  and finite adaptive towers. No claim about the full possibly infinite
  etale-Brauer intersection is made.
- FD.3: an explicit rational Laurent-series construction verifies the
  square-root case, including ramification and poles. The canonical
  root-sum and cycle branches have trivial labels and unit lifts.
- FD.4: symbols with products of the CC twist constants in their first
  slots split at 2. For the CC.4 boundary family, finite subgroups of this
  type cannot exclude the canonical local domain either.

The next target at the September 11 checkpoint was a genuine arithmetic
descent. In the corner-label-1 branch, n^2=(ai+cg)/2 supplies an odd
integer 0<n<m. The note re-expresses all nine equations in half-sum
coordinates, but no new admissible grid is constructed. The m=5,n=3 AP
control shows that merely replacing the center is not a descent. The
other corner labels remain unbounded. Further finite covers may organize
the arithmetic, but cannot alone close the finite-Brauer endgame.

The UT.2 family still includes twists with smooth rational boundary
points, so the GB.3 barrier remains relevant. The selected fixed cover's
rational-point set is also still unknown. No uniform global contradiction
or finite reduction of the numerical twist labels has been proved.

## Arithmetic continuation, 2026-09-14

The [arithmetic-descent audit](arithmetic-descent-audit.md) resumes that
target from 7ab300b. Its new results are local to the corner-label-1 branch:

- AD.1, **PROVEN:** an exact divisor model r,s dividing n^2, with five
  square equations retaining the center and all four sides. Positivity,
  distinctness and gcd(n,y,w)=1 complete the reconstruction conditions.
  Fixed n gives finitely many divisor inputs and 2m^2<=n^4+1; n itself
  remains unbounded. A positive, distinct five-square control at
  n=399,m=4225 shows that the corner equations do not imply the side
  conditions; all four sides fail there.
- AD.2, **PROVEN:** a homogeneous linear root formula centered at n,
  satisfying the full equations identically, has constant projective
  shape. The certificate is the exact Gram matrix 128*I_9 of signed
  all-equal n=0 boundary points. Constant shape does not mean all entries
  equal, and does not exclude a possible constant MSS3 solution.
- AD.3, **PROVEN with an exact finite certificate:** quadratic output
  roots with center nD, D linear, all have a common factor n modulo the
  defining quadrics. Quadratic-over-linear formulas centered at n reduce
  projectively to linear ones, so the apparent scale cancels on primitive
  normalization. The boundary evaluation kernel has dimension seven:
  exactly the six magic quadrics and ai+cg. The restrictions do not
  cover higher-degree or arithmetic-subset constructions.

At that checkpoint the next target was the five square equations of AD.1.
A nonlinear correspondence must preserve them, stay in a branch where it
can be iterated, and decrease
the primitive integer invariant after clearing denominators. Alternatively,
a uniform exclusion of that divisor system would settle this branch.
Neither is known; the other corner labels still need a universal argument.
No new MSS3 or campaign exclusion has been made.

## Nonlinear continuation, 2026-09-14

The [nonlinear-descent fiber audit](nonlinear-descent-fibers.md) continues
from cc54456:

- ND.1, **PROVEN:** n -> rs/n preserves all five square equations but
  acts on the grid as vertical reflection times rs/n^2. Primitive integer
  normalization restores the original center. The apparent nonlinear
  decrease is a symmetry and a scale change.
- ND.2, **PROVEN:** fixing k=r/s gives five explicit quartic square
  equations in t=n/s. The center quartic maps to an elliptic cubic, but
  ordinary doubling can lose its rational t-lift: at k=3 the section
  (10,100) doubles to (16,-136), requiring t^2=8/5.
- ND.3: **PROVEN** discriminant and resultant identities show that the
  five quartics have 20 disjoint simple roots for every rational
  k!=0,+/-1. The connected square-root cover has degree 32 and is
  unramified at infinity. Its genus is 129, a **CITED deduction** from
  Riemann--Hurwitz. This covers every admissible positive ratio.
- ND.4, **CITED deduction:** a nonconstant rational map between any two
  such full fibers has degree one. Consequently elliptic multiplication
  of degree >1 cannot lift to a full fixed-ratio rational self-map.
  Point-dependent ratio changes and multivalued correspondences are
  outside this argument.
- ND.5: each fiber has 128 explicit rational AP points over t=+/-1,+/-k.
  They are all of its rational degenerate points, a **CITED deduction**
  from the classical four-square AP theorem, with zero and infinity
  audited. Rational interior points remain unclassified. A full local
  interior point at k=3,t=13 is verified through precision 401^8.

Resume with a point-dependent change of ratio or a multivalued arithmetic
correspondence and a justified rational branch. Preserve all five square
tests and an iteratable domain, and prove a decrease after denominator
clearing and primitive normalization. A uniform exclusion of the relevant
rational interior is another possible target. None is established; the
other canonical corner labels also remain unbounded. No new MSS3 or
campaign class has been excluded.

## Reproduce

```text
python -m compute.global_obstruction_probe --ap-bound 100
python -m compute.global_obstruction_probe --boundary-certificate
python -m compute.universal_twist_probe --precision 8
python -m compute.coupled_cycle_probe
python -m compute.formal_boundary_probe
python -m compute.arithmetic_descent_probe
python -m compute.nonlinear_descent_probe
python -m verify --only nlf.
python -m verify --only ard.
python -m verify --only fdb.
python -m verify --only cce.
python -m verify --only ut.
python -m verify --only gb.
python -m verify --fast --only a5.
python -m verify --fast --only f5.
python -m verify --fast --only f1.
python -m verify --fast --only f4.
python -m verify --only gauntlet
```

At checkpoint bfd894a, the 11 gb branch checks passed at FULL bounds
(three added since 2c91f31).
The complete count certificate and the separate GP quotient diagnostic
also ran successfully. That checkpoint had 233 registered checks.
Five existing f4 checks at FAST bounds and both gauntlet checks at FULL
were rerun and passed: 18 checks passed in this continuation.
At the preceding checkpoint, 18 related existing checks passed (a5, f5,
f1, f4 at FAST bounds; the two gauntlet checks at FULL). This is not a
replay of the full suite or other branches' computations.

The universal continuation adds five ut checks (238 registered total).
Their FULL run passed: 277 canonical AP controls x 4 frames, 199 support
controls x 4 frames, 19 full square-grid lifts to 2^24, and the complete
32-product residue certificate with all nine roots lifted to 401^8.
The all-precision local statements follow from the written lifting proofs.
The support check also uses 12 admissible local grids x 4 frames x 8
sign choices, independently checking cancellation of a common offset prime.
The 11 gb checks and both gauntlet checks also passed at FULL bounds in
this continuation, along with the five f4 checks at FAST bounds: 23
relevant checks passed in total. The strengthened product support identity
was followed by another successful run of all five ut checks.

The coupled-cycle continuation adds five cce checks (243 registered total).
All five cce, five ut, eleven gb and two gauntlet checks passed at FULL
bounds: 23 targeted checks. The new certificates include four independent
valuation rows, all 16 canonical offset residues modulo 32, 400 signed
corner identities, a complete 97-adic sign certificate, the explicit
resolved boundary point, and nine admissible local lifts on the rescaled
degree-16 cover. An initial broad substring filter also ran and passed
the seven existing a7cc checks; the new prefix is now cce to avoid that
unrelated match. This was not a replay of the full verification suite.

The finite-descent continuation adds five fdb checks (248 registered total).
All five fdb, five cce, five ut, eleven gb and two gauntlet checks passed
at FULL bounds: 28 targeted checks. The new controls include all nine
formal square equations through t^17, 18 Laurent-series lift certificates,
six canonical full grids to 2^24 with seven unit cover lifts to 2^20,
twist-first-slot splitting controls, and 179 exact AP controls for the
smaller-integer identities. The first local test attempted to lift the
untwisted three-sum cover on too large a canonical neighborhood; it now
uses u=2^e,v=3*2^e with e>=5 and retains e=3 as a negative control.
The cited lifting and formal-lemma theorems are not replaced by these checks.

The arithmetic continuation adds six ard checks (254 registered total).
All six ard, five fdb, five cce, five ut, eleven gb and two gauntlet
checks passed at FULL bounds during this continuation: 34 targeted checks.
The new certificates include exact divisor identities, 179 canonical AP
round-trips, the positive five-square control, the rank-nine linear
boundary matrix, and 384 real algebraic boundary points yielding 284
rational quadratic-evaluation rows of rank 38. Five rescalings of an
unequal AP grid verify the constant-shape and primitive-normalization
distinction. The standalone probe also ran successfully. This was not a
replay of the complete verification suite.

The nonlinear continuation adds seven nlf checks (261 registered total).
The new checks passed at FULL bounds: 179 full AP reciprocity controls,
175 divisor/fiber comparisons, 495 exact determinants certifying all
five discriminants and ten resultants, the complete rational exceptional
set, genus bookkeeping, 128 rational boundary points on each of seven
control fibers, the exact failed doubling lift, and a full local interior
grid through 401^8. These finite checks do not replace the cited curve
theorems or classify rational interior points.
All 34 existing ard, fdb, cce, ut, gb and gauntlet checks also passed at
FULL bounds: 41 targeted checks passed in this continuation. The standalone
nonlinear probe ran successfully. The complete suite was not replayed.

Optional PARI diagnostic, using the actual executable rather than the
PowerShell `gp` alias:

```powershell
& 'C:\Users\Will\pari-2.17.4\gp.exe' -q -f compute/global_boundary_quotients.gp
```

The new checks cover explicit algebra and finite calculations. They do
not reprove Harari, Lang--Weil, Hasse--Minkowski, Riemann--Hurwitz, Tunnell,
or surface resolution. No
candidate nonexistence proof or new MSS3 exclusion is asserted.

## Root-function reciprocity, 2026-09-17

The previous session left `compute/root_reciprocity.py` untracked in the
primary checkout with its note unwritten. The module is now on this branch
with [root-functions-and-reciprocity.md](root-functions-and-reciprocity.md)
and the checks `rr.`:

- RR.1, **PROVEN:** the grids with square cross entries are exactly
  `entries(1, x^2-1, X^2-1)` for two rational points of x^2+y^2=2, up to a
  square scale; the classical five-square control is replayed.
- RR.2, **PROVEN (trivial):** Hilbert reciprocity for the root ratios
  (r_0/r_4, r_2/r_4) holds for every rational pair, so it rejects nothing
  by itself; the control (113/114, 17/114) has symbol -1 at 3 and 113 only.
- RR.3, **PROVEN:** the local symbol is determined by the roots modulo a
  sufficient prime power; the evaluator refuses insufficient data.
- RR.4, **PROVEN by exact controls:** a full Q_113 point (three exact
  roots, six Hensel lifts) has symbol -1, while fourth-power local
  configurations at 2, 3, 113 have symbol +1. The local value is not forced
  at any tested place. **FAILED-ATTEMPT** as an exclusion: reciprocity of
  the root ratios cannot constrain rational MSS3 without a global
  restriction of the realized local profiles, and GB.3 bars finite
  Brauer-type restrictions on the open surface.

No campaign ledger or headline predicate changes. The resumed next
targets are unchanged: a point-dependent divisor-ratio change or a
multivalued arithmetic correspondence for the corner-label-1 branch, a
uniform argument for the other corner labels, or a proof that the 128
boundary points exhaust the rational domain.
