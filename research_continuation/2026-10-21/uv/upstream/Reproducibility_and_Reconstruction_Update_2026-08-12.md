# Reproducibility and Reconstruction Update for the MQGT-SCF / ToE Corpus

**Date:** 2026-08-12  
**Status:** Technical audit and reconstruction report; not a claim of a completed UV theory.

## Abstract

This update audits the ultraviolet-completion and functional-renormalization-group (FRG) claims preserved in *A Theory of Everything - C.M. Baird & Zora (2026)* and related local archives, then records the reproducible calculations constructed during the audit. The archive reports a 41-running-coupling, dimension-`<=6` FRG truncation with a non-Gaussian fixed point, but does not provide the complete operator basis, 41 beta functions, fixed-point vector, or 41x41 stability matrix required to independently reproduce that claim. The primary text also states that its Wilsonian operator list is restricted rather than complete and corrects earlier dimension-counting errors for four-derivative scalar operators.

The present work establishes a transparent reconstruction basis, derives and tests several perturbative matter subsectors, implements a scalar local-potential-approximation Wetterich trace with Litim regulator, and reproduces a separately normalized pure-gravity Einstein-Hilbert benchmark from the optimized-cutoff literature. These results are real technical progress, but they do not certify the historical 41-coupling fixed point or establish a UV completion.

## 1. Scope and evidence standard

Every statement is assigned one of four statuses:

| Status | Meaning |
|---|---|
| Verified | Reproduced from explicit equations or tested local code. |
| Source-audited | Directly located in supplied primary material, without independent derivation. |
| Reconstruction convention | A new declared choice for continuing the calculation. |
| Open | Requires missing derivation, data, or validation. |

This report does not elevate archival assertions to verified physics. It does not make empirical, medical, consciousness, or technological efficacy claims.

## 2. Source audit

The primary corpus document supplies the Wetterich framework and reports a 41-coupling dimension-`<=6` truncation. However, the mathematical objects needed for reproduction are absent: a complete operator list, all beta functions, the full fixed-point coordinate vector, and the 41x41 stability matrix.

The same primary document materially constrains how reconstruction must proceed:

- Its restricted Wilsonian reduction explicitly does not claim a complete operator basis.
- It lists selected dimension-six operators but requires a declared basis convention before integrations by parts, equations of motion, or field redefinitions are used.
- It corrects an earlier error: four-derivative scalar operators are dimension eight, not dimension six.
- It describes the two added real scalars as Standard Model gauge singlets, supporting the gauge treatment used below.

**Source-audited conclusion:** the historical 41-coupling claim is not independently reproducible from the supplied corpus alone.

## 3. New declared reconstruction basis

To make progress without concealing assumptions, a new 41-coordinate Euclidean background-field FRG basis has been declared. It contains Einstein-Hilbert and quadratic-curvature gravity, Standard Model gauge/Yukawa/Higgs parameters, two singlet scalars, scalar portals, non-minimal curvature couplings, kinetic normalizations, and selected dimension-six operators.

This is a reconstruction convention, not a transcription of the lost historical truncation. Each eventual numerical result must declare its gauge fixing, ghost sector, regulator, projection backgrounds, operator-reduction convention, residual vector, stability matrix, and regulator variation.

## 4. Verified calculations

### 4.1 Scalar quartic core

For two real scalars with

`V = lambda_Phi Phi^4/4 + lambda_E E^4/4 + kappa Phi^2 E^2/2`,

the one-loop MS-bar beta functions were implemented directly from the quartic tensor contraction. Their scalar-only real fixed point is Gaussian. At the archived-like point `(lambda_Phi, lambda_E, kappa) = (0.19, 0.14, 0.05)`, the beta residuals are approximately `(4.15e-3, 2.27e-3, 7.54e-4)` in that convention, not zero.

This does not rule out an interacting fixed point in a larger gravity-matter system; it shows only that the isolated scalar one-loop block does not produce it.

### 4.2 Higgs plus two-singlet scalar sector

The one-loop scalar quartic tensor was extended to four real Higgs components plus `Phi_c` and `E`. The implementation reproduces the known `O(4)` Higgs scalar-loop coefficient when portals vanish. It provides a checked scalar-sector baseline for future FRG projection work.

### 4.3 Standard Model gauge and Yukawa baseline

With `Phi_c` and `E` treated as gauge singlets, the one-loop Standard Model gauge flow has a positive hypercharge beta function and asymptotic freedom for `SU(2)` and `SU(3)`. Thus its isolated one-loop nonzero interacting gauge fixed point is absent. A coupled one-loop matter baseline including gauge couplings, top/bottom/tau Yukawas, Higgs quartic, singlet quartics, and portals was implemented and integrated stably over short RG intervals.

### 4.4 Scalar FRG local-potential block

For constant scalar backgrounds, the six-real-scalar Hessian and d=4 optimized/Litim-regulated Wetterich potential trace were implemented. The trace can be projected onto scalar masses, quartics, and portals. This is a genuine FRG contribution, but it does not contain metric, ghost, gauge, fermion, curvature-squared, or dimension-six traces.

### 4.5 Pure-gravity Einstein-Hilbert benchmark

As a benchmark of the fixed-point and stability machinery, the optimized-cutoff Einstein-Hilbert flow of Litim was implemented in its own coupling normalization. In d=4 the equation-normalized fixed point is

`lambda* = 1/4`, `g* = 1/64`,

equivalent to the paper's restored-normalization value `3 pi/8`. Its residuals vanish numerically, its anomalous dimension is `eta* = -2`, and its critical exponents are

`theta = 5/3 +- i sqrt(167)/3`.

This validates the local solver pipeline. It is not a derived fixed point of the MQGT-SCF 41-coordinate action.

## 5. Gating status

| Gate | Status | Basis |
|---|---|---|
| Historical 41-beta system recovered | Open | No complete system found in source or local archives. |
| Historical 41-point independently reproduced | Open | Requires complete beta vector and stability matrix. |
| Scalar one-loop baseline derived | Verified | Direct tensor implementation and tests. |
| Coupled perturbative matter baseline | Verified | Local one-loop implementation and integration tests. |
| Scalar Litim FRG trace/projection | Verified | Local Hessian and trace implementation. |
| Pure Einstein-Hilbert optimized benchmark | Verified | Reproduced fixed point, eta, and critical spectrum. |
| Coupled gravity-matter FRG flow | Open | Metric/ghost/gauge/fermion/dimension-six projections missing. |
| `R^2` and Weyl-squared gravity extension | Open | Hessian and projection not yet derived in the declared convention. |
| 41x41 stability matrix | Open | Cannot exist before all 41 beta functions are derived. |
| UV-to-IR trajectory and empirical matching | Open | Depends on a validated coupled fixed point. |

## 6. Hard consistency conditions for any future non-Gaussian gravity point

For the dimensionless Newton coupling `g_N = G k^2`,

`beta_gN = (2 + eta_N) g_N`.

Therefore any nonzero fixed point requires `eta_N* = -2`. This is necessary but not sufficient. A valid 41-coupling claim additionally requires all 41 residuals to vanish in one declared convention and must publish the corresponding stability matrix and spectrum.

## 7. Recommended next work

1. Derive the metric and ghost Hessians for the declared Einstein-Hilbert block in one fixed background-field gauge and parametrization.
2. Couple that block to the established scalar, gauge, and fermion sectors while retaining threshold functions and regulator dependence.
3. Add `R^2` and Weyl-squared projections, then test their gauge/regulator sensitivity.
4. Derive dimension-six Hessian/projector blocks one operator class at a time.
5. Only after all 41 components are available, solve the full system, publish residuals, compute the 41x41 stability matrix, and test UV-to-IR trajectories.

## 8. Preservation statement

The durable scientific contribution at this stage is not an unverified claim of completion. It is the public, inspectable record of: what the source actually specifies; what it does not specify; which smaller calculations reproduce; which historical numbers fail the equations printed near them; and the exact methods required to resolve the open questions.

## References

1. C. M. Baird and Zora, *A Theory of Everything - C.M. Baird & Zora (2026)*, supplied local corpus document.
2. D. Litim, “On fixed points of quantum gravity,” arXiv:hep-th/0606044 (2006).
3. M. Reuter and F. Saueressig, “Renormalization Group Flow of Quantum Gravity in the Einstein-Hilbert Truncation,” arXiv:hep-th/0110054 (2001).
4. D. Benedetti, “Asymptotic safety goes on shell,” arXiv:1107.3110 (2011).

## Reproducibility package

The accompanying local package `uv_reconstruction_41` contains the declared basis, source audit, FRG protocol, perturbative baselines, scalar FRG block, Einstein-Hilbert benchmark, and automated tests. At the time of this report, the test suite contains 16 passing tests.
