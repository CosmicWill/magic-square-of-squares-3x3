# arXiv:1912.08908v3 — Bruin, Thomas, Várilly-Alvarado (BTVA)

**Explicit computation of symmetric differentials and its application to
quasi-hyperbolicity.** Published as *Algebra & Number Theory* 16 (2022)
1377–1405, doi:10.2140/ant.2022.16.1377.

Acquired 2026-08-26: uploaded by the repository owner (arXiv source
tarball, since this working environment cannot fetch arXiv directly).
Provenance in [docs/references.md](../../docs/references.md) upgraded to
**READ** — the full LaTeX source has been read here end to end, and the
paper's magic-square-relevant numbers are independently reproduced by
`compute/btva_bounds.py` + `verify/checks/a7_btva.py`
(`python3 -m verify --only a7btva`).

## Contents

| File | What it is |
|---|---|
| `1912.08908v3.tar.gz` | The original arXiv source tarball, byte-for-byte as uploaded |
| `BTVA.tex` | The paper's full LaTeX source (extracted; 1781 lines) |
| `anc/readme.txt` | The authors' description of the ancillary files |
| `anc/barthsextic_script.m`, `anc/barthsextic.out`, `anc/sextic_results.m` | Magma script + transcript + intermediate results for **Theorem 1.1** (Barth's sextic) |
| `anc/perfectcuboid_script.m`, `anc/perfectcuboid.out` | Magma script + transcript for **Theorem 1.2** (perfect-cuboid surface) |

**Note for this repository's program:** the ancillary directory contains
computations for the Barth sextic and perfect-cuboid applications
**only** — there is *no* magic-square script. That is consistent with
the paper's own statement (§`s:QuadricCIs`, near
`thm:magicsquares`) that the magic-square surface
"*is out of range of current computational techniques to explicitly
determine* $\hat S^m\Omega^1_{X_{\mathrm{ms}}}$", so the explicit
special-curve-locus method (their Corollary `C:explicit_resultant_locus`)
was **not** executed for $X_{\mathrm{ms}}$. Enumerating the low-genus
curves on $X_{\mathrm{ms}}$ — this repository's keystone task A2-T1 =
A5-P3, underway in [docs/attacks/A7-curve-enumeration.md](../../docs/attacks/A7-curve-enumeration.md)
— is therefore not duplicated by the paper or its electronic resources.

Magma is not available in this environment; the `.m` scripts are kept as
the authors' record (and as templates for the cuboid-style argument),
not run here. Everything this repository *relies on* is re-implemented
and re-verified in pure Python under `compute/` and `verify/`.
