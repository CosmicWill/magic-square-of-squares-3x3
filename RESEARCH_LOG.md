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
