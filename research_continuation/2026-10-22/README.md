# Research continuation — 22 October 2026

## Spectral Profile Nonuniqueness at a Common Stationary Vacuum

This additive continuation contains the common-vacuum spectral-profile theorem
and its reproducibility materials. The research note is dated 21 October 2026;
the publication package is dated 22 October 2026.

- [Publication summary and reproduction instructions](electromagnetic/README.md)
- [Complete research note (PDF)](electromagnetic/Spectral_Profile_Common_Vacuum_2026-10-21.pdf)
- [LaTeX source](electromagnetic/research_note.tex)
- [Release notes](publication/RELEASE_NOTES.md)
- [Exact approved publication ZIP](publication/Spectral_Profile_Common_Vacuum_Publication_2026-10-22.zip)
- [Research prerelease and publication record](https://github.com/Cbaird26/mqgt-scf-continued/releases/tag/v2026.10.22-spectral-profile-common-vacuum)

For every finite retained local order, the theorem constructs suitable distinct
positive exponential profiles with common local data, stationary radius,
subtraction, and gravitational coefficient, but different exact hypercharge
coefficients. Both restricted radius-potential curvatures are positive. This is
an existential result within the stipulated action and profile class. It does
not select a physical action, derive the measured fine-structure constant, or
establish complete compactification stability.

The [October 21 checkpoint](../2026-10-21/README.md) is the historical predecessor.
Its five- and six-component examples selected their stationary vacua separately;
the present theorem and ten-component example retain a common vacuum and
gravitational coefficient.

## Preservation and publication records

The approved ZIP and all files within it are preserved byte-for-byte. Its SHA-256
is `9fa24e444bc603432673d9f9f6c3369e4e909d0706725bbb1e965cd3ee07e218`.

The four metadata files in `publication/` reproduce the original archive-root
files. In particular, `publication/SHA256SUMS.txt` describes paths relative to
the ZIP root, not relative to that repository subdirectory. The electromagnetic
directory has a separate manifest for its own contents.

`PREPUBLICATION_RECORD.json`, `PACKAGE_README.txt`, and the original research
`provenance.json` describe their historical preparation stages. Statements there
that publication had not occurred remain preserved as historical statements.
The release's separate `PUBLICATION_RECORD.json` records the actual source
commit, tag, and asset identities; GitHub records the publication time. The
publisher also retains an execution receipt with that time in its workflow
artifact.

The narrow publication workflow verifies the approved archive, every archived
file, the ten original research files, and uploaded asset digests before making
the research prerelease public. It does not rerun or rewrite the calculations.

License: CC BY 4.0, matching the repository and the included research license.

## Scalar and anomaly-complete sector (same date, later continuation)

### A Microscopic Scalar and Anomaly-Complete Sector for the Shared Spectral Action

- [Summary and reproduction instructions](scalar_anomaly_sector/README.md)
- [Complete research note (PDF, 13 pages)](scalar_anomaly_sector/Scalar_Anomaly_Sector_Coupled_Vacuum_2026-10-22.pdf)
- [LaTeX source](scalar_anomaly_sector/research_note.tex)
- [Explicit assumptions](scalar_anomaly_sector/ASSUMPTIONS.md) and [review record](scalar_anomaly_sector/REVIEW_RESPONSE.md)
- Research prerelease: `v2026.10.22-scalar-anomaly-sector`

This continuation adjoins a specified six-dimensional scalar sector to the inherited shared
spectral action. It has two charged scalars, Phi_d and Phi_u, with x = +1 and -1, entering the
Dirac operator as Yukawa insertions. The continuation:

- derives the a_2–a_4 scalar action and delimits the exact mode-sum (ultraviolet) remainder;
- cancels the U(1)_X anomalies with a Stueckelberg axion (a six-dimensional two-form on the flux);
- solves the coupled scalar, radius, and axion vacuum;
- computes the broken-background neutral kinetic and mass matrices;
- identifies the surviving massless generator, (1,1,0), with the null-space residue formula,
  giving e^-2 = K_WW + K_BB + 2 K_WB;
- scopes the quantum-matching setup.

The published pair difference Delta(e^-2/kappa) = 1.5519080018e-7 holds at the inherited radius.
At the tuned coupled vacuum it acquires an O(eps) radius-splitting correction, whose Y part is
computed. The untuned truncated action places the Higgs vacuum at the cutoff and admits no flat
stationary radius on the scanned range.

The result is conditional on the declared completion. It does not derive the measured
fine-structure constant, does not fix kappa, and computes no thresholds or running. Two
predecessor notes are cited from the shared research transcript, because their bundles are not
yet in this repository:

- Geometric Weak-Gauge Response and Electromagnetic Profile Dependence;
- Neutral Gauge and Higgs Matching.

The weak coefficient Z_W is taken from the first of these and is not recomputed. The
reproduction bundle passes 228 recorded assertions. A separate AI review pass (not external peer
review) produced 14 findings, all addressed in `REVIEW_RESPONSE.md`. The bundle's
`SHA256SUMS.txt` covers every file in `scalar_anomaly_sector/`.

## Exact internal mode sums and Higgs-induced neutral kinetics (next continuation)

- [Publication record and package links](exact_scalar_mode_sums/PUBLICATION.md)
- [Research note (PDF, 11 pages)](exact_scalar_mode_sums/Exact_Scalar_Mode_Sums_and_Higgs_Kinetics_2026-10-22.pdf)
- [Reproduction instructions](exact_scalar_mode_sums/README.md) and [LaTeX source](exact_scalar_mode_sums/main.tex)
- [Assumptions](exact_scalar_mode_sums/ASSUMPTIONS.md), [self-audit](exact_scalar_mode_sums/REVIEW.md), and [release caveats](exact_scalar_mode_sums/RELEASE_NOTES.md)
- [Research prerelease: v2026.10.22-exact-scalar-mode-sums](https://github.com/Cbaird26/mqgt-scf-continued/releases/tag/v2026.10.22-exact-scalar-mode-sums)

This continuation evaluates exact internal spectral representations for the scalar coefficients
and full neutral kinetic response, recomputes the inherited unbroken weak/Y/X coefficients,
and gives the leading Higgs-induced kinetic shifts. The mixed quartics are unequal at the
inherited radius. The photon direction (1,1,0) is retained. The predecessor's A9 order-counting
is corrected: the geometric weak Higgs correction already has an a4 curvature contribution.

The 126 recorded computational checks pass; a fresh extraction reproduced the numerical
result files byte-for-byte. The source bundle and PDF remain unchanged from the sealed
preparation. Preparation-stage statements about local publication status are historical;
the separate publication record and release establish the subsequent publication.

The calculation is conditional on the specified insertion and geometric lift, with finite
numerical cutoffs and no universal tail certificate. It computes no new coupled vacuum,
physical scalar pole masses, full anomaly completion, independent normalization, or quantum
thresholds and running. The measured fine-structure constant remains unexplained. The work
is AI-assisted and has not undergone external peer review.
