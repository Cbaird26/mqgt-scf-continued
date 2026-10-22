This research prerelease continues the [scalar and anomaly-sector note](https://github.com/Cbaird26/mqgt-scf-continued/releases/tag/v2026.10.22-scalar-anomaly-sector) with exact internal spectral representations for the scalar coefficients and Higgs-induced neutral kinetic response. It includes an 11-page research note and a reproducibility bundle containing manuscript source, scripts, numerical results, inputs, assumptions, provenance, and the self-audit record.

## Results

- Computes the scalar quadratic coefficient, wave-function coefficient, quartics, full transverse neutral kinetic and mass response, and leading Higgs-induced kinetic shifts for the specified microscopic Yukawa insertion and geometric weak lift.
- At the inherited radius, the two mixed quartics split: `C0 != C1`, while `C0 + C1 = 2 A4`. The common-vacuum profile pair also yields distinct scalar coefficients.
- For the minus profile, the canonical low-momentum quadratic mass parameter is approximately `-1.76153736315 Lambda^2`, compared with `-1.49015750336 Lambda^2` in the local truncation. This is **not a physical pole mass**.
- Reproduces all three inherited unbroken neutral kinetic coefficients, retains the photon null direction `(1,1,0)`, and computes its Higgs-induced normalization shift. With four copied blocks, unit Yukawa parameters, and identical noncanonical amplitudes, `e^-2/kappa = 0.399990428306938 - 0.03932044964836 h_d^2 - 0.03773847661343 h_u^2 + O(h^4)` for the minus profile.
- Corrects predecessor A9: the geometric weak-field Higgs correction already has an `a4` scalar-curvature contribution; it does not first arise at `a6`. The shared-local-moment invariance statement is unchanged.

## Reproducibility and verification

The sealed package records **126/126 passing checks**, including independent Wigner-function sphere quadratures, block-exponential/Cauchy comparisons, an external-Clifford finite-momentum check, and cutoff/contour/step-size comparisons. These are computational checks, not 126 independent physical predictions. A fresh extraction reproduced `results.json` and `checks.json` byte-for-byte on the recorded environment. All eleven final PDF pages were inspected.

Download the PDF, ZIP, and `RELEASE_SHA256SUMS.txt` into the same directory, then run:

```bash
shasum -a 256 -c RELEASE_SHA256SUMS.txt
unzip Exact_Scalar_Mode_Sums_Reproducibility_2026-10-22.zip
cd Exact_Scalar_Mode_Sums_2026-10-22
shasum -a 256 -c SHA256SUMS.txt
```

The bundle README gives dependency and reproduction commands. Run calculations from a writable copy to preserve the sealed results. Tested versions and broader minimum requirements are both supplied.

| Asset | SHA-256 |
| --- | --- |
| `Exact_Scalar_Mode_Sums_and_Higgs_Kinetics_2026-10-22.pdf` | `e61f019843dfcb55dae8c8a74d9ef70fd6891250a349906ebdbbc9fb50449a46` |
| `Exact_Scalar_Mode_Sums_Reproducibility_2026-10-22.zip` | `413dd59946383a9404975d0683a5c269a231252a8052ea2a1c3b2807aab4b93d` |

## Scientific status and caveats

The result is conditional on the declared microscopic insertion and torsion-free geometric weak lift; it does not establish a unique ultraviolet completion. “Exact” describes the internal spectral representations. Numerical values use finite angular cutoffs and float64/complex128; the 95-digit inherited profile input is preserved unchanged. There is no interval-rounding enclosure or universal tail certificate.

The potential is expanded through quartic order, the scalar kinetic term through two external derivatives at the symmetric background, and the displayed neutral kinetic shifts through second order in the Higgs amplitudes. Profile comparisons hold the inherited radius and noncanonical fields fixed. The finite-background example is a prescribed diagnostic background, not a solved physical vacuum.

No new coupled scalar/radius/anomaly vacuum, physical scalar pole masses, higher-boson integration, full compactification stability, six-dimensional anomaly polynomial/Green–Schwarz reduction, or independently derived Stueckelberg mass is supplied. Independent normalization (`kappa`), profile selection, quantum thresholds, and running remain open. The heat kernels are classical spectral-action data, not a loop computation. **The measured fine-structure constant remains unexplained; no measured coupling was fitted.**

This is AI-assisted research prepared with OpenAI Codex. The self-audit and independent computational methods were performed in the same assistant session; there was no separate agent referee or external peer review.

## Source and preservation

The tagged source is in [`research_continuation/2026-10-22/exact_scalar_mode_sums/`](https://github.com/Cbaird26/mqgt-scf-continued/tree/v2026.10.22-exact-scalar-mode-sums/research_continuation/2026-10-22/exact_scalar_mode_sums). The 22 payload files and their manifest are preserved byte-for-byte from the sealed ZIP. Their statements that publication had not occurred describe the preparation stage; this prerelease records the subsequent publication. Additional publication metadata is outside that original manifest. Earlier research files remain unchanged, with additive index links in the two READMEs.

License: CC BY 4.0, preserving predecessor attribution. This is a research prerelease, not a validated phenomenological prediction.
