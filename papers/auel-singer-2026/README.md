# Source for the entry-148 intersection-matrix audit

`IntersectionMatrix.m.gz` is a gzip archive of the complete, unmodified
`IntersectionMatrix.m` published in Benjamin Singer's
[companion repository](https://github.com/BenSinger2005/A-Geometric-Approach-to-3-x-3-Magic-Squares-of-Squares/blob/main/IntersectionMatrix.m)
to Auel–Singer, [arXiv:2609.09351v1](https://arxiv.org/html/2609.09351v1).

- Retrieved: 2026-09-17, from the repository's `main` branch.
- Uncompressed size: 3,109,801 bytes.
- Uncompressed SHA-256:
  `9e019c79166b152939bb1d57e8f03ff720d5ba88a1b2e39fc15efda57b0af075`.
- Format: 1,204 bracketed rows of 1,204 space-separated integers. Line
  wrapping is part of the archived source; it does not delimit matrix rows.
- The source is numerical research data, preserved with attribution for
  reproducibility. The hash identifies the audited bytes independently of
  subsequent changes to the upstream branch.

## Offline replay

```sh
python -m compute.picard_matrix_audit
python -m verify --only picard_module_148
```

The first command verifies the source hash, extracts the principal minor
at one-based indices 321, 642, 704, 710, 812, and checks an exact rational
congruence with two positive directions. The verifier also performs an
independent Sturm count and checks the entry's arrangement and trace data.
Neither calculation needs network access or Magma.

An optional full-matrix calculation uses the project's PARI/GP installation
(`MSS3_GP` can specify it):

```sh
python -m compute.picard_matrix_audit --full
```

It checks an exact rational congruence of all 1,204 rows, with a nonzero
determinant modulo 1000003 certifying that the change of basis is invertible
over the rationals. This calculation allows the PARI stack to grow up to
2 GB and has a ten-minute timeout. It is separate from the ordinary verifier.
The 2026-09-17 replay confirmed rank 518 and inertia
(63 positive, 455 negative, 686 zero); its output is preserved in
`compute/qc/picard_matrix148.audit.json`.

The exact five-row witness suffices to contradict the interpretation of
these bytes as a divisor intersection matrix. It does not locate the
incorrect geometric entries or determine the surface's Picard rank.
