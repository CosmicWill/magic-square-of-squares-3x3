# Review and proof plan — 2026-09-08

*Postscript (entry 134, the same day): Theorem A3.SQ (the binomial square root) killed the eight tower records of §3 and most open classes of every campaign; the counts below are those of entry 132. The joint-sign quotient technique of §3 is carried to the 28 surviving (1,1,1) classes in entry 135.*

The strongest next move is to connect the uniform prime-column theory to the
arithmetic hidden in its survivors. The recent work provides both ingredients:
exact inequalities that eliminate whole classes for every choice of primes,
and repeated reductions to a small collection of curves. Neither ingredient
yet controls arbitrary prime support. Cancellation-pattern descent remains
the principal ambitious investigation, alongside independent routes that
can change its direction.

**A concrete new opening emerged during this review:** all eight remaining
(1,1,1) tower records have maps to just two bielliptic genus-2 curves. Their
genus-25 pullbacks need not be the starting point for point arithmetic.
The maps and elliptic ranks are reproduced by
[`compute/genus25_quotient_probe.py`](../compute/genus25_quotient_probe.py).
This is a necessary-condition reduction, **not eight new exclusions**.

## 1. What the current results establish

Reviewed through entry 132, commit `cc52b7a`, including the height system,
bounded divisibility searches, orientation theorem, higher-prime campaigns,
bielliptic reductions, and Magma point certificates. The ledgers give:

| Campaign scope | Recorded classes | Dead | Certified finite, still open | Provisional | Height-only undecided |
|---|---:|---:|---:|---:|---:|
| Full (1,1,1) | 2,944 | 2,798 | 146 | 0 | 0 |
| Additional three-frame (2,1,1) | 79,368 | 77,980 | 1,388 | 0 | 0 |
| Additional three-frame (3,1,1) | 290,064 | 287,858 | 1,025 | 1,181 | 0 |
| Four primes, all exponents 1, full support | 48,854 | 45,702 | 0 | 0 | 3,152 |
| Five primes, all exponents 1, full support | 497,166 | 468,256 | 0 | 0 | 28,910 |

The last two dead totals combine the prime-column gate with the height
system: 41,767 + 3,935 and 452,284 + 15,972 respectively. These are counts
of canonical classes in different campaign scopes, not distinct curves or
solutions. No complete nonexistence result follows for any of these shapes.
The (3,1,1) provisional records and unresolved base-locus uniformity also
prevent promoting that campaign to a complete finiteness theorem.

The generated inventory contains **2,559 certified finite records**. It is
not the whole frontier: 1,181 provisional records and 32,062 higher-prime
height survivors belong in research planning too. The report now states
this explicitly, displays provisional counts, labels compact (3,1,1)
certificates accurately, and renders all three representative columns.

The mathematical progress is substantial:

* **A3.PC is uniform:** every nonzero prime column has at least three entries
  attaining its maximum absolute exponent. It excludes every free frame.
* **A3.HS uses information valuations alone lose:** exact Gaussian-unit
  cancellation, nonvanishing, conjugation, shared divisibility, and parity
  yield inequalities valid for all choices of center primes. The reality
  sharpening and the coefficient-2 improvement are meaningful additions.
* **A3.OR makes the inequalities intelligible:** orientation patterns
  explain many exclusions and the prime hierarchies that remain possible.
  The falling height exclusion rate as support grows is a reason to seek
  information lost by the inequalities, not a theorem that all local
  arithmetic is exhausted.
* **Curve arithmetic is becoming reusable:** the C2 descent, repeated G1
  quotient, F1 calculation, and octic-tower closures show that original
  genus is a poor predictor of the easiest arithmetic route.
* **The geometric and sphere fronts remain relevant:** the explicit
  differential web, low-genus restrictions, and exact sphere identities
  address structure that the prime-height system does not see. Classifying
  families alone would still leave isolated rational points.

## 2. Review findings and evidence boundaries

Ten focused FAST checks passed: `a3.height_system`, `a3.height_pairs`,
`a3.orientation`, the (3,1,1), four-prime and five-prime campaign checks,
the three recent tower checks, and `a3.research_inventory`. This was not
a replay of all 214 registered checks, the complete large searches, or
the external Magma/Sage point computations.

**Priority verification gap: connect exact bounds to exhaustive searches.**
`height_system.verify_certificate` verifies the multiplier identity for a
capped coordinate but does not recompute or validate its recorded `D`,
`product`, or `cap`. It also accepts an empty `per_prime` dictionary for a
nominally feasible result. Altering all capped bound fields to 1 still
passes the current checker. The search checks use the supplied caps.

I independently recomputed the exact multiplier products and integer bounds
for **all 52 capped-search (2,1,1) records and all 16 (3,1,1) records**:
204 prime bounds in total. Every recorded search cap covers its exact
bound. Thus this audit found an inadequate rejection check, not an
incorrect cap or an invalidated exclusion. Strengthen the checker to
validate coverage/status, derive bounds exactly, link those bounds to
the searched ranges, and reject malformed certificates. Add negative
tests with missing coordinates and altered bounds.

An exact recession direction certifies a homogeneous statement. Calling
the affine system feasible or unbounded additionally requires feasibility;
the current solver obtains that from floating-point LP. Record an exact
feasible witness or qualify the claim. In particular, a recession
direction does not prove that arbitrary improvements to constants leave
the affine system feasible.

Other corrections to research interpretation:

* The original surface, a Pythagorean pullback, a quotient, and its twist
  must remain distinct. The new reduction below exploits exactly this.
* Failure of a bielliptic-involution test does not by itself establish
  absolute simplicity of a genus-2 Jacobian. Higher-degree elliptic maps
  require separate analysis; numerical Frobenius evidence is not that proof.
* The recorded rank-one Magma `Chabauty(P)` calls have a suitable method:
  this overload includes saturation and returns all points when the
  Jacobian has rank one. It differs from the prime-specific overload with
  its index hypothesis. Preserve the rank and point-completeness evidence
  with each use. [Magma handbook](https://magma.maths.usyd.edu.au/magma/handbook/text/1620)
* A birational Markov/Vieta iteration on the general-type surface itself
  cannot supply an infinite orbit of birational self-maps: its birational
  automorphism group is finite. Arithmetic descent on auxiliary covers or
  correspondences remains possible. Likewise, target elliptic structures
  on appropriate quotients or covers rather than assuming an elliptic
  fibration of the general-type surface. [Hacon–McKernan–Xu](https://annals.math.princeton.edu/2013/177-3/p06)

## 3. New reduction: the eight tower records reach two genus-2 curves

The records are `111:2841,2843,2845,2847,2892,2893,2896,2897`, all in frame 1.
Their elimination components have bidegree (3,3); imposing both remaining
Pythagorean conditions produced the recorded genus-25 curves. Instead,
take a quotient of the (3,3) component first.

For `2841`, write the frame ratios as g,h. Its component is

\[
\Phi=3g^3h^3-g^3h-17g^2h^2+3g^2+3gh^3-17gh-h^2+3.
\]

The joint sign change (g,h) ↦ (−g,−h) gives invariant coordinates
x=g², y=gh. The identity Q(g²,gh)=g²Φ(g,h) holds for

\[
Q=(3-y)x^2+(3y^3-17y^2-17y+3)x+3y^3-y^2.
\]

Its quadratic discriminant is

\[
D_+(y)=9y^6-102y^5+199y^4+556y^3+199y^2-102y+9.
\]

Putting y=(z+1)/(z−1) gives the exact identity

\[
(z-1)^6D_+((z+1)/(z-1))=64(12z^6-44z^4+40z^2+1).
\]

The other family gives the same identity with
D₋=9y⁶−6y⁵−185y⁴−404y³−185y²−6y+9. Thus the targets are

\[
H_+:v^2=12z^6-44z^4+40z^2+1,\qquad
H_-:v^2=-12z^6+28z^4-8z^2+1.
\]

For `2843,2847,2893,2897`, first replace h by 1/h and multiply by h³;
the resulting even model is reciprocal, and (z,v) ↦ (1/z,v/z³)
puts it into the displayed form. All eight substitutions, the quadratic
discriminant identities, smoothness of the sextics, and the elliptic
quotient identities are checked exactly by the probe. The square factor
64 is retained; no nonsquare twist has been discarded.

| Target | Direct cases | Cases using the reciprocal chart | Elliptic factors, with PARI rank bounds |
|---|---|---|---|
| H₊ | 2841, 2896 | 2843, 2897 | 123a1 [1,1], 1968c1 [1,1] |
| H₋ | 2845, 2892 | 2847, 2893 | 123a1 [1,1], 984d1 [1,1] |

Both share an elliptic factor with **rational 5-torsion**. The other factors
have trivial rational torsion. The current `qc_general.sage` explicitly
assumes trivial torsion in both elliptic factors and the Jacobian; removing
its assertions would not extend its proof. Its logarithms and local images
must track torsion cosets, the chosen subgroup and its index, and saturation.

Bielliptic quadratic Chabauty is a concrete next route for these rank-two
genus-2 Jacobians, subject to the implementation and precision hypotheses.
[Bianchi–Padurariu](https://arxiv.org/abs/2212.11635)
An alternative worth testing is descent using the common factor's
5-isogeny, coupled to the square-coordinate conditions in both elliptic
images. The shared factor might explain the reduction, rather than merely
serve as input to a point algorithm.

Completion requires all rational points or a sufficient obstruction to
their lifts, followed by every omitted affine/projective fiber, the
conditions x=g² and 1+g²,1+h² square, and the eliminated frame's original
relations. The probe deliberately does not certify those steps.

## 4. The ambitious portfolio

### A. Complete a quotient atlas and turn reductions into a mechanism

Start with H₊ and H₋: implement torsion-aware quadratic Chabauty and the
Mordell–Weil sieve, with known rational points as controls, or obtain an
independent lift obstruction via isogeny/cover descent. A successful
complete lift calculation could close the last eight tower records;
the other **138 (1,1,1) records would still remain**.

Then audit those 138 using joint sign symmetries, ratio inversions,
automorphisms of the original components, and retained square covers.
Organize an atlas by rational maps, twists, elliptic factors, and lift
conditions. A genus label alone is not a useful queue. The ambitious
target is a theorem explaining why the same elliptic factors recur and
when their points cannot satisfy the prime-frame lifts.

**Checkpoint:** two complete lift certificates, or a precise arithmetic
obstruction to the selected method, plus an atlas of distinct targets.
Do not start another box merely because point arithmetic stalls.

### B. Compress arbitrary prime support into finitely many column types

For all-one exponents, A3.PC leaves, up to reversing an entire column,
**16 three-maximal sign columns and 8 four-maximal sign columns**. Group
primes with the same column c into a Gaussian integer γ_c. Their combined
contribution to label X is (γ_c/\barγ_c)^(2c_X). Distinct groups retain
disjoint rational-prime supports; γ_c and \barγ_c remain coprime.

This gives a specific alternative to sweeping ω=6,7,…: derive cancellation
and gcd identities between these 24 products, with the coprimality kept.
It is an exact rewriting, not permission to treat a product as a prime.

For arbitrary exponents, write a column with three top entries ±M and
one smaller entry ±m, 0<m<M, as

\[
w=(M-m)c_3+mc_4,
\]

where c₃ has zero at the deficient entry and c₄ completes its actual sign.
There are 32 such directed choices up to column reversal, in addition
to the 16 pure three-entry and 8 pure four-entry types: **56 structural
types of prime contribution**. A mixed prime contributes to two linked
products. Their shared support is essential and must not be replaced by
an independence assumption.

**Target theorem:** an obstruction or effective bound for these products
that is uniform in how many primes they contain. First prove and implement
the exact grouping and its support conditions, then derive one new gcd
restriction for a family that survives A3.HS. A finite vocabulary is not
a finite search or a solution; its value is exposing recurring arithmetic
across every support size.

### C. Make exact cancellation cofactors the principal descent experiment

The current inequalities retain sizes of Gaussian binomials/trinomials
but discard their exact quotients by forced prime powers. Keep those
cofactors. Compare them across columns using gcds, resultants and square
classes, starting with hierarchical survivors and four-maximal columns.
Use the grouping in B when several primes play the same role.

The first deliverable should be one of:

1. A transformation to another admissible configuration with a strictly
   smaller integer height, with all original equations preserved.
2. An effective height/radical bound for an infinite family.
3. A compatibility obstruction among cofactors that excludes an infinite
   family despite its feasible height inequalities.

Merely determining the largest prime from the other primes is not descent.
Neither is finding a smaller divisor if its configuration loses the square
conditions or introduces uncontrolled prime support. Track closure and a
well-founded measure explicitly. If closure fails, the exact failure may
instead identify a useful covering or Selmer obstruction. An effective
uniform bound would also be a route to a proof; support descent is not
the only possible arithmetic endgame.

### D. Keep geometry and global obstructions independent

Two separate questions deserve bounded experiments:

* **Differential web:** use the explicit tangent field to solve a specified
  low-degree first-integral problem, including singularities and removed
  divisors. A first integral or a rigorous obstruction could explain the
  curve atlas. Failure within a degree bound excludes only that ansatz.
* **Cover compatibility:** express one survivor's retained square covers
  as divisor/squareclass data, construct a candidate Brauer or descent
  class, and calculate ramification and local evaluations. First prove
  that it is well-defined and nontrivial. Local solvability of the original
  surface does not settle compatibility of lifts to a specified cover.

These need not wait for cancellation descent to succeed. Neither a
low-genus curve classification nor a single nontrivial obstruction alone
would establish absence of every isolated admissible point.

### E. Use construction and exact counting to challenge our conjectures

Select near misses by structural role, orientation and cofactor behavior,
including higher-prime and provisional cases. Compare examples that lose
one retained square condition, and use them to falsify proposed descents
or bounds before broad computation. On the sphere front, test a precisely
defined composition/counting identity against the true coupled count;
retain local factors and positivity. A signed count or a suggestive
coefficient match is not an absence theorem.

## 5. What to do next, and when to change direction

1. **Secure the evidence and expose the whole frontier.** Repair cap
   verification, distinguish recession certificates from affine witnesses,
   and extend the inventory with provisional and height-only records while
   preserving their status. Retain source hashes and maps between views.
2. **Pursue the new H₊/H₋ opening.** Complete torsion-aware point/lift
   arithmetic, while using the common 123a1 factor to test the isogeny idea.
3. **Keep the uniform theory in active work.** Prove the grouping in B and
   attack a specific cofactor family in C. Closing a shape is a valuable
   milestone, but must not consume the entire proof program.
4. **Maintain at least one independent geometry/global probe and one
   counterexample control.** Promote either when it reveals new structure.

Reassess after each theorem, complete lift computation, failed descent
closure, or counterexample to a conjectured invariant. Expand an experiment
only when it addresses a stated uncertainty. The strongest success would
be a mechanism applying to an infinite family or arbitrary support; an
exact limitation that changes the next question is also progress.

Reproduction of the new calculation:

```text
python -m compute.genus25_quotient_probe --ranks --check
python -m compute.research_inventory --check
```

The first uses SymPy and PARI/GP and checks the committed quotient artifact.
It does not run Sage, Magma, quadratic Chabauty, or an exhaustive point search.
