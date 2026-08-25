# Protocol — status taxonomy

Every mathematical claim in this repository carries **exactly one** of the
following tags. The tag is part of the claim; changing it is a logged event
(RESEARCH_LOG.md).

| Tag | Meaning | Obligations |
|---|---|---|
| **PROVEN** | Complete proof in this repository, written by/for this project. | Proof in the doc; every computationally checkable step covered by a named check in `verify/checks/`. |
| **PROVEN-CLASSICAL** | Complete proof included, but the result is classical (we claim correctness, not novelty). | Same obligations as PROVEN. |
| **CITED** | Taken from the literature. | Listed in `docs/references.md` with a provenance flag (READ / SUMMARY-ONLY / EXISTENCE-VERIFIED). **Never load-bearing** for a headline PROVEN claim: anything we build proofs on is reproved. |
| **VERIFIED($B$)** | Established by finite computation up to the explicit bound $B$. | Reproducible via a named check; both FULL and FAST bounds printed by the check so documents can cite the FULL bound. |
| **CONJECTURED** | Believed, with stated evidence. | Evidence pointer (data file, heuristic, or literature). |
| **FAILED-ATTEMPT** | An approach that was tried and did not work. | An autopsy: what was attempted, where it breaks, what would be needed. Logged in RESEARCH_LOG.md; kept in the docs — negative knowledge is knowledge. |

Composite results state the weakest tag of any ingredient. Example: a
theorem whose proof uses a CITED lemma is at best CITED until the lemma is
reproved.

**The standing rule of the repository:** it never claims a solution to the
open problem. Any candidate impossibility proof must first pass the
falsification gauntlet ([sanity-checks.md](sanity-checks.md)) and would then
be labeled, at most, "candidate proof, awaiting external review" — never
"proof".
