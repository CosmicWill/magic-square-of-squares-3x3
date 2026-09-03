# The proof program — strategic roadmap

*Drafted 2026-08-28, after the full-access literature sweep, the Hill
refutation, and the completion of the A8.18 ladder. This is the
standing battle plan toward the goal: **a proof, in either direction,
of the 3×3 magic square of squares problem.** It is deliberately
ambitious; every claim of current fact carries the repository's tags,
and every ambition is labeled as such. Companion documents:
[PROGRESS.md](PROGRESS.md) (what is true now),
[RESEARCH_LOG.md](../RESEARCH_LOG.md) (how we got here).*

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
