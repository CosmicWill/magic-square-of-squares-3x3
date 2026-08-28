# A1 — Audit of the claimed proof arXiv:2510.08286 (Hill, Oct 2025)

**Status:** paper text **ACQUIRED 2026-08-28** (v3, Apr 2026 —
`papers/2510.08286v3-hill.pdf`; the audit below through §5 predates the
text and stands unchanged); machinery reconstruction **PROVEN** equivalent
to the F2 layer; boundary meta-theorem A1.1 **PROVEN** with executable
witnesses. **Formal re-audit complete (§7): the paper's proof is REFUTED**
— its eq. (29) is PROVEN to be an identity-multiple of its own Lemma-3.2
constraint (no Diophantine content), and the final inference
"(29) ⟹ β₁ = 1" is PROVEN invalid by an explicit witness (a genuine magic
square with six perfect-square entries) satisfying every hypothesis and
positivity requirement of the step with β₁ = 6/5 and both sides of (29)
nonzero. The open problem itself is untouched.
Verification: `python3 -m verify --only a1` (5 checks; the re-audit adds
`a1.eq29_identity`, `a1.eq29_witness`, `a1.hill_grid`).

## 1. The object under audit

O. Hill, *"On Arithmetic Progressions and a Proof of the Nonexistence of
Magic Squares of Squares"*, arXiv:2510.08286 (v1 Oct 2025 titled *"An
Algebraic Proof of…"*; v2 retitled). Classified `math.GM` (arXiv's
moderation holding category); as of 2026-08-25 we found **no published
refutation, no endorsement, no journal acceptance**, and the community
status pages still list the problem as open and prizes unclaimed. Abstract:

> "We explore some of the properties of consecutive arithmetic progressions
> of odd numbers with equal sums, particularly their offsets and said sums,
> before using them to prove that no 3×3 magic squares of distinct square
> integers exist."

**Fetch log (2026-08-25):** `curl` to `arxiv.org/abs`, `export.arxiv.org`
(HTML + API), plus proxied fetches of `arxiv.org/html/2510.08286v2`,
Semantic Scholar API, and a mirror — all blocked by this environment's
egress proxy (000/403/EGRESS_BLOCKED). Everything below is therefore an
audit of the **reconstructed method space**, not of the paper's literal
text. If the text becomes available, re-run this audit against §5's
checklist.

## 2. Reconstruction of the machinery (PROVEN dictionary)

The classical encoding: the odd numbers from $2p+1$ to $2q-1$ (an
"arithmetic progression of odd numbers", $q - p$ terms, mean $p+q$) sum to
$$\sum_{j=p+1}^{q} (2j-1) \;=\; q^2 - p^2 .$$
Hence:

- an entry $x^2$ *is* the initial segment $[1, 2x-1]$;
- a **pair of consecutive APs of odd numbers with equal sums** —
  $[2p{+}1,\, 2q{-}1]$ followed by $[2q{+}1,\, 2r{-}1]$ with
  $q^2 - p^2 = r^2 - q^2$ — *is* a three-term AP of squares
  $(p^2, q^2, r^2)$, i.e. exactly an object of
  [F2.2](../foundations/F2-aps-and-pythagorean.md);
- its "sum" is the common difference $\delta = q^2 - p^2 = (q-p)(q+p)$:
  (number of terms) × (mean) — the exact identities
  $\delta = L_1(p+q) = L_2(q+r)$ with lengths $L_1 = q-p$, $L_2 = r-q$;
- its "offsets" are (linear functions of) the interval endpoints, i.e. of
  the **roots** $p, q, r$.

By [F1/F2]: an MSS3 is precisely four such equal-sum consecutive pairs
pivoting at one square $m^2$, with sums $d_1, d_2, d_1{+}d_2, d_1{-}d_2$.
So the paper's language is a faithful re-encoding of the standard
reduction; nothing is lost or gained. Its stated base (entries $\equiv 1
\bmod 24$, Pierrat–Thiriet–Zimmermann) is our
[F4.1](../foundations/F4-congruences-mod-72.md), sound. The check
`a1.dictionary` verifies the encoding mechanically, and verifies that
Euler's 4×4 satisfies every *line-level* interval identity — so any lemma
of the form "such-and-such equal-sum interval systems are impossible"
that does not engage the specifically 3×3 eight-line structure is false
outright.

## 3. Theorem A1.1 — the boundary: what interval identities + congruences + order can never prove

**Theorem A1.1.** For every modulus $N$ there exist tuples of positive
integers $(m;\, p_1, q_1, \dots, p_4, q_4)$, pairwise distinct and in any
prescribed order pattern, all $\equiv 1 \pmod{24}$-compatible (roots
coprime to 6), such that **all** defining relations of an MSS3 hold
modulo $N$ — the four AP relations $p_i^2 + q_i^2 \equiv 2m^2$, the
additive sum relations $\delta_3 \equiv \delta_1 + \delta_2$,
$\delta_4 \equiv \delta_1 - \delta_2 \pmod N$ — and all real/order
constraints hold exactly, yet the tuple is **not** an MSS3 (the exact
integer relations fail).

*Proof.* Choose all roots $\equiv 1 \pmod{\mathrm{lcm}(N,24)}$: every
quadratic relation becomes $1 + 1 \equiv 2$, $0 \equiv 0 + 0$ mod $N$
— satisfied. The roots themselves may be chosen as **any** distinct
positive integers in that residue class, in any order pattern; a generic
choice violates the exact relations (an exact solution would *be* an
MSS3, and in fact any single exact relation $p^2 + q^2 = 2m^2$ can be
dodged by choosing $q$ last within its class). ∎

(The same holds with $\mathbb{Z}/N$ replaced by any finite set of
completions: the exact system has solutions over every $\mathbb{Z}_p$ and
over $\mathbb{R}$ with distinct ordered entries —
[F5.2](../foundations/F5-local-solubility.md).)

**Consequence (the audit's teeth).** Any nonexistence argument whose
skeleton is:

> *exact algebraic identities among interval sums/offsets (all polynomial
> relations in the roots), followed by an endgame contradiction that is a
> congruence, parity, or counting statement modulo some fixed $N$, plus
> ordering/positivity facts*

is **invalid**, no matter how intricate the middle: the full hypothesis
set it uses is satisfied by the A1.1 pseudo-solutions (implemented
explicitly in `a1.pseudo_solutions`, including with $N = 2^{20}$, $72$,
and $\mathrm{lcm}$s), which are not magic squares of squares. A valid
proof must at some point use the **exact** integer quadratic relations in
an essentially global way — in practice: infinite descent / minimality
(as in [F3](../foundations/F3-no-four-term-ap.md), which combines exact
identities, parity, *and* a strictly decreasing positive quantity), or a
size-vs-multiplicative-structure argument (e.g. trapping an entry
strictly between consecutive squares), or genuine factorization input
($\mathbb{Z}[i]$-level, as in F2/F4.2).

## 4. Verdict

1. The paper's advertised ingredients — "properties of consecutive APs of
   odd numbers with equal sums, particularly their offsets and said sums",
   over the PTZ congruence base — live, as far as the abstract and
   section descriptions reveal, entirely inside the language covered by
   Theorem A1.1. **No mention of descent, minimality, or height appears
   in any accessible description.**
2. Therefore: *either* the paper contains a descent/size mechanism not
   hinted at in its abstract, *or* it is invalid by A1.1 — with the error
   necessarily located at the step where a congruence/counting conclusion
   is drawn from relations that only hold exactly (a step which A1.1
   guarantees cannot be watertight, commonly manifesting as a dropped
   sign case, e.g. $d_4 = d_1 - d_2$ needing $|{\cdot}|$, or an
   unjustified divisibility).
3. **Formal verdict: UNRESOLVED** as to the specific error (text
   unavailable); **PROVEN** that the method space it describes cannot
   contain a correct proof. This repository's program continues unchanged.
   (For calibration: the identically-classified claim arXiv:1506.06621
   (2015) has sat unaccepted for a decade; the problem's status pages
   list both, and the prizes, as they were.)

## 5. Checklist if/when the text becomes available

- [ ] Does any lemma use minimality/descent or an unbounded strictly
      decreasing quantity? If none: A1.1 applies — locate the endgame
      congruence and extract the pseudo-solution that breaks it.
- [ ] Is the $\varepsilon = \pm 1$ / $|d_1 - d_2|$ sign case split
      handled everywhere?
- [ ] Do the interval manipulations implicitly assume the four APs'
      intervals are disjoint/nested in a fixed pattern? (The $D_4$ orbit
      allows several order patterns of $p_i, q_i$ around $m$.)
- [ ] Is anything claimed for 3×3 that would equally apply to a single
      row/column system of a 4×4? Test against Euler's square via
      `a1.dictionary`.
- [ ] Would the argument survive over $\mathbb{F}_p$, $p \ge 107$
      ([F5.3](../foundations/F5-local-solubility.md))? It must fail
      there — identify the step that does.

## 6. Addendum 2026-08-28 — the text in hand: first pass against the checklist (PRELIMINARY)

The v3 text (7 pages) was acquired in the full-access sweep
(RESEARCH_LOG entry 30) and read in full. Version history: v1
2025-10-09, v2 2025-10-19, v3 2026-04-07 ("updated notation,
particularly around singular APs"); still math.GM; still no endorsement,
refutation, or acceptance anywhere we could find.

**Checklist item 1 — descent/minimality: CONFIRMED ABSENT.** The proof
of its Theorem 3.1 is: encode the 8 line relations as equal-sum AP data
(its §2–3 — a faithful match to our §2 dictionary, including the
$\kappa, \alpha$ reparametrization of a 3-term AP of squares); derive a
single algebraic relation, its eq. (29), among the derived quantities
$N_2, N_3, \alpha_{1d}, \beta_{1n}, \beta_{1d}, \beta_{2n}, \beta_{2d}$;
then conclude. No infinite descent, no minimal counterexample, no
height/size argument, no factorization input appears anywhere.

**The crux (where it collapses).** From eq. (29) the paper argues: the
LHS contains only even powers of $\alpha_{1d}$, "and as such, the
coefficients of odd powers of $\alpha_{1d}$ are 0, which must also hold
in the RHS" — forcing the RHS prefactor
$\beta_{1d}^2 - \beta_{1n}^2 = 0$, i.e. $\beta_1 = 1$, hence
$\mathcal{P}_1 = \mathcal{P}_2 = \mathcal{P}_3$, contradiction. This is
**coefficient comparison applied to a single numerical equation, not a
polynomial identity in a free variable**: for any actual (hypothetical)
magic square, $\alpha_{1d}$ is one fixed integer, and the "coefficients"
are themselves functions of quantities ($N_1$ via its eqs. (11)–(12),
the $\beta$'s via (21)–(26)) that are *algebraically dependent on*
$\alpha_{1d}$ and on each other. Nothing makes eq. (29) hold for a range
of $\alpha_{1d}$ values with everything else fixed, which is what
equating coefficients requires. (Note also its $\beta_{1n}, \beta_{1d}$
are defined by square roots — eqs. (23)–(26) — so they are not even
rational functions of the integer data; the "polynomial in
$\alpha_{1d}$" framing is doubly unfounded.)

This is the precise realization of §4.2's prediction: an endgame that
draws a structural conclusion (here "odd coefficients vanish") from
relations that only hold as one exact numerical instance. It is a
sibling of the congruence-endgame fallacy bounded by Theorem A1.1 —
not literally within A1.1's stated hypothesis class (the endgame is a
polynomial-identity claim, not a congruence), so A1.1 is not itself the
refutation; the refutation is the direct invalidity of the
coefficient-comparison step.

*(The re-audit items listed here in the preliminary pass are now
executed — see §7, which confirms every prediction of this section and
sharpens them to PROVEN statements.)*

## 7. The formal re-audit (2026-08-28) — the proof is refuted

> *A self-contained, shareable write-up of this refutation — suitable
> for sending to the author or a third party, with a standalone
> verification script — is at
> [docs/refutations/2510.08286-hill.md](../refutations/2510.08286-hill.md).*

All statements in this section are machine-verified by
`a1.eq29_identity`, `a1.eq29_witness`, and `a1.hill_grid` (exact
arithmetic throughout: integer multivariate polynomial expansion,
$\mathbb{Q}$, and $\mathbb{Q}(\sqrt{105961})$). Variable dictionary:
$n = \alpha_{1n}$, $d = \alpha_{1d}$, $N_2, N_3$ = Hill's per-pair $N$;
$b_{1n} = \beta_{1n}^2 = \alpha_{2n}/\alpha_{1n}$,
$b_{1d} = \beta_{1d}^2$, $b_{2n} = \beta_{2n}^2$,
$b_{2d} = \beta_{2d}^2$ (every $\beta$ enters (29) squared).

### 7.1 The encoding is the full problem (Theorem A1.2)

**Theorem A1.2** (`a1.hill_grid`). Hill's constraint set — three AP
pairs $\mathcal{P}_1, \mathcal{P}_2, \mathcal{P}_3$ with equal sums
$D_1$ plus the Lemma-3.2 spacing constraint $\Sigma p_A = \Sigma p_B$ —
is *equivalent* to: the nine values form a 3×3 additive grid
$M + iD + jF$ $(i, j \in \{0,1,2\})$, which is exactly the Lucas magic
structure (the grid arranges into a magic square via a pair of
orthogonal Latin squares, every line summing to $3(M+D+F)$).

*Consequences.* (i) The reduction in his §3 is faithful **and
complete** — this upgrades §2's line-level dictionary to the full
system. (ii) **No integer hypothesis-level counterexample to his
Theorem 3.1 can exist**: nine distinct integer squares satisfying his
constraint set would *be* a magic square of squares. The only possible
flaw in the paper was therefore inferential — and §7.3 locates it.
(iii) Over $\mathbb{R}$ his constraint set has solutions in abundance
(any grid of nine distinct positive reals; cf. F5.2), so no chain of
real-algebraic reasoning can conclude nonexistence. That is precisely
the boundary his proof crashes into:

### 7.2 Equation (29) is an identity in costume (Theorem A1.3)

**Theorem A1.3** (`a1.eq29_identity`; exact polynomial identity in
$\mathbb{Z}[n, d, N_2, N_3, b_{1n}, b_{1d}, b_{2n}, b_{2d}]$).
$$\mathrm{LHS}(29) - \mathrm{RHS}(29) \;=\; 4\,N_2^2 N_3^2\, b_{1d}^2
b_{2d}^2\, d^2 \;\cdot\; \frac{4E}{t^2},$$
where $E := (p_2^2 - q_1^2) - (p_3^2 - q_2^2)$ is the Lemma-3.2
spacing constraint (written via his own formulas (7)–(8), (11)–(14),
(21)–(28), denominators cleared) and $t = \mathcal{P}_3^{n_2}$ the free
scale. The cofactor is strictly positive on every configuration, so:

**Corollary.** *Equation (29) is equivalent to the single constraint
$E = 0$.* His entire §2–3 apparatus — the $\kappa, \alpha, N$
reparametrization, the $\beta$-splits, Lemma 3.2 (whose case
trichotomy is handled correctly, checklist items 2–3) — is a chain of
real-algebraic identities that repackages one equation of the system as
(29). **It contains no Diophantine content whatsoever**: nothing in the
derivation distinguishes integer configurations from real ones. (The
printed (30) is also verified correct — the RHS factors as
$4N_2^2N_3^2\beta_{2n}^2\beta_{2d}^2(\beta_{1d}^2 - \beta_{1n}^2)
(\beta_{1n}^2\alpha_{1n}^2 - \beta_{1d}^2\alpha_{1d}^2)$, and his
bracket is the second factor expanded via (12). The error is *not* an
algebra slip.)

### 7.3 The witness: the final inference is a non-sequitur

The proof's only remaining step is: *"(29) holds; the LHS contains only
even powers of $\alpha_{1d}$; therefore the odd-power coefficients of
the RHS vanish; since [positivity], $\beta_{1d}^2 - \beta_{1n}^2 = 0$"*
— forcing $\beta_1 = 1$ and the degeneracy contradiction. The step
treats a single numerical equation among mutually dependent quantities
as a polynomial identity in a free variable $\alpha_{1d}$. It is
refuted by an explicit witness (`a1.eq29_witness`):

**The witness.** The 3×3 additive grid $(M, D, F) = (4, 3360, 2112)$ —
a genuine magic square (magic constant 16428, center $5476 = 74^2$)
whose nine entries contain **six** perfect squares:
$$\begin{pmatrix} 94^2 & 2^2 & 7588 \\ 4228 & 74^2 & 82^2 \\
58^2 & 10948 & 46^2 \end{pmatrix}$$
Its three AP pairs are $\mathcal{P}_1 = (2, 58, 82)$ and
$\mathcal{P}_2 = (46, 74, 94)$ — **fully integral Hill pairs** with
common congruum $D_1 = 3360$, exact data $(\alpha_1, s_1, N_1) =
(35/6,\, 1,\, 16)$ and $(\alpha_2, s_2, N_2) = (42/5,\, 23,\, 4)$,
coprime representations, all of (11)–(14) satisfied in $\mathbb{Z}$ —
and the third pair $(\sqrt{4228}, \sqrt{7588}, \sqrt{10948})$, *forced
by the spacing constraint itself*, real (the three values are positive)
and genuinely non-integral (none is a perfect square — as §7.1(ii)
guarantees must happen for some pair). Its interleaving is Hill's own
case (c).
Exact facts (in $\mathbb{Q}(g)$, $g = \sqrt{105961}$, $t^2 = 18536 -
56g$, $\alpha_3 = (2317+7g)/420$):

- every quantity his step needs is defined and **positive** — including
  $N_3 > 0$, $s_3^2 = 1057(331+g)/504 > 0$ — i.e. the step's entire
  stated justification ("Obviously $N_1, N_2, N_3, \beta_{1n},
  \beta_{1d}, \beta_{2n}, \beta_{2d} > 0$") is satisfied;
- equation (29) **holds exactly** (Theorem A1.3 + $E = 0$, an integer
  identity: $46^2 - 58^2 = 4228 - 74^2 = -1248$);
- both sides of (29) equal $4N_2^2N_3^2\beta_{2n}^2\beta_{2d}^2 \cdot
  (\beta_{1d}^2 - \beta_{1n}^2)(\beta_{1n}^2\alpha_{1n}^2 -
  \beta_{1d}^2\alpha_{1d}^2)$ with every factor **nonzero**
  ($\approx -298392.59$; his argument would force both sides to be 0);
- and $\beta_1^2 = 36/25 \neq 1$, prefactor $\beta_{1d}^2 -
  \beta_{1n}^2 = -11/30 \neq 0$.

So a configuration satisfying **every hypothesis and every positivity
condition the final step invokes** — with the first two pairs not
merely real but integral — fails its conclusion. The inference is
invalid, and with it the proof of his Theorem 3.1.

### 7.4 Verdict and checklist resolution

**The claimed proof in arXiv:2510.08286v3 is invalid (PROVEN).** The
precise error: the passage from eq. (29) to "$\beta_{1d}^2 -
\beta_{1n}^2 = 0$" applies polynomial coefficient comparison in
$\alpha_{1d}$ to an equation that is not a polynomial identity — by
Theorem A1.3 it is the Lemma-3.2 constraint itself, satisfied over
$\mathbb{R}$ by the full 3-parameter grid family $(M, D, F)$ of
Theorem A1.2, on which $\alpha_{1d}$ is not free and $\beta_1 \neq 1$
generically. No repair short of a genuinely new
Diophantine argument is possible: by §7.1(iii) the derivation is valid
over $\mathbb{R}$, where his constraint set is abundantly solvable, so
*any* completion of the proof must inject integrality somewhere — and
the paper never does (its integrality conditions — coprime
$\alpha_n/\alpha_d$, perfect-square discriminant — are never used by
the derivation, as Theorem A1.3 shows). The open problem is untouched;
the $100 prizes are safe.

§5 checklist, resolved against the text: **(1)** no
descent/minimality/height anywhere — confirmed; the endgame is not a
congruence (so A1.1 is not itself the refutation) but its sibling
fallacy, and the located error is exactly of the predicted character
(§4.2: a structural conclusion drawn from relations that hold only as
one exact instance). **(2–3)** the sign/case handling (his (16)
trichotomy, Lemma 3.2 cases (a)/(b)/(c)) is *correct* — verified, the
flaw is not there. **(4)** the 4×4 test does not bite: his (29) is
genuinely 3×3-specific (Theorem A1.2). **(5)** the $\mathbb{R}$/
$\mathbb{F}_p$ boundary is the deepest diagnosis: the derivation never
leaves the real-algebraic world (§7.2), and over $\mathbb{R}$ the
system is solvable (F5.2) — the witness is precisely such a real
solution pushed through his own formalism with maximal integrality.

### 7.5 Steelman — every alternative reading, closed (adversarial controls)

Because refuting someone's work demands more than one reading, the
re-audit was itself audited: the critical pages (his (21)–(28), Lemma
3.2, (29), (30), and the final paragraph) were re-read against the PDF
page images, and every check above was re-run through a **second,
independent implementation that follows the paper's definitions
literally** — raw offsets, his AP-sum formula (2), his case-(c)
$\Sigma p_A = \Sigma p_B$ construction, and (29)/(30) exactly as
printed, with his cited input equations (6), (7), (8), (11)–(14),
(20), (21) asserted numerically at every configuration
([`compute/hill_literal_controls.py`](../../compute/hill_literal_controls.py),
60-digit precision). Results: at the witness, LHS(29) = RHS(29) =
$-298392.5892\ldots$ to 55 decimal places; $\Sigma p_A = \Sigma p_B
= 1248$ via his own case-(c) formulas; **the "odd part" of (30) that
his step declares must be zero evaluates to $-152180.22\ldots$**;
perturbing one grid value by 1 makes (29) *fail* (so (29) is exactly
the constraint, no more); (29) held on all 500 random real grids
sampled, with $\beta_1$ ranging over $[1.0008, 3.998]$ and never 1;
and the representation choice $\alpha_{3d} = 1$ instead of $5$ changes
nothing. Against that background, the possible objections:

- **"You mis-transcribed (29) or (30)."** Ruled out three ways: visual
  re-read of the page images; the exact polynomial identity closing
  (a mis-transcription would not reduce to cofactor × constraint); and
  his printed (30) reproducing our RHS(29) term-for-term at the
  witness.
- **"His step is not coefficient comparison — you misread the
  argument."** His words, in full: *"Clearly, this is a quadratic in
  $\alpha_{1d}^2$ and, as such, the coefficients of odd powers of
  $\alpha_{1d}$ are 0, which must also hold in the RHS. Obviously,
  $N_1, N_2, N_3, \beta_{1n}, \beta_{1d}, \beta_{2n}, \beta_{2d} > 0$,
  as per the definitions in equations (11), (21) and (22), so
  $\beta_{1d}^2 - \beta_{1n}^2 = 0$."* There are exactly two readings.
  *Numeric reading*: (29) is one equation between two numbers; numbers
  do not have coefficients; the "odd part" is $-152180.22$ at the
  witness. *Polynomial reading* (all quantities free variables): then
  the premise is false — LHS $-$ RHS is **not** the zero polynomial
  (Theorem A1.3: it is cofactor × constraint), so (29) is not a
  polynomial identity and comparison is unavailable. Both readings
  fail; there is no third: any hypothetical variation of
  $\alpha_{1d}$ drags $N_1$ (present in his RHS coefficients, defined
  from $\alpha_{1d}$ by his (11)–(12)) and the $\beta$'s along with
  it, so "coefficients" are not even well-defined constants.
- **"The witness is outside his framework: pair 3 has irrational
  $\alpha_3$ / $\beta_2$, so (21)'s $\beta_2 \in \mathbb{Q}^+$ and
  §2.3's perfect-square discriminant fail."** Three answers. (i) The
  step under refutation justifies itself by *positivity alone* (quoted
  above) — every positivity it invokes holds at the witness, and
  $\alpha_{1d} = 6$, the variable he compares coefficients in, is a
  genuine integer from a fully integral pair; rationality of pair 3
  plays no role in the inference as written. (ii) He himself places
  $\beta_{1n}, \beta_{1d}, \beta_{2n}, \beta_{2d} \in \mathbb{R}^+$
  (p. 5), and they enter (29) only squared. (iii) Decisive: restricting
  the step's validity to all-rational configurations cannot save it,
  because by Theorem A1.2 the all-rational domain being empty *is* the
  theorem being proved — a step that is sound only if the conclusion
  is true is circular, not a proof. Any repair must supply a new
  Diophantine argument the paper does not contain.
- **"Perhaps (29) encodes more than the spacing constraint and the
  witness misses a hypothesis."** Empirically closed: every equation
  he cites as an input to (29) — (7), (8), (13)/(14), (21)–(28),
  Lemma 3.2 — is asserted numerically at the witness by the literal
  implementation, and the perturbation control shows (29) tracks the
  spacing constraint exactly (fails the moment it is broken).
