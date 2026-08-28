# A1 — Audit of the claimed proof arXiv:2510.08286 (Hill, Oct 2025)

**Status:** paper text **ACQUIRED 2026-08-28** (v3, Apr 2026 —
`papers/2510.08286v3-hill.pdf`; the audit below through §5 predates the
text and stands unchanged); machinery reconstruction **PROVEN** equivalent
to the F2 layer; boundary meta-theorem A1.1 **PROVEN** with executable
witnesses; verdict on the paper: **PRELIMINARY — invalid as written**, crux
located at its eq. (29) coefficient-comparison step (§6); formal re-audit
with executable counterexample pending.
Verification: `python3 -m verify --only a1`.

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
(RESEARCH_LOG entry 29) and read in full. Version history: v1
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

**What remains for the formal re-audit (scheduled):**
1. re-derive its eq. (29) symbolically from the dictionary (its
   (7)–(8), (13)–(14), (21)–(28) + Lemma 3.2) and confirm the derivation
   is otherwise sound;
2. produce an **executable counterexample**: a near-miss configuration
   (e.g. a row-system of Euler's 4×4 via `a1.dictionary`, or an A1.1
   pseudo-solution) satisfying every hypothesis actually used up to
   eq. (29) with $\beta_1 \neq 1$ — exhibiting that (29) does not force
   $\beta_{1d}^2 = \beta_{1n}^2$;
3. checklist items 2–5 (sign cases in its (16) ordering trichotomy;
   Lemma 3.2's case split; the 4×4-row test; the $\mathbb{F}_p$ test —
   note the proof as written never uses positivity beyond ordering, so
   F5.3 already implies *some* step must fail over $\mathbb{F}_p$).

Until the re-audit lands, the formal repo verdict moves from UNRESOLVED
to **PRELIMINARY: invalid as written (crux located)** — and the program
continues unchanged.
