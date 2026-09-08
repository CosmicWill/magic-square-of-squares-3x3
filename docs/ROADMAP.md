# The proof program — strategic roadmap

*Drafted 2026-08-28, after the full-access literature sweep, the Hill
refutation, and the completion of the A8.18 ladder. This is the
standing battle plan toward the goal: **a proof, in either direction,
of the 3×3 magic square of squares problem.** It is deliberately
ambitious; every claim of current fact carries the repository's tags,
and every ambition is labeled as such. Companion documents:
[PROGRESS.md](PROGRESS.md) (what is true now),
[RESEARCH_LOG.md](../RESEARCH_LOG.md) (how we got here).*

## R.12 Current research portfolio (2026-09-06)

**A flexible portfolio, with cancellation-pattern descent as the current lead.** The purpose is a proof and a deeper explanation of the problem's structure. Keep several independent attacks in play; an unexpected theorem, a counterexample to a proposed mechanism, or a new connection can change the ordering. The lead is a working hypothesis about where to learn next, not a commitment to one eventual proof architecture.

This section supersedes the ordering and pending-work lists in R.1–R.11 and the older sequencing section. Those sections retain the history and detailed ideas; completed work and old counts there are not current queues. No large new sweep is running under this plan.

**Current evidence.** The prime-column lemma A3.PC applies to arbitrary numbers of split primes and arbitrary exponent shapes. Every nonzero column has at least three maximal absolute exponents; every free-frame class is excluded. Both class-decision entry points now apply this inexpensive certificate before curve computation. The verified working ledgers contain:

| Scope | Dead classes | Open finite classes |
|---|---:|---:|
| Full (1,1,1) campaign | 2,774 | 170 |
| Additional three-frame (2,1,1) campaign | 77,980 | 1,388 |
| Additional three-frame (3,1,1) campaign (entry 126) | 287,858 | 1,025 (+ 1181 provisional, 0 undecided) |

*Updated at entry 123 (the height system, [A11](attacks/A11-height-system.md)): the sharpened unit congruences kill 274 + 2,784 of the classes that were open at entry 121, unconditionally for all primes; the inventory is regenerated on the 214 + 1,960 survivors.  The lead attack's first experiment is therefore a success, not the negative result recorded below, and its next step is fixed: the survivors are the classes whose inequalities admit a recession direction — use the exact divisibilities as congruences between the primes (a bounded search per class), the next-order values of the binomials (the deficient label's leading unit), and the four-maxima trinomials' 2-adic structure.*

These are canonical-class counts, not counts of curves or solutions. The two finiteness results remain ineffective; neither shape has a complete nonexistence proof. The sixteen C2 cases are closed by entry 118's lift-preserving bielliptic descent and QC/Mordell–Weil sieve. The remaining twist-normalization sites were repaired and their 108 recorded exclusions rechecked in entry 119. The base-locus uniformity argument still has its both-trinomial case to handle.

The [generated research inventory](RESEARCH-INVENTORY.md) replaces the old finite-class queues. Every open record has its candidate, source index/hash, signed cancellation pattern, exponent gaps, deciding frame, and recorded curve/tower evidence. It supports multiple views of the same cases. Similar cancellation roles do not automatically mean isomorphic curves or identical arithmetic.

### The attacks and the questions that could change our understanding

| Attack | Ambitious target | Next bounded experiment / useful deliverable | Reason to expand or redirect |
|---|---|---|---|
| **Cancellation patterns and global descent — current lead** | Turn shared prime support into a strict descent, effective height bound, or forced exact monomial relation for arbitrary support. | [A10](attacks/A10-cancellation-descent.md): couple unit congruences for `***` and `*CD` survivors through shared gcds or the four-maximal trinomial equations. The individual norm bounds are already shown insufficient. | Expand after a proved inequality on an infinite family. If a proposed height fails, record the obstruction and try a different invariant or front. |
| **Lift-preserving arithmetic of curves — active** | Explain when a high-genus point problem reduces to a controlled family of twists with tractable elliptic factors. | Inspect the 88 surviving (1,1,1) tower records: factor homogenized forms, bound gcd squareclasses, preserve lifts and exceptional fibers, and identify what made the completed C2 example tractable. | Expand when a reusable descent applies to more than one model. A stubborn Jacobian or growing resultant support identifies the mechanism's limits. |
| **Differential geometry and dynamics — active independent probe** | Classify rational curves by a first integral or a justified degree bound for the slope-surface foliation. | Use the explicit F(c,v,p) and tangent field in [the proof-directions note](PROOF-DIRECTIONS-2026-09-06.md#5-third-program-treat-the-quartic-differential-as-a-dynamical-system); attempt a specified low-degree rational first integral and analyze removed divisors and singularities. | A first integral or singularity constraint can reorganize the geometry. A bounded search failure does not exclude all first integrals. Even success addresses families, not isolated rational points. |
| **Global descent and Brauer/Picard obstructions — independent exploratory front** | Find a global compatibility condition on the four square covers that survives every known local control. | Pick a survivor and express its covers as divisor/squareclass data; construct one candidate unramified class or prove why it ramifies or evaluates trivially. Compare this with the unit congruences. | Expand only with a well-defined invariant and a verified nontrivial evaluation or compatibility statement. Triviality is useful evidence about which cover information is missing. |
| **Uniform two-prime and genus mechanisms — theorem-building front** | Resolve an infinite exponent family, or prove a uniform genus/low-genus classification including the exceptional base loci. | Revisit R_J through its covers, keeping the original superelliptic curve separate from its genus-(J−1) quadratic quotient; use the survivor inventory to test label-to-genus claims before another box campaign. | A formula with explicit hypotheses is more valuable than another isolated genus computation. Stop a conjectured formula at its first counterexample and explain the missing variable. |
| **Sphere composition and exact counting — exploratory front** | Explain the additive desert by an exact composition law or a counting identity that retains the square's full coupling. | Define one precise weighted count, test its relation to the true nonnegative count on known centers, and test a proposed modular/composition identity with local factors included. | A finite coefficient test matters only after modularity and weight/level, or another exact identity, are proved. A heuristic or signed count alone does not prove absence. |
| **Counterexample-guided construction — continuous check on all fronts** | Find a square, or isolate exactly which final compatibility condition fails in near misses. | Select experiments by uncovered survivor roles, compare matched examples differing in one square/lift constraint, and record the applicable hypotheses of every control. | A new family of near misses can redirect the theorem program. Larger bounds alone are supporting evidence, not the principal milestone. |

### What the first cancellation experiment taught us

[A10, CP.1](attacks/A10-cancellation-descent.md#2-cp1-the-column-rule-exhausts-rational-valuation-directions-of-the-relaxed-system) proves that the three-maxima rule already gives every rational valuation direction of the relaxed Laurent system over an algebraically closed valued field. Further valuation-support computation cannot remove its surviving signs. The arithmetic information must come from the shared Gaussian support, squares, conjugation, or global size.

CP.2 supplies the leading-square roles: a C/D deficit forces its prime to be 1 modulo 8; four maxima require t, 1+t, 1−t to be nonzero squares modulo that prime. CP.3 retains unit congruences modulo pi^(2g), where g is the exponent gap, or pi^(4M) when all four labels are maximal. These are proved necessary conditions. No strict global height decrease has yet been found.

CP.4 proves that the three-maximum binomials cannot vanish and derives explicit prime-height inequalities. The first global experiment has a negative answer: **every open record has a certified positive direction along which these inequalities allow unbounded real log-primes**. The inventory retains all 5,232 witnesses. A successful descent must exploit compatibility lost by these individual norm estimates, or additional equations. This result changes the next experiment; it does not weaken the reason to explore other fronts.

### How priorities stay flexible

Keep the lead investigation and at least two conceptually different questions available at each research checkpoint. They need not depend on cancellation descent succeeding. Choose the next task for the uncertainty it resolves, the new structure it exposes, or the theorem it might yield; do not assign permanent rankings to entire subjects.

For each experiment, record the exact question, hypotheses, expected artifact, relevant controls, and what each possible result would teach us. Reconsider the portfolio after a conceptual result or a failed mechanism, rather than after a fixed number of excluded classes. A rigorous limitation, a counterexample to our conjecture, or an equivalence between two attacks can justify changing direction.

Large sweeps should answer a stated structural question, apply A3.PC first, and use a measured budget. The next immediate work is small coupled-unit systems alongside the retained-lift tower inspection and the foliation probe. Free-frame/content-2 closure and the sixteen C2 classes are completed tasks, not future projects.

## R.13 The paths to a proof (2026-09-07, after entries 118–126)

**What a proof has to do.**  A magic square of squares has a center with some number ω of split primes and some exponent shape; a proof must cover every ω and every shape at once.  Everything class-by-class — curve verdicts, height certificates, box sweeps — can only close finitely many shapes.  A proof therefore needs a uniform invariant no solution can satisfy, or a descent that turns a solution into a smaller one.  The record holds two genuinely uniform pieces, the prime-column lemma (A3.PC) and the height system (A3.HS), and they show exactly where uniform arguments stop: at the classes whose offsets are essentially coprime to the split primes of the center (the four-maxima and C/D-deficit families).  For those the local information at the center's primes is weak and what remains is the class curve, a global object.

**The paths, each with its mechanism, its evidence and its next experiment.**

| # | Path | Mechanism | Evidence so far | Next experiment | Cost / probability |
|---|---|---|---|---|---|
| 1 | **The role-word theorem** (uniform local structure) | Prove, for every ω and shape, which label configurations survive A3.PC + A3.HS; the linear programmes depend only on combinatorial data (exponent differences, spreads) | **answered (entry 129, A12):** the rows are functions of the flip pattern (Theorem A3.OR); Theorem T1 (three never-disagreeing offsets) is the uniform single-row exclusion; the survivors are the orientation-generic classes with a feasible prime hierarchy | the hierarchical open classes (forced prime ratios ≥ 125) as the first targets of a descent (path 3) | done; a theorem about what any solution must look like, not a proof |
| 2 | **Closing one shape** (the (1,1,1) box to zero open classes) | curve arithmetic on the survivors: rank bounds + Chabauty on the genus-2 quotients of the tower classes; elimination curves and bielliptic models (entry 118's pipeline) for the rest | 24/24 genus-0-quotient classes closed; **entry 130: 12 tower classes closed by the bielliptic pipeline (G₁ again, and F₁); 158 open** | Magma rank bounds for the 20 remaining tower classes' genus-2 quotients; hyperelliptic models for the (6,6) components | high; moderate; the first complete shape, a template |
| 3 | **Descent on the number of primes** (goal G) | a solution with support S forces one with smaller support, or a contradiction | the free-frame reduction did it for one family (now subsumed); the pair-search rigidity (the largest prime is determined by the others) is rigidity, not descent | look for a descent mechanism inside the survivor family of path 1 | the only arithmetic route to a full proof; low probability |
| 4 | **The surface geometry** | elliptic fibrations of the magic-square surface, Picard rank, Brauer classes; why the same fifteen rank-0 curves kill everything at genus 1 | fifteen killers across every route; the differential web; the foliation probe (PROOF-DIRECTIONS §5) | explain the killers by a fibration; test the foliation for a first integral | high; exploratory; unlikely to give full nonexistence alone (degenerate points are dense) |
| 5 | **Higher ω with the local method only** (the (1,1,1,1) box) | the lemma and the height system work for any number of columns and need no engine | **done (entries 127–128): it decays** — kill rates 76.8% / 55.5% / 35.6% at 3 / 4 / 5 frames; two A/B deficits no longer exclude at four, up to five A/B deficits survive at five | path 1 in its new form: what the open classes share that the local method does not see | minutes; answered |
| 6 | **A structured computational search** | extend the literature's entry bounds with the new necessary conditions (offsets coprime to the split part, residues, the divisibilities) | the pair search: no solution with two smallest primes ≤ 500 in any open class | a bounded search over centers with the local filters | moderate; evidence and consistency, never a proof |

**Sequencing.**  Path 5 now; path 1 as the theory front; path 2 when Magma is available; path 4 kept warm as the exploratory front; path 3 as the target that paths 1 and 5 are meant to inform; path 6 as the running consistency test.  None of these is a known road to a complete proof: paths 1 and 5 are the likeliest to produce uniform theorems, path 2 the first complete shape, paths 3 and 4 the only ones that could end the problem.

**Standing rules.**  Every kill carries an exact certificate re-verified by the suite; the two-agent working tree needs one committer at a time; the survivor inventory is regenerated after every ledger change.

## R. The 2026-08-28 realignment (post-ladder)

*Written the day the scaling law, the ladder sweep, and the
fertile-seed arithmetic landed (A9.13–A9.14, entries 48–50). This
section is the standing analysis of what those findings mean for the
plan; the workstreams below are reprioritized accordingly.*

### R.1 The three-regime picture (what the findings actually say)

Any magic square of squares is a Lucas grid: center $m^2$, offsets
$U, V$ with $U, V \in D(m)$ (rows and columns are 3-APs of squares),
and the four corners square **iff additionally $U{+}V, U{-}V \in
D(m)$** — the additive quadruple. The program's empirical and proven
state now separates into three regimes with *opposite* characters:

1. **The pair-sieve regime LEAKS.** The three/four sieves
   (positivity, coherence, representation = the A9.12 Diophantine
   law) are necessary conditions for corner-squareness. The desert
   verified them lethal to $53400$ — but Lemma A9.13 (verdicts only
   soften along $(m,U,V) \to (qm, q^2U, q^2V)$) plus the ladder
   sweep proved transparency is *abundant at scale*: 20 golden pairs
   in one window, upward-closed forever, and A9.14's eligibility
   directions even let us **predict** a golden center in advance
   (m = 210125, the 41-ladder — confirmed). Survivor counts grow
   with $m$. **Conclusion: no refinement of this sieve family can
   prove nonexistence. The sieves are scaffolding, not the wall.**
2. **The additive regime is bone-dry.** Not one additive *triple*
   ($d_1 + d_2 = d_3$ in any $D(m)$) exists to $m \le 10^7$ — let
   alone the quadruple a square needs. The heuristic count is
   *convergent* ($\sum_m |D(m)|^3/m^2 < \infty$-type), unlike the
   divergent pair-sieve expectation. **The entire difficulty of the
   open problem is concentrated here — and this layer is the exact
   condition, not another necessary-condition sieve, so theory here
   is terminal: there is no deeper regress.**
3. **The rigid class is the sieve regime's one deep mystery.** Some
   seeds (including the $m = 925$ three-sieve passer) are dead in a
   scaling-invariant way beyond every local, character, and
   congruence test we built (A9.14 panel) — flat resurrection curves
   through two decades. A named "rigidity invariant" would prove
   infinite ladder families sieve-dead — the only known mechanism by
   which sieve-side arguments could survive scaling at all.

### R.2 The reprioritized program

- **P1 (new center of gravity) — the additive layer, W10.**
  $D(m) = \{\,|\mathrm{Im}(z^2)| : z \in \mathbb{Z}[i],\ |z|^2 = m^2\}$,
  so an additive triple is a **six-term vanishing sum on the
  norm-$m^4$ torus**: $w_1 + w_2 - w_3 = \overline{w_1 + w_2 - w_3}$
  with $w_j = z_j^2$, $\bar w_j = m^4/w_j$ — an S-unit-equation
  structure over $\mathbb{Q}(i)$, the machinery (Evertse–
  Schlickewei–Schmidt, Baker for few terms) that actually finishes
  such problems. Targets: **A3-S1** formalize + machine-verify the
  reformulation; **A3-S2** unconditional no-triple theorems for
  small $\omega(m)$ (all $m$ with $\le 2$ distinct split primes
  first) — real nonexistence slices; **A3-S3** the convergent-sum
  heuristic made rigorous as far as honest tools allow.
- **P2 — the rigidity invariant (W4's sharp target).** Compute the
  composition-layer obstruction element for the rigid seeds' lines
  along rungs; find what is invariant; prove it. Payoff: infinite
  provably-sieve-dead families containing the anatomy passers.
- **P3 — geometry demoted to structural support (W1/W2).** The
  η⋆-web eliminations are the curve-enumeration half of any future
  Bombieri–Lang-conditional statement ("sporadic points only"); they
  proceed as background theorems (A8.19 momentum), not as the main
  thrust.
- **P4 — the hunt as calibration + insurance (W6).** Ladder hunting
  is now cheap and *targeted* (eligibility directions known). Roles:
  falsification insurance (if a square exists, ladder + additive
  telescopes find it first), A9.14 validation, actuarial data. The
  desert resumes after the $m = 7$ survey (standing instruction).
- **P5 — consolidation (W8).** The A9.12–A9.14 chain + ladder
  discovery + honest refutations is a coherent, publishable story;
  drafting it enforces rigor and invites the community in.

### R.3 Risk register (honest)

- The S-unit front may stall beyond small $\omega$ (subspace-theorem
  territory is non-effective); mitigation: small-$\omega$ theorems
  stand alone, rigidity covers sieve-side families, heuristics stay
  calibrated and labeled.
- The rigid class may be spinor-genus-deep; even so, *measuring* the
  invariant on data (P2 step 1) is decisive either way.
- Discipline: golden ≠ magic — every transparency result is about
  *our necessary conditions*, and is reported as such; the suite
  keeps every claim pinned.

### R.4 Status after the first two W10 theorems (2026-08-29)

The realignment is validated: two days on the additive layer
produced two unconditional theorems (A3.6, A3.7). The strategic
facts they establish:

1. **The summit statement is now explicit.** Conjecture A3.C ("no
   additive triple in any D(m)") **implies the full nonexistence
   theorem** — a quadruple contains a triple. Every rung of A3.C
   climbed is a permanent slice of the open problem, and two rungs
   are climbed: split part $p^a$ (all powers) and $pq$.
2. **The proof mechanisms so far are prime-uniform.** Nothing in
   A3.6/A3.7 depended on which primes $p, q$ occur — valuation
   combinatorics and tan-half factorization depend only on the
   exponent box, and the seven residual descents were uniform.
   If this uniformity persists, A3.C decomposes into a box-indexed
   family of finite pattern problems plus a master induction — a
   conceivable full proof shape.
3. **The honest risk is rank growth.** At $\omega = 3$ the group
   has rank 3; valuation pruning weakens and residual patterns
   multiply. If they stop landing on classical descents, the
   frontier tools (effective S-units) prove finiteness, not
   emptiness. The program's exposure is exactly there.

Priority order stands: W10 (next rung: split part $p^2q$ — the
$(a,b) = (2,1)$ box), then W8 (consolidate the S-unit framing and
the sieve-program story for community scrutiny), W4/W6 in support.

### R.5 Phase two of W10 (planned 2026-08-29, after A3.6-A3.8)

Three days on the additive layer produced three unconditional
theorems, one honest retraction-and-restoration, and a clear view
of the terrain. The findings that set the next phase:

1. **The ladder repeats itself.** Every box so far is closed by the
   same five weapons (valuation prune, tan-half factorization,
   congruences, cyclotomic collapse, divisibility trees ending in
   the leg-window or a classical Fermat descent), and the residual
   families are visibly parametric in the box size. Box-by-box
   grinding cannot finish an infinite ladder — but a UNIFORM
   omega <= 2 theorem plausibly can, and the evidence for it is now
   structural, not hopeful.
2. **Enumeration completeness is a theorem obligation.** The
   all-plus gap survived three "complete" theorems and was caught
   by an unrelated consistency check. The pipeline itself must be
   proven complete before more boxes are claimed.
3. **The open problem now lives at omega >= 3.** The corollary
   pushes any MSS3 center's split part to p^3 q / p^2 q^2 /
   >= 3 distinct split primes — so the rank-3 frontier is where
   the problem's remaining mass sits.

**The plan, in order:**
- **N1 — the completeness meta-audit** (integrity gate before any
  further box claims): prove and pin that the canonical pattern
  enumeration is exhaustive (brute-force cross-check on small
  boxes), and add end-to-end pipeline controls on synthetic
  relation instances.
- **N2 — finish (3,1) and (2,2) as lemma-building**: close the 74
  remaining patterns and 42 level-shift re-derivations with lemmas
  stated for general (a, b) wherever proofs allow; output Theorems
  A3.9 (p^3 q) and A3.10 (p^2 q^2) plus the uniform toolkit.
- **N3 — the uniform omega <= 2 theorem** (declared summit of this
  phase): classify the residual families parametrically and prove
  the family lemmas once — subsuming the infinite (a, b) ladder.
- **N4 — omega = 3 reconnaissance** (cheap, parallel): extend the
  machinery to rank 3 and census the (1,1,1) box; measure whether
  the weapons still bite where the problem now lives.
- **N5 — the consolidation paper (W8), started now**: the Z[i]
  reformulation, A3.4-A3.8 with full proofs, the verification
  methodology including the gap-and-repair episode, and the MSS3
  corollary. External scrutiny is part of the integrity plan.
- **N6 — the targeted omega >= 3 desert** (compute, after the m = 7
  survey and desert resume): re-filter the additive desert to the
  only centers the theorems do not cover and push the verified
  bound well past 10^7 on that thin set.

### R.6 The 2026-09-02 breather: what the corpus says, and where a proof can come from

*Drafted after entries 68–79 (the (2,2) box, the rigidity lemma
campaign, the Rank-1 Theorem, the certificates) and **adopted
2026-09-02** as the standing plan: A is the main thrust with B
alongside; C is held ready as the pivot the moment ω ≥ 3 stalls.*

**What the corpus says, in five sentences.** (1) Every route we built
converges on one terminal layer: a magic square is an additive
quadruple in $D(m)$, and $D(m)$ is the set of imaginary parts of
squares in the *free abelian group of rational points on the unit
circle* — generators $g_p = \pi_p/\bar\pi_p$, one per prime $p\equiv1\pmod4$ —
so the whole problem is a relation $\operatorname{Im}u_1+\operatorname{Im}u_2=\operatorname{Im}u_3$
among elements of that group with bounded exponents. (2) The sieve
front (A9) is a proven elementary law that *leaks* (golden centers);
the surface front (A8) constrains families, not points; neither can
carry nonexistence. (3) The additive ladder has proven the problem
for split parts $p^a$, $pq$, $p^2q$, $p^3q$, and $p^2q^2$ up to a
rigidity lemma that is now a theorem for every prime outside a thin,
explicitly characterized set (transparent primes whose congruent-
number curve has rank $\ge2$). (4) The tools that actually *finished*
cases are exactly three: valuation combinatorics, classical rank-0
descents (Fermat/Ljunggren quartics), and — new here — **reduction
rigidity**: two 2-descent-equivalent points with incompatible
reductions at a special prime (the Rank-1/Rank-$r$ criteria). (5) The
convergent heuristic ($\sum_m |D(m)|^3/m^2$, an absolutely convergent
Euler product) says the expected number of additive triples over *all*
$m$ is $O(1)$ with a negligible tail beyond $10^7$ — so A3.C is a
sound target and existence is not a realistic bet.

**The honest wall.** A uniform proof of A3.C for all $\omega$ is a
statement about a torus equation whose $S$-unit group *varies with
$m$*. Every finiteness tool (Laurent/ESS, Baker, Chabauty, Faltings)
is per-$S$ or per-curve; none is uniform in $S$. The rigidity lemma
showed the true shape of the residual obstruction: positive-rank
curves whose ranks vary with the prime. So the realistic unconditional
summit is not "A3.C for all $m$" by present tools; it is **"no
additive triple for every $m$ outside an explicit thin set $T$, with
$T$ verified empty in range"** — plus the conditional finiteness from
the surface. That is still the strongest statement anyone would have.

**The proposal, in order.**

- **A. The uniform $\omega\le2$ theorem, reorganized as Lucas
  coincidences (main thrust, weeks).** Every residual endpoint of the
  $(a,b)$ ladder is an equality between a term of the Lucas-type
  sequence $\operatorname{Re}\rho^{2k}$ and a prime power times a term
  of $\operatorname{Re}\pi^{2j}$ (the rigidity lemma is $(k,j)=(4,2)$).
  Classify the endpoints as one two-parameter family, prove the order
  lemma in general ($p^2\mid\operatorname{Re}\rho^{2k}\Rightarrow 4k\mid p-1$
  in exact form), bring Bilu–Hanrot–Voutier primitive divisors and the
  size relation $q^k\approx p^{j+2}$, and generalize reduction rigidity
  to the frame curves of each $(k,j)$. Target: Theorem A3.11 with an
  explicit exceptional set; A3.10 falls as the special case.
- **B. The $(1,1,1)$ box with the new arsenal (parallel, cheap).** 27
  orbit-families; the mod-$p$ criteria, PARI certificates and the $L'$
  sieve did not exist when N4 was surveyed. Either it closes — a new
  theorem, "three first-power split primes cannot carry a triple" — or
  it exposes the $\omega\ge3$ obstruction concretely.
- **C. The quadruple pivot (the creative bet).** A3.C is *stronger*
  than needed. The exact condition is the quadruple: $\{d_4,d_1,d_3\}$
  a 3-term AP in $D(m)$ *whose common difference $d_2$ is also in
  $D(m)$*. Euler's four-squares-in-AP descent works precisely because
  it uses both relations at once; our machine has only ever used one.
  If $\omega\ge3$ stalls for triples, attack quadruples: two relations
  give two levers per prime, and the second relation may be exactly
  the "second point" the rank-$\ge2$ curves were missing.
- **D. The A2.L descent, revisited in the additive language (one
  session).** The function-field degree-halving descent is the only
  known mechanism that *finishes* problems of this species. The
  autopsy (M12-E) found the transplant to $\mathbb{Z}$ blocked by a
  "dimensional" wall — diagnosed before the additive reformulation
  existed. Re-run the autopsy on the torus equation: if the wall is
  the sieve-vs-additive gap, the terminal layer may close it.
- **E. The paper (W8, now).** A3.6–A3.10, the rigidity campaign, the
  Rank-1 Theorem and the "descent blind at $p$" phenomenon are a
  coherent story with new mathematics in it; writing it is the
  community lever and the rigor audit.
- **F. Insurance and calibration (background only).** The targeted
  $\omega\ge3$ desert (N6) on the thin set the theorems do not cover;
  the PARI generator campaign for the 22 rank-2 curves only if cheap.

**What not to do.** No more box-by-box grinding without a uniform
lemma in hand (R.5.1 stands); no descent-only local criteria at $p$
(proven vacuous, entry 79); no further $(D,E)$-level reciprocity
(entry 75); no sieve refinements as a route to nonexistence (R.1).

### R.7 The 2026-09-03 direction: a long-term goal, and the ω ≥ 3 front

*Adopted 2026-09-03 after entries 95–96 (the quadruple theorem for a
finite family of ω = 2 shapes and its audit).  Updated as the fronts move.*

**G — the long-term goal (standing).**  A **global invariant for all
ω**: either a descent on a curve or surface with finitely many rational
points, in the historic pattern (Fermat, Euler, Faltings/Chabauty), or a
**reduction of ω ≥ 3 to lower ω**.  Every front below reports against
G: what it proves, and whether the mechanism that proves it is uniform
in the primes and in ω.  The first instance appeared at once (entry 97):
at ω = 3 the quadruple's two relations, after one elimination, are
rational points on fixed plane curves; the kills are rank-0 elliptic
curves of the Fermat–Euler family.  G is updated when a front shows the
mechanism generalizes (a family of curves that stays finite as the box
grows) or fails (an infinite Pythagorean family that only primality
kills).

**The active front: ω ≥ 3, starting with the (1,1,1) box (entry 97).**
Chosen over the uniform ω = 2 program because it holds the problem's
mass and teaches the most per result.  Status after entry 98: 2944 quadruple classes; **1077 dead uniformly
in the primes** (trivial factors; thirteen rank-0 curves; the monomial
lemma — every rational Pythagorean family is an angle-multiple
coincidence w_g^a = ε w_h^b, impossible for distinct primes; non-square
discriminants); 600 Faltings-finite; 1267 high-bidegree, not yet
analysed; **no class infinite or candidate**.  Next in order: (a) quotient
towers for the 600 finite models (even + reciprocal → elliptic
quotients, PARI ranks; Chabauty where towers stop); (b) the
high-bidegree components by a cheaper route (numeric Pythagorean
evaluation and p-adic reducibility tests before factoring); (c) the
(2,1,1) box and the test of whether the killing curves stay in one
finite family.

**The secondary road: ω = 2 made uniform.**  The joint forms' extreme
coefficients are small (leading 3, constant 63 for the (5,1) orbits), so
a closed form in J would kill the whole column p^J q by the rational
root theorem; then the double-lever and diagonal families.  Kept warm,
not active.

**Still true.**  R.6's "what not to do" stands; box-by-box extension of
the ω = 2 theorem is evidence, not a path; Conjecture R_J is unreduced
(entry 96).

### R.8 The 2026-09-04 plan after the (1,1,1) lift

*Adopted 2026-09-04 (entry 99), after entries 97–98 opened ω = 3.  Reports
against the long-term goal G of R.7.*

**The fact that shapes it.**  The thirteen rank-0 quartics that do all the
elliptic killing in the (1,1,1) box are five curves up to isomorphism —
32a2 (j = 1728, CM by ℤ[i], the Fermat/congruent-number curve), 48a1,
48a3, 56a2, 80a1 — because the Pythagorean frame conditions are double
covers of the circle branched at degenerate frame values, so the genus-1
pieces are (2,2)-covers of the line branched over four points with only a
few possible cross-ratios.  If that holds for every box, the elliptic part
of every quadruple curve is a twist of a curve from a fixed finite list,
and uniformity reduces to ranks: **the Fermat–Euler descent as the
universal mechanism, the monomial lemma for the families.**  This is the
current candidate for G.

**Status 2026-09-04 (entry 100).**  Phase 1 done: 296 of the 600 die
through eight rank-0 quotient curves (30a2, 80a1, 11a3, 48a3, 528j2, 24a1,
128c2, 400d1); 304 remain, blocked by rank-1/2 elliptic quotients or with
no elliptic quotient, all with empty height searches — the
elliptic-Chabauty / two-cover situation, needing Magma or Sage.  The
five-curve reading holds at the (2,2) level only; tower quotients range
over two dozen curves.  Box tally: dead 1373, finite 304, unknown 1267.

**The plan, in order.**
1. **Quotient towers for the 600 finite classes** ✅ (entry 100) (even → u = t²; reciprocal
   → the genus-2 sextics split into two elliptic curves; PARI ranks at every
   level; enumerate lifts at rank 0).  Record every quotient's j-invariant:
   the test of the finite-list reading.
2. **The 1267 high-bidegree components** ✅ (entries 102–103): smoothness
   fails (they are singular at the degenerate frame values) and the local
   sieve is vacuous; the Riemann–Hurwitz lower bound of entry 102 (as
   committed: 1224 certified, 43 left — computed with a non-monic-modulus
   factorization; corrected in entry 103: 1264 certified, none lost) is
   superseded by the EXACT GENUS by resolution of singularities (entry
   103): every high-bidegree component has genus 3..23, cross-checked by
   Riemann–Hurwitz with the exact branch counts; the 3 "degenerate"
   classes die by dividing out the common factor of their relations.
   **Box (1,1,1) closed: dead 1376, finite 1568, unknown 0** — finiteness,
   not effectivity.
3. **The (2,1,1) box** with the same engine (Chebyshev elements) — sampled
   (entry 101): 400 of its 79,368 new classes give dead 88 / finite 55 /
   unknown 257; the same killers and the monomial lemma recur (angle
   multiples up to 4), the curve list grows modestly; 64% unknown because
   the components exceed the pullback threshold.  The full sweep (~60
   CPU-hours) waits for phase 2.
4. **The structural lemma**: every quadruple component's Pythagorean cover is
   branched only over degenerate frame values, hence its genus-1 quotients
   are twists of curves from a fixed finite list.  The theoretical core.
5. Kept warm: the uniform ω = 2 column p^J q via the joint forms' extreme
   coefficients.

**Lines recorded, not started.**  The S-unit framing (each additive relation
is a six-term unit equation in ℚ(i); Laurent's theorem: solutions in a
torus lie on translates of subtori — the monomial families — plus isolated
points — the curve points; the only framework in view for ω ≥ 4, where one
elimination leaves a surface).  The near-miss literature (7-of-9 and 8-of-9
squares should sit on positive-rank objects at larger boxes; translate one
into the frame language).  A targeted ω = 3 desert (centers pqr swept far
beyond 10⁷, recording near-quadruples).  Infrastructure: PARI/FLINT
factorization above bidegree 6.

**Still needed for a proof**: uniformity across boxes with unbounded
exponents (phase 4 is the route in view) and ω ≥ 4 (the S-unit framing is
the route in view).  Nothing at ω = 3 is closed.

### R.9 The big picture after the (1,1,1) closure (2026-09-04): findings, plans, and the ambitious attempts

*Written after entries 97–104, at the user's request for a step back.
Everything below reports against the long-term goal G of R.7.  The
standing banner applies: nothing here claims the open problem solved.*

**R.9.1 The problem in our language.**  A 3×3 magic square of squares
(MSS3) is a Lucas grid: center m², offsets U, V, and it exists iff the
four numbers U, V, U+V, U−V all lie in D(m), the set of imaginary parts
of squares in the group of rational points on the unit circle — one
generator g_p = π_p/π̄_p per split prime p ≡ 1 (mod 4) dividing m, with
exponents bounded by the multiplicities.  The center's split part
p₁^{a₁}···p_ω^{a_ω} fixes a **box** of admissible labels; the inert
cofactor only scales.  So the problem is a family of finite
combinatorial-arithmetic problems indexed by the exponent shape
(a₁,…,a_ω), and "uniformity" means a mechanism that works for every
shape at once.

**R.9.2 What is proven (machine-verified, suite of 185 checks).**

- *ω = 1 (Theorem A3.6):* no additive relation in D(m) for any split
  part p^a, any inert cofactor.  Hence no MSS3 with one split prime.
- *ω = 2:* no additive relation for split parts pq (A3.7), p²q (A3.8),
  p³q (A3.9), p²q² (A3.10).  The tools that finished them: valuation
  combinatorics, the classical rank-0 quartic descents (Fermat,
  Ljunggren), the Im-collapse identities, reduction rigidity (the
  Rank-1 Theorem), the concentration theorem, and the fact that the
  rigidity system is a fixed curve (Faltings).  The (a,b) ladder stands
  at 2044 of 2136 patterns; the residual is the (J,1) content-3 family
  (Conjecture R_J, entry 92).  For the shapes at that frontier the
  quadruple itself — both relations at once — is excluded directly
  (entries 94–96): **no MSS3 for that family of shapes even where the
  additive conjecture A3.C is open.**
- *ω = 3, shape (1,1,1) (entries 97–103):* the quadruple's two
  relations, after eliminating one frame, are rational points on fixed
  plane curves in the frame ratios, **independent of the primes**.  Of
  the 2944 classes, 1376 are dead for every triple of distinct primes
  (trivial factors; the five rank-0 curves 32a2, 48a1, 48a3, 56a2, 80a1
  and their twists; the monomial lemma — every rational Pythagorean
  family is an angle-multiple coincidence w_g^a = ε w_h^b, impossible for
  distinct primes; eight rank-0 quotient towers; the common-factor
  rule), and 1568 are Faltings-finite (304 hyperelliptic models blocked
  by positive-rank elliptic quotients; 1264 curves of exact genus 3..23,
  by resolution of singularities with a Riemann–Hurwitz cross-check).
  **Every class of the box is impossible or has finitely many frame
  pairs.**  Finiteness, not effectivity; not yet a theorem about
  squares (see R.9.5.A for the one missing check).
- *The sieve side (A9):* the exact sphere dictionary, three
  proven-necessary sieves, the representation theorem A9.12, and the
  scaling law (Lemma A9.13) proving that this whole family of sieves
  **leaks** — golden centers exist and are upward-closed — so no sieve
  refinement can prove nonexistence.  Scaffolding, not the wall.
- *The surface side (A8):* the symmetric-differential computation on X,
  the node-passage theorems, the atlas; the function-field analogue is
  one geometry milestone (Conjecture A2.C) from solved by the
  degree-halving descent A2.L.
- *Numerics:* no additive triple in any D(m) to m ≤ 10⁷; the convergent
  heuristic Σ|D(m)|³/m² says the expected number of additive triples
  over all m is O(1) with a negligible tail.

**R.9.3 What the findings say.**  (1) Every route converges on the
additive layer, which is the exact condition, so theory there is
terminal.  (2) The mechanisms that finish cases are few and classical:
valuations, rank-0 descents on a fixed finite family of elliptic curves
(the Fermat–Euler family: five curves at the (2,2) level), reduction
rigidity, angle-coincidence impossibility (the monomial lemma), and —
new at ω = 3 — the genus of fixed curves.  (3) At ω = 3 the primes
disappear from the equations: the frame ratios are the coordinates, the
curves are fixed, and the primes enter only through "each coordinate is
a Pythagorean ratio of one prime".  This is the global invariant G asked
for, in its first concrete form: **an MSS3 of a given split shape is a
rational point with Pythagorean coordinates on one of finitely many
fixed curves.**  (4) The honest wall has moved: from "no uniform tool
in the primes" to **effectivity** (Faltings does not list the points)
and **uniformity in the exponents** (each shape is its own finite list
of curves; a proof for all shapes needs a structural reason the lists
stay controlled) and **dimension** (at ω ≥ 4 one elimination leaves a
surface, where finiteness of rational points is conjectural).

**R.9.4 The plan (standing, in order).**

1. **The (2,1,1) sweep** (entry 104: the engine made fast — the
   monomial test as an exact polynomial identity over ℚ(i), the genus
   routes inside the engine, the bivariate resultant, a two-pass
   decision: 21 s → 1.2 s per class; on the 400-class sample no verdict
   regressed and 254 of 257 unknowns became finite, 125 of them
   provisionally.  **Done 2026-09-05, entry 107**: 44.9 CPU-hours; dead 11962, finite
   41784 + 25428 provisional, unknown 188; the killers are ten curves
   up to isomorphism).  Question answered by it: do
   the same killers, the same finite-curve picture and the same genus
   profile persist when one exponent grows?
2. **Effective finiteness for shape (1,1,1)** — R.9.5.B.
3. **The structural lemma** — R.9.5.C.
4. **The uniform ω = 2 theorem (A3.11)** as Lucas coincidences with
   primitive divisors (kept warm; the P1 rigidity lemma is its core).
5. **ω ≥ 4** — R.9.5.D.  The S-unit framing is the only framework in
   view.
6. **Force multiplication:** the paper (A3.6–A3.10, the rigidity
   campaign, the ω = 3 curves) and Magma/Sage access for Chabauty.

**R.9.5 The ambitious attempts (what a partial solution would look
like, and what each needs).**

- **A. A finiteness theorem for a prime shape (reachable now).**  For
  shape (1,1,1) every class is dead or finite.  If, in addition, no
  class has a *base point* — a frame pair (t_g, t_h) at which both
  relations vanish identically in the eliminated frame, which would
  give a square for every third prime — then, since a frame ratio
  determines its prime and Faltings bounds the points on each curve:
  **up to scaling, only finitely many MSS3 have a center whose split
  part is a product of three distinct first-power primes.**  The base
  loci are zero-dimensional systems, one per class, computed in this
  session (`omega3_baselocus`).  Ineffective (Faltings), but a theorem
  of a kind the problem has not had: finiteness for an infinite family
  of centers.  The same statement follows for every box the engine
  closes.
- **B. Making it effective: "no MSS3 of shape (1,1,1)".**  *(Steps 1–2 done,
  entries 105–106: quotients by the involutions kill 72 of the 1264 curves,
  the two-step route through the joint quotient 36 more; the remaining
  finite sets — 1460 classes — are the Chabauty list, and the 24
  hyperelliptic ones need a rational-curve parametrization first: Sage.)*  The finite
  sets are 304 hyperelliptic models and 1264 curves of genus 3..23.  The
  frame symmetries (conjugation t → −t, reciprocity, the swap of equal
  exponents) act on the curves, so their Jacobians decompose; the
  quotient towers of entry 100 killed 296 classes exactly this way
  (rank-0 elliptic factors + complete point enumeration).  The attempt:
  compute the automorphism groups and the isogeny decomposition of the
  Jacobians of the 1568 curves; where an elliptic factor has rank 0 the
  points are listable in PARI (done for the towers); where the rank is
  positive, elliptic Chabauty or Chabauty–Coleman (Magma/Sage) applies
  whenever rank < genus of a quotient.  If all 1568 finite sets are
  empty of admissible points, shape (1,1,1) is excluded outright — the
  first ω = 3 theorem — and the same pipeline runs on every box.  Needs:
  Magma or Sage (Chabauty), or a collaborator with either.
- **C. Uniformity in the exponents: the structural lemma.**  *(First
  step, entry 105: the minor formula — every quadruple curve is a pullback
  of the circle under a map of bidegree ≤ (4,4); the singular locus is
  its base locus plus torsion fibers; the three frame conditions are
  explicit double covers of Φ_f.)*  The
  Pythagorean frame conditions are double covers of the line branched
  at the degenerate frame values; the (2,2)-level killers are five
  curves because a (2,2)-cover of P¹ branched over four points has few
  cross-ratios.  The conjecture: every quadruple component's Pythagorean
  cover is branched only over a fixed finite set of frame values
  (0, ±1, ∞, ±i, tan(π/8)-type values), so its genus-1 quotients are
  twists of curves from a fixed finite list and its high-genus
  components have bounded branch data.  If true, the elliptic part of
  every box is a rank question about a fixed list of twists, and the
  Faltings part is bounded uniformly — the shape of a proof for all
  ω = 3 boxes at once.  Test: the branch loci of the (2,1,1) components
  (the sweep records them), then the (2,2,1) and (3,1,1) boxes.
- **D. ω ≥ 4 and the dimension wall.**  With four frames and two
  relations the solution set is a surface in (P¹)⁴; rational points on
  surfaces of general type are conjecturally sparse (Bombieri–Lang) but
  no finiteness theorem exists.  Three ways in: (i) the common-factor
  and monomial reductions already collapse many classes to fewer frames
  (the (2,+-2) relations, the norms); (ii) look for fibrations of the
  ω = 4 surfaces by the ω = 3 curves — a reduction of ω ≥ 4 to lower ω,
  the second branch of G; (iii) the S-unit framing (Laurent: solutions
  in a torus lie on translates of subtori — the monomial families —
  plus isolated points), which is the only framework that names the
  general structure.  Honest status: no route to unconditional
  finiteness at ω ≥ 4 is in view; conditional results (on Bombieri–Lang
  or on explicit rank hypotheses) would still be new.
- **E. The uniform ω = 2 theorem (A3.11).**  Every residual endpoint of
  the (a,b) ladder is a Lucas coincidence Re ρ^{2k} = (prime power)·Re
  π^{2j}; the order lemma, Bilu–Hanrot–Voutier primitive divisors and
  reduction rigidity generalized to the (k,j) frame curves would give
  the theorem with an explicit exceptional set.  The P1 rigidity lemma
  (c₂⁴ − 6c₂²s₂² + s₂⁴ = c₁⁴ − s₁⁴ has no coprime solution) is the core.
- **F. The transplant of the function-field descent.**  A2.L finishes
  the k[t] analogue; the autopsy (M12-E) found a dimensional wall for
  ℤ.  Re-run it on the frame curves: the ω = 3 curves are the first
  objects over ℚ where the problem is literally "rational points on a
  fixed curve", the setting the descent was built for.

**R.9.6 How we work (unchanged, and why it matters here).**  Every
claim is a check in the suite; the fast gate runs before every commit;
corrections are logged as entries (entry 68's silent failures, entry
96's audit of the model switch, entry 103's non-monic-modulus bug).
The ω = 3 engine is now the largest single verified computation in the
repository; its soundness rests on PARI's factorization over number
fields, ellrank's unconditional rank bounds, and the resolution's
Riemann–Hurwitz cross-check, each pinned by live re-computations in the
checks.

**R.9.7 The honest odds.**  A full proof remains a boulder.  What has
changed since R.6 is the *kind* of statement within reach: finiteness
theorems per prime shape (A), possibly exclusion theorems per shape (B),
and a structural conjecture (C) whose truth would make ω = 3 a rank
computation on a fixed list.  ω ≥ 4 is where the problem's difficulty
now sits, and it is a different kind of difficulty — dimension, not
arithmetic — which is itself a finding.

### R.11 — The plan after entries 110–115 (2026-09-06): theory first, computation in its service

*Written after the deep look the user asked for.  Supersedes R.10's ordering; R.10's objectives stay as the ledger.*

**Where the record stands.**  Two finiteness theorems (shapes pqr and p²qr, Faltings-ineffective), with the base-locus half made structural for every shape (2.41).  For ω ≤ 2 the boxes (1,1), (2,1), (3,1), (2,2) are theorems and the frontier is Conjecture R_J, a genus-(J−1) curve problem per J with no concentration route (2.44).  Exclusion (what the goal needs) exists only class by class: the (1,1,1) box has 2456 dead and 488 finite classes, the (2,1,1) box 74,624 dead and 4,744 finite (entry 120: the prime-column lemma, a uniform valuation exclusion, did most of the killing at no cost); O2's first step (2.45) showed how a finite class dies — a quotient tower ending in a rank-0 elliptic curve — and where the tower stops: a genus-2 curve with a generic Jacobian and many points (𝒞₂), beyond Chabauty without a rank bound and beyond quadratic Chabauty without extra endomorphisms.  The killers are fifteen curves, eleven Legendre with λ ∈ {2, 4, 5, 8, 9, 16, 33, 25/9, 8/3} (2.42).  The genus census over both boxes: every finite component has genus ≥ 3, never 2; the deficit from (a−1)(b−1) is large and comes entirely from the base points.

**What the goal needs, again.**  Non-existence needs every class of every shape excluded, and there are infinitely many shapes.  Per-shape exclusion cannot be the proof; a uniform argument must carry the weight somewhere.  The only uniform statement so far is the elimination base-locus theorem.  So the priorities are the statements that hold for all shapes at once, with computation used to find and test them.

**P-A (theory, highest value) — the uniform ω = 3 finiteness theorem.**  Statement to aim at: *for every exponent shape (a,b,c), up to scaling there are finitely many MSS3 with split part p^a q^b r^c.*  By 2.41 the base-locus half is done *except* for the classes whose eliminated frame has one absolute exponent in all four labels (both relations trinomial-type: the locus is the intersection of two trinomial curves, possibly with a common component), which a uniform theorem must still handle uniformly; and every component of every class must have genus ≥ 2 or be dead by a uniform mechanism (wording corrected in entry 117 after the review).  Evidence: minimum genus 3 in both boxes, no genus-2 component anywhere.  Program: (1) a genus formula from the labels — the dichotomy theorem gives g = (a−1)(b−1) − Σ δ_P over the base points and the boundary, the base points are classified (2.40), so bound the δ_P from the classification and the multiplicities of the minors; (2) the genus-0/1 components: show they occur only in the label patterns where the monomial lemma or a rank-0 quotient kills them, uniformly.  Computation: a per-component table over both boxes (labels, bidegree, base-point census with multiplicities, exact genus) to conjecture the formula; the (3,1,1) box as the first test outside the data it was found on.  This would be the first theorem covering infinitely many shapes — still ineffective, but the right kind of statement.

**P-B (theory) — the killers as a theorem.**  The same fifteen curves recur across two boxes; the quotient models are y² = ax⁴ + bx² + c with ac a square and λ = (b − 2√ac)/(b + 2√ac).  Conjecture to test: the killing curve depends only on a local pattern of the labels (which elements involve the involuted frame, and how), so that a class with that pattern dies in every box.  Computation: from the (2,1,1) records, the map (label pattern → killer) and whether it is deterministic; if so, rank 0 is verified once per pattern and the pattern kills uniformly — a second uniform mechanism, and half of P-A's step (2).

**P-C (computation, effective exclusion of the pqr shape) — O2 continued.**  For the 1452 finite classes: enumerate the full involution group of each component and the quotient tower; every elliptic quotient → PARI rank (rank 0 kills); every genus-2 endpoint → collect the distinct curves (expect a handful, as 𝒞₁, 𝒞₂ for the genus-0 route) → Magma `RankBound`/Chabauty per curve (the online calculator's 120 s suffices for RankBound).  Ceiling without Magma: the elliptic-quotient kills plus an inventory of genus-2 endpoints.  A Magma license is the single most valuable tool decision for this objective.

**P-D (computation, data for P-A and P-B) — the (3,1,1) box.**  388,216 classes (290,064 with every frame at its top exponent), ~100 CPU-hours at 1.2 s/class, a multi-day job at low priority; its value is as test data for P-A's formula and P-B's pattern map, and a third finiteness theorem.  The user's decision; start it when approved.

**P-E — goal G: the free-frame reduction (DONE in its first instance, entry 116) and R_J (parked).**  Free-frame classes occur in every box (15% of (1,1,1), 15% of (2,1,1)); with the free label C or D the class dies by the ladder theorem of the two-frame shape — uniformly, before any sweep — and with the free label A or B by torsion cosets, degeneracy or rank-0 frame-condition curves (2.46).  Next: (i) a content-2 extension of A3.7/A3.8 for the weighted relation 2e(B) ∓ e(C) ± e(D) = 0, which would kill every free-frame class of every box by theorem; (ii) apply the reduction to the (3,1,1) box before sweeping it (shapes (3,1) and (1,1) are proven).  R_J needs a global idea (or Magma Chabauty per J).

**Decisions pending with the user.**  (1) Magma access (license or the online calculator: 120 s per run, RankBound fits); (2) launching the (3,1,1) sweep.

**Order of work.**  P-A(1) and P-C's inventory share the same per-class structure tables: build them together.  P-B after the (3,1,1) data.  P-D as soon as approved.  P-E when a new idea appears, not before.

## R.10 The plan after the two closed boxes (2026-09-06): objectives, in order

> **R.10 status (entry 113, 2026-09-06).** O1 DONE: the finiteness statement for shape (2,1,1) (2.43) — the rigorous pass upgraded 25378 of the 25,428 provisional classes (50 left) and the elimination base loci of all finite classes carry no admissible point. O4 sized (`compute.omega3.all_candidates` after `set_box`): the (3,1,1) box has 388,216 classes (290,064 with every frame at its top exponent; 31 labels), the (2,2,1) box 801,088 (621,836; 37 labels) — at the sweep engine's ~1.2 s/class about 100 and 200 CPU-hours, i.e. multi-day low-priority jobs (the user's decision); by the entry-111 theorem their finiteness statements would need, besides the sweep, only the elimination base loci of the classes whose deciding frame has one absolute exponent in all four labels. O3: the minor-map base locus classified over the whole (1,1,1) box (entries 110–111) and THE ELIMINATION BASE-LOCUS THEOREM proved (2.41): the base-locus condition is automatic except for the classes whose eliminated frame has one absolute exponent in all four labels — the finiteness statements now rest on Faltings-finiteness plus a finite trinomial computation. Next in O3: the coset lemma for the minor-map locus in general; the killers are fifteen curves, eleven Legendre (entry 112) — rank 0 verified, not explained. O2 (Sage) still pending the user's decision.

*Adopted after entries 103–109.  Supersedes the phase list of R.8 as the
active plan; R.7's goal G and R.9's map of attempts stand.*

**Where we stand.**  Box $(1,1,1)$: every class dead (1484) or Faltings-finite
(1460); base loci empty ⇒ *up to scaling, finitely many magic squares of squares
have split part $pqr$* (entry 104).  Box $(2,1,1)$: all $79{,}368$ new classes
decided — dead $12{,}132$, finite $41{,}808$ rigorously and $25{,}428$ with a
provisional genus, unknown $0$ (entries 107–108).  The elliptic killers are ten
curves up to isomorphism across both boxes.  The quadruple curves are pullbacks
of the circle under the minor map (entry 105), and their singular locus is now a
theorem (entry 109): base points of the minor map, singular points of the space
curve, or the toric boundary.  The engine decides a class in ~1 s.

**O1 — The finiteness statement for shape $(2,1,1)$** *(mechanical; a day of
CPU at low priority).*  (a) The rigorous pass over the $25{,}428$ provisional
classes: a Riemann–Hurwitz cross-check that avoids initializing the large
branch-value fields (gcd refinement over the branch field), or the bound with a
longer alarm on three workers, or Sage.  (b) The base loci of every finite class
(the entry-104 tool, minutes).  Output: Theorem A3.13, finiteness for the shape
$(2,1,1)$, by the same argument as $(1,1,1)$.

**O2 — The first exclusion theorem, "no MSS3 of shape $(1,1,1)$"** *(needs Sage
or Magma).*  The $1460$ finite classes: $304$ hyperelliptic models blocked by
positive-rank elliptic quotients (elliptic Chabauty), $1156$ curves of genus
$3$–$23$ whose rank-$0$ quotients are exhausted (Jacobian decomposition under the
frame symmetries; Chabauty–Coleman on quotients with rank below genus).  The
quotient tools of entries 105–106 produce the exact list.  **Decision point:** a
Sage installation in the WSL Ubuntu on this machine unblocks O2, the genus-$0$
parametrizations, and O1(a) at once.

**O3 — Uniformity in the exponents (attempt C, the theory thread).**  Done: the
trigonometric form, the minor formula, the singular-locus dichotomy.  Next, in
order: (i) the *base-locus theorem* — the base points of the minor map are
torsion points of bounded order and half-Pythagorean points, by the structure of
vanishing sums of few roots of unity (Conway–Jones) applied to the proportionality
of the two coefficient rows; (ii) *why ten curves* — the genus-$1$ quotients of
the quadruple curves as $(2,2)$-covers of the line branched over the torsion
set, their $j$-invariants from cross-ratios, hence a finite list for every box
$(a,1,1)$; (iii) the branch loci of the three frame double covers on $\Phi_f$
(the third frame in closed form) — the statement that would make ω = 3 a rank
question about a fixed list of twists.

**O4 — The next boxes** *(cheap with the fast engine).*  Seeded samples of
$1000$ classes of $(2,2,1)$ and $(3,1,1)$ (about a CPU-hour each) to test the
ten-curve list, the monomial multiples and the singular-locus picture where the
eliminated frame still has exponent $1$; then a first look at $(1,1,1,1)$
(ω = 4): the common-factor reductions and whether the elimination surfaces fiber
over ω = 3 curves (the reduction branch of G).

**O5 — Kept warm.**  The uniform ω = 2 theorem (A3.11), whose frontier is
Conjecture R_J (2.23/2.27/2.44) — NOT the P1 rigidity lemma, which was superseded
by the concentration theorem and Theorem A3.10 (entries 83–84); R_J needs a global
method (Chabauty on w² = 3(y^{2J}+y^{2J−1}+1) over ℚ(i), genus J−1: Magma, per J);
the S-unit framing for ω ≥ 4; the paper — the ω = 3 chapter (entries 97–113) is
now a coherent story with new mathematics in it.

**Retired.**  The local sieve (vacuous); PARI's factor on six-variable
resultants; the arithmetic-genus shortcut; median-based CPU estimates; the
towers on the $(2,1,1)$ box (optional, ~9 s per finite class, deferred).

## 0. Doctrine

1. **Both directions are the goal.** A constructed square is a proof.
   A nonexistence proof is a proof. A proof *modulo a named standard
   conjecture* (effective abc, Bombieri–Lang) is a publishable rung
   below. We climb whichever ladder moves.
2. **Every candidate argument passes the gauntlet** (A1.1, the
   real-boundary lemma of the Hill refutation, F5 local solubility,
   the near-miss anchors). We now know *four* ways proofs of this
   problem die: congruence endgames (A1.1), order/positivity endgames
   (A1.1), real-algebraic endgames (Hill §7), and effective-Chern
   bounds that ignore the nodes (A8 §1). The gauntlet is our immune
   system; it stays.
3. **The convergence finding is the compass.** Both fronts say the
   obstruction is *global arithmetic* — class-group structure (sphere
   side), one rigid differential (surface side), no local component
   (F5). So the plan concentrates force on the two places where
   global-arithmetic obstructions have exact laws: **class field
   theory** (Front 2) and **the Picard/Brauer arithmetic of $X$**
   (Front 1) — plus the one classical mechanism that ever finishes
   such problems outright: **descent with a height that decreases**
   (the F3/A2 mechanism).

## 1. The asset inventory (what we uniquely hold)

- **Geometry:** the only explicit symmetric-differential computation
  on $X$ in existence ($m_{\min} = 4$, $\eta_\star$ unique through
  degree 8, all-character vanishing at 5 and 6); node-passage
  theorems (≥ 3 triple points, sharp); the census reducing every
  unknown rational curve to the single web $\eta_\star$ at Lucas
  degree ≥ 3 (A8.16–A8.18).
- **Arithmetic:** the exact sphere dictionary
  ($r_3^*(3m^2) = 24\,h(-3m^2)$, one field $\mathbb{Q}(\sqrt{-3})$);
  three proven-necessary sieves annihilating all 1782 ordered congrua
  pairs to $m \le 1200$; the anatomy showing 36 kills live *inside*
  cosets of $\mathrm{Cl}^2$ — beyond every congruence and character
  condition (A9).
- **Function field:** the degree-halving descent (A2.L) proving the
  $k[t]$ analogues; Conjecture A2.C ⟺ no nondegenerate rational
  curves on $X$ — i.e. *the function-field problem is one geometry
  milestone away from fully solved*.
- **Meta:** the boundary theorems that prune dead strategy classes in
  advance; a 111-check verification culture; the acquired literature
  (Stoll–Testa and Horie–Yamauchi as the worked Picard/L-function
  playbook; Bruin–Creutz as the worked Brauer–Manin playbook; EMV +
  Schulze-Pillot + the spinor-genus papers as the composition toolkit).

## 2. The workstreams

Ordered so that each has (i) a first concrete action, (ii) a
deliverable that is valuable even if the grand goal stalls, (iii) an
honest statement of the wall it will hit.

### W1 — Close the geometry: the $k[t]$ theorem (the ripest fruit)

**Target.** Finish M11-J (the $\eta_\star$-web at cubic level and
beyond) → prove **A2.C**: no nondegenerate rational curves on $X$ →
**unconditional theorem: no nonconstant magic square of squares over
$k(t)$, any characteristic ∉ {2,3}** — the problem's exact analogue,
solved, standing alone as a paper. Simultaneously this makes the
Bombieri–Lang conditional ("at most finitely many squares") fully
explicit.

**Why believe it.** The web's line and conic levels closed with
nothing new; the cubic level is a finite, explicitly-bounded system
(A7.6 budget + A8.17 machinery); the AP families saturate every
freedom the census allows.

**First actions.** Enumerate the $\eta_\star$-integral cubic system
over the Lucas plane (the M11-J-2 plan in A8 §9); reuse the
resultant-peeling infrastructure; budget one cloud campaign for the
elimination certificates.

**Wall.** Degree-by-degree closure never *ends* by itself; the finish
needs either a degree bound for integral curves of a web on a
quasi-hyperbolic surface (a provable lemma — GFU-style Vojta towers
give exactly this shape; attempt it) or the Bruin–Ilten–Xu local
$\chi$ machinery to force contradiction for all degrees ≥ some $d_0$.
This is a real theorem-shaped wall, not a fog: attack it.

### W2 — The motive atlas of $X$ (make the surface modular)

**Target.** Compute $\operatorname{Pic}(\widetilde X)$ **with Galois
action**, the Brauer group, and — the ambitious summit — the
$L$-function of $X$: the full Stoll–Testa + Horie–Yamauchi program
executed on the magic-square surface. $b_2 = 766$, $h^{1,1} = 544$,
$h^{2,0} = 111$: decide whether $\rho$ is maximal, and whether the
transcendental motive decomposes into curve/K3 pieces.

**The creative lever (new here).** $X$ is the $(\mathbb{Z}/2)^8$
cover of the Lucas plane branched on 12 lines; $H^2$ splits into the
256 character eigenspaces *we already control* (the A8 descent
machinery was built for exactly this decomposition, just for
differentials). Each character corresponds to a double-cover of
$\mathbb{P}^2$ branched on a sub-arrangement of ≤ 12 lines — surfaces
that are rational, K3, or elliptic in low degree. **Build the
character-by-character atlas: which quotient carries which piece of
$H^{2,0}$.** If every transcendental class comes from K3 or
curve-product quotients, the motive of $X$ is modular in the
practical sense, the $L$-function is computable, and the surface
joins the cuboid as an arithmetically *rigid* object. That is the
gateway to W3.

**First actions.** Extend the A8 character bookkeeping from
$S^m\Omega^1$ to $H^0(K)$ (the 111 holomorphic 2-forms): compute the
character multiplicities of $H^{2,0}$ (finite, explicit — same
plane-level linear algebra); classify the 256 sub-arrangement double
covers by Kodaira type. Cheap, decisive, fully in-house.

**Wall.** 544 Picard classes with Galois action is a heavy
computation (Stoll–Testa did 64). Stage it; this is also the natural
collaboration surface (see W8).

### W3 — The arithmetic endgame, stated honestly (descent on twists)

**Fact to respect:** $X(\mathbb{Q}) \neq \emptyset$ — the degenerate
AP components carry rational points — so no naive Brauer–Manin
obstruction can kill "all rational points." The correct formulation,
and the plan's central Front-1 conjecture:

**Target statement (Conjecture E).** Every rational point of $X$ lies
on the degenerate locus (the 128 AP components and their known
companions). **Attack shape:** descent along the
$(\mathbb{Z}/2)^8$-cover. A nondegenerate point lifts to one of the
twisted covers $Y_\sigma$; degenerate points occupy an explicit,
computable set of twists. The dream theorem: *for every twist
$\sigma$ outside the degenerate set, $Y_\sigma$ is everywhere locally
solvable only for $\sigma$ in a family where a Brauer class
(computed via W2) obstructs.* Bruin–Creutz is the worked modern
template for the obstruction computations; the F4 congruence theory
(entries ≡ 1 mod 24, the ℓ ≡ 3,5 mod 8 divisor laws) is secretly a
statement about which twists are locally solvable — *reinterpret F4
as the local half of the descent, then hunt the global half.*

**Why this could actually close.** This is the one known mechanism
that kills rational points on varieties that *have* local points
everywhere — and the repo's F5 anomaly ("solvable mod everything")
is exactly the signature of a problem whose obstruction lives in a
Brauer class of a cover, not in congruences of the base.

**Wall.** Infinitely many twists; the finiteness must come from the
interaction of ramification with the 12-line arrangement. Unproven
territory. But every ingredient is now on our bench.

### W4 — The exact laws of the sphere: composition, spinor, Rédei
*(the flagship creative bet)*

**Target.** Upgrade the fourth sieve from "measured" to **law**. The
36 beyond-genus kills live inside cosets of $\mathrm{Cl}^2$: the
question "which classes inside a genus represent which co-norms" is
governed not by characters but by the *next* layer of class field
theory — spinor genera and, deeper, **Rédei symbols and governing
fields** (the exact reciprocity laws behind 2-parts of class groups
and 2-Selmer structure in twist families).

**The concrete creative hypothesis (H-Rédei).** *Each of the 36
beyond-genus kills is the vanishing/non-vanishing of an explicit
Rédei-symbol identity in $\mathbb{Q}(\sqrt{-3m^2})$; the gluing law
A9.1 forces a product of Rédei symbols to equal $-1$ while the grid
coupling forces it to equal $+1$.* If H-Rédei holds and the identity
is *uniform in $m$*, the pair desert becomes an all-$m$ theorem — and
because Rédei reciprocity is exact (not equidistributional), this
route is immune to the "large-$m$ equidistribution eventually defeats
class conditions" objection that dooms naive sieve-forever hopes.

**First actions.** (1) Take the fully-worked kill at $m = 725$ and
compute every Rédei symbol in sight; find the identity. (2) Repeat
across all 36; look for the uniform shape. (3) Formulate the fourth
sieve as a statement about lattice-coset spinor genera (the
arXiv:2104.08798 machinery, acquired, is literally about spinor
genera of lattice cosets — our congruence-conditioned
representations). (4) Connect to the 2-descent view: the four coupled
congrua conditions are 2-Selmer conditions on four coupled
congruent-number twists; Rédei symbols are the standard control
language there too — **the sphere front and the elliptic-curve front
are the same 2-adic object viewed twice; prove the dictionary.**

**Deliverable even if the summit fails:** the exact spinor/Rédei
anatomy of the desert — new mathematics about class groups of
$-3m^2$, publishable independently.

**Wall.** The heuristic threat: if the true asymptotic count of
surviving pairs grows, no exact law can kill all $m$; W6's model will
tell us which world we live in *before* we over-invest.

### W5 — Height descent and the abc bridge

**Target.** The only classical mechanism that fully finishes
problems of this species is descent on a decreasing height (F3;
A2.L). Two attacks:

1. **Transplant A2.L.** Dissect exactly which step of the
   function-field degree-halving descent fails over $\mathbb{Z}$
   (expected: the Wronskian/derivative step — the abc wall). Write
   the autopsy as a theorem: "A2.L transplants to $\mathbb{Z}$ given
   inequality (★)" where (★) is an explicit abc/Vojta-type radical
   inequality *specialized to the grid system*.
2. **The conditional capstone.** Prove: **effective abc ⟹ no MSS3
   with entries above an explicit bound $H_0$(abc-constants)** — and
   pair it with W6's verified search floor. A "proof modulo abc with
   explicit constants + finite verified check" would be a complete
   conditional resolution, the strongest statement anyone has ever
   had for this problem. The grid gives the multiplicative purchase:
   three squares in AP with common difference $D$ factor as
   $(q-p)(q+p) = (r-q)(r+q) = D$ with the congruum structure
   $D = 4uv(u^2 - v^2)k^2$ — radical-poor numbers forced into
   additive coincidences $d_3 = d_1 + d_2$, $d_4 = d_1 - d_2$:
   exactly abc's habitat.

**First action.** The A2.L autopsy (one focused session); then the
$d_1 + d_2 = d_3$ radical analysis on the known near-miss data.

### W6 — The telescope (existence direction) and the actuarial model

**Target.** Turn the sieves into a search instrument. Extend the
pair-desert computation beyond $m = 1200$ until survivors appear
(they must, eventually, or W4's all-$m$ theorem is *true* — either
outcome is decisive intelligence). Each surviving $m$ is a **golden
center**: run the full 8-point sphere-gluing search only there, with
the class-group data steering. If a magic square of squares exists
within reach, this finds it years before brute force; if none is
found, the survivor statistics calibrate the fourth sieve.

**The actuarial model.** Build the honest random model of the
9-point grid correlation *with all known structure priced in*
(mod-24/72 laws, class coherence, sieve survival rates): compute the
expected count of MSS3 with entries ≤ $H$. This number decides
resource allocation between the two directions — and it is
publishable heuristic evidence either way (the BTVA + BL heuristic,
made quantitative for the first time).

**First actions.** `congrua_search` extension to $m \le 10^4$ with
sieve instrumentation; the model as a short compute module with
pinned data.

### W7 — Exact counting identities (the modular long shot)

**Target.** The pair-count and slice structures are correlations of
class numbers $h(-3m^2)$ — the natural home of **Hurwitz–Kronecker
class-number relations** and Eichler-type identities. Hunt for an
exact identity expressing (a signed, symmetrized version of) the
congrua-pair count as a finite combination of modular coefficients.
If found, vanishing to $m \le 1200$ plus a Sturm-type bound would
*prove* vanishing for all $m$ — the "verify finitely many
coefficients, conclude identically zero" endgame. Honest obstacle,
stated up front: the positivity/ordering conditions in the true
count break modularity; the workstream's real question is whether a
signed version both (a) is modular and (b) still dominates the true
count. Timeboxed probe.

### W8 — Force multiplication (papers and people)

The program is now sitting on at least three papers that the
relevant community does not know exist:

1. *Explicit symmetric differentials and rational-curve rigidity on
   the magic square surface* (A8: executes BTVA's "out of range"
   computation; node passage; the $\eta_\star$ web; A8.18).
2. *The discrete-sphere structure of magic squares of squares*
   (A9: the dictionary, the sieves, the beyond-genus anatomy).
3. *The refutation of arXiv:2510.08286* (done — shipped to the
   author; post publicly after the exchange).

Writing 1–2 for arXiv and engaging the named experts
(Várilly-Alvarado — whose CV shows he still popularizes exactly this
problem; Bruin; Stoll) is not vanity: **W2/W3 (Picard at rank 544,
descent obstructions) are the exact specialties of these groups.**
The fastest path to a full proof plausibly runs through making this
program public and collaborative at the right moment — after W1
lands the function-field theorem as the calling card.

### W9 — The wild reserve (timeboxed, gauntlet-first)

Probes, each pre-registered with its falsification test, none funded
past a week without a survival signal:

- **Arithmetic jets (Buium):** is there a $\delta$-arithmetic avatar
  of $\eta_\star$ — an arithmetic differential equation vanishing on
  $X(\mathbb{Z}_p^{\mathrm{ur}})$ constraining rational points the
  way $\eta_\star$ constrains curves? (The "differentiate a point"
  dream. Probably dies at the first computation; the analogy is too
  pretty not to spend five days on.)
- **Quaternionic rigidity:** rewrite the 8-point gluing on
  $\mathcal{S}(3m^2)$ as ideal identities in the Venkov quaternion
  parametrization (EMV, acquired); hunt a norm-form identity that
  the grid coupling violates.
- **Governing fields:** the 36 kills as splitting conditions in an
  explicit governing field over $\mathbb{Q}(\sqrt{-3})$ — if one
  field governs all $m$ in a residue family, W4 gets its uniformity
  for free.

### W10 — The additive layer: the S-unit front (opened by the realignment, P1)

The terminal layer (§R.1): a magic square *is* an additive quadruple
in $D(m)$, and $D(m) = \{|\mathrm{Im}(z^2)| : z \in \mathbb{Z}[i],\
|z|^2 = m^2\}$ turns an additive triple into a six-term vanishing
sum $w_1 + w_2 - w_3 - m^4/w_1 - m^4/w_2 + m^4/w_3 = 0$ with
$w_j = z_j^2$ on the norm-$m^4$ torus — S-unit-equation habitat
(check `a3.zi_reformulation`). Program: **A3-S1** the reformulation,
formalized and pinned (done with this entry); **A3-S2** unconditional
no-triple theorems for small $\omega(m)$ — each is a genuine
nonexistence slice of the open problem; **A3-S3** rigorous upper
bounds toward the convergent heuristic; the abc bridge (W5) plugs in
here as the same equation's radical analysis.

**First action.** Classify the degenerate subsums of the six-term
relation (they must correspond exactly to $U = \pm V$ and
sign-trivialities — provable), then attack $\omega(m) = 1$ (single
split prime: $D(m)$ is an explicit geometric progression of
congrua) and $\omega(m) = 2$ by 3-term unit-equation methods.

## 3. Sequencing and dependencies

```
W10 (additive/S-unit) ─────────── the terminal layer ──────┐
W1 (k[t] theorem)  ──────────────► paper #1, calling card ─┤
W2 (motive atlas) ──► W3 (descent endgame)                 ├─► W8 (community) ─► full-proof push
W4 (rigidity invariant) ◄─┬─► W6 (ladder telescope)        │
W5 (abc bridge → W10)     └── calibration loop ────────────┘
W7, W9: timeboxed probes feeding W4/W2
```

Near-term order of operations: **W2-atlas first actions** (cheap,
in-house, unlocks the most), **W4 step (1)** (the $m = 725$ Rédei
computation — one focused session, highest information density),
**W1 cubic campaign** (cloud), **W6 extension** (background compute),
**W5 autopsy** (one session). W3 waits for W2; W8 waits for W1.

## 4. Milestones (acceptance = suite-verified, tagged, logged)

| ID | Statement to prove/compute | Workstream |
|---|---|---|
| M13-J | ✅ **SUPERSEDED by M13-N (2026-09-02): A3.10 is PROVEN** — the rigidity SYSTEM (not the one-equation lemma below) is what the ladder produces, and it is dead by concentration. Historical record: 🔬 2026-08-30 — **A3.10 (p²q²) REDUCED, not proven; pivot to the uniform program (P1)**. The (2,2) box partitions with zero gaps (`a3.p2q2_accounting`): 1008 machine + 34+26 A3.8 sub-boxes + 32 ledger (24 G3 + 8 H3) + 44 replications. The 18 j-children are p↔q transposes of k-children, so only the 26 k-children remain; 12 close rigorously (collapsed-valuation, x⁴+y⁴=2z², squeeze/pinch), 14 reduce to the **rigidity quartic c₂⁴−6c₂²s₂²+s₂⁴ = c₁⁴−s₁⁴** (`a3.p2q2_reduction`). **Corrected same day (entry 72): the bare quartic surface HAS a point, (1369,3320,1017,320) at height ~3300 — not a frame point (neither c²+s² is a square).** The real lemma is the **frame version** (both c²+s² perfect squares): empty on prime frames to 2000 and on all primitive Pythagorean frames with generators < 300; in Gaussian-prime form Re(ρ⁸) = N(π)²Re(π⁴), where primality gives the lever p ≡ 1 mod 16. Attack = Gaussian-prime arithmetic, not K3 geometry. **Descent (entry 73):** (R₄−I₄)(R₄+I₄)=p²A₄ splits p² into one factor ⟹ 2q⁴ = p⁴D² + (A₄/D)² over divisors D of A₄ — a finite check per prime, EMPTY for every p < 10⁶ and all q; D=±1 is Fermat x⁴+y⁴=z⁴, D=±A₄ is Ljunggren; Case N (D=c₁±s₁) ⟺ ρ⁴ = π² + K(1+i); general intermediate D OPEN (`a3.rigidity_frame_lemma`). **Intermediate case (entry 74):** the obstruction is quadratic but not local; "T square" is an integral point on the congruent-number curve y²=x³−A₄²x, which always has rank ≥ 1 (the frame point) — so no Selmer argument; the lever is the fourth power: quartic-residue conditions at primes of D, E, R₄, I₄, K plus the 2-adic (mod 32/64) and combination-prime families kill **all 3128 intermediate cases to p<15000** — the equation is exact (no unit) so every condition is a fixed equality (`a3.rigidity_quartic_sieve`, self-tested end to end). A sieve complete on data, not a proof. **Reciprocity verdict (entry 75):** two lemmas PROVEN — the Class Lemma (every prime of A₄ is ≡ ±1 mod 16; with the order-16 lemma the rigidity lemma is a theorem for ~96% of split primes) and the 2-adic Lemma (D ≡ E ≡ 1 mod 16); and the [D][E] condition-sum is ≡ 0 on every transparent case — quartic reciprocity is a CONSISTENCY, not an obstruction, so the classical route is closed; the residual obstruction is at the primes of R₄, I₄ (transversal). `a3.rigidity_reciprocity`. **Height argument (entry 76):** PROVEN that any solution is an integral point P_sol = (X², 2IRX) on the congruent-number curve y² = x³ − A²x with descent image (1,2,2) = that of the frame point, so P_sol ∈ P₀ + 2E(ℚ); a validated complete 2-descent (`compute/selmer_descent.py`) gives Selmer rank bounds {1: 4, 2: 5, 3: 5} on transparent p < 6000 — rank-1 primes reduce to effective integrality of odd multiples (EDS/Baker, standard, not done); higher-Selmer primes have undetermined rank. `a3.rigidity_height`. **RANK-1 THEOREM (entry 77), PROVEN with no heights:** on the p-minimal model P₀ reduces to (0,0) while P_sol reduces to O, and P_sol = kG + T₀ with the same T₀ and k, m odd — in the cyclic group ⟨G̃⟩ every case contradicts (parity, or two distinct order-2 points). The rigidity lemma is now a THEOREM for every non-transparent prime and every transparent prime of 2-Selmer rank 1 (21 of 67 transparent p < 30000); the 46 higher-Selmer transparent primes remain (rank undetermined). `a3.rigidity_rank1_theorem`. **Rank certificates (entry 78):** parity is free (root number of E_n by n mod 8; Selmer parity matches it on every transparent prime): 27 of the 46 have EVEN rank ≥ 2 (need a rank-2 argument, not a certificate); 19 have rank 1 or 3, and L′(E,1) ≠ 0 certifies rank 1 unconditionally (GZK). `compute/lseries_cm.py` (CM twist coefficients, controls to 12 digits) certified p = 337, 1201, 6353, 15073 (L′ = 2.1048, 0.4962, 1.5905, 0.2777, tails ≤ 10⁻⁵) → 25 of 67 transparent p < 30000 proven; 15 odd-rank primes have conductors beyond this machine and need PARI (`ellrank` / Cassels–Tate). `a3.rigidity_rank_certificates`. **PARI certificates (entry 79):** PARI/GP 2.17.4 (portable extraction) `ellrank` on all 67 curves: 32 certified rank 1 → proven; **Rank-r criterion** (T̃₁ ∉ 2⟨G̃ᵢ⟩ with 2-saturated generators ⟹ no solution) proves 4 rank-2 primes (3137, 8369, 9473, 13633) and provably fails for 3 (2657, 9137, 29201); 22 rank-2 curves lack their second generator (beyond effort 20); the 2-descent is BLIND at p (2 a quartic residue, trivial localization); segmented L′ certifies p = 4001, 4657, 4817 (Ш with 4-torsion). **39 of 67 transparent p < 30000 proven**; 28 remain (22 missing a generator, 3 criterion-fails, 3 huge conductors). `a3.rigidity_pari_certificates`, `compute/pari_rank.py`, `compute/data_pari_ranks.json`. **N4 verdict (ω=3 box (1,1,1)): valuation pruning weakens to 48%; 464/552 genuine patterns survive the machine, but only 27 orbit-families, 6 with a single-prime lever.** ω≥3 does NOT reduce for free. | W10 |
| M15-G | 🏆 **2026-09-07 (entry 132) — THE OCTIC TOWERS CLOSED BY MAGMA: eight more (1,1,1) classes dead (R.13 path 2).** The user ran `compute/qc/magma_towers131.m` in the online calculator: C_a and C_b have rank 1 (2-descent), Mordell–Weil group ℤ/2 × ℤ/4 × ℤ proved, and Chabauty + the Mordell–Weil sieve give exactly seven rational points each, with u ∈ {0, ±1, ∞, −1/5} (degenerate or a non-square): both frames of every octic class dead. Tally dead 2798 / finite 146; the towers are closed except the eight genus-25 (6,6) classes. `compute/qc/magma_towers131.out.txt`; `a3.towers_magma`; suite 214. | W10 |
| M15-F | 🏆 **2026-09-07 (entry 131) — THE GENERAL BIELLIPTIC TEST; the genus-2 curves of the octic towers; four more (1,1,1) classes dead through the LMFDB (R.13 path 2).** A genus-2 curve is bielliptic iff a Möbius involution permutes its six branch points, and such an involution fixes none of them: one candidate per perfect matching (15), built exactly and tested (`compute/qc/bielliptic_test.sage`, five controls). The twelve octic tower classes' odd quotients are three genus-2 curves, none bielliptic (the E₁×E₂ QC route is closed there). C_c: w² = u⁵ − 4u⁴ + 6u³ + 12u² + u is the LMFDB curve 1408.b.180224.2 (Jacobian rank 0 by 2-descent; torsion ℤ/2 × ℤ/8); its five rational points, enumerated from the 16 torsion classes, are all degenerate: four classes dead. C_a, C_b have rank ≥ 1 (infinite-order known points) and need Magma (`compute/qc/magma_towers131.m`). Tally dead 2790 / finite 154; `a3.towers_genus2`; suite 213. | W10 |
| M15-E | 🏆 **2026-09-07 (entry 130) — THE TOWERS' BIELLIPTIC MODELS: twelve open (1,1,1) classes dead (R.13 path 2).** Eight have G₁ (2.47) as a frame's level-0 model, four have F₁ = t⁶ + 11t⁴ − 5t² + 1 (quotients 352b1, 352c1 of rank 1), decided by the same bielliptic QC + E₁×E₂ sieve; every rational point degenerate, the frame dead. Tally dead 2786 / finite 158. `compute/qc/qc_general.sage` (the pipeline for any even sextic); `a3.towers_bielliptic`; suite 212. The remaining 20 tower classes need a genus-2 rank bound (Magma). | W10 |
| M15-D | 🏆 **2026-09-07 (entry 129) — ORIENTATION: what the open classes share (R.13 path 1).** The height system's rows are functions of the flip pattern of the signed exponent vectors (Theorem A3.OR, verified row by row on 52,719 classes); Theorem T1 — three labels of a circuit that never flip relative to one another kill the class — is uniform in ω and the shape, explains a third of all local kills and fires on no open class; the open classes are the orientation-generic ones with a feasible prime hierarchy (a third balanced, the rest forced to a spread, some above 10⁹). `compute/orientation.py`, A12; `a3.orientation`; suite 211. | W10 |
| M15-C | 🧭 **2026-09-07 (entry 128) — THE (1,1,1,1,1) BOX and the trend.** The column canonical form (linear in the number of frames, reproducing both smaller ledgers exactly); 497,166 five-frame classes; the lemma leaves 44,882; the height system kills 15,972 (35.6%), caps none, leaves 28,910 open with up to five A/B deficits. Kill rates 76.8% → 55.5% → 35.6% at 3 → 4 → 5 frames: the local method decays with ω. `a3.omega5_box11111`; suite 210. | W10 |
| M15-B | 🧭 **2026-09-07 (entry 127) — THE (1,1,1,1) BOX: the local method weakens with the number of primes.** 48,854 four-frame classes; the lemma leaves 7,087; the height system kills 3,935 (55.5%, against 76.8% of the (1,1,1) lemma survivors), caps none, leaves 3,152 open; the three-frame regularity "no two A/B deficits" fails (801 / 94 / 1 open classes with 2 / 3 / 4). `compute/omega_boxes.py` (validated on the (1,1,1) ledger); `a3.omega4_box1111`; suite 209. R.13 path 5 answered: the uniform argument must come from what the survivors share, not from counting deficits. | W10 |
| M15-A | 🏆 **2026-09-07 (entry 126) — THE (3,1,1) BOX with the lemma and the height system first.** 290,064 new three-frame classes: the prime-column lemma kills 281,362 (97%), the height system 6,464 + 16 (cap + search), and the curve engine decides the 2,222 left in 7.53 CPU-hours: tally dead 287,858 / finite 1,025 / finite* 1181 / undecided 0. Stage A took 44 seconds. `compute/data_omega3_box311.json.gz`; `a3.omega3_box311`; the inventory extended to the third campaign; suite 208. | W10 |
| M14-Z | 🧭 **2026-09-07 (entry 125) — THE PAIR SEARCH; the local method exhausted for the survivors.** A pair of primes determines the third through a column's divisibility, so enumerating pairs ≤ 500 in every column finds every solution whose two smallest primes are ≤ 500: over all 170 + 1,388 open classes no candidate passes every divisibility (no near miss). Version 3 (the even-S constant for 2, ±1, ±1 circuits) changes no verdict: the survivors are unbounded whatever the constants; the binomial rows admit no reality sharpening. `compute/height_pairs.py`; `a3.height_pairs`; suite 207. Next: the survivors are curve problems — their elimination curves, towers and bielliptic models (entry 118's pipeline) and the (3,1,1) box with the lemma and the height system applied first. | W10 |
| M14-Y | 🏆 **2026-09-07 (entry 124) — THE REALITY SHARPENING (T′).** A trinomial congruence is the shadow of the exact identity π̄^{4M}W = π^{4M}W̄, so S₁ = S/π^{4M} has S₁Ḡ real and |S₁| ≥ ∏ p_k^{|fmax+fmin|}: the trinomial exponents drop from the spread to 2·min(fmax, −fmin), often 0 or negative. Re-deciding the 214 + 1,960 unbounded classes: **44 + 572 more impossible for all primes**; open 170 + 1,388. Tallies (1,1,1) dead 2774 / finite 170; (2,1,1) dead 77,980 / finite 1,388. Version 2 of `height_system` (certificates carry their version); `circuit_identity_tests`. | W10 |
| M14-X | 🏆 **2026-09-07 (entry 123) — THE HEIGHT SYSTEM (Theorem A3.HS, A11): CP.4 sharpened and completed.** For λ = ±1 the binomial congruence is read on the rational integer A ∓ Ā (p^{2g} | Im A or Re A: the exponent doubles, 4 | Im A); every trinomial circuit gives π^{4M} | S with S ≠ 0 (equilateral / collinearity); same-integer binomials of different columns multiply; CP.2 lower bounds. Linear programming in log p with exact Farkas certificates: **(1,1,1): 274 of the 488 open classes impossible for all primes, 214 unbounded; (2,1,1): 2,732 impossible + 52 capped (≤ 6561) and searched to death, 1,960 unbounded.** Tallies (1,1,1) dead 2730 / finite 214; (2,1,1) dead 77,408 / finite 1,960. The first unconditional, curve-free kills of the record. `compute/height_system.py`, `height_search.py`, `height_identities.py`; `a3.height_system`; suite 206. | W10 |
| M14-W | 🏆 **2026-09-06 (entry 120) — THE PRIME-COLUMN LEMMA FOLDED INTO THE LEDGER (Theorem A3.PC, proposed by the independent review).** At every split prime of the center the maximal absolute exponent is attained by ≥ 3 of the 4 labels (v_p(d_X) = 2(a − |e_X|) exactly when e_X ≠ 0; the minimal valuation among U, V, U+V, U−V occurs ≥ 3 times). Uniform in primes and exponents; a free frame is impossible outright. (1,1,1): 956 finite classes dead → **dead 2456 / finite 488**; (2,1,1): 58,592 finite classes dead → **dead 74,624 / finite 4,744**; every free-frame class fails (P-E retired), the sixteen 𝒞₂ classes pass. `compute/prime_column.py`; `a3.prime_column` (additive half exhaustive, Gaussian half on the engine's own elements, census recomputed record by record); suite 202. R.12 written. | W10 |
| M14-V | ⚠ **2026-09-06 (entry 119) — THE TWIST AUDIT, CONTINUED.** The reviewer's follow-up found three more copies of the constant-dropping step (the two W-route sites of `omega3_quotients`, `omega3_unknowns._rank0_model_points`; live control 337(t⁴+1) with t = 4/3 missed) and `gp_model`'s `int()` truncation; repaired; the 108 quotient/two-step kills re-decided with the correct models: all stand (two had dropped the sign −1 in one branch); no verdict changes; source guards + two live controls in `a3.omega3_twist`. The reviewer's second document (`docs/PROOF-DIRECTIONS-2026-09-06.md`) also states a **universal prime-column lemma** (at every split prime of the center, the maximal absolute exponent occurs in ≥ 3 of the 4 labels): proof checked by hand, census reproduced (excludes 956 of the finite (1,1,1) classes and 58,592 of the finite (2,1,1) classes, every free-frame class among them; the sixteen 𝒞₂ classes survive it) — NOT yet folded into the ledger: a decision for the owner (see the response document). | W10 |
| M14-U | 🏆 **2026-09-06 (entry 118) — THE BIELLIPTIC DESCENT COMPLETED: the sixteen classes of entry 115 are dead.** The review's descent (verified: sum-of-squares forms, F − G = −32a²b²(a²−b²), gcd ∈ {1, 8, 25, 200}) sends every 𝒞₂-point with a square coordinate to G_δ: z² = δ(25t⁶−29t⁴+11t²+1), δ ∈ {1,2}; Bianchi–Padurariu's bielliptic quadratic Chabauty (Sage, p = 11, 13) plus a Mordell–Weil sieve on E₁ × E₂ (written here; controls survive, every candidate dies) give G₁(ℚ) = {(0,±1), ∞±}, G₂(ℚ) = {(±1,±4)} ⇒ t ∈ {0, ±1, ∞} ⇒ degenerate lifts. (1,1,1) tally: dead 1500, finite 1444. The genus-0-quotient route is closed end to end. `compute/qc/`; `a3.omega3_bielliptic`; suite 201. | W10 |
| M14-T | ⚠ **2026-09-06 (entry 117) — THE TWIST AUDIT (the independent review's finding 1): genus-1 models had dropped non-square constants (quadratic twists) in `_disc_model`, `gp_model` and the towers' `int_coeffs`; repaired (`squarefree_part`, `square_part_of_gcd`); every engine, tower, quotient, two-step and attack kill of both boxes re-decided with the correct twists.** (1,1,1): all 206 flagged engine kills survive, 8 tower kills void (4 rescued by the free-frame reduction), tally {'dead': 1484, 'finite': 1460}; (2,1,1): 4581 flagged, 0 lost, tally {'dead': 16032, 'finite': 63336}. No finiteness statement changes. The review's findings 2–4 applied (cache key, PARI discovery, four summary corrections); the bielliptic descent for 𝒞₂ adopted as the next O2 computation; the certification architecture scheduled. `a3.omega3_twist`; suite 200. | W10 |
| M14-S | 🏆 **2026-09-06 (entry 116) — THE FREE-FRAME REDUCTION: ω = 3 → ω = 2, goal G's first instance.** A class with a frame in exactly one label L: for L = C or D the relation without e(L) is a signed three-term relation of the two-frame box, killed by the ladder theorems (A3.7/A3.8/A3.9/A3.10) — DEAD BY THEOREM before any sweep; for L = A or B the weighted relation 2e(B) ∓ e(C) ± e(D) = 0 dies by torsion cosets (Lemma B), degeneracy, or a rank-0 elliptic frame-condition curve y² = P² + Q² (the killers of 2.42 are exactly these curves). (2,1,1): 3900 of 8130 finite free-frame classes dead (3576 by A3.8), tally {'dead': 16032, 'finite': 63336}; (1,1,1): the 444 free-frame classes (all dead already) re-derived. `compute/omega3_freeframe.py`; `a3.omega3_freeframe`; suite 199. | W10 |
| M14-R | 🧭 **2026-09-06 (entry 115) — O2 WITH SAGE: the 24 genus-0-quotient classes — EIGHT DEAD (genus-5 hyperelliptic models y² = N² + 4M², genus-2 quotients, the curve 𝒞₁ with the involution s ↦ 1/s whose elliptic quotient is 11a3 of rank 0, degenerate lifts), SIXTEEN on one genus-2 curve 𝒞₂ (≥ 14 rational points, presumably simple Jacobian: Magma `RankBound` pending, script in compute/magma/).** Tally of the (1,1,1) box: dead 1492, finite 1452. Sage 10.7 installed in WSL. R.11 written: the prioritized plan (uniform ω = 3 finiteness theorem first; the killers as a theorem; O2's quotient towers; the (3,1,1) box as data; Magma the key tool decision). `a3.omega3_genus0`; suite 198. | W10 |
| M14-Q | 🧭 **2026-09-06 (entry 114) — the (2,1,1) box has no provisional class (the last 50 re-resolved; tally {'dead': 12132, 'finite': 67236}); R_J has no concentration route (the trinomial y^{2J}+y^{2J−1}+1 irreducible over ℚ(i) and the cyclotomic fields up to ℚ(ζ₂₄) for J ≢ 1 mod 3); the "P1 rigidity lemma" pointer withdrawn (superseded since entry 84) — O5 now names R_J.** `a3.rj_trinomial`; suite 197. | W10 |
| M14-P | 🧭 **2026-09-06 (entry 113) — THE FINITENESS STATEMENT FOR SHAPE (2,1,1): up to scaling, finitely many MSS3 with split part p²qr (Faltings-ineffective).** (a) The rigorous pass: every provisional component re-resolved with the field-free cross-check — 25378 of 25,428 classes upgraded, 50 left; tally {'dead': 12132, 'finite': 67186, 'finite*': 50}; genera 7..53; 16.7 CPU-h. (b) The elimination base loci of all 67236 finite classes: 1982 rational base points, all degenerate, no admissible point or line; the entry-111 theorem's prediction ({'empty': 26390, 'trinomial': 22474, 'torsion': 18372}) agrees with the pass everywhere. `a3.omega3_box211_finiteness`; suite 196. O1 DONE. | W10 |
| M14-O | 🧭 **2026-09-06 (entry 112) — THE KILLERS ARE FIFTEEN CURVES, ELEVEN OF THEM LEGENDRE (a correction to "ten").** All 31 rank-0 coordinate/joint quotient models on record identify as eleven curves (the ten of entries 100/107 + 120b2, 16 kills in entry 105), all with full 2-torsion: y² = x(x−1)(x−λ), λ ∈ {2, 8/3, 25/9, 4, 5, 8, 9, 16, 33}; every even model y² = ax⁴ + bx² + c has ac a square and λ = (b − 2√ac)/(b + 2√ac). The two-step route (entry 106) used four more: 30a1, 240b1, 30a2, 240b2. Rank 0 verified, not explained; branch points show no uniform pattern. `a3.omega3_killers`; suite 195. | W10 |
| M14-N | 🧭 **2026-09-06 (entry 111) — THE ELIMINATION BASE-LOCUS THEOREM: the base-locus half of every finiteness statement is structural.** The coefficient of w_f^j of a relation has #{l_e = j} + #{l_e = −j} signed monomial terms; a monomial never vanishes on the torus, a binomial vanishes on a torsion coset, and unique factorization in ℤ[i] puts no pair of frame ratios of distinct primes on a proper torsion coset (Lemma B). So the elimination base locus is empty, or on torsion cosets, or — only when the eliminated frame has the same absolute exponent in all four labels — the intersection of two trinomial curves. On the (1,1,1) box the label prediction (834 empty-type, 516 torsion-type and 218 trinomial-type classes among the 1568 finite at entry 104) agrees with the exact loci in every class; the 218 trinomial-type classes are exactly the self-base classes of the minor-map census (18 + 200 low-bidegree, that census now extended to all finite classes). `compute/omega3_finiteness.elimination_type/elimination_locus`; `a3.omega3_elimination`; suite 194. | W10 |
| M14-M | 🧭 **2026-09-06 (entry 110) — THE BASE LOCUS OF THE MINOR MAP, CLASSIFIED; the field-free cross-check; the rigorous pass launched.** In the torus coordinate the relations are quadratics αw² + βw + γ (γ conjugate to α); the base locus is the common zero set of α₁γ₂ − α₂γ₁ and α₁β₂ − α₂β₁ (≤ 9 monomials; a torsion coset plus a one-variable equation of degree ≤ 4 when both α's are monomials: 262 of 1264 pairs). Census over all 1264 certified classes (`compute/omega3_minors.base_locus_points`): curves = the same-prime cosets w_g = ±w_h^{±1} and, for the 18 classes with β₁ = β₂ = 0 (the eliminated frame in all three elements of both relations), the quadruple curve itself, a (4,4) curve of genus 7 or 9 (equal frames (same prime) in 36 classes; perpendicular frames (same prime) in 36 classes; the quadruple curve itself in 18 classes; conjugate frames (same prime) in 6 classes; conjugate-perpendicular frames (same prime) in 6 classes); lines = degenerate/boundary only (t_h = ±i in 68 classes; t_h = 0 in 36 classes); isolated points with coordinates degenerate, ±i, torsion n ∈ {3,6,8,12}, half-Pythagorean, tan-2θ-rational, quartic; **outside the 18 self-base classes no base point is an admissible frame pair** (on those 18 it is the class's own finiteness). The Riemann–Hurwitz cross-check without nfinit (`exact_ramification`: fiber squarefree degrees + the resolution's branch counts) reproduces the old one 100× faster; the rigorous pass over the 25,428 provisional (2,1,1) classes runs on it (3 workers, low priority). `a3.omega3_baselocus`; suite 193. | W10 |
| M14-L | 🧭 **2026-09-06 (entry 109) — THE SINGULAR-LOCUS DICHOTOMY IS A THEOREM; the plan reorganized (R.10).** With the eliminated frame at exponent 1 the relations are quadratics in w_f and the space curve Γ projects onto Φ_f: a vertical tangent means a double root of both quadratics, hence proportional quadratics (a base point of the minor map); two points of Γ over one point means two common roots, again proportional; so every singular point of Φ_f is a base point of the minor map, a singular point of Γ, or on the toric boundary. Verified exactly on all 492 exceptional points of the entry-105 census: all are base points (rank 0 or 1 rows; the old test used a non-squarefree gcd) except 28 boundary points over t = ±i with t_f = ±i; corrected census: 1248 of 1264 curves entirely on the base locus. R.10 = the reorganized plan: O1 finiteness for (2,1,1), O2 the exclusion theorem (Sage/Magma), O3 the base-locus theorem and the ten curves, O4 the next boxes, O5 kept warm. `a3.omega3_minors` updated. | W10 |
| M14-K | 🧭 **2026-09-05 (entry 108) — NO UNKNOWN CLASS IN THE (2,1,1) BOX: the 188 unknowns decided (164 dead, 24 finite), the six degenerate classes dead; box dead 12132, finite 41808 + 25428 provisional.** Routes (`compute/omega3_unknowns.py`): the two-step trick one level up (a genus-1 component's own quartic model through a genus-0 quotient; rank-0 genus-1 quotients with preimages), the pullback at cap 12 for genus-0 components quadratic in a variable, and the decisive CONJUGATE-COMPONENTS KILL: 156 classes whose "genus-1" components are irreducible over ℚ but split over ℚ(√3) into conjugate pieces, so their rational points are the finitely many common zeros of the rational and √3-parts, none admissible. In the engine: a failed absolute-irreducibility certificate no longer blocks finiteness (the dichotomy); one-frame common factors t = ±1 are dead. Next for the shape's finiteness statement: the rigorous pass on the provisional third, then the base loci. `a3.omega3_unknowns`; suite 192. | W10 |
| M14-J | 🏁 **2026-09-05 (entry 107) — THE (2,1,1) SWEEP DONE: all 79,368 new classes decided (44.9 CPU-hours); dead 11962, finite 41784 + 25428 provisional, unknown 188; the killers are TEN curves up to isomorphism.** The five curves of (1,1,1) return with five twists/neighbours (24a1, 15a3, 528j2, 240d2, 240d4; eight j-invariants; conductors from {2,3,5,7,11}): the finite-list reading of the elliptic killers survives the exponent growth (R.9.C). Monomial relations to angle multiple 4 (5 in the residue). Singular loci sampled: the same torsion/±i/algebraic-tail picture. Open: genus-0/1 components at high bidegree (no elliptic/parametrization route there yet), the provisional third (cross-check without nfinit, or Sage), then the finiteness statement for the shape. `a3.omega3_box211_sweep`; suite 191. | W10 |
| M14-I | 🧭 **2026-09-05 (entry 106) — THE TWO-STEP QUOTIENT ROUTE: 36 more classes dead through a second involution of the joint quotient; box dead 1484, finite 1460.** The joint quotient E = Φ/σ of genus 1 has no quadratic model (bidegree up to (4,4) in both natural models); a second involution descends to E and W = E/τ̄ has lower degree — W of genus 1: rank 0 + preimages on E + squares on the curve; W of genus 0: parametrization, E's own quartic y² = Δ(λ), rank 0 (`compute/omega3_quotients.py`: two_step_joint, two_step_joint_more, _w_route). 32 kills through t → −1/t, 1/t; 4 through the swap. Blocked: 16 (non-quadratic W), 28 (no second involution). Bug fixed: cubic models never "complete" (point at infinity uncounted; no earlier kill affected). The 24 genus-0 quotients (hyperelliptic curves) need a rational parametrization of a (4,6)/(3,6) rational curve: Sage/Magma territory (WSL Ubuntu is available for a Sage install). `a3.omega3_quotients` extended; suite 190. | W10 |
| M14-H | 🧭 **2026-09-05 (entry 105) — THE MINOR FORMULA: every quadruple curve is a pullback of the circle; the singular locus is the base locus of the minor map plus torsion fibers; 72 finite classes die through rank-0 quotients by their involutions.** In the frame to eliminate every element is linear in (X, Y, N) = (2c s, c² − s², c² + s²), so the relations are two linear forms and Res = 4(D_X² + D_Y² − D_N²) (the classical resultant of two binary quadratics): Φ_f is a component of the pullback of X² + Y² = N² under the minor map of bidegree ≤ (4,4) (`compute/omega3_minors.py`, verified on all 1264 certified classes). Singular points = base points of the map (the relations proportional: a node) or tangencies, which lie only over t ∈ {0, ±1, ±i, tan 22.5°} (3908 singular t-factors tested exactly); the base points sit at torsion points of order | 24 and at half-Pythagorean values (cos 2θ rational). Third frame in closed form: t_f = D_X/(D_N + D_Y), Pythagorean iff 2D_N(D_N + D_Y) = □ — the frame-triple curve is an explicit (2,2,2)-cover of Φ_f. Attempt B step 1 (`compute/omega3_quotients.py`): quotients by the involutions (all 1264 carry the joint sign change; 944 a second one), exact genera, rank-0 kills with complete lifts: **72 classes dead; box dead 1448, finite 1496**. The sweep's first lessons: tan 5θ families (monomial cap 4 → 8), three-frame monomial common factors (dead), high-bidegree components of genus 0/1 in the (2,1,1) box (new routes needed, entry 106). `a3.omega3_minors`, `a3.omega3_quotients`; suite 190. | W10 |
| M14-G | 🏁 **2026-09-05 (entry 104) — THE FINITENESS STATEMENT FOR SHAPE (1,1,1); THE SWEEP MADE FAST (21 s → 1.2 s per class); THE BIG PICTURE (R.9).** Base loci of the elimination (`compute/omega3_finiteness.py`): 1024 of the 1568 finite classes empty, 544 with only degenerate points, no admissible base point ⇒ **up to scaling, finitely many MSS3 have a center whose split part is a product of three distinct first-power primes** (ineffective; resting on the engine's verdicts). Engine: the monomial test as an exact identity over ℚ(i) (95% of the slowest class was sympy's simplify); the genus routes in the engine (bound with cap + alarm, resolution with cross-check, provisional otherwise); two-pass fast decision; the bivariate resultant (dehomogenize first; 144/144 agree with the six-variable route). Sample re-decided: no regression, 254/257 unknowns → finite (129 rigorous, 125 provisional). Sweep launched. `a3.omega3_finiteness`, `a3.omega3_sweep_engine`, `a3.omega3_box211_resample`; suite 188. | W10 |
| M14-F | 🧭 **2026-09-04 (entry 103) — THE (1,1,1) BOX CLOSED: exact genera by resolution of singularities; the three degenerate classes dead by a common-factor rule; entry 102 corrected.** Tool (`compute/omega3_resolve.py`): g = p_a − Σδ_Q by blowing up (δ_Q = Σ m_P(m_P−1)/2 over the infinitely near points; conjugate directions in extension fields via PARI rnfequation, every field monic integral), branch counts r_Q from the tree, and the REQUIRED Riemann–Hurwitz cross-check R = R_lb + Σ(m_Q − r_Q) (discriminant factors to degree 400). Validated on eight textbook singularities and 40 recorded hyperelliptic genera. **Result: all 1264 high-bidegree classes finite, each by one component of exact genus 3..23** (no cusp in the box; 128 singular orbits with fewer branches than multiplicity, where the bound lost). Correction: entry 102's bounds used PARI `factor` over a non-monic modulus (generator silently rescaled) — 204 values wrong, none crossing the threshold downward; the corrected bound certifies 1264 of 1267, the 3 others being the degenerate classes. Those three: the relations share a common factor depending on every frame; R1 = R2 = 0 iff G = 0 or the reduced pair vanishes — degenerate frames, norms, same-prime relations t₁ = t₂, t₁t₂ = −1 (the (2,±2) monomial relation) only ⇒ DEAD (`compute.omega3.reduced_relations`; 48 classes have a common factor, 45 already dead). **Box: dead 1376, finite 1568, unknown 0** — every class impossible for every prime triple or carried by at most finitely many prime pairs; NOT a theorem: effectivity (Chabauty on 304 models + 1264 curves of genus ≤ 23) needs Magma/Sage. `a3.omega3_resolve`; suite 185. | W10 |
| M14-E | 🧭 **2026-09-04 (entry 102) — PHASE 2: a genus lower bound certifies 1224 of the 1267 high-bidegree classes Faltings-finite; 43 remain; the local sieve is vacuous.** *(Corrected in M14-F: the bounds were computed with a non-monic-modulus factorization; the 1224 stand, the corrected count is 1264 of 1267, the 3 others degenerate.)* The unknown components are absolutely irreducible, singular exactly at the degenerate frame values, real, with irreducible pullbacks. Tool (`compute/omega3_genus.py`): Riemann–Hurwitz with the ramification over each branch value bounded below by dh − Σ m_Q (a point of multiplicity m carries ≤ m branches), computed exactly over the number fields of the branch values in PARI (discriminant factors to degree 40, both projections), plus absolute irreducibility via irreducibility mod p with a smooth F_p-point. Bounds: 21 for (8,8), 14 for (7,5), 9 for (4,8), 7 for (6,6). **Box tally: dead 1373, finite 1528, unknown 43** — every class but 43 is dead for all primes or on an explicit Faltings-finite curve. The local sieve (`compute/omega3_sieve.py`) is vacuous: the all-real residue class solves every Im-type relation. `a3.omega3_genus`. Next: Newton–Puiseux branch counts for the 43; the (2,1,1) sweep with this tool; the finite set needs Chabauty-type tools. | W10 |
| M14-D | 🧭 **2026-09-04 (entry 101) — THE (2,1,1) BOX, SAMPLED: the same engine and the same shapes recur with Chebyshev elements; coverage drops.** `compute.omega3.set_box` generalizes the engine to any exponents (elements are (2a,2b,2c)-forms; group = conjugations × permutations of equal-exponent frames). (2,1,1): 22 labels, (4,2,2)-forms, cross-checked against cleared_terms; 89,732 classes, 79,368 new. Seeded sample of 400: **dead 88 (55 decision + 33 towers), finite 55, unknown 257**; median 9 s/class (~60 CPU-hours for a full sweep, not run). Killers: the (1,1,1) rank-0 quartics plus new twists (t⁴−14t²+1, 4t⁴+7t²+4, 3t⁴−10t²+3); the monomial lemma with angle multiples up to 4; tower killers 30a2, 11a3, 24a1, 80a1, … plus 34a2, 592c1, 48a1, 56a2, 14a4, 80a2. 64% unknown = components of bidegree up to (16,16) not pulled back ⇒ phase 2 (high-bidegree components) is the bottleneck for every box beyond (1,1,1). `a3.omega3_box211`, `compute/data_omega3_box211_sample.json`. | W10 |
| M14-C | 🧭 **2026-09-04 (entry 100) — QUOTIENT TOWERS: 296 of the 600 finite classes dead through eight rank-0 elliptic quotients; 304 remain, blocked by positive-rank quotients.** Every finite model is even; the quotients u = t², w = t + κ/t (twisted reciprocity), the odd companion Y² = x·Q₀(x) and their iterates give elliptic curves; a rank-0 quotient with a complete enumeration lifts to finitely many t, none a frame ratio ⇒ dead. Killers: 30a2 (×96), 80a1 (×48), 11a3 (×40), 48a3 (×36), 528j2 (×32), 24a1 (×20), 128c2, 400d1 (×12). Remaining 304: 224 rank-1 quotients only, 24 rank 2 (389a1, 664a1, 13280a1), 56 no elliptic quotient; height searches to 2000 empty on 276 of them (evidence). **Box tally: dead 1373, finite 304, unknown 1267.** The five-curve pattern is a (2,2)-level fact, not a tower fact (two dozen quotient curves). `compute/omega3_towers.py`, `a3.omega3_towers`. Next: the (2,1,1) box and the high-bidegree components; the 304 need elliptic Chabauty / two-cover descent (Magma/Sage). | W10 |
| M14-B | 🧭 **2026-09-03 (entry 98) — THE THIRD-FRAME LIFT: every rational Pythagorean family of the (1,1,1) box is an angle-multiple coincidence, dead by the MONOMIAL LEMMA; 1077 of 2944 dead, none infinite.** Parametrizing every genus-0 factor of the pullback (linear; discriminant = square × constant; conic through a small point; missed points kept as candidates), each family satisfies w_g^a = ε w_h^b identically (w = π/π̄; (a,b) = (1,2) ×424, (1,−2) ×112, (2,1) ×120, (2,−1) ×72, (1,3) ×48, (2,3) ×64 in best frames) — impossible for distinct primes since π_g would divide π̄_g^a π_h^b; the remaining genus-0 shapes have non-square constant discriminants. The lift itself was never needed. **Tally: dead 1077, finite 600, unknown 1267 (bidegree > 6), infinite 0, candidate 0.** Within the box the obstruction is now purely the finite one. `compute/omega3.py` (parametrize, monomial_relation, lift, decide_genus0), `compute/data_omega3_box111.json` regenerated, `a3.omega3_engine` updated. Next: quotient towers for the 600; a cheaper route for the high-bidegree components; the (2,1,1) box. | W10 |
| M14-A | 🧭 **2026-09-03 (entry 97) — THE ω = 3 FRONT OPENED: the (1,1,1) box's quadruples are curves; 821 of 2944 classes dead uniformly in the primes.** Three-frame elements are (2,2,2)-forms; a quadruple's two relations on one frame, eliminating a frame, give a PLANE CURVE Φ_f(t_g,t_h) = 0 in the other two frame ratios, independent of the primes. Sound kills: trivial factors; same-prime factors; components quadratic in one variable via y² = disc(t) with PARI rank 0 + complete enumeration (only t ∈ {0,±1,∞}); the Pythagorean pullback t = 2τ/(1−τ²) decided the same way. **Result: dead 821 (349 trivial + 472 by THIRTEEN rank-0 even quartics of conductor 32/48/56/80 — the Fermat–Euler family), finite 540 (hyperelliptic genus 2/3/5, even + reciprocal ⇒ quotient towers), infinite 316 (a genus-0 Pythagorean family on the projection: the third frame + primality remain), unknown 1267 (bidegree > 6).** Not a theorem for the box; the first uniform-in-the-primes statement at ω = 3, by the long-term goal's own mechanism (R.7). `compute/omega3.py`, `compute/pari_genus1.py`, `compute/data_omega3_box111.json`, `a3.omega3_engine`. Next: third-frame lift of the 316; pullback of the high-degree components; towers for the 540; the (2,1,1) box. | W10 |
| M13-Z | 🔍 **2026-09-03 (entry 96) — THE AUDIT of entries 93–95: the MSS3 theorem STANDS; entry 93's cyclotomic reduction is WITHDRAWN.** Recomputed outside the committed code paths (92 open triples rebuilt from the entry-90 survivors; pairs re-enumerated independently; every pair re-killed; cyclotomic algebra re-derived; the (J,1) rigid form re-derived by machine per J). (1) `_is_frame_ratio` rejected negative ratios, but frames have either sign (3−4i is a frame) — a soundness gap in the joint solver, closed; every joint form's linear factors have roots ±1 only, so every kill stands. (2) `quadruple_pairs` compared raw labels after the conjugation images: blind to shared j=0 elements (none among the 92) and 4× inflated — the 56 'pairs' are **14 distinct orbits** (2 in (5,1), 4 in (4,2), 8 in (3,3)): 4 pincer + 10 joint, zero open; rewritten in normal form with orbit representatives. Theorem unchanged in substance (family now incl. (1,1)). (3) At J ≡ 1 mod 3 the machine's (J,1) rigid form is Z_J/(−F) — the gcd stage cancels F — with content bound 1 and all branches open (G_J irreducible over ℚ(i)); the frontier there is ρ⁴ = ±G_J. The literal 3ρ⁴ = Z_J is unsolvable outright by norms (q⁴ | F vs |F||G| = 3q²; 5 ∤ R_J) — a straw man. **Nothing about R_J is reduced.** `a3.audit_entry96`; `compute/data_quadruple_pairs.json` regenerated (92 triples + 14 orbits). Lessons: re-derive hand-generalized shapes by machine per parameter; audit frame-ratio tests against all orientations; count orbits, not listings. | W10 |
| M13-Y | 🏆 **2026-09-03 (entry 95) — THE JOINT RESIDUAL SOLVER: no MSS3 for a family of split-part shapes (direct, where A3.C is open).** Where the pincer left a window, a quadruple's two cleared relations R1=R2=0 on one frame give Res_{s2}(R1,R2)=0; every non-monomial factor is pure in (c1,s1) (w-frame decouples) with no frame-ratio root (r=m/n a frame ratio iff m^2+n^2 a square) -> no common frame. **All 14 distinct quadruple orbits among the 92 open triples die (4 pincer + 10 joint; the '56 = 16 + 40' were four listings per orbit — entry 96); boxes (1,1),(2,1),(2,2),(3,1),(4,1) have 0 open triples.** THEOREM: no MSS3 with center split part p^a q^b for (a,b) in {(2,1),(2,2),(3,1),(3,2),(4,1),(4,2),(5,1),(3,3)} and transposes -- INCLUDING (3,2),(4,2),(5,1),(3,3) where A3.C is still open. MSS3 is strictly easier than A3.C. `a3.quadruple_joint`, `compute/data_quadruple_pairs.json`. Next: (5,2),(6,1),(4,3),(4,4)... toward all omega=2. | W10 |
| M13-X | 🧭 **2026-09-03 (entry 94) — the RIGOROUS quadruple engine: MSS3 attacked directly.** `compute/quadruple.py`: MSS3 = a quadruple = two triples sharing an edge; the sound kill requires a pincer for EVERY target selection (correcting entry 93's best-target 'all 56 die'). Over the 92 open triples: 16 pairs DIE by the pooled pincer (balanced shapes, e.g. (4,2), min exp 2 -> no MSS3 there), 40 SURVIVE (8 of (5,1) = R_5, 32 of (3,3) = diagonal window p~q) because both triples bound the same direction (T1 only p-levers). The pivot pincers iff the two levers OPPOSE (balanced boxes) and reduces (J,1)/diagonal boxes to the frontier residuals. Narrows MSS3, not a uniform solution. Next: the joint residual solver (two equations in the same rho). `a3.quadruple_engine`. | W10 |
| M13-W | ⚠ **2026-09-02 (entry 93) — the quadruple pivot works on every candidate; the cyclotomic splitting reduces R_J to J ≢ 1 mod 3 — WITHDRAWN as a reduction by the entry-96 audit (M13-Z): the analysed equation is not the machine's residual at J ≡ 1 mod 3.** QUADRUPLE (recon): MSS3 needs a quadruple x, y, x+y, x-y = two triples sharing an edge → two levers per prime; all 56 candidate quadruples among the 92 open triples die by the pooled two-lever pincer; no quadruple in D(m) for m < 4000. Validates the pivot; a theorem needs the joint-valuation engine (`a3.quadruple_pivot`). CYCLOTOMIC SPLITTING (theorem, thin residual): Z_J has the factor F = 3C₁² - S₁² iff 3 | J-1; 3ρ⁴ = (3)(ρ)⁴ = (F)(G) → main branch ρ⁴|G ⇒ F|3 ⇒ |F| ≤ 3 impossible (|F| ≥ 5, unconditional); thin branch ρ⁴|F ⇒ |G| ≤ 3 empty in range. R_J now open only for J ≢ 1 mod 3 (`a3.cyclotomic_split`; subsumes entry 90's J=4 gcd). R_J is ABC-over-ℚ(i)-quality 4J/(J+4); local methods cannot prove it. | W10 |
| M13-V | 🧭 **2026-09-02 (entry 92) — the frontier residual: reconnaissance, no theorem; Conjecture R_J.** 3ρ⁴ = ℓ̄^{2J} + 2C₁ℓ^{2J−1} (9 | S₁, p ≡ 1 mod 12), J ≥ 5. Size fails by p^{J−4}; local methods cannot work (π = ρ = 1 solves the bare equation); ℤ[ζ₁₂] gives constraints only (3 quartic residue; primes ≡ 5 mod 12 of C₁ to even powers); it is a ℚ(i)-point of 3X⁴ = y^{2J} + y^{2J−1} + 1 (genus 13 at J = 5, Faltings-finite, non-uniform). Empty to p < 10⁶ (J=5), to 200000 (J=7,9), and for every primitive π of norm ≤ 20000. **Conjecture R_J** gates the single-lever part of the uniform program; the (J,1) boxes, J ≥ 5, are conditional on it. | W10 |
| M13-U | 🔬 **2026-09-02 (entry 91) — the pin stage: the k=3 family closed; ladder 2044/2136 (95.7%); the (J,1) content-3 residual is the frontier.** Per-content size kill with pins (a target surviving the window is pinned T = tp^e, t enumerated from q < (M/d)^{1/k}, tested by shape: range and the mod-3 obstruction). All 8 k=3 replications die. 92 open = 88 doubles + the 4 J=5 singles, whose content-3 residual 3ρ⁴ = ℓ̄¹⁰ + 2C₁ℓ⁹ (9 | S₁, p ≡ 1 mod 12) has q ≥ p⁴/2 against only q < p⁵ — no pin, no size kill; empty for 181 frames < 20000; the blind-descent situation over ℤ[ζ₁₂]. Next: the doubles' pair residuals; a new idea for the (J,1) residual (J ≥ 5). | W10 |
| M13-T | 🔬 **2026-09-02 (entry 90) — build B v2a: polynomial gcd, split index-3 cofactor, bounded primes; ladder 2036/2136 (95.3%).** The rigid form cancels the polynomial gcd of (A, B) (frame-nonvanishing checked by rational roots); 4X₁² − P² = (2X₁ − P)(2X₁ + P) as fine targets; when the levers bound a prime below an explicit K, the frames are enumerated exactly. 20 of the 32 singles and 22 doubles die: (3,2) 310/322, (4,1) 138/140, (5,1) 210/220, (4,2) 542/576, (3,3) 668/732; 100 open = 12 singles (the k=3 H2 replications → a conic tree with one genus-1 endpoint V₁² = b⁴ − 3a²b² + 9a⁴; the J=5 family, no constant window) + 88 doubles. Next: v2b — conic splitting after pins, elliptic endpoints by rank, the pair residuals. | W10 |
| M13-S | 🏆 **2026-09-02 (entry 89) — THE DEEP DESCENT: the content-3 lemma is a theorem; Theorem A3.9 BY MACHINE (78/78).** p² | Im(ρ⁴) = 4uv(u−v)(u+v) with ρ = u + iv the Gaussian prime itself (pairwise coprime factors < √(2q)) gives q ≥ p⁴/2, against g·q² = |ℓ⁶ + ℓ̄⁶ + ℓ⁵ℓ̄| ≤ 3p⁶: p ≤ 2√3, both contents. Entry 66's descent was this and content-independent; only its finite residue check was content-1-specific. Mechanized as deep index-1 targets (every w-lever inequality gains a square root) and the rigid-form size kill (`DEAD-residual-size`). The twelve hand-tree rows of the (3,1) ledger die by machine (`a3.box31_machine`); **Theorems A3.7–A3.10 all rest on machine certificates alone.** Ladder after the deep descent: (3,2) 310/322, (4,1) 134/140, (5,1) 202/220, (4,2) 534/576, (3,3) 668/732 — 1994/2136 (93.4%), 142 open (110 doubles, 32 singles: the k=3 H2 replications needing the (2U₁∓q) factor of the index-3 Im-cofactor, and the (J,1)-type families with J ≥ 4 needing a pin on ρ's legs). Next: build B v2. | W10 |
| M13-R | 🔬 **2026-09-02 (entry 88) — build B v1, the residual finisher; ladder 1936/2136 (90.6%); the content-3 gap in H2.** A collapse equation linear in the legs of one index forces the rigid form (X_k, Y_k) = ±(B, −A)/gcd(A,B), i.e. frame^k = ±(B − iA)/g, killed by parity, the content lemma and the concentration/sliver certifiers (`compute/residual_kill.py`, last stage of `kill_pattern`). 96 of 168 single-lever survivors die; in the (3,1) audit the four H2 same-sign combos and the four M2-opp rows are machine theorems. **Every remaining single lever (72) and the four H2 X6-route rows are one residual**, dead at content 1 (concentration) and open at content 3 — which is half of all frames (3 | S₁) and which entry 66 never treated. **Theorem A3.9 now rests on one open lemma** (p ≡ 1 mod 12, 9 | S₁, the four X6-route patterns with gcd(A,X) = 3), numerically empty to p < 20000. The 128 double-lever survivors need v2 (quadratic residuals). | W10 |
| M13-Q | 🔬 **2026-09-02 (entry 87) — the audit, and build A (targets at every index).** Audit: the (1,1) box is 8/8 by machine (A3.7 is a machine theorem); the (3,1) box is 66/78, and the 12 survivors are exactly the H2 (8) and M2-opp (4) hand-tree families of A3.9 — single p-levers p² | Re/Im(w²); their identities are pinned, the sign-class case analysis is hand work: **A3.9 stands on 12 hand-closed patterns the machine cannot yet reproduce** (build B's first targets). Build A: Chebyshev cofactors at every odd index (|cof| < nP^{n−1}, gcd | n, residues 1 / n mod 8; Re odd, Im ≡ 0 mod 4), even index by recursion, split cases with explicit frames, the homogeneous cofactor-pair solver, pin-and-substitute (two-squares uniqueness). 108 of the 404 ladder survivors die (all 72 [1,5]); ladder 1840/2136 (86%). The 296 left: 168 single levers, 128 double levers with non-homogeneous cofactor pairs or non-constant windows — size bookkeeping exhausted; build B (the residual equation) is next. | W10 |
| M13-P | 🏆 **2026-09-02 (entry 86) — the WINDOW finisher: the (2,2) box closed end to end by machine (120/120); a ledger gap found and closed.** `compute/window_kill.py`: levers on any collapse, coprime-factor targets with size and parity (even index: (C_h∓S_h) ≤ √2P^h odd, legs < P^h; index 3: X₁(4X₁²−aP²), gcd | 3), the pincer, the window (B/Rᵉ ≤ 2 ⟹ exact pin; parity kill), the Fermat pin (even index and even exponent only — odd-index pins are not Fermat: 25²+312²=313²), and the index-3 cofactor pair (mod 8 + leg windows ⟹ empty interval for p²/q²). All 32 ledger survivors die (H3 ×8 by pin+Fermat/parity, G3 ×20 by pincers). **Gap:** entry 63's G3 identities are those of the (2,2) sign class; the class {(1,2),(2,1),(2,−2)} (2 patterns, 4 ledger rows) has both levers on index-3 values and the stated pincer never applied — now closed by the index-3 cofactor lemma. Theorem A3.10 rests on machine certificates only (`a3.window_finisher`, `a3.p2q2_theorem`). Lesson: a ledger tag is a claim, not a proof. **Ladder under the complete stack:** (2,1) 26/26, (2,2) 120/120, (3,2) 278/322, (4,1) 110/140, (5,1) 160/220, (4,2) 478/576, (3,3) 560/732 — 1732/2136 (81%); the 404 survivors are 168 single levers on index-2/4/6 values (the H1/H2 bracket-identity shape) and 236 double levers with a value of index ≥ 5 (no double-lever pattern with both indices ≤ 4 survives). Next builds: (A) general-index Chebyshev targets (the 236); (B) the residual-system finisher for single levers (the 168). | W10 |
| M13-O | 🏆 **2026-09-02 (entry 85) — Theorem A3.8 BY MACHINE; the general unit collapse.** `unit_collapse_kill`: lever product form with the structural unit test, same-side cofactor coprimality by the angle-polynomial resultant, T = ±c′P^e, difference-of-squares coprime split, residual factors certified never 2^k·square (exact modular tests / two-squares size kill). All 26 distinct OPEN patterns of the (2,1) box die in the complete machine (10 residual, 4 valuation, 8 concentration, 4 unit collapse) with no hand tree (`a3.box21_machine`); the doubled patterns are Lemma G4's. Layer order: valuation → chase → residual parity → concentration/sliver → unit collapse. | W10 |
| M13-N | 🏆 **THEOREM 2026-09-02 (entry 84) — A3.10: the (2,2) box is closed (split part p²q²).** Corollary: any MSS3 center's split part is p⁴q or higher, or has ≥ 3 distinct split primes. The 26 k-children are killed end to end by machine (`a3.p2q2_theorem`, certificates recomputed each run): 4 valuation, 10 residual parity, 8 concentration (Z± systems; the content lemma d | 3 + sliver certificate), 4 Block B by the unit collapse T = ±q⁴ with the coprime split and 2-adic kill (`block_b_lemma`). The tree layer: the content lemma (cyclotomic resultants: gcd(S_x, G) | ∏ Res(B, Φ_d)), the sliver certificate, the structural unit test, cross-exponent Lucas rules. The one-equation rigidity lemma is moot. | W10 |
| M13-M | 🏆 **THEOREM 2026-09-02 (entry 83) — the concentration theorem: every weighted coincidence family of the ladder is EMPTY, uniformly in k, p, q.** The E3 argument on the pinned Gaussian integer: ρ^{2k} + ℓ̄⁴ = 2c₁π⁶ = (ρ^k + iℓ̄²)(ρ^k − iℓ̄²), gcd | 2, π⁶ in one factor, the other divides 2c₁ (modulus < 2p) yet is ≡ ∓2iπ̄⁴ mod π⁶ — contradiction; same for Z₋, W, and mechanically for (4,4), (2,4), (2,8): 24 certificates (`concentration_kill`). The rigidity family of A3.10 is dead in both sign variants; the one-equation rigidity lemma was never the right statement. A3.10: 6 of 14 children closed end-to-end by machine; 8 (Block A opposite-sign, Block B) await the tree layer — NOT claimed. `a3.concentration_theorem`. | W10 |
| M13-L | 🏆 **THEOREM 2026-09-02 (entry 82) — the rigidity system is a fixed curve.** The chase's residual V₄ = ±S₂(4C₂+p²) joins U₄ = ±p²C₂, and together they determine w⁴ = ±Z, ±Z̄ with Z = p²C₂ + iS₂(4C₂+p²) = ℓ⁴ + ℓ³ℓ̄ − ℓ̄⁴ = π̄⁸(s⁸+s⁶−1), s = π/π̄. So every (k,2)-system (rigidity = k=4; the (2,1) survivor = k=2) is a ℚ(i)-point of the FIXED curve y² = ε(s⁸+s⁶−1) (genus 3; y⁴ for even k, genus 9) — by Faltings the whole family has finitely many solutions (p,q,k), unconditionally: the rigidity lemma fails for at most finitely many primes. N(Z) is never a perfect power on any prime frame below 20000 (the family for every k, q). Effective route: Jac(H) ~ E × Jac(Y² = x(x⁴+x³−1)) (genus 2), Chabauty over ℚ(i); PARI: ranks of y² = d(x⁴+x³−1) are 2,1,1,1 (d = 1,−1,2,−2), so the elliptic quotient alone doesn't finish. `a3.rigidity_fixed_curve`. | W10 |
| M13-K | 🔧 **BUILT 2026-09-02 (entry 81) — Front A step 2: the mechanical endpoint extractor** (`compute/lucas_endpoints.py`, `a3.lucas_extractor`). Three facts make the hand-trees mechanical: the cleared weights are exactly the sum-to-product weights (every pair collapses by an exact polynomial identity to ±2p^{2a}q^{2b}Trig(D)Trig(M)); mixed trig-monomials are units, so only pure-w monomials absorb p-powers and only pure-ℓ ones q-powers; the lever prime power of the third term must land on a pure factor or the pattern is dead. Census over boxes (2,1)…(5,1): all 2008 distinct OPEN patterns are ENDPOINTs (no failed collapse), every OPEN distinct pattern carries a lever, the exponent-families grow with the box (17, 55, 105, 219, 41, 110, 54 new per box; 601 total) but fall into ~18 shape types. **The uniform ω ≤ 2 theorem is a finite list of type-lemmas.** **The chase** (Lucas values, all three collapses, Pythagorean rewrites, coprimality closure) re-derives the rigidity lemma U₄ = ±p²C₂ with its residual; coincidence types on (2,1)/(2,2): the unweighted S_x = ±V_y and the weighted Trig(w^y) = ±p²Trig(ℓ²) family and mirror; a coincidence alone never kills (equal congrua (29,37)). **The valuation layer** (product-equality balance; rank of apparition + LTE) kills ~10% of endpoints per box outright and pins exact divisibility configurations — on the rigidity family r_p = 8, v_p(Re w⁴) = 2, the order-16 lemma by machine. An endpoint is now a system: valuation configuration + coincidence + residual. **Residual parity** (odd residual factors 2U ± p^k cannot vanish) closes 10 more (2,1) endpoints — with valuations, 14 of 26 closed by machine; the 4 survivors are one system U₂ = ±p²C₂, V₂ = ±S₂(4C₂+p²), the (k,2)-family with k = 2 (the rigidity lemma is k = 4); 8 remain for the Gaussian-prime concentration layer. Next: the (k,2) type-lemma; the concentration layer. | W10 |
| M13-I | ✅ 2026-08-30 — **H3 closed by the double lever; the additive queue is EMPTY**: the last native (2,2)-box family {(1,ε),(2,2),(2,−2)} ×8 collapses to p²q²·Im(ℓ²w^{2ε}) = −2ε₁·(U·2CS or V·C₄); the q-lever and p-lever pin each other exact (C or S = ±q², u = ±p²), landing every branch on p⁴−q⁴ = □ — Fermat's x⁴−y⁴ = z², sign-uniform. Every native pattern of the (1,1)/(2,1)/(3,1)/(2,2) boxes is now closed; Theorem A3.10 gates only on the 44 replication transfers. PLUS the verify-integrity redesign: five wave checks had rotted (pinning live-queue counts; failing silently since entry 62) — waypoints now assert durable ledger invariants (`a3.h3_closed`) | W10 |
| M13-H | 🏆 **THEOREM 2026-08-30 — A3.9 (the (3,1) box)** — ✅ *2026-09-02 (entry 89): 78/78 by machine; the content-3 question of entries 87–88 is settled by the deep descent (the hand descent was right; only its finite check was content-specific); see M13-S*: no signed additive relation for split part p³q. The complete pattern space closed by the machine layers + eight named tree-families (G1–G4 lemmas, the pincer, parity/leg-window finishers; Fermat appearances 5–8). **Corollary: any MSS3 center's split part is p²q², p⁴q+, or has ≥ 3 distinct split primes.** The (2,2) box is one family from Theorem A3.10 (`a3.p3q_theorem`) | W10 |
| M13-G | 🏆 **THEOREM 2026-08-29 — A3.8 COMPLETE (the (2,1) box)**: no signed additive relation in D(m) for split part p²q. All 189 patterns closed: valuation/factorization/congruence machine layers, Fermat-at-level-2 trees, the Im(ℓ³w²) collapse, F-F replication, the β₂ coprime-factorization (4a²+9b²)(4a²+b²) = p², the E3 four-factor λ̄-concentration, the (μ²±iℓ̄²) two-factor kill, and the final sliver descent: q² = U² + p⁴V² against the q < p² window. **Corollary: the split part of any MSS3 center is p³q, p²q², or has ≥ 3 distinct split primes.** The exploration curve y² = x³−2214x+40041 has rank ≥ 1 — no rank-0 shortcut existed (`a3.box21_complete`) | W10 |
| M13-F | 🏆 **THEOREM 2026-08-29 — A3.7 (two split primes, first powers)**: no signed additive relation in D(m) for m = 2^s r p q — 36 patterns: 20 valuation, 6 tan-half-factored, 3 mod-16, 7 closed by classical quartic descents (Fermat's x⁴−y⁴ = □, non-congruence of 2 and 3; L1–L5 self-contained). **Corollary: the split part of any MSS3 center has ≥ 3 prime factors with multiplicity.** Next: higher boxes, ω = 3 (`a3.omega2_ab1`) | W10 |
| M13-C | 🏆 **THEOREM 2026-08-28 — A3.6 (the ω = 1 theorem)**: no signed additive relation in D(m) for any m with a single split prime (any power, any inert cofactor) — the first unconditional slice of Conjecture A3.C, via D(m) = {m²\|Im σᵏ\|} + the Gauss-content contradiction. Corollary: every MSS3 center has ≥ 2 distinct primes ≡ 1 mod 4. Plus A3.5 (degenerate subsums classify; triples are nondegenerate) and A3.4 (equal-modulus rigidity in ℚ(i)). Next: A3-S2b, two split primes (`a3.omega1_theorem`, `a3.degenerate_subsums`) | W10 |
| M13-D | ⚗️ **MEASURED 2026-08-28** — P2 rigidity probe: the rigid seed's death is PAIR-LEVEL (all three pair equations empty — persistent global binary-form class obstruction, locally soluble everywhere) and rigidity is a **rate** (2/72 vs 22/72 conversions; blips at q = 19, 25), not an absolute lock. Target refined: the conversion-rate law in the ideal-product frame (`a9.rigidity_probe`) | W4 |
| M13-E | 📋 **MANIFEST READY 2026-08-28** — M12-C non-graph cubic campaign: 56 triple-point configurations = 23 Klein-orbits enumerated (`data_cubic_campaign_manifest.json`); next build: implicit η⋆-restriction machinery (graphs closed by A8.19) | W1 |
| M12-P | 🌋 **THE SCALING LAW (2026-08-28)** — **Lemma A9.13 proven**: sieve verdicts only soften along $(m,U,V) \to (qm, q^2U, q^2V)$ (witnesses scale; alive stays alive). The golden pair = 37·(a coherence-dead 925 pair); the C2-exception = 29·(the 725 passer); the square-root motif = the self-scaling slice ((5q)² = q·5²q). Ladder sweep of the window (53400, 150000]: **20 golden + 68 near from 4 fertile seeds**; minimal new golden centers 96425/105125/126875/147175 all nonsquare ⟹ "sieves total off the square family" REFUTED; fertility is seed-intrinsic (725 broad-spectrum vs 925/1025 self-prime-only). **Program pivot: the sieves cannot carry nonexistence; the frontier is the representable-vs-attained gap and the fertile-seed arithmetic** (`a9.scaling_law`, `a9.family_primitivity`, `a9.ladder_sweep`, `a9.square_family_ext`) | W4/W6 |
| M12-A | ✅ **DONE 2026-08-28** — the atlas: 84 K3 + 9 Horikawa characters, $t_3$-census, $\rho \ge 16+t_3$, 19 orbit types (A8 §10, `a8.h20_atlas`) | W2 |
| M12-B | ✅ **DONE 2026-08-28** — verdict: H-Rédei refuted as universal (30/36 ARC kills, Lemma A9.5), confirmed as the 4-rank layer (6/36, all separators order exactly 4, all at 481/962); ideal-product law EXACT 62/62; hypothesis refined to **H-align** (A9 §3 fifth layer, `a9.kill_mechanism`) | W4 |
| M12-C | ⚠️ **OPENED 2026-08-28, first slice closed** — **Theorem A8.19 proven**: no eta*-integral GRAPH cubic through ≥ 3 triple points (thirteen incidence families, all eliminations Qbar-complete, every solution a known integral line). New rational curves with cubic image need genuine degree-≥2 terms in both coordinates; the general 6-parameter-per-configuration eliminations are the continuing campaign, machinery built (`a8.web_cubics`) | W1 |
| M12-D | ✅ **EXCEEDED 2026-08-28** — desert VERIFIED($3\times10^4$), zero golden centers (5,292 rep kills, 240× anatomy corpus; `a9.desert_ext` pins both frozen artifacts); extension toward $10^5$ running; additive desert VERIFIED($10^7$) as a bonus (`a3.additive_ext`) | W6 |
| M12-E | ✅ **DONE 2026-08-28** — autopsy verdict: A2.L transplants (no derivative wall in the descent — F3 *is* the transplant; class/unit friction finite); the true wall is dimensional, and the Wronskian wall lives at the geometry-finish (Vojta) level. (★-V) and (★-abc) formulated; naive-abc recorded FAILED-ATTEMPT (realized triples abc-cheap, q ≤ 0.43); the squarefull-enrichment lever measured (0.674 vs 0.279, ratio 2.41) (A2 §6, `a2.abc_probe`) | W5 |
| M12-F | m = 7 nontrivial-character survey (A8.18 scope closure) — running, orbit-checkpointed | W1/A8 |
| M12-O | ⚖️ **RESOLVED BY REFUTATION 2026-08-28** — A9.C2 and the k_c ≥ 1 companion are FALSE: the corpus-scale census (350 pairs, class-group-free via A9.12) found the counterexample at m = 21,025 = 145² — a pure outer-line kill (pattern {6}, product π(v−,B−)) with both phantoms alive at every layer (`a9.c2_refuted`). k_c ≥ 1 was a 99.7% regularity; the center cap (A9.6) and the law (A9.12) stand. Motif: exceptions and golden centers both sit at square center roots (145², 185²) — the m = k² family flagged for W4/W6 follow-up | W4 |
| M12-N | 🔭 **THE TELESCOPE CATCHES (2026-08-28)** — first golden centers at m = 34,225 = 185² (pair (108786216, 718725000), both orders; `a9.golden`): the sieves' totality was probabilistic, exactly as the actuarial decision rule anticipated (predicted onset decade 10^4.5–10^5 — observed 10^4.53); the A9.12 law confirmed live on all 8 lines; no additive quadruple (desert to 10^7 stands). W6 validated; W4's all-m sieve-totality hypothesis honestly refuted; the desert's depth is additive-structural | W6/W4 |
| M12-M | 🏆 **THEOREM 2026-08-28** — **A9.12 (= C4) PROVEN, both directions**: the representation sieve ≡ the elementary Diophantine system (pair equations + syzygy). Sufficiency closed by **Theorem A9.11** (the full overlattice lemma: per-prime chain to the target valuation; the 2-adic case via anisotropy of the unramified norm space, forced by 8 | U and co-norms ≡ 2 mod 8 — verified corpus-wide, zero exceptions). The fourth sieve — beyond all characters by M12-B — is an elementary Diophantine LAW; the class group was the language, never the mechanism (`a9.c4_theorem`) | W4 |
| M12-L | ⚠️ **OPENED 2026-08-28, half proven** — C4 sufficiency: **Theorem A9.10 proven** (q = 1 witnesses are constructively sufficient: the generated lattice is automatically even of det N; real lines carry q = 1 by construction — the sphere point IS the kernel vector). Census: 28/31 alive lines certified constructively; q = 1 test still fails all 57 kills; the three q > 1 boundary lines pinned (425/850 line 4: q = 77, identical reduced witness under doubling; 1025 line 6: q = 31). Remaining gap: isotropic overlattices of order q at q > 1 witnesses (`a9.q1_sufficiency`) | W4 |
| M12-K | 🔓 **BREAKTHROUGH 2026-08-28** — **Theorem A9.9 proven** (syzygy necessity: three vectors in rank 2 are dependent ⇒ det₃ = 0 on top of the pair equations); census: **pairwise Gram + syzygy explains 57/57 anatomy kills** with zero soundness violations — the single pairwise survivor dies at the determinant. **Conjecture A9.C4**: the representation sieve ≡ the elementary Diophantine system (necessity proven; sufficiency = an overlattice integrality condition). If C4 holds, the fourth sieve and the desert are statements in elementary arithmetic — no class groups. Lemma A9.8.1: free products pass by the column-law identity. C2/transfer relocated to the witness-system level, still open (41/41) (`a9.syzygy`) | W4 |
| M12-J | ⚠️ **OPENED 2026-08-28, scaffold built** — A9.C2: **Theorem A9.8 proven** (the Gram sandwich: k=1 solvability ⇒ pairwise representability ⇒ Gram equation); losslessness measured (exact = Gram on all 264 passer pairs, Conjecture A9.C3: the sieve without class enumeration); the Z[i] root-grid dictionary proven (all ten values are Gaussian norms over the root grid; Gram = Q(i)-vs-Q(√−3) norm interplay in Q(ζ₁₂)); the product atlas pinned (free products never fail; π(A+,A−) fails 11/11 passers; A9.C2 verified 41/41 at Gram layer). Remaining: the transfer lemma via ζ₁₂-factorization (`a9.gram_sandwich`) | W4 |
| M12-I | ⚠️ **OPENED 2026-08-28, major progress** — the k_c ≥ 1 companion: **Theorem A9.7 proven** (pairwise Gram necessity: alive lines need w_iw_j = t² + Nk²; coherence = its local shadow, Prop A9.7.1); census: Gram explains **56/57** anatomy kills including the beyond-genus ARC ones (single syzygy exception pinned); companion mechanized (30/30 phantom kills are Gram failures). H-align refined to **H-Gram**; remaining: prove Conjecture A9.C2 (any Gram failure forces a phantom Gram failure) (`a9.gram_sieve`) | W4 |
| M12-H | ✅ **DONE 2026-08-28** — **Theorem A9.6 proven**: the center cap is a theorem for all m (real center lines carry actual sphere points; only the phantom U±V lines can die); the fourth sieve = the class-group shadow of the A3 additive condition (`a9.center_cap`, constructive certificates over the corpus) | W4 |
| M12-G | ✅ **DONE 2026-08-28** — actuarial model v1: desert-to-$3	imes10^4$ is *expected* under the random baseline (E ≈ 0.2–0.4); expectation crosses 1 near $10^5$; **decision rule**: zero golden at $10^6$ strains every model variant ⟹ real evidence for the W4 law. Two law-shaped regularities found: the center cap ($k_c \in \{1,2\}$ always) and every-kill-includes-a-center-kill (`a9.actuarial_sample`) | W6 |
| M13-A | $\operatorname{Pic}(\widetilde X)$ with Galois action | W2 |
| M13-B | The fourth-sieve law: spinor/Rédei theorem for a residue family of $m$ | W4 |
| M13-C | A2.C proven → the $k[t]$ theorem; paper #1 drafted | W1, W8 |
| M14 | Conjecture E formalized with the twist-descent framework; first Brauer classes computed | W3 |
| M15 | Conditional capstone: effective-abc ⟹ bounded MSS3, with constants | W5 |

## 5. The honest odds, and the ladder of victory

A full unconditional proof is a boulder that has not moved for
fifty years, and nothing here pretends otherwise. But this program
has genuinely narrowed where a proof must live: it must be global
(F5), exact (A1.1, Hill §7), and arithmetic (the convergence) — and
the plan above concentrates on precisely the three known mechanisms
matching that profile: class-field reciprocity (W4), cover descent
with Brauer obstructions (W2→W3), and height descent (W5). The
guaranteed harvest, even in the worst mathematical world: the
function-field theorem (W1), the motive atlas and likely the
$L$-function of $X$ (W2), the spinor/Rédei anatomy of the desert
(W4), the quantitative heuristic (W6), and a community engaged with
the strongest partial results in the problem's history (W8). Each
rung is real mathematics; the top of the ladder is the proof.

*Maintenance: this roadmap is updated when milestones land or walls
are hit; every status change is logged. The standing banner applies:
nothing here claims the problem is solved.*

## R.12-0 The first reordering after the prime-column lemma (2026-09-06, entry 120; absorbed into the portfolio R.12 at the top of this file)

**What changed.**  Theorem A3.PC (2.49) is the first exclusion in the record that is uniform in the primes *and* the exponents and costs nothing: a class dies from its labels alone.  It removes two thirds of the finite classes of the (1,1,1) box and 92% of those of the (2,1,1) box, every free-frame class among them.  The inventories are rebased on the survivors: **488 finite classes of (1,1,1)** and **4,744 of (2,1,1)** (with 290 + 694 dead classes that also pass the lemma — the killers of entries 100–118 are the only reasons those are dead).

**The plan, reordered.**
- **P-A′ (theory, first): the leading-unit step.**  The lemma fixes the valuation pattern; the next invariant is the residue of the unit parts.  The reviewer's first experiment: does the three-maxima condition exhaust the valuation obstruction of the full ideal (the four three-term relations, not just R₁, R₂), or do further initial-ideal / leading-unit conditions kill more sign patterns?  Work symbolically in the exponents; the 488 + 4,744 survivors are the test set.  A second uniform lemma of this kind would be the natural route to a statement for arbitrary prime support (goal G).
- **P-B′ (computation): the survivors' towers.**  The 488 finite (1,1,1) classes: quotient towers (entries 105–106) and the bielliptic pattern of entry 118 (a common squareclass of the two factors of a hyperelliptic model gives a bielliptic genus-2 curve with rank-1 quotients — QC + the E₁ × E₂ sieve are now a working pipeline).  Which of the 488 have such a model is the first census.
- **P-C′: the (3,1,1) box with the lemma first.**  388,216 classes; the lemma prunes before any curve is built (expect a survival rate near the (2,1,1) box's 7%), so the sweep cost drops from ~100 CPU-h to a few; wire `prime_column.excluded` into the sweep's class enumeration before launching.
- **P-D′: the killers as a theorem** (unchanged from R.11 P-B), now on a much smaller set: the 290 + 694 dead-and-passing classes are exactly the ones the curve machinery was needed for — the place to look for the reason the fifteen curves recur.
- **Retired:** P-E (the content-2 ladder extension for the weighted free-frame relation) — subsumed by A3.PC.  The Magma question (R.11) is now moot for 𝒞₂ and open only for future genus-2 endpoints without a bielliptic structure — which entry 131 produced: C_a and C_b, the non-bielliptic genus-2 curves of the octic towers, need a 2-descent rank bound and (if rank 1) Chabauty; `compute/qc/magma_towers131.m` is ready for the online calculator — and was run there (entry 132): both have rank 1 and exactly seven rational points, all degenerate or with a non-square u; the octic towers are closed.

**Stop criteria** (from the reviewer, adopted): if the initial ideals add nothing beyond the column lemma, stop expanding the tropical computation and go to the residue-unit/height step; do not call the prevalence of a pattern in local models evidence of a global theorem.
