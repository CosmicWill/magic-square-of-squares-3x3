# Research log

Dated, append-only. Negative results and failed attempts are logged with the
same care as positive ones — an autopsy per failure. Newest entries at the
bottom.

---

## 2026-08-25 — Entry 0: project start, environment probe

**Decisions made at kickoff** (user-confirmed): goal = impossibility proof
attempts (partial results accepted as the realistic outcome); write-ups in
Markdown; no Lean — rigor = complete classical proofs + mechanical
verification (`python3 -m verify`).

**Environment probe results:**

| Tool | Result |
|---|---|
| Python | 3.11.15 (stdlib `math.isqrt`, native bigints) |
| sympy | 1.14.0 — installed OK via pip |
| gmpy2 | 2.3.1 — installed OK via pip |
| PARI/GP | **2.15.4 installed OK via apt** (has `ellrank`) — elliptic-curve rank experiments unblocked |
| gcc / Rust | 13.3.0 / 1.94.1 available (fast-search stretch goals) |
| LaTeX / Lean | absent by design (Markdown-only; no formalization this phase) |
| Network | PyPI + apt reachable through proxy; **general WebFetch blocked** (arXiv/Wikipedia/multimagie unfetchable) — literature is therefore SUMMARY-ONLY unless stated otherwise, see `docs/references.md` |

**Rule adopted:** proof-critical verification runs on pure stdlib; sympy /
gmpy2 / PARI are allowed only in exploratory scripts and in checks that SKIP
cleanly when absent. Rank *upper* bounds without PARI would be CITED/SKIPPED,
never silently degraded — with PARI present we can do better.

**Plan of record:** foundations F1–F6 proven from scratch with named checks;
attack lines A1–A6 as described below.

---

## 2026-08-25 — Entry 1: Foundations landed (M1–M2); findings and errata

**Landed:** F1–F6 (F1, F2, F4, F5.1–F5.2 fully PROVEN; F3's chain PROVEN
down to the classical quartic (Q), which remains Open Task F3-T1;
F5.3–F5.4 VERIFIED; F6 anchors VERIFIED). 29 checks green at FULL bounds.

**Findings worth recording:**

1. *(F3)* While writing the four-square-theorem document, the classical
   reduction came out cleaner than the literature summaries suggested: a
   primitive 4-AP of squares forces the single quartic
   $(\alpha^2+\gamma^2)(2w^2+\tau^2) = 6w\alpha\gamma\tau$, which
   rigidifies (via $\mathbb{Z}[\sqrt{-2}]$ + a parity kill of one root) to
   $\alpha^2+\gamma^2 = 2w\tau$, $2w^2+\tau^2 = 3\alpha\gamma$, then to a
   concordant pair $a^2+b^2 = w^2$, $4a^2+b^2 = \tau^2$, then to
   $r^4 - r^2s^2 + s^4 = \square$. Every step is proven and
   machine-verified here; only the last quartic's impossibility is taken
   as classical. Closing F3-T1 would be a nice self-contained write-up of
   Euler's theorem.
2. *(F5.3, surprise)* The naive "each entry is a square with probability
   1/2" heuristic for $\mathbb{F}_p$ solutions fails hard below $p = 59$:
   exhaustively, magic squares of nine distinct nonzero squares over
   $\mathbb{F}_p$ exist iff $p \in \{59, 73, 83, 97\}$ or $107 \le p$
   (verified to $p < 1000$). The nine quadratic conditions on $(u,v)$ are
   strongly correlated. A Weil-bound argument should prove "all
   $p \ge 107$" (Open Task F5-T1).

**Erratum:** the M2 commit message states the mod-72 enumeration has
"5832 admissible residue triples"; the correct count, as printed by
`f4.mod72`, is **27** ($c \in \{1,25,49\}$, $u, v \in \{0,24,48\}$
mod 72). The docs and checks were always correct; only the commit
message prose is wrong. Recorded here rather than rewriting pushed
history.

---

## 2026-08-25 — Entry 2: A1 — audit of arXiv:2510.08286 (Hill)

**Fetch attempts** (all blocked by the egress proxy, logged in the doc):
arxiv.org abs/html/pdf, export.arxiv.org HTML+API, Semantic Scholar API,
huggingface mirror. Audit proceeded against the reconstructed method.

**Outcome:** the paper's language ("consecutive APs of odd numbers with
equal sums; offsets and sums") is PROVEN to be a faithful re-encoding of
the F2 layer. Theorem A1.1 (new, proven, executable): for every modulus
$N$ there are ordered, distinct, positive pseudo-solutions satisfying
every MSS3 relation mod $N$ plus all order constraints — so **no
descent-free congruence/order endgame can prove nonexistence**. The
abstract advertises no descent or minimality mechanism. Verdict:
UNRESOLVED (text unavailable; not refuted, not validated); the method
space as described cannot contain a correct proof; checklist §5 of the
doc prepared for when the text is accessible. The program continues.

---

## 2026-08-25 — Entry 3: A2 — the function-field attack (M4)

**The big one landed.** Lemma A2.L ("pairs of conics"): over an
algebraically closed constant field, the system $aX^2+bY^2 = P^2$,
$cX^2+dY^2 = Q^2$ with $ad \ne bc$, $abcd \ne 0$, $\gcd(X,Y)=1$ has only
constant solutions — proved by a degree-halving Fermat descent whose
nondegeneracy conditions **self-propagate** (the new parameter tuple
$(1,-\theta,1,-\bar\theta)$ has $a'd'-b'c' = \theta-\bar\theta \ne 0$ and
$a'b'c'd' = \theta\bar\theta = 1$ automatically). Consequences, both
PROVEN unconditionally for char $\notin\{2,3\}$:

- **A2.4**: every 4-term AP of squares in $k[t]$ is a square multiple of a
  constant one (primitive $\Rightarrow$ constant). Sharp: over
  $\mathbb{F}_{13}[t]$ the scaled-constant 4-AP $(2g)^2,(6g)^2,(4g)^2,(3g)^2$
  exists because $4,10,3,9$ are squares in AP in $\mathbb{F}_{13}$ —
  caught while writing the theorem statement, hypothesis added.
- **A2.5**: same for square-congruum 3-APs; over $\mathbb{Q}[t]$ outright
  (constant layer killed by F3.2b).
- **A2.3** (independent, effective): Mason–Stothers proof of the
  congruum theorem over $-1$-nonsquare constant fields.

**Frontier isolated:** the full conjecture (no MSS3 over $k[t]$ beyond
square-scaled constants) is exactly "no nondegenerate rational curves on
the BTVA surface"; Lemma A2.L cannot reach it (3-variable quadrics do not
factor). Exhaustive searches (complete per center degree by Prop. A2.1):
no MSS3 with nonconstant center over $\mathbb{F}_q[t]$ for q=3 (deg M<=5),
5 (<=4), 7/11/13 (<=3), 17/19/23 (<=2). Open Task A2-T1 recorded — in our
judgment the most tractable path to a genuinely new theorem in this
problem complex.

---

## 2026-08-25 — Entry 4: A3 — simultaneous congrua, the additive desert, the descent gap (M5)

**The additive desert (new first-party exhaustive fact, Theorem A3.3):**
for every $m \le 300{,}000$, no two congrua of $m$ sum to a congruum of
$m$ — the level-3 additive pattern (which would produce a 7-square magic
square of the never-seen three-full-AP type) never occurs, although
69,398 centers in range have $\ge 4$ congrua available. Conjecture A3.C
(no additive triple exists for any $m$) posed as a realistic intermediate
impossibility target strictly weaker than the full problem.

**Theorem A3.K (derived independently of the literature):** no quadratic
field admits a center-zero magic square of nine distinct squares (the
configuration forces $i \in K$, and rank $E_1(\mathbb{Q}(i)) = 0$);
$\mathbb{Q}(i,\sqrt n)$ works for every congruent $n$ via
rank $E_1(\mathbb{Q}(i,\sqrt n)) = 2\,\mathrm{rank}\,E_n(\mathbb{Q})$.
Fully explicit witness for $n = 5$: $L(0, 41^2, 720)$ with entries
$\{0, \pm 41^2, \pm 720, \pm 49^2, \pm 31^2\}$ — squares of
$41, 49i, 12\sqrt5, 31i, 0, 31, 12i\sqrt5, 49, 41i$ — verified in exact
quartic-algebra arithmetic and added to the falsification gauntlet as
anchor (e). PARI certifies the rank inputs (E_1..E_4 rank 0, E_5,6,7
rank 1, torsion (Z/2)^2).

**Gap question A3-Q posed:** a Selmer-type invariant for the four-twist
system with same-m gluing that would explain the desert over Q.

---

## 2026-08-25 — Entry 5: A4 — the eight-square case (M6)

**Taxonomy proven** (classes C/E/K by the non-square cell, orbit sizes
1/4/4) and each class reduced to an explicit additive pattern in
$\widetilde D(c)$. Class E *requires* an additive triple at a square
center — dead to center $9\times10^{10}$ by A3.3, conjecturally empty
(A3.C). Sweep of ALL centers $\le 10^6$: no quadruple, no class-K
pattern, hence **no 8-square magic square with center $\le 10^6$**
(first-party bound). Census re-found AB1 (and its $2^2$-scale at
$850^2$) as the only $\ge 7$-square configurations in range —
independent uniqueness confirmation.

**Discovery:** the additive desert is a *square-center* phenomenon: four
additive triples exist below $10^6$, all at NON-square centers — the
primitive ones at $c = 157441$ (congrua 19800, 135240, 155040; a
6-square fully magic square) and $c = 411625$. Whatever blocks additive
triples at square centers is genuinely about squareness, not density —
exactly the arithmetic the main problem turns on. A3.C sharpened
accordingly.

**The AB1 fiber computed:** fixing the $v$-slot at $t_1 = 7/11$, the
one-extra-square condition is the quartic
$(85Y)^2 = 1681x^4-28900x^3+3362x^2+28900x+1681$ with AB1 at $x = 3/4$;
PARI certifies its Jacobian ($y^2 = x^3+3362x^2-846513044x+2769975186072$,
minimal $y^2 = x^3-53142545x+58165355025$) has **rank 3**, torsion
$(\mathbb{Z}/2)^2$. The eighth-square condition is a second 2-cover over
this rank-3 family — Open Task A4-T1: compute its genus; $\ge 2$ would
give the first unconditional finiteness theorem for 8-square candidates
on the fiber (via Faltings).

---

## 2026-08-25 — Entry 6: A5/A6 — geometry nuggets and the bound ladder (M7)

**A5 (surface):** explicit model verified — X is cut by exactly 6
independent quadrics in P^8 (rank computed exactly); every point with
all nine coordinates nonzero is SMOOTH (Jacobian = 2 M diag(x), rank 6);
X is an iterated double cover of the Lucas plane branched over the
9-line arrangement with (t2, t3) = (12, 8) — the concrete Hirzebruch-
style route to the missing invariants. F_p point counts (all divisible
by 64, dominated by the degeneracy locus; nondegenerate locus EMPTY for
p < 59 by F5.3): Lang philosophy in miniature. Problems P1 (Picard),
P2 (Brauer-Manin), P3 (curve enumeration — the keystone, = A2-T1), P4
(Cain reconciliation) posed precisely.

**A6 (bounds):** the ladder — m <= 8,000 (independent direct
implementation), m <= 300,000 (desert sieve; centers to 9e10, and not
even three APs realizable), centers <= 1e6 of any kind incl. all
8-square classes (taxonomy sweep); Morgenstern 1e14 CITED-only. The
three congrua implementations cross-validated elementwise. Sieve design
recorded (wheel: roots coprime to 6, offsets 0 mod 24, centers with
prod(2a_i+1) >= 9); compiled-sieve push deliberately deferred (A6-T1) —
bounds cannot settle the problem (F5).

---

## 2026-08-25 — Entry 7: M8 wrap-up — state of the program

**Suite:** 53 checks, all green at FULL bounds (~15 s total); CI runs the
FAST profile with clean SKIPs where PARI is absent. Every PROVEN claim
has its machine-checkable content covered; every VERIFIED claim is
reproducible by a named command.

**What we believe the most promising next moves are, in order:**
1. A2-T1 / A5-P3 (the keystone): enumerate the finitely many genus ≤ 1
   curves on X (BTVA) and check each is degenerate — settles the
   function-field conjecture over char-0 constants and turns
   "probably finitely many" into a structured finiteness statement.
2. A3.C via A3-Q: explain the square-center additive desert. The
   157441 example shows it is genuinely about squareness. A proof would
   kill class E of the 8-square problem outright — the first
   impossibility theorem anyone would have proven in this family.
3. A4-T1: genus of the eighth-square condition over the rank-3 AB1
   fiber; genus ≥ 2 gives unconditional Faltings-finiteness there.
4. F3-T1 and F5-T1 are self-contained write-up tasks with known
   endpoints.

**Honest bottom line:** the open problem remains open, exactly as
expected. The program's value is the verified structure now in place:
the obstruction cannot be local (F5), cannot be congruence+order (A1.1),
is invisible to function fields below the rational-curve frontier (A2),
and manifests concretely as the square-center additive desert (A3/A4) —
which is where we would dig next.

---

## 2026-08-26 — Entry 8: Front 1 launched; state-of-the-field sweep (M9, phase R/W)

User chose Front 1 (curve enumeration on X) and asked for a duplication
check first, offering to acquire unfetchable papers. Sweep (~35 searches
+ agent; keyword-negative, citation-graph access unavailable): **nobody
has enumerated the low-genus curves on X**, computed its Picard/NS
lattice or Brauer group, or proven its genus ≤ 1 curves degenerate.
Decisive method fact: BTVA's finiteness is Jouanolou-based — structurally
non-effective; the singularity-passage refinements in their abstract are
for Barth's sextic and the cuboid surface, not X. Their Magma code lives
in arXiv ancillary files (unfetchable here). The Stoll–Testa cuboid
computation is the worked template for our M10. papers/WANTED.md
committed with the prioritized acquisition list; fetch attempts at
cecm.sfu.ca and scottkom.com confirmed blocked.

---

## 2026-08-26 — Entry 9: A7 — the line theorem, invariants, conic sweeps (M9)

**Theorem A7.3 (new, PROVEN):** complete classification of genus ≤ 1
curves on X with line image. Machinery: the (Z/2)^8-cover splitting
lemma with genus g = 1 + 2^(k-2)(r_eff - 4), and for lines the rigidity
k = r - 1, so genus ≤ 1 ⟺ r ≤ 4 ⟺ the line passes ≥ 2 multiple points
in patterns (3,3,3)/(3,3,2,1)/(3,2,2,2) — 69 candidates, mechanically
swept. Verdict: exactly u=0, v=0 (genus 0, 64 components each — the
classical 3-AP families, entry-degenerate) and c=0 (genus 1, 16
components — the center-zero curve gamma^2 = alpha^2+beta^2, delta^2 =
alpha^2-beta^2, whose rational points are all degenerate by OUR F3.2,
and which carries the Q(i,sqrt5) witness of A3.K: the catalog and the
descent-gap analysis meet exactly where they should).

**Corollary A7.4 (new, unconditional):** every nonconstant k(t) magic
square of squares has Lucas-image degree ≥ 2.

**Invariants (VERIFIED, discovery):** chi_top(X~) = 768, K^2 = 576 (two
independent routes), chi(O) = 112 (Noether integral), s2 = -192 < 0 —
and no intermediate double plane has s2 > 0. The naive Bogomolov route
is closed: **the quasi-hyperbolicity of X is carried by its 256 A_1
nodes** (which we located: 32 over each triple point). The effective
enumeration must go through orbifold-Miyaoka with node contributions or
BTVA's differentials (acquisition P1/P4/P6). Also b_2 = 766 + 4q: the
NS lattice is far larger than the cuboid surface's — M10 should work on
intermediate quotients.

**Conic layer:** exact analyzer (tangency = free absorption; conjugate
pairs as Galois columns); budget lemma; sweeps of 216 candidates
(tangent-to-5 complete for its class; 5-triple conics; 4-triple pencils
at rational tangency parameters; symmetric families): zero genus ≤ 1
components. High stakes noted: a genus-0 conic hit would DISPROVE A2.C
(conic entries are automatically distinct and nonzero). The showcase
circle u^2+v^2 = c^2 — tangent to four lines at four triple points! —
still has genus 9. Remaining conic configurations and extension-field
coefficients: precisely scoped for M10 in the A7 roadmap.

## 2026-08-26 — Entry 10: BTVA acquired and digested; their X numbers reproduced (M10-A)

The repository owner uploaded the arXiv source tarball of BTVA
(arXiv:1912.08908v3 = Algebra & Number Theory 16 (2022) 1377-1405) —
the P1 item of papers/WANTED.md. Archived in papers/1912.08908/
(tarball + full .tex + the authors' ancillary Magma files), READ end to
end; provenance upgraded in docs/references.md. Digest in A7 §7;
reproduction suite `verify/checks/a7_btva.py` on top of
`compute/btva_bounds.py` (exact rational arithmetic).

**The P1 questions, answered.** (a) The sweep's "Theorem 1.5" snippet
was the perfect-cuboid theorem (`thm:CuboidIntro`) — the paper contains
NO node-passage refinement, NO curve list, and NO ancillary code for
the magic-square surface; its complete X-content is quasi-hyperbolicity
(256 nodes > ell_min(8) = 217) plus "sections from m = 47 on, h^0 >=
8448", and it explicitly calls X "out of range of current computational
techniques" for the explicit special-curve method. Our enumeration
program is non-duplicative — now confirmed from the primary source.
(b) Their model of X is our model; 256 ordinary double points stated,
matching our count. (c) No effective degree bound anywhere in the body
(Jouanolou finiteness), as predicted. (d) anc/ = Barth sextic + cuboid
scripts only.

**Reproductions (all exact, all green):** chi^0 first-values table;
chi^0 + chi^1 = chi(s) across their three independently printed
piecewise families (to m = 2000); ell_min table 73/145/217/145/0;
their CI Chern formulas give (K^2, c_2) = (576, 768) at n = 8 — equal
to our branched-cover stratification values from M9 (two fully
independent routes now agree); **X: bound positive exactly from m = 47
with value 8448** (proved for all m >= 47 via Cauchy root bounds) and
growth (160/27)m^3; cuboid partial-information calibration (r = 35
poles, leading coefficient 1/108, threshold 862, r minimal); Barth
decic 160/15755; Sarti 28/7646. Also: the Serre-duality (BO) route
fails for X (leading -160/27; would need 315 nodes) — the chi^1 bound
is the one that works, by a 39-node margin.

**Three display-level errata found** (their conclusions all verify):
"3n^2 - 27 + 66" for 3n^2 - 27n + 66 in the quadric-CI display; a
missing S^47 in the section-7 restatement of the X bound; and the
Barth-decic displayed piecewise bound matching ell = 339 (all 12
coefficients) instead of the correct ell = 345 that its stated
conclusions use.

**Strategic outcome.** The direct route ("compute their differentials
on X, intersect base loci") is confirmed closed at current technology —
but the cuboid proof's real engine turns out to be a *base-descended*
differential: omega = phi^*(eta)/(y1 y2 y3 z^2) with eta a degree-2
symmetric differential on P^2 whose integral curves they classify
completely (a conic + its tangents). The X-analogue — eta on the Lucas
plane with entry-line-monomial denominator, regularity checked by
exactly our M9 absorption calculus along the nine branch lines, then an
integral-curve classification — would constrain genus <= 1 curves of
ALL image degrees at once, bypassing the infeasible module computation.
Precedent: García-Fritz–Urzúa got "every genus <= 1 curve through >= 2
nodes" for the cuboid this way. That is now A7 roadmap item 2 and the
lead candidate for M11.

## 2026-08-26 — Entry 11: the conic layer is closed (Theorem A7.6) (M10-B)

**Lemma A7.5 (sharp conic budget).** For a smooth conic every entry
line through one of its points is transversal or THE tangent there, so
per-point profiles are forced: (s,t) = (mu,0) or (mu-1,1). With total
multiplicity 18 and the genus formula, genus 0 over a conic needs >= 5
tangent entry lines, and genus 1 needs exactly 4 effective points with
tangency count T in {3,4} realizing EXACTLY six type-multiset classes
C1-C6. The case analysis is itself machine-verified
(a7cc.budget_lemma regenerates the six signatures exhaustively).

**Theorem A7.6: no curve of geometric genus <= 1 on X has conic image
(char 0).** Legs: (1) T>=5 is complete and rational — a smooth conic
tangent to five entry lines has a smooth dual through five rational
dual points, so no concurrent triple among them (98 of 126 5-subsets
die here) and the unique dual conic is rational (28 candidates, swept
in M9, zero hits). (2) Pencil classes C1/C4: members = common roots of
nine discriminant quadratics — resolved exactly over Q and Q(sqrt D)
by a new field-generic analyzer (validated: agrees with the M9
analyzer on all 216 rational candidates); collinear point sets (47 and
822; the 8 triple points carry exactly 10 collinear 3-subsets) admit
only reducible conics. (3) Linear classes C3/C5/C6 (tangent-at-a-
multiple-point conditions are linear: Mp || l): 10,932 systems; unique
solutions analyzed; degenerate solution spaces skipped only with PROOF
of all-member reducibility (det cubic vanishing on a {0..3}^d grid
vanishes identically). (4) Net class C2: 46 nets x 126 tangency
4-subsets; pairwise Sylvester z-resultants after a basis change making
all leading coefficients nonzero constants (the naive formal resultant
vanishes spuriously — caught and fixed); constant gcd certifies
emptiness over Qbar: 5792/5796 certified, and the 4 surviving
candidates are all the SAME conic — the circle u^2+v^2 = c^2, genus 9.
Total: 1265 irreducible conics analyzed across all classes, ZERO of
genus <= 1, zero unresolved flags.

**Corollaries.** Every genus <= 1 curve on X (char 0) has Lucas-image
degree >= 3; every nonconstant k(t) magic square of squares with
char k = 0 has image degree >= 3 (was: >= 2). Conjecture A2.C is now a
statement about degree >= 3 images. The circle — tangent to four lines
AT four triple points and still genus 9 — is the unique near-miss of
the entire layer, found independently by two different engines.

New code: compute/conic_complete.py (exact Q(sqrt D) layer, field-
generic analyzer, linear-condition solver, pencil disc-root engine,
elimination certificates); verify/checks/a7_conics.py (7 checks).
Suite: 74 checks green.

## 2026-08-26 — Entry 12: six Tier-1 papers ingested; A8 launched — the descent computation (M10-C, M11-A)

The owner uploaded all six Tier-1 PDFs (García-Fritz–Urzúa
arXiv:1804.07671 — the guessed ID was right; Stoll–Testa 1009.0388v2
(2025 update!); Horie–Yamauchi 2512.22520; Lu–Miyaoka MRL 1995;
Miyaoka Publ. RIMS 2008; Bruin–Ilten–Xu 2312.01722). All in papers/,
provenance upgraded (GFU READ in full; others READ to main-theorem
depth). Three digests matter strategically: (1) GFU's Vojta machinery
(omega-integral curves, cyclic-cover towers, toric local calculus,
node-passage bounds on the cuboid); (2) Stoll–Testa 2025: the cuboid
benchmark trio — BTVA (>=7 nodes spanning P^6), GFU (>=2 nodes;
rational non-conic C.E >= 8), lattice (C.E >= 8 / >= 4) — nothing
analogous exists for X; (3) the NEGATIVE: Lu–Miyaoka/Miyaoka-2008
effective bounds need K^2 > c_2, and X has 576 < 768, still 576 < 640
after the A_1-orbifold correction — the old A7 roadmap item
"orbifold-Miyaoka" is closed for the full surface.

**A8 (new attack doc): descent of symmetric differentials.** Theorem
A8.1: H^0(X - nodes, S^m Omega^1) decomposes under the (Z/2)^8 Galois
group into 256 character eigenspaces V_S (S = even sets of entry
lines), and each V_S is a finite exact linear-algebra problem ON THE
LUCAS PLANE: membership is divisorial (poles of bundle sections live
in codim 1; nodes and multiple-point fibers are codim 2), with
explicit per-line order conditions from the double-cover local model
f = w^2. This replaces BTVA's infeasible P^8 Groebner route ("out of
range of current computational techniques") — the structure they did
not use is the abelian cover.

**Engine** (compute/descent_differentials.py): exact sparse linear
algebra over Q; two charts (u=1 sees all nine lines; c=1 sees u=0);
saturation-checked degree bounds; 8 grid symmetries reduce 256
characters to 51 orbits. Controls: the two-line sub-cover (= P^1 x
P^1) returns 0 in all characters at m=1,2,3; the instructive near-trap
eta = dl1*dl2 (pullback 4 dx1 dx2, affinely regular) is rejected for
exactly its order-4 pole over u=0; orbit equivariance; and m=1 equals
the classical Zariski/Esnault–Viehweg prediction. Structural facts
proven en route: the 8 triple points are the 8 lines-of-three of the
3x3 grid; the two 3-pencil systems have base points on v=0 / u=0
(where the degenerate curve families live); the nine lines split as
"6 tangents of a smooth conic + a 3-line pencil" in two ways.

**Results.** (m=1) q(X~) = 0: hence b_1 = 0, b_2 = 766 (M9's
b_2 = 766 + 4q resolved), h^{1,1} = 544. (m=2) ALL 256 characters
vanish: h^0(X - nodes, S^2 Omega^1) = 0. Contrast the cuboid's
13-dimensional space, which powers the entire BTVA/GFU explicit
program there. So on the magic-square surface the m=2 program is not
"out of range" — ITS INPUT SPACE IS EMPTY. Any explicit-differential
attack must start at m >= 3 (survey running). Honest caveat, recorded
in A8 §4: the gold-standard positive control (reproducing the
cuboid's 13 by the same descent, over Q(i) with a conic branch
component) is the next milestone; until it passes, the zeros carry
that caveat.

Also in A8 §6: the Vojta/GFU route has a structural deficit on the
full 9-line cover (every pencil-theta or conic-dual differential pays
4 per 3 lines covered; Bott kills cheaper sections; balance would
need 9 lines tangent to one conic, we have 6) — properly so, since X
does have genus <= 1 curves; the productive continuations are the
zero-deficit sub-cover statements and GFU-§3-style node-passage
bounds, both scoped in the A8 roadmap. Suite: 81 checks green.

## 2026-08-26 — Entry 13: the cuboid control PASSES; first-section bracket {3..7} (M11-B)

**The decisive validation.** The descent engine, pointed at the
perfect-cuboid surface (a (Z/2)^4 cover of P^2 branched on four
Q-irreducible conics — three line pairs and the circle; 48 nodes over
the 3 line-pair vertices (8 each) and the 6 tangencies with the circle
(4 each), all codim 2), reproduces BTVA's Magma-computed
h^0(X_pc, hat-S^2 Omega^1) = 13 EXACTLY — and not just the total: the
full 16-character fingerprint read off their Table 1 (dims 3, 3, 3 on
the trivial, z-, and y1y2y3-characters; 1 on each y-pair and on
y1y2y3z; 0 on the other nine), with element-level membership of their
descended generators (omega_4 -> dc^2/Q3 - dv^2/Q2 in V_{z};
omega_7 -> (Q2 dc^2 - 2cv dcdv + Q3 dv^2)/Q4 and x2·, x3·omega_7 in
V_{y1y2y3}), plus q(X_pc') = 0 at m = 1. New machinery exercised:
mod-conic divisibility conditions (adapted bases with unit partials),
singular branch conics, and the |T|-pole allowance along the etale
line x1 = 0 from projective balancing. First run, no tuning.
compute/descent_cuboid.py; check a8.cuboid_control.

The A8 zeros for the magic-square surface (q = 0; h^0(S^2) = 0 across
all 256 characters) therefore stand with their positive control in
place — the pending-caveat is retired.

**Theorem A8.4 (first-section bracket).** chi(X, hat-S^m) =
chi(Y, S^m) + 256 chi_loc(m) = -624, -1344, -1360, -1632, -560, +384
for m = 2..7 (near-miss at m = 6). With the classical h^2-vanishing
(m >= 3; PROVEN-CLASSICAL via BO/Deschamps as in BTVA's Leray lemma):
h^0(X - nodes, S^7 Omega^1) >= 384. So the FIRST NONZERO SYMMETRIC
DEGREE on X-minus-nodes lies in {3, ..., 7} — dramatically below
BTVA's m >= 47 guarantee on the resolution. The m = 3 exact survey is
running; m = 4..6 will go through a mod-p fast path (nullity mod p = 0
proves Q-nullity = 0). Locating the first nonzero m and extracting
explicit generators would put BTVA's own resultant corollary to work
on X at n = 8 — the full explicit special-curve program that has never
been executed on this surface.

Suite: 83 checks green.

## 2026-08-26 — Entry 14: FIRST EXPLICIT SYMMETRIC DIFFERENTIALS ON X — m_min = 4, h^0(S^4) = 6 (M11-C)

**The "out of range" computation is executed.** With the mod-p fast
path (a zero nullity mod p PROVES the exact zero — rank only drops
under reduction; validated against the cuboid's nonzero 13-fingerprint
and the exact m=2 dims), the surveys give:

  m = 1: 0    m = 2: 0    m = 3: 0 (all 256 characters, saturated)
  m = 4: h^0(X - nodes, S^4 Omega^1) = 6 — ONLY the trivial character.

The m = 4 trivial eigenspace is certified sandwich-style: six exact
rational vectors verified against the exact condition system (dim >=
6) meeting the mod-p nullity (dim <= 6) — no exact elimination needed
(mod-p RREF -> rational reconstruction -> exact row verification).
The six generators are stored with exact coefficients in
compute/data_m4_generators.py (numerators over prod l_(a,b)^2, degree
<= 23) and re-verified from scratch by a8.m4_generators; the 51-orbit
spectrum record is compute/data_m4_spectrum.json (a8.m4_spectrum).

So the first nonzero symmetric degree on the magic-square surface is
m_min = 4 — against BTVA's resolution-level guarantee m >= 47 — and
ALL six first differentials are Galois-invariant: they descend from
orbifold symmetric differentials of (P^2, (1/2) sum of the nine entry
lines). The Lucas plane itself carries the hyperbolicity data.
(Contrast the cuboid: its m = 2 space of 13 spreads over seven
characters.)

Consequence: BTVA's explicit special-curve machinery is applicable to
X for the first time. With any two independent omega_i among the six:
every complete genus-0 curve on X avoiding the nodes lies in
res(omega_i, omega_j) (their s:resultants, intro passage on X-level
sections); node-passage refinements follow the cuboid template. The
next milestone (M11-D) computes the resultant locus and intersects
over the 15 pairs.

Ops note: an overly broad pkill killed both background surveys once
(the redundant exact m=3 AND the m=4 survey — restarted parallelized);
the m=3 exact run was retired as redundant (its zero already proven by
saturated mod-p at two degree bounds).

## 2026-08-26 — Entry 15: NODE PASSAGE — every complete genus-0 curve on X meets a node (M11-D)

**The resultant-locus program is executed** (compute/special_locus.py;
checks a8.z_properness, a8.z_catalogue, a8.z_scan — the whole module,
6-scan certificate included, runs in ~3 s).

The six invariant m = 4 generators give six binary direction-quartics
F_a(P; dc, dv) = sum_k N_k^(a)(P) dc^k dv^(4-k); the special-curve
locus Z is the set of plane points where all six share a projective
root. Structure established:

- Lemma A8.6 (PROVEN, unconditional): a node-avoiding complete
  genus-0 curve on X has Lucas image avoiding all 8 triple points
  (their pi-fibres consist of nodes only: the (Z/2)^3 local cover is
  the A_1 cone, the residual (Z/2)^5 acts freely — 8 x 32 = 256), of
  degree >= 3 (A7.3 + A7.6), and contained in Z (the whole 6-space is
  invariant, so integrality descends: genus 0 kills sections of
  O(-8), and off the branch lines pullback is injective on rational
  symmetric differentials).
- Exact catalogue (PROVEN): all nine entry lines lie in Z; v = 0,
  u = 0 and the six distinctness lines are NOT integral. u = 0 —
  invisible in the (c,v)-chart — is tested by a chart-2 slice
  formula: regularity along u = 0 forces deg N_0 <= 14 (it holds,
  = dN - 9), and the restriction is the degree-14 part of N_0 over
  (1-z^2)^6; verdict cross-checked by the transpose symmetry
  swapping u=0 <-> v=0.
- Certificate A8.7 (VERIFIED mod p): along 3 exact rational lines
  (each certified generic: nine pairwise-distinct crossings) at 2
  primes (999999937, 1000003919), the gcd of all 15 pairwise
  resultants Res(F_a, F_b) — degrees 92..96 against the a-priori
  bound 8 x 14 = 112 — has degree exactly 72 = 9 crossings x
  multiplicity 8, NOTHING else, in all six scans. The nine entry
  lines account for the entire gcd: mod p, the curve part of Z is
  exactly the nine entry lines.

**Theorem A8.8 (node passage for rational curves): every complete
curve of geometric genus 0 on X passes through at least one of the
256 nodes** — equivalently, every rational curve on the resolution
meets the (-2)-locus. PROVEN modulo the certificate's exact upgrade
(A8-T3: exact bivariate gcd / primary decomposition of Z; until then
the mod-p tag stays on honestly). Non-vacuous and sharp: the 64 + 64
classical AP-families over u=0 / v=0 are complete rational curves on
X, their images carry the A-/B-triple points, and they duly pass
through nodes. BTVA prove node-passage only for Barth's sextic and
the cuboid and declare X out of range; this is the first such
statement for the magic-square surface, at m_min = 4.

Next: the node-extension layer (which of the six sections extend over
which exceptional (-2)-curves — the chi^0-conditions on the cone
model) to push ">= 1 node" toward the cuboid-grade ">= 2 nodes"
(A8 §8 item 3); m = 5..7 surveys for the section-ring growth; A8-T3.

Suite: 90 checks green (FULL).

## 2026-08-26 — Entry 16: THEOREM A8.8 MADE UNCONDITIONAL — the exact special-curve locus (M11-E / A8-T3 closed)

The mod-p caveat lasted one commit. compute/z_exact.py (~5 s,
a8.z_exact) computes the two pairwise resultants R_12 =
Res(F_1, F_2), R_34 = Res(F_3, F_4) EXACTLY in Z[c, v] and identifies
Z's curve part over Q-bar:

- Provably exact CRT: the six generators have 2-3-digit integer
  coefficients once content-free, so the permutation-expansion bound
  |coeff(Res)| <= prod_rows l1(row) is ~10^24 and THREE 30-bit primes
  make the 113 x 113 grid interpolation provably complete — no
  Hadamard slack, no sampling. Independently spot-verified at six
  integer points against exact integer Sylvester determinants.
  R_12: total degree 96, 864 terms, <= 15-digit coefficients.
  R_34: degree 92.
- Exact peeling over Z (synthetic division by the monic-in-c entry
  lines): R_12 = (prod l^8) l_(0,0)^4 C_12 (deg C_12 = 20),
  R_34 = (prod l^8) l_(-1,0)^2 l_(1,0)^2 l_(0,-1)^4 l_(0,1)^4 C_34
  (deg C_34 = 8); no entry line divides a cofactor.
- Coprimality of C_12, C_34 over Q in the sound direction: their
  v-leading coefficients stay alive mod p = 999999937, and
  Res_v(C_12, C_34)(c_0 = 2) != 0 mod p, so a common factor with
  deg_v >= 1 is impossible (Gauss + lc_v divisibility); deg_v = 0
  common factors die by the exact v-content gcd (= 1).

Hence gcd(R_12, R_34) = prod over all nine lines of l^8, up to a
constant — the SAME divisor the M11-D line scans measured (their
crossing multiplicity 8 = these gcd exponents; two independent
computations agree). An irreducible curve inside Z divides both
resultants, so it is an entry line:

  THEOREM A8.7' (exact): the curve part of Z over Q-bar is contained
  in the nine entry lines. PROVEN.
  THEOREM A8.8: every complete genus-0 curve on X passes through at
  least one of the 256 nodes. PROVEN — UNCONDITIONAL.

The exact resultants are committed (compute/data_z_resultants.json,
38 KiB) and the verify check re-derives the whole certificate from
the stored generators on every run, FULL and FAST, comparing against
the stored file. A8-T3 is closed the day it was opened; docs, ledger
and roadmaps updated (remaining §7-adjacent work: node-extension
layer toward ">= 2 nodes", m = 5..7 surveys).

Suite: 91 checks green (FULL).

## 2026-08-26 — Entry 17: THE RESOLUTION CARRIES A SYMMETRIC DIFFERENTIAL — h^0(Ytilde, S^4) = 1 (M11-F)

The node-extension layer, executed (compute/node_extension.py;
checks a8.node_tau, a8.node_extension; ~25 s total).

Local calculus (Lemma A8.9): every one of the 8 triple points is a
3-term ARITHMETIC PROGRESSION of entry lines (rows, columns and
diagonals of the grid: l_A + l_C = 2 l_B), so the local (Z/2)^3
subcover is always the SAME cone z_3^2 = (z_1^2+z_2^2)/2 — with the
integer parametrization q_1 = s^2+2st-t^2, q_2 = -s^2+2st+t^2,
q_3 = s^2+t^2 (q_1^2 + q_2^2 = 2 q_3^2). For an invariant germ, tau
= minimal (s,t)-order (even, >= 0); the resolution chart (s^2, t/s)
gives ord >= ceil((tau+4-2j)/2) per component: EXTENSION iff
tau >= 4, else pole order 2 - tau/2 <= 2.

The exact tau-table (all 8 points; B's via the transpose): at EVERY
triple point the filtration is dim 6 / 4 / 4 / 0 (tau >= 0/2/4/6) —
tau jumps 0 -> 4, pole orders in {2, 0}. The 6-space is an explicit
D4-representation (sigma: eta_1 <-> eta_2 up to 4, eta_3 <-> eta_6;
flips diagonal; all pinned). Extension-subspace lattice: pairwise
dim 2 (22 pairs) or 3 (the five middle-pencil pairs + D+D-);
A-/B-triples dim 2; and the GLOBAL intersection is 1-dimensional:

  W = <eta_4>, certified directly (tau(eta_4) = 4 at the 5 visible
  points AND tau(sigma* eta_4) = 4, covering the 3 B-points).

Restriction to X - nodes is injective on resolution sections, so

  h^0(Ytilde, S^4 Omega^1) = 1  (and 0 for m <= 3):

THE RESOLUTION OF THE MAGIC-SQUARE SURFACE CARRIES A UNIQUE
SYMMETRIC QUARTIC DIFFERENTIAL eta* = eta_4 — at m = 4, against
BTVA's resolution-level guarantee m >= 47. eta* spans the trivial
D4-line.

Consequences (all PROVEN, exact):
- Theorem A8.11: EVERY complete genus-0 curve on X — through nodes
  or not — has Lucas image an integral curve of the single web
  eta*. The classical AP families comply: u=0 and v=0 ARE
  eta*-integral (and the six distinctness lines are not — matching
  A7.3's list of genus-0 line images exactly).
- Theorem A8.12: every complete genus-0 curve has Ctilde . E >= 4 on
  the resolution (some section restricts nonzero by A7.3 + A8.7';
  poles in {0,2}). Cuboid benchmark: C.E >= 8 (Stoll-Testa Lemma
  21); ours is the first bound of this type for X.
- Theorem A8.13 (pattern dichotomy): a genus-0 curve with node
  pattern S (triple points visited; S nonempty by A8.8) has image
  integral for V_S = the intersection of the visited extension
  subspaces (dim >= 2 for |S| <= 2). Consistency verified exactly:
  u=0 is integral for the FULL 2-dim B-triple space <eta_3, eta_4>
  and v=0 for the A-triple space <eta_4, eta_6> — exactly what the
  AP components' patterns S = {B's} resp. {A's} demand.

Next (M11-G): per-pattern resultant loci — run the exact A8.7'
machinery on the subsystems V_S to classify their integral curves,
turning the dichotomy into "|S| >= k or an explicit finite list";
then the single-web analysis of eta* (GFU §2-style). The endgame is
a Stoll-Testa-grade classification of all rational curves on X.

Suite: 93 checks green (FULL).

## 2026-08-26 — Entry 18: TWO NODES — singleton patterns excluded at all eight triple points (M11-G)

Theorem A8.14 (PROVEN, compute/pattern_loci.py, a8.pattern_singletons,
~45 s): EVERY COMPLETE GENUS-0 CURVE ON X MEETS NODES OVER AT LEAST
TWO DISTINCT TRIPLE POINTS — in particular passes through >= 2
distinct nodes. The magic-square analogue of BTVA's cuboid Theorem
1.2 (">= 2 of the 48 nodes"), by a different mechanism: extension
subspaces instead of E-vanishing counting.

Proof shape: a singleton pattern S = {P} forces the Lucas image into
the curve part of Z(V_P) for the 4-dimensional extension subsystem
V_P (Theorem A8.13); the A8.7'-machinery applied at EACH of the
eight triple points — two basis-pair resultants, provably exact CRT,
entry lines peeling to order >= 8, peeled cofactors witnessed
coprime over Q — pins that curve part inside the nine entry lines;
genus-0 curves have no entry-line images (A7.3). The first basis
pair choice (b0b1, b0b2) succeeded at all eight points (cofactor
degrees 8..24; B-point bases via the exact transpose transfer).

Consistency: the classical AP families visit THREE triple points
each (their images u=0 / v=0 carry the B- resp. A-triples).

Next (M11-H): the |S| = 2 loci (dim-2/3 subsystems, one resultant +
component analysis vs the six outside triple points), aiming at
|S| >= 3; then the eta*-web analysis toward full enumeration.

Suite: 94 checks green (FULL).

## 2026-08-26 — Entry 19: THREE TRIPLE POINTS, SHARP — the pattern-counting layer is complete (M11-H)

Theorem A8.15 (PROVEN, a8.pattern_pairs, ~90 s for all 28 patterns):
EVERY COMPLETE GENUS-0 CURVE ON X MEETS NODES OVER AT LEAST THREE
DISTINCT TRIPLE POINTS — hence >= 3 distinct nodes — AND THE BOUND
IS SHARP: the classical AP components over u=0 / v=0 have pattern
exactly {B0, B+, B-} resp. {A0, A+, A-}.

A pattern-{P,Q} image must contain P and Q, avoid the other six
triple points, be integral for the pencil V_S = V_P cap V_Q (for
dim 2, Z(V_S) = V(Res) EXACTLY), and not be an entry line (A7.3).
The 28 patterns die three ways:
- 6 (the dim-3 lattice pairs): coprime peeled cofactors — Z(V_S)
  curve part = entry lines;
- 10: the peeled cofactor does not vanish at P or Q (exact
  projective evaluation); where the PQ-line divides first (the
  pencil carriers for A-A / B-B pairs) it is excluded by the third
  family point it carries — exactly the AP-family mechanism — and
  divided out;
- 12 (outer points of different families): the cofactor is a
  degree-18 curve through ALL EIGHT triple points, PROVEN
  irreducible over Q (restrictions to degree-preserving rational
  lines, squarefree over Q, mod-p factor-degree subset-sums empty
  across 3 lines x 8 primes; one line/prime even gives an
  irreducible restriction mod p). A rational point on a
  Q-irreducible curve lies on EVERY Galois-conjugate component, and
  the six outside triple points are rational and on the curve: every
  component excluded.

With A8.8 (|S| >= 1), A8.14 (>= 2) and A8.15 (>= 3, attained), the
pattern-COUNTING story is closed. What remains is CLASSIFICATION at
|S| = 3: the integral curves of the triple-pattern subsystems beyond
the classical families (A-/B-triples: the 2-spaces <eta_4, eta_6> /
<eta_3, eta_4>; mixed triples: down to the eta*-web itself) — the
road to a Stoll-Testa-grade classification of all rational curves
on X (M11-I).

New machinery: sympy-free bivariate irreducibility certificates
(DDF degree subset-sums over multiple lines/primes), exact
projective point evaluation, affine-line division, sound-direction
integrality refutation via mod-p pseudo-remainders.

Suite: 95 checks green (FULL).

## 2026-08-26 — Entry 20: THE CLASSIFICATION LAYER CLOSES — dim >= 2 patterns are classical; everything else is the eta*-web (M11-I)

Theorem A8.16 (PROVEN, a8.pattern_spaces, ~50 s): a complete genus-0
curve on X whose node pattern S has dim V_S >= 2 is one of the 128
classical AP components (image v=0 with S = {A0,A+,A-}, or u=0 with
{B0,B+,B-}).

The census: over ALL patterns |S| >= 3, V_S takes exactly EIGHT
values — seven of dimension 2 and <eta_4>. The seven have beautiful
geometric meaning:
- the A-cluster <eta4,eta6> (A-triple + each 2-A's-plus-B0 pattern)
  and the B-cluster <eta3,eta4> (dual);
- the central-line space <eta3+eta6,eta4>: patterns inside
  {A0,B0,D+,D-} — exactly the four triple points ON the central
  entry line;
- four outer spaces for the coherent triples {A±,B±,D±} — exactly
  the triples of triple points ON the outer entry lines l_(±1,±1).

Per space, the integral curves of Z(W) are classified exactly: entry
lines; v=0 precisely for the A-cluster; u=0 precisely for the
B-cluster; and the leftover cofactors K (degrees 8/8/12/18^4) are
certified irreducible over Q with the integrality identity
K | F(grad K) REFUTED mod p. The refutation kills every
Qbar-component at once: W is defined over Q, so integrality of a
Q-irreducible curve is Galois-all-or-none, and all-integral would
force the identity (K squarefree). Hence dim >= 2 patterns force
image u=0/v=0 — classical — and the 17 non-family dim-2 patterns
are IMPOSSIBLE.

COROLLARY (the web reduction): every complete genus-0 curve on X
other than the 128 classical AP components has V_S = <eta*>: its
image is an eta*-integral curve of degree >= 3 through >= 3 triple
points, pattern among 200 listed dim-1 subsets. THE RATIONAL-CURVE
PROBLEM ON X IS REDUCED TO THE ALGEBRAIC INTEGRAL CURVES OF THE
SINGLE WEB eta* — the resolution's unique symmetric quartic
differential. M11-J opens the web analysis (GFU §2-style).

Suite: 96 checks green (FULL).

## 2026-08-26 — Entry 21: THE WEB'S LINE LEVEL — fifteen integral lines, four of them new (M11-J opening)

Theorem A8.17 (PROVEN, compute/web_lines.py, a8.web_lines, < 1 s):
the eta*-web has EXACTLY FIFTEEN integral lines over Qbar — the nine
entry lines, u = 0, v = 0, and a genuine discovery:

    FOUR NEW LINES OVER Q(sqrt3):   sqrt3 c = +-u +- v,

each passing through exactly one diagonal triple point D+- and no
other triple point. By A7.3 the X-components over these lines all
have genus >= 2 (a line through only one triple point crosses the
arrangement too often), so the web's line level carries no rational
curves beyond the classical families — exactly as A8.15/A8.16
demand. (Had a genus-0 component lived there, its pattern would
have size 1 — contradicting the three-triple-points theorem. The
edifice is consistent.)

Method: the restriction of eta* to c = a + b v gives 11 coefficient
equations in Z[a,b]; two NONZERO a-resultants (identically-zero pair
resultants certify nothing and are skipped — caught a vacuous first
attempt; nonzero ones are sound by the Bezout identity) have exact
gcd peeling as b^24 (b^2-1)^24 (3b^2-1)^6 down to a CONSTANT, so
b in {0, +-1, +-1/sqrt3}; per-candidate exact gcds over Q resp.
Q(sqrt3) (reusing conic_complete's field arithmetic) pin 13 points,
each verified integral by substitution; v = k reduces to k^2 = 0;
u = 0 is the chart-2 slice. Conics are excluded by A7.6 wholesale:
the web frontier starts at CUBIC integral curves.

Also caught en route: a truncation bug in a throwaway script
(int(Fraction) silently floors) produced a wrong Groebner basis on
the first pass — the repo module clears denominators exactly and
cross-checks the 15 lines by direct substitution.

Suite: 97 checks green (FULL).

## 2026-08-27 — Entry 22: A9 — the discrete-sphere model (owner's picture, made exact)

New attack file A9 (docs/attacks/A9-discrete-spheres.md;
compute/discrete_spheres.py; checks a9.dictionary, a9.tension),
formalizing the owner's geometric brainstorm: the problem as lattice
points on spheres.

The dictionary (PROVEN, machine-checked): with center entry m^2,
every magic line sums to 3 m^2, so a magic square of squares is
EIGHT POINTS OF THE SINGLE DISCRETE SPHERE S(3 m^2) in root
coordinates, glued by shared coordinates (center on 4 lines, square
corners on 3, edges on 2); the trivial point (m, m, m) is the
all-equal square; and the m-SLICE (points with a coordinate = m)
bijects exactly with A3's congrua set D(m) via
(e, f) -> (|e-f|, m, e+f) — A3 is the discrete-circle slice of the
sphere model. Parity shadow: 3 m^2 == 3 (mod 8) forces all-odd
coordinates on every representation.

A subtlety the checks enforce (caught by a failing first draft): the
square's 8 MAGIC lines are the zero-sum label triples, while the 8
TRIPLE POINTS of the arrangement are the grid-collinear triples —
exactly four of which are magic lines (A0, B0, D+-: genuine sphere
collapses, and precisely the four triple points on the central entry
line that organize the A8 §8 classification), while the outer four
(A+-, B+-) are oblique. The A8 counting theorems read: any
1-parameter family of solutions passes through >= 3 of these eight
degeneration points.

The tension, quantified (a9.tension): by m <= 200 the sphere reaches
64 points (abundance ~ class numbers; Duke equidistribution), while
the compatibility ladder on the slice — an MSS3 needs an additive
quadruple in D(m) — stays at L3 = L4 = 0 (consistent with A3's far
larger desert). Abundance without compatibility: the counting
heuristics' optimism against the Bombieri-Lang scarcity our surface
theorems support.

Open: A9-T1 (the class-group torsor formulation of the 8-point glued
configuration via Gauss/Venkov, genus-theory constraints first);
P8 backlog acquisitions (Duke, Aka-Einsiedler-Shapira, Venkov).

Suite: 99 checks green (FULL). [M11-K surveys still running in the
background: m=6 nearly done all-zero; m=8 tau-test in its big
elimination.]

## 2026-08-27 — Entry 23: A9-T1 first layer — the Eisenstein anchor and slice confinement

compute/sphere_classes.py (checks a9.class_numbers, a9.gauss_map):

THE EISENSTEIN ANCHOR: every magic-square sphere has n = 3 m^2, so
its binary quadratic theory lives in the ONE field Q(sqrt-3) — the
order Z[m sqrt-3] of conductor m — and the primitive sphere size is
exactly a ring class number:

    r3*(3 m^2) = 24 h(-3 m^2)   (8 = 24/3 at m = 1),

verified for 13 sample m up to 105, with h computed two independent
ways (conductor formula vs primitive reduced forms, agreeing for all
m < 60). Caught en route: the imprimitive form (2,2,2) inflating a
naive h(-12) count — order class numbers are primitive-form counts.

THE GAUSS MAP (the Aka-Einsiedler-Shapira object, implemented):
point -> class of the orthogonal lattice v^perp cap Z^3 (determinant
certified by saturation). Fibers uniform (48 = signed-permutation
orbit; torsor behavior); hit-classes track h up to the expected
conflations.

SLICE CONFINEMENT (measured; the first class-group constraint on
configurations): primitive through-center points exist iff every odd
prime of m is == 1 mod 4, and then number 48 * 2^(w-1) in at most
2^w classes (w = #such primes) — EXPONENTIALLY CLASS-CONFINED while
the ambient class number grows linearly. The four through-center
lines of any magic square must sit inside this thin window; the next
A9-T1 step expresses the outer-line gluing as Gauss-composition
relations against it.

Suite: 101 checks green (FULL). [M11-K still grinding: m=6 survey
and the m=8 tau-test elimination.]

## 2026-08-27 — Entry 24: A9-T1 second layer — the gluing law and the coherence obstruction

The user's directive: push the outer-line gluing through Gauss
composition against the slice window and see what it forbids. It
forbids most of the cross-branch pairings.

THE GLUING LAW (Lemma A9.1; one-line proof, machine-verified on 960
points): for v = (x, y, z) on S(n) the cross-vectors (0,-z,y),
(z,0,-x), (-y,x,0) lie in v^perp with norms n - x^2, n - y^2,
n - z^2. So the Gauss class of every magic LINE represents the
co-norm 3m^2 - e of each of its ENTRIES — gluing (shared entries)
becomes shared represented values between classes: the bridge from
configuration to composition. Bonus (Lemma A9.4): all-odd
coordinates force every orthogonal lattice EVEN.

THE OBSTRUCTION (Theorem A9.3): the genus characters chi_p (odd
p | 3 m^2; machine-validated as class invariants per sphere, the
2-adic candidates correctly failing since n == 3 mod 4) must be
constant on each line's co-norm triple. In Lucas differences (U, V)
the 8 lines give 8 explicit triples among 2m^2 +- {0, U, V, U+V,
U-V}; necessity is proven, and NO assumption that U +- V are
congrua is needed — it applies to bare congrua PAIRS.

THE BITE (measured, pinned in a9.coherence): ordered congrua pairs
killed — 10/12 at m = 65, 85, 130 (survivors: exactly the two
imprimitive branches paired together), 6/12 at m = 145 (survivors:
exactly the pairs involving the 5-branch congruum 21000), 0 at the
prime powers 25, 125. Cross-branch gluing at multi-prime
hypotenuses is mostly arithmetically incoherent — the first
necessary condition on extending congrua pairs to magic squares
beyond the classical 24 | d layer (A3/F4). Also measured: the
slice window sits STRICTLY inside Rep(2m^2) (2 vs 5 classes at
m = 13) — confinement is finer than representation alone.

Open next: what kills the surviving same-branch pairs (genus
characters cannot separate within a genus — class/spinor structure
under composition, Venkov / Aka–Einsiedler–Shapira territory), and
the full 9-entry gluing: each corner entry lies on TWO outer lines,
forcing shared representations between those classes.

Suite: 103 checks green (FULL). [M11-K: m=6 survey and the m=8
tau-test still grinding in the background.]

## 2026-08-27 — Entry 25: A9-T1 third layer — the three-sieve pair desert

An honest correction opens this entry: looking again at entry 24's
coherence "survivors", every one of them has U + V > m^2 — the
smallest edge entry m^2 - U - V would be NEGATIVE. Positivity, the
most elementary sieve of all, kills them trivially; the character
sieve had been measured in isolation. Stacking the sieves turned
the correction into the strongest A9 result so far.

THE THREE SIEVES (each proven necessary for a pair (U, V) in
D(m)^2 to extend to a magic square of squares with center m^2):
(1) POSITIVITY: U + V <= m^2. (2) COHERENCE: Theorem A9.3's
chi_p-constancy on all eight co-norm triples. (3) REPRESENTATION:
each triple must be represented by a SINGLE even class at an
admissible discriminant -4(3m^2)/g^2, g over the possible contents
(odd, g^2 | 3m^2, g^2 | the triple) — necessity by Lemmas A9.1 +
A9.4 applied to the reduced point; strictly stronger than the
character layer, since same genus is not same class.

THE RESULT (measured, pinned in a9.pair_desert): for EVERY center
m <= 1200, EVERY ordered congrua pair dies. 153 centers with
|D| >= 2, 1782 ordered pairs: 1608 killed by positivity, 152 by
coherence, and all 22 character-passers (11 unordered — first at
m = 425 with (54600, 97104); centers 425, 481, 725, 845, 850,
901, 925, 962, 1025) killed by representation. Zero remain. In
every one of the 22, the U+V diagonal center line's triple
(2m^2, 2m^2 +- (U+V)) is representable by NO class — the class
group bites strictly beyond genus, the first time the
representation level does work characters cannot.

SOUNDNESS CONTROLS (built into the check): the actual U- and
V-center lines — which exist as sphere points — always have
nonempty candidate sets (the machinery never kills a real line),
and their actual (content, reduced class) pairs are verified to
lie in their own lines' candidate sets.

The framing, honestly: not a new desert BOUND (A3's quadruple
search reaches much further); the first structural EXPLANATION of
the pair desert — three arithmetic obstructions, none needing any
square-testing search, jointly annihilate the range. Open: make
the representation sieve theoretical (spinor/composition — the P8
acquisitions), find where the three sieves first fail, and what
fourth sieve lives there.

Suite: 104 checks green (FULL). [M11-K: m=6 survey and m=8
tau-test re-armed after two container restarts; checkpoint-resume
added to the survey runner.]

## 2026-08-27 — Entry 26: A9-T1 fourth layer — the sieve pushed to theory: local certificates and the composition frontier

The user's directive: push the representation sieve toward theory.
Done, in three moves — with one soundness correction the process
itself forced.

THE CORRECTION (found by the anatomy's own assertion, fixed,
controlled): the content enumeration behind the representation
sieve looped over odd point contents — justified by the all-odd
lemma, which needs m ODD. For even centers every coordinate of
every point has 2-adic valuation exactly v_2(m) (three squares
summing to 0 mod 4 are all even: the sphere reduces to the odd
sphere), so the true content is 2^(v_2(m)) times odd. Fixed; all
22 kills STAND with identical signatures, and the even centers
now exactly reproduce their odd cores (850 = 2.425, 962 = 2.481,
pairs 4x the odd pairs) — the controls now run at even centers
too. Lesson banked: the machinery's own positive controls catch
this class of bug; extend them wherever the hypothesis quietly
narrows.

MOVE 1 — GAUSS COMPOSITION (compute/sphere_composition.py,
a9.composition): composition of primitive classes via united
representatives, with determinant +1 ENFORCED — the first draft
completed (x, y) to GL2 with det -1 half the time, silently
inverting classes, and the group axioms caught it (every f o f
came out trivial). Verified: identity/inverse/closure/orders —
Cl(-507) = Z/4, Cl(-3.65^2) = Z/12 x Z/2 (pinned order
multisets) — and GAUSS'S PRINCIPAL GENUS THEOREM (squares =
trivial-character genus) machine-checked. So "invisible to every
character" now rigorously means "inside a coset of Cl^2".

MOVE 2 — THE LOCAL CRITERION (a9.local_criterion): classical
local lattice theory, derived and validated: odd w > 0 is
represented by SOME primitive class of disc -3k^2 iff inert
primes divide it to even order; at p | k valuations below 2 v_p(k)
are even with pinned character (and the anisotropic p == 2 mod 3
keeps parity above); and the pinned signs extend to an OCCURRING
character vector — the occurring vectors form an index-2 subgroup
whose annihilator, derived from the data, is supported at 3
alone: every class value's 3-free part is == 1 mod 3 (the
norm-residue law of the Eisenstein family; my first guess at the
relation — product of all chi_p = +1 — was WRONG, exposed by 438
mismatches, and the derived relation then validated with ZERO
mismatches on 9000 values across three discriminants).

MOVE 3 — THE ANATOMY THEOREM (a9.kill_anatomy): all 57 killed
lines behind the m <= 1200 pair desert classified:
  21 L0 — provably LOCAL: a single co-norm value violates the
     validated criterion at every stratum (all 24 values
     certified);
   0 genus-mismatch;
  36 GLOBAL — provably BEYOND-LOCAL: every value locally fine, a
     single genus admits all three (same-genus witnesses pinned,
     e.g. a 45-class genus at m = 425 with representing sets of
     sizes 45/8/2 and empty triple intersection), no class
     represents the triple. These kills live inside cosets of
     Cl^2: no congruence or character argument can ever prove
     them.
THE SHARPEST INSTANCE: at m = 725 BOTH pairs die exclusively
through GLOBAL kills — that part of the pair desert exists ONLY
because of composition structure. The fourth sieve is the class
group proper, and the open question is now precise: what
invariant of (2m^2, 2m^2 +- X) separates the three representing
sets inside one genus? (Venkov / Aka-Einsiedler-Shapira
territory — the P8 acquisitions have a concrete target.)

Suite: 107 checks green (FULL). [M11-K: m=6 survey and m=8
tau-test still grinding in the background.]

## 2026-08-27 — Entry 27: M11-K decided — no second section: the web is spectrally rigid (Theorem A8.18)

The decisive background verdict landed: the m = 8 mod-p tau-test
(basis 15690 x 9729, four hours; then the reconstruction-free
node-extension rows) cut the 33-dimensional ambient invariant
eigenspace to RESOLUTION DIMENSION 1. Combined with the exact
lower bound — eta*^2, the convolution square of the certified
eta* numerators, verified exactly to have tau = 8 at all five
visible triple points and through sigma* at the three B-points —
the sandwich closes:

    h^0(Ytilde, S^8 Omega^1)^inv = <eta*^2>   EXACTLY.

With the full m = 5 survey (51 orbits, 256 characters, ALL ZERO —
each mod-p zero an exact-vanishing proof) and the m = 7 trivial
tau-test (ambient 10 -> resolution 0), the trivial-character
resolution ladder through degree 8 reads

    m:   4    5    6    7    8
    dim: 1    0   (0?)  0    1      (powers of eta*, nothing else)

— the m = 6 slot's tau-test is running (ambient 10; no
half-integral power of eta* can exist, 0 expected). THE
SECOND-SECTION HUNT IS SETTLED NEGATIVELY: no second invariant
section exists at any degree <= 8, so the cuboid-style two-section
resultant/finiteness shortcut is closed at these levels, and the
M11-J analysis of the single web eta* is genuinely unavoidable.
The 33-dimensional ambient octic space (which does contain >= 12
non-product-shaped mod-p vectors) is a statement about X minus its
nodes; at the resolution everything except <eta*^2> dies at the
256 exceptional curves.

Scope, honestly: nontrivial characters at m in {6, 7, 8} are
partial (m = 6 survey: 22/51 orbits so far, all zero except the
trivial ambient 10) resp. infeasible (m = 7: ~71 min/orbit =>
days). The trivial character — where products live and where any
finiteness shortcut would have to live — is settled decisively.
The m = 8 certified-basis job (CRT reconstruction) is retired:
the tau-test verdict is rigorous without it.

Artifacts: compute/data_section_spectrum.json (the m = 5 table,
the m = 7/8 verdicts with pinned system shapes); check
a8.section_spectrum re-certifies eta*^2 exactly on every run
(21 s) and validates the stored records. Doc: A8 §8 Theorem A8.18
+ roadmap and verify-summary updates; ledger row.

Suite: 108 checks green (FULL). [Still running: the m = 6
tau-test and the m = 6 survey tail; their results will be a small
addendum.]

## 2026-08-27 — Entry 27 addendum: the m = 6 slot closes — the ladder is complete

The m = 6 trivial-character tau-test landed 13 minutes after the
milestone commit (system 7138 x 4410, dN = 34, basis in ~13 min):
RESOLUTION DIMENSION 0, proven exactly (a zero mod p is a proof).
The trivial-character resolution ladder of Theorem A8.18 is now
complete with no gaps:

    m:   4    5    6    7    8
    dim: 1    0    0    0    1    — powers of eta*, nothing else.

Data file, check (a8.section_spectrum pins the m = 6 record), doc
and ledger updated. [Still running: the m = 6 survey tail for the
nontrivial characters — all zero so far.]

## 2026-08-28 — Entry 28: the PROGRESS memo — a standing honest self-assessment

At the owner's request after the step-back review: docs/PROGRESS.md
now carries the standing state-of-the-program assessment — the
one-sentence truth (the existence question untouched, the structural
map genuinely new), the two fronts with their theorem chains and
frontiers, the convergence finding (the obstruction is genuinely
global arithmetic: no congruence excludes the square, and the deep
sieve kills live beyond every character, inside cosets of Cl^2),
the honest calibrations (rational curves are not rational points;
range-verified is not all-m; novelty modulo reachable literature;
machine-verified, not peer-reviewed), and the three known-shaped
paths to an actual resolution. README front matter links it. To be
updated at milestones.

## 2026-08-28 — Entry 29: the m = 6 survey completes — h^0(Ytilde, S^6) = 0 outright

The 10.3-hour m = 6 character survey (checkpoint-resumed across
three container restarts) finished: all 51 orbits, 256 characters,
and the ONLY nonzero ambient eigenspace is the trivial character
(dimension 10) — whose resolution subspace the tau-test already
proved zero. Combined: h^0(Ytilde, S^6 Omega^1) = 0 for EVERY
character, and m = 6 joins m = 5 as a fully settled degree.
Theorem A8.18's scope note shrinks to the nontrivial characters at
m in {7, 8} only. Survey table stored in
data_section_spectrum.json; check, doc, ledger, and PROGRESS memo
updated.

## 2026-08-28 — Entry 30: the full-access literature sweep — backlog cleared, Hill v3 in hand, the frontier confirmed ours

The program ran for the first time on the owner's local machine with
unrestricted web access. One session cleared the entire WANTED backlog
(P2, P5, P7, P8 — 25 PDFs + 4 archived web pages, all verified
`%PDF`/HTML and logged in papers/README.md) and re-ran the
state-of-the-field checks that the cloud environment could only do
through search snippets. Everything below is dated 2026-08-28.

**Field status — the frontier is still ours.** (i) Rome–Yamagishi is
now formally published (Res. Number Theory 11:91, 2025): n×n magic
squares of squares exist for all n ≥ 4; **n = 3 remains the only open
order** — both the arXiv v2 and the published PDF are archived. (ii)
Várilly-Alvarado's CV (August 2026, fetched directly) lists **no new
work** on the magic-square surface — BTVA 2022 remains his latest word
on it; his 2026 preprints are elsewhere (del Pezzo irrationality, K3
Brauer moduli). (iii) Bruin's publication page likewise shows nothing
new on cuboids or magic squares beyond Bruin–Ilten–Xu (EPIGA 2025,
already ACQUIRED/READ). (iv) multimagie.com still lists the problem
open, prizes unclaimed; the search/bounds pages (Morgenstern ≥ 10^14
per entry, the 2008–2010 AP sweeps) are now archived in
papers/multimagie/, turning those CITED bounds into READ-able
artifacts. Conclusion: nobody has moved on either front since our
last sweep; the A8/A9 structural results still have no competition in
the literature.

**Hill arXiv:2510.08286 — the text finally in hand, and the crux
found (PRELIMINARY).** The claimed nonexistence proof is now at **v3**
(2026-04-07; still math.GM, still zero endorsement/refutation/
acceptance anywhere). Read in full (7 pages) against the A1 §5
checklist: **no descent, minimality, or height argument exists in the
paper** — checklist item 1 resolved negative, exactly as the audit
predicted from the abstract. The endgame is its eq. (29): a single
exact numerical relation among mutually dependent derived quantities,
to which the paper applies **coefficient comparison in α_{1d} as if it
were a polynomial identity in a free variable**, forcing β₁ = 1 and
the degeneracy contradiction. That step is invalid on its face (the
"coefficients" are functions of quantities algebraically dependent on
α_{1d}; the β's are not even rational in the data). A1 §6 (new
addendum) records the full analysis; formal verdict moved UNRESOLVED →
PRELIMINARY-invalid; the re-audit (symbolic re-derivation of (29) +
executable β₁ ≠ 1 counterexample via `a1.dictionary`, checklist items
2–5) is the scheduled follow-up. The program is unaffected either way.

**Acquisitions that sharpen the frontiers.** Front 1 endgame: found
and archived Bruin–Creutz, "Explicit Brauer–Manin obstructions on
plane quartics" (arXiv:2601.16975, 2026) — a worked modern template
for exactly the Picard/Galois → Brauer–Manin arithmetic-endgame step
the A7/A8 roadmap names, from one of the two BTVA-adjacent authors.
Front 2 composition question ("the law governing representing classes
inside a genus"): the P8 stack is now real — Ellenberg–Michel–
Venkatesh arXiv:1001.0897 (the modern Venkov/class-group
parametrization of S(n), the A9-T1 input), Duke 1988 + Duke's Linnik
survey, Aka–Einsiedler–Shapira arXiv:1502.04209, the Schulze-Pillot
representation survey, and three spinor-genus papers (arXiv:1711.05811,
2203.02620, 2104.08798) that carry the precise machinery for the
36 beyond-genus line kills. Context/adjacent 2026 papers archived:
quantum-period magic-square systems (arXiv:2605.04106 — checked: does
not touch n = 3 squares existence), Euler-brick elliptic obstructions
(arXiv:2604.09328), Hilbert cubes of dimension 3 in the squares
(arXiv:2604.05459). P5 context (Hirzebruch 1983 scan, Pokora,
line-arrangement surfaces) also in.

**Still wanted (only):** arXiv:math/0509484 (average representation
numbers for spinor genera — old-style-ID fetch failed); BTVA published
page numbers (nice-to-have). The PROGRESS memo's "citation databases
unreachable" calibration is now historical; the next milestone update
should soften it to "novelty verified against a 2026-08-28 full-access
sweep".

**Next steps queued by this entry:** (1) the A1 formal re-audit
(counterexample + checklist 2–5); (2) digest Bremner I/II → A4
cross-check; (3) digest Kominers → A3.K; (4) digest EMV + Schulze-
Pillot → pose the A9-T1 composition question precisely; (5) read
Bruin–Creutz alongside Stoll–Testa/Horie–Yamauchi as the endgame
template pair.

## 2026-08-28 — Entry 31: the A1 formal re-audit — Hill's claimed proof is refuted

With the v3 text in hand (entry 30), the §5 checklist and the §6
preliminary diagnosis were pushed to a complete formal re-audit, and
the outcome is stronger than the preliminary verdict: **the claimed
proof of arXiv:2510.08286v3 is refuted**, with the entire analysis
machine-verified (three new checks: `a1.eq29_identity`,
`a1.eq29_witness`, `a1.hill_grid`; suite now 111 checks). A1 §7 is the
write-up. The anatomy, in three verified layers:

**1. The encoding is the full problem (Theorem A1.2).** Hill's
constraint set — three equal-sum AP pairs plus his Lemma-3.2 spacing
relation — is exactly equivalent to nine squares in a 3×3 additive
grid M + iD + jF, i.e. to the Lucas structure. His reduction is
faithful and complete; consequently no integer hypothesis-level
counterexample can exist (it would BE a magic square of squares), and
the audit had to be inferential.

**2. His equation (29) is an identity in costume (Theorem A1.3).** As
polynomials in his own eight variables, LHS(29) − RHS(29) =
4N₂²N₃²β₁d⁴β₂d⁴α₁d² × (the Lemma-3.2 constraint, denominators
cleared) — verified by exact integer polynomial expansion, pure
stdlib. So (29) is *equivalent* to the constraint it was derived from:
the whole §2–3 apparatus is real-algebraic repackaging with no
Diophantine content (his integrality side conditions are never used).
The printed (30) and its factorization
(β₁d²−β₁n²)(β₁n²α₁n²−β₁d²α₁d²) are also verified correct — the error
is not an algebra slip.

**3. The final inference is a non-sequitur (the witness).** The step
"(29) has only even powers of α₁d on the left, so the odd coefficients
on the right vanish, so β₁ = 1" treats one numerical equation among
dependent quantities as a polynomial identity in a free variable. The
executable counterexample: the additive grid (M, D, F) = (4, 3360,
2112) — a genuine magic square, constant 16428, center 74², with SIX
perfect-square entries — whose first two AP pairs (2,58,82), (46,74,94)
are fully integral Hill pairs (congruum 3360, data (35/6, 1, 16) and
(42/5, 23, 4)) and whose third pair is forced real by the constraint
itself. Every quantity his step invokes is defined and positive
(verified exactly in ℚ(√105961)); (29) holds; both sides equal
≈ −298392.59 ≠ 0 (his argument forces 0); β₁ = 6/5 ≠ 1. The step, and
with it the proof, is invalid. Deepest diagnosis (checklist item 5):
the derivation never leaves the real-algebraic world, and over ℝ the
system is solvable (F5.2) — no such derivation can conclude.

Ledger updated (UNRESOLVED → proof REFUTED, PROVEN); references.md
row updated; to our knowledge this is the first refutation of the
paper anywhere (none public as of 2026-08-28). The open problem is,
as ever, untouched — and the A1.1 boundary theorem now has a worked
companion example of the adjacent fallacy class (polynomial-identity
misreading, sibling of the congruence endgame).

Incidental yield: the witness grid (4, 3360, 2112) is a pleasant
6-of-9-squares near-miss (magic sum 16428) found by pure structure —
two same-congruum triples with the spacing relation — not search; the
construction generalizes (any two triples T₁, T₂ of a common congruum
D with q₂² + p₂² − q₁² > 0 give one) and could feed F6/A4 as a
family of rank-style near-miss anchors if ever useful.

## 2026-08-28 — Entry 32: the refutation, audited — adversarial controls on our own reading of Hill

Prompted by the owner's (correct) insistence that refuting someone's
paper demands maximal certainty, the A1 §7 refutation was itself put
through an adversarial pass — could WE have misread the paper?

**Controls run** (A1 §7.5; `compute/hill_literal_controls.py`, a second
implementation built from the paper's literal definitions — raw
offsets, his sum formula (2), his case-(c) Lemma-3.2 construction,
(29)/(30) exactly as printed, with his (6),(7),(8),(11)–(14),(20),(21)
asserted at every configuration, 60-digit precision):
1. transcription of (29)/(30) re-verified against the page images, and
   cross-confirmed by the identity closing and (30) reproducing RHS(29)
   term-for-term (a mis-transcription could not do either);
2. the witness re-verified literally: both sides of (29) equal to 55
   decimal places; ΣpA = ΣpB = 1248 by his own case-(c) formulas; the
   "odd part" his step declares must vanish evaluates to −152180.22;
3. perturbation control: one grid value off by 1 ⟹ (29) FAILS — (29)
   is exactly the spacing constraint, nothing more;
4. 500 random real grids: (29) holds on every one, β₁ ∈ [1.0008,
   3.998], never 1 — the ℝ-family point made empirical;
5. representation control: α₃d = 1 in place of 5 changes nothing.

**Steelman documented** (§7.5): the only two readings of his final
step both fail — numeric (numbers have no coefficients; the odd part
is −152180.22 at a configuration satisfying (29)) and polynomial
(LHS − RHS is provably NOT the zero polynomial, so the identity
premise is false); and the "pair 3 is irrational so the witness is
outside his framework" objection is closed three ways, decisively by
circularity: restricting the step to all-rational configurations makes
its soundness equivalent to the theorem it is meant to prove. The
refutation stands at the highest standard we can impose on it.

## 2026-08-28 — Entry 33: the standalone refutation document

The A1 §7 refutation now has a self-contained, shareable write-up:
docs/refutations/2510.08286-hill.md — written to be handed directly to
the paper's author or any third party, with no dependence on the
repository's internal language. Contents: the paper's framework
recalled in its own notation; what is CORRECT in the paper stated
fairly (the encoding is faithful and complete; the algebra through
(30) checks out); Theorem 1 (eq. (29) = positive cofactor x the
Lemma-3.2 constraint, with a term-by-term proof checkable by hand);
Theorem 2 (the six-square witness, all data exact, every positivity
verified); the final step quoted verbatim and analyzed under both
possible readings (numeric: numbers have no coefficients; polynomial:
the premise is a provably nonzero polynomial); the no-local-repair
argument (positivity-only justification, R+ betas per the paper
itself, circularity of a rationality restriction); scope (the problem
remains open); and an embedded ~40-line sympy script verifying both
theorems (also stored as compute/hill_refutation_standalone.py and run
green from the repo). Cross-linked from A1 §7, the README headline and
ledger row.

Contact route for the author identified: the arXiv abstract page for
2510.08286 carries the standard "From: Oscar Hill [view email]"
submitter link (arxiv.org/show-email/8a625028/2510.08286), visible to
logged-in arXiv users — the author-consented channel, and the only
one that identifies the actual submitter with certainty (a same-named
Cambridge CS PhD student found in open search does NOT list the paper
on his profiles, so no identification was assumed). The owner will
make contact personally.

## 2026-08-28 — Entry 34: the strategic roadmap — nine workstreams toward a proof

With both fronts at named frontiers, the sweep digested, and the
field's only claimed proof refuted, the program now has a standing
battle plan: docs/ROADMAP.md. The doctrine: both directions count;
every argument passes the gauntlet (we now know FOUR ways proofs of
this problem die); force concentrates where the convergence finding
points — exact global-arithmetic laws.

The nine workstreams, with their first actions:
W1 close M11-J -> prove A2.C -> the unconditional k[t] theorem (the
   ripest fruit; paper #1);
W2 the motive atlas of X — extend the A8 character machinery from
   differentials to H^{2,0} (111 forms, 256 characters), classify
   the sub-arrangement double covers, then the Stoll-Testa/
   Horie-Yamauchi program: Pic with Galois action, Brauer, L-function;
W3 the endgame stated honestly as Conjecture E (all rational points
   degenerate) attacked by descent on (Z/2)^8-twists with Brauer
   obstructions — F4 reinterpreted as the local half of that descent;
W4 THE FLAGSHIP BET (H-Redei): the 36 beyond-genus kills as exact
   Redei-symbol identities — reciprocity, not equidistribution; first
   action: full Redei computation at m = 725; ties the sphere front
   to 2-Selmer structure of coupled congruent-number twists;
W5 the abc bridge: autopsy exactly where the A2.L degree-halving
   descent breaks over Z; formulate inequality (*); aim at the
   conditional capstone (effective abc => explicit bound + finite
   check = complete conditional resolution);
W6 the telescope: extend the pair desert past 1200 until golden
   centers appear, search only there; plus the actuarial model that
   decides W4-vs-W6 resource allocation;
W7 exact Hurwitz-class-number counting identities (Sturm-style
   finish if a signed count is modular; obstacle named honestly);
W8 force multiplication: papers 1-2 to arXiv, then engage
   Varilly-Alvarado/Bruin/Stoll — W2/W3 are literally their
   specialties; timing: after W1 lands as the calling card;
W9 wild reserve, timeboxed: Buium arithmetic jets avatar of
   eta_star, quaternionic norm-identity reformulation, governing
   fields for the kill family.

Milestones M12-A..M15 defined with acceptance criteria (suite-
verified, tagged, logged). Near-term order: M12-A (H^{2,0} atlas,
cheap and unlocking), M12-B (m=725 Redei session), M12-C (cubic
cloud campaign), M12-D (desert extension in background), M12-E
(A2.L autopsy). The honest odds are stated in the roadmap's §5: the
boulder is real, but the plan concentrates on the only three
mechanisms matching the obstruction's proven profile — class-field
reciprocity, cover descent with Brauer classes, and height descent —
and every rung of the ladder is real mathematics on its own.
