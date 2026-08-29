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
