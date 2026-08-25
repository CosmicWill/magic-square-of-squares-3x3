# Protocol — the falsification gauntlet

Any argument that purports to obstruct magic squares of squares must be
consistent with the near-solutions that **exist**. The gauntlet makes this
executable: every candidate obstruction developed in `docs/attacks/` is
encoded as a predicate in `verify/` (interface in `verify/gauntlet.py`) and
run against the anchor targets by `verify/checks/sanity_gauntlet.py`. **No
claim in an attack document may be tagged PROVEN unless its gauntlet entry
is green or its scope is explicitly encoded in the predicate.**

## The anchor targets (all VERIFIED in [F6](../foundations/F6-known-squares.md) / [F5](../foundations/F5-local-solubility.md))

1. **AB1** — the Bremner–Sallows square: fully magic, **seven** of nine
   entries square. Any argument claiming to rule out "a magic square with
   ≥ 7 square entries" (or any subsystem AB1 satisfies) is wrong.
2. **EULER4** — Euler's 4×4 magic square of 16 distinct squares; and
   (CITED, Rome–Yamagishi) $n\times n$ examples exist for every
   $n \ge 4$. Any argument **insensitive to the order $n = 3$** is wrong.
3. **𝔽_p witnesses** — magic squares of nine distinct nonzero squares over
   $\mathbb{F}_p$ (stored/recomputed for a range of $p$). Any argument that
   works "prime by prime" and would apply to $\mathbb{F}_p$ is wrong.
4. **mod-$2^N$ witness** — a full magic square of squares modulo $2^{32}$
   (our own lift, F5). Any 2-adic congruence argument is wrong.
5. **ℚ(i,√n) center-zero solutions** — (CITED, Kominers) magic squares of
   distinct squares exist over degree-4 number fields. Any argument that
   is insensitive to the base field ℚ is wrong.

## The checklist for any candidate impossibility argument

- [ ] Which 3×3-specific structure does it use? (else target 2 kills it)
- [ ] Which global/Archimedean input does it use — size, positivity,
      distinctness, descent? (else targets 3–4 kill it: the congruence
      system is solvable mod every $n$ and over every $\mathbb{Z}_p$,
      [F5](../foundations/F5-local-solubility.md))
- [ ] Which property of ℚ does it use — unit group, class-field-ish
      splitting, real place? (else target 5 kills it)
- [ ] Does it *not* also "prove" that seven square entries are impossible?
      (else target 1 kills it)
- [ ] Encode it as a `Predicate` and run `python3 -m verify --only gauntlet`.

## Negative control

The gauntlet harness itself is tested with a deliberately wrong predicate
(one that "rules out" seven-square magic squares); the check asserts the
harness **catches** it against AB1. A gauntlet that cannot fail is not a
gauntlet.
