# MQGT-SCF — Continued Development Line

This repository is the **forward development line** of the MQGT-SCF
(Multi-Quantum Geometric Theory / Self-Consistent Field) program, carrying the
corpus forward with the September 2026 independent-verification repairs
**applied**.

It is deliberately separate from the frozen record:

- **Frozen verification record (do not modify):**
  [`Cbaird26/mqgt-scf-independent-verification`](https://github.com/Cbaird26/mqgt-scf-independent-verification),
  release `v1.0-paper` — the paper, errata E1–E13, and verification code,
  minted as a permanent snapshot.
- **Canonical upstream corpus:**
  [`Cbaird26/mqgt-scf-science-public`](https://github.com/Cbaird26/mqgt-scf-science-public).

This repo is where the errata stop being annotations and become the text.

**Census (2026-09-18).** Wyler–Nielsen geometric α⁻¹ = 137.03608245 is a
six-correct-digit approximation to CODATA 2022 (residual 6.0765×10⁻⁷);
the O(10⁻⁷) correction is not in the round-bundle spectrum (two
certified exclusions, `exclusions/`); T-3 constants are identified as
spectral determinants on S⁷ and S⁹, not derived.

> **This record does NOT claim:**
> - an eight-digit (or better) derivation of α from geometry
> - first-principles derivation of the T-3 normalizations (identification only)
> - experimental detection of any MQGT-SCF observable — all experimental
>   work is software-validation / protocol-development stage
> - tested confirmations of the corpus's Φ_c / E-sector observables
> - a natural ultralight scalar coupled to the physical Higgs (the
>   sequestering note's minimal model fails that scale check, erratum 7)
> - the general symmetry-allowed hidden model (the note's §1 is minimal)
> - institutional independence of the frozen verification repo — the
>   independence is procedural (minted snapshot, preregistered scripts),
>   same account
> - Lean-4 compile checks as physics evidence (they are proof-assistant
>   checks of stated theorems, where used)

## Research continuation — 22 October 2026

**Radion kinetics and scalar mixing (next continuation).**
[Research note and reproducibility package](research_continuation/2026-10-22/radion_dynamics/PUBLICATION.md)
derives the radion/lowest-scalar kinetic metric and Einstein-frame mixing at two external
derivatives. Both profiles at both supplied tunings have positive nine-field Einstein
kinetic matrices, five positive generalized squared-mass parameters and four symmetry
zeros. The assumed axion sector leaves one physical phase massless. **The radion parameter
near `0.91 Lambda` is not a verified full-theory pole; full compactification and ultraviolet
stability remain unresolved.** The mass counterterm and flatness subtraction remain
selected inputs. The package preserves 109 passing computational checks and fresh-extraction
reproduction, with all stated caveats. The measured fine-structure constant remains unexplained.
**Research prerelease:** [v2026.10.22-radion-kinetics-scalar-mixing](https://github.com/Cbaird26/mqgt-scf-continued/releases/tag/v2026.10.22-radion-kinetics-scalar-mixing).

**Exact scalar-radius vacuum: instability and tuned stationary branches (next continuation).**
[Research note and reproducibility package](research_continuation/2026-10-22/exact_coupled_vacuum/PUBLICATION.md)
evaluates the full spectral potential in the retained lowest scalar harmonics.
The untuned inherited action has a scalar saddle and an analytic unbounded direction
at fixed subtraction. With an explicitly chosen scalar-mass counterterm and separately
selected flatness subtraction, coupled branches have positive retained static curvatures,
modulo gauge/phase flat directions. The exact radius shift reverses the local approximation.
The package records 51 passing computational checks and fresh-extraction reproduction.
These restricted-background results do not establish full dynamical or compactification
stability or physical pole masses; the measured fine-structure constant remains unexplained.
**Research prerelease:** [v2026.10.22-exact-coupled-vacuum](https://github.com/Cbaird26/mqgt-scf-continued/releases/tag/v2026.10.22-exact-coupled-vacuum).

**Exact internal mode sums and Higgs-induced neutral kinetics (next continuation).**
[Research note and reproducibility package](research_continuation/2026-10-22/exact_scalar_mode_sums/PUBLICATION.md)
computes scalar quadratic, wave-function and quartic coefficients and the full transverse
neutral response, including leading Higgs-induced kinetic shifts. The mixed quartics split
at finite radius, and the geometric weak correction already contributes at a4, correcting
the predecessor's A9 order-counting. The package records 126 passing computational checks.
These conditional classical spectral-action results use converged finite-cutoff evaluations
of exact internal representations. No new coupled vacuum or physical pole masses are computed;
the measured fine-structure constant remains unexplained.
**Research prerelease:** [v2026.10.22-exact-scalar-mode-sums](https://github.com/Cbaird26/mqgt-scf-continued/releases/tag/v2026.10.22-exact-scalar-mode-sums).

**Scalar and anomaly-complete sector (later the same day).**
[A Microscopic Scalar and Anomaly-Complete Sector for the Shared Spectral Action](research_continuation/2026-10-22/scalar_anomaly_sector/README.md)
specifies a six-dimensional two-doublet scalar sector and a Stueckelberg axion for the U(1)_X
anomalies. It then solves the coupled vacuum, computes the broken-background neutral matrices,
and identifies the surviving photon (1,1,0) with its tree-level normalization
e^-2 = Z_W + Z_Y + delta K_gamma. The published profile-pair difference survives at the inherited
radius. The measured fine-structure constant remains unexplained.
**Research prerelease:** [v2026.10.22-scalar-anomaly-sector](https://github.com/Cbaird26/mqgt-scf-continued/releases/tag/v2026.10.22-scalar-anomaly-sector).

[Spectral Profile Nonuniqueness at a Common Stationary Vacuum](research_continuation/2026-10-22/electromagnetic/README.md)
extends the spectral-profile analysis to an arbitrary-order existence theorem.
For every finite local order, suitable distinct positive exponential profiles
share the retained local data, a stationary radius, subtraction, and gravitational
coefficient, while their exact hypercharge coefficients differ. Both restricted
radius-potential curvatures remain positive.

The [dated continuation](research_continuation/2026-10-22/README.md) includes the
analytic proof, rational seed certificate, ten-component numerical illustration,
reproduction scripts, and preserved preparation records.
**Research prerelease:** [v2026.10.22-spectral-profile-common-vacuum](https://github.com/Cbaird26/mqgt-scf-continued/releases/tag/v2026.10.22-spectral-profile-common-vacuum).
This conditional nonuniqueness result does not select a physical action, derive
the measured fine-structure constant, or establish complete compactification
stability. The October 21 checkpoint remains its historical predecessor.

## Research continuation — 21 October 2026

The [dated checkpoint](research_continuation/2026-10-21/README.md) brings together
six executed workstreams: common action conventions, thermal-history and EOS
sensitivity, public interferometry count reanalysis, spectral-profile
identifiability, an ultraviolet audit, and a synthetic causal-memory study.
It includes code, compact results, source hashes, claim status, and reproducibility
instructions.

**Release checkpoint:** [v2026.10.21-research-continuation](https://github.com/Cbaird26/mqgt-scf-continued/releases/tag/v2026.10.21-research-continuation).
The release contains the report, complete offline package, SHA-256
checksums, and an explicit clean-build and packaging record. The
scientific status below remains unchanged.

These are conditional computational and methodological results. The checkpoint
records the additional physics needed for full unification or a new experimental
claim. See its [claim-status record](research_continuation/2026-10-21/sources/claim_status.json)
and [release notes](research_continuation/2026-10-21/RELEASE_NOTES.md).

## What's in here

| Path | What it is |
|---|---|
| `ERRATA_STATUS.md` | E1–E13 disposition: which repairs are applied here, which remain open, which belong to the TUFT upstream |
| `LEDGER.md` | **Cross-repository research ledger**: claim → assumptions → derivation → code → controls → status → provenance, with the full review trail (ChatGPT rounds 1–8, Zora self-review, Grok referee disposition and directives) and open gates/refusals |
| `exclusions/` | Certified negative results: Door 1 (twisted Hopf-line towers — U(1) fiber isometry) and Door 2 (Berger/canonical deformation — D1 susceptibility lock), both CLOSED with lab certificates |
| `artifacts/T1_E4_DEPOSIT_NOTE_2026-09-18.md` | The T-1/E4 census: gated six-digit conjecture, residual 6.0765×10⁻⁷, uncitable prefactors, exclusion record |
| `neutrino_portal_v2.py` | E2 repair, applied: the neutrino portal with the 3-Yukawa texture. **Record claim = Variant A**; Variant B retained in-file as a robustness cross-check, not a menu option (referee requirement, Grok disposition) — both oscillation splittings fit exactly |
| `A_Theory_of_Everything_UPDATED_2026-09-18.pdf` | The 6,926-page unified edition: corpus + verification supplement + verification paper |
| `E4_ALPHA_GATE_RESEARCH_NOTE.md`, `E4_DERIVATION_NOTE.md`, `E4_FINAL_STATUS.md` + `mqgt_t1_e4_*.py` | E4 (T-1 α⁻¹ gate) research record: pinned target c₃ = −1.56371823031276, exclusion record across fits, QED running, existing invariants, heat kernel |
| `supporting_analysis/` | 2026-09-18 record-side theorems: middle-tower D₁ lemma and L closed forms (exact rational), mirror-check residual −1/16 closed, ζ(0) theorem (65/65 coexact towers, scalar conventions A/B), and the Part-0 open-problem-1 closure: one-loop radiative sequestering of J = κ_ES² in an explicit minimal Z₂_h-even model (Lemma 1′: E\|H\|² absent to all loop orders *in that model*; errata 1–7 on record) |
| `play_notes/` | Clearly labeled exploration branch (interior-observer / refractive α idea): pre-declared combination-rule exclusion record across eight principled weightings; kept separate from the record side per program discipline |

## Conventions

- Every repaired claim keeps a pointer to the erratum that motivated the
  change (E-number) and to the verification-repo commit that froze the
  original claim.
- Nothing here rewrites history: the minted verification release remains the
  citable record of what was claimed and when.
- TUFT-side findings (E6, E7, E9, E10) are documented here as **notes for the
  upstream author**, not applied by us — her repo, her call.

License: CC BY 4.0 (matching the verification packet).
