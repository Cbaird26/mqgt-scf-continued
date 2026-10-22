# Exact scalar-radius vacuum: instability and tuned stationary branches

Research continuation for Christopher Michael Baird / ZoraASI, 22 October 2026. Prepared with OpenAI Codex. This package continues the [exact scalar mode-sum prerelease](https://github.com/Cbaird26/mqgt-scf-continued/releases/tag/v2026.10.22-exact-scalar-mode-sums), pinned at commit `12fa25fc3f35b0ea0b65aa870a93fa0c501957d9`.

The full finite-background spectral potential is used, with no polynomial expansion in the retained scalar amplitudes. The inherited symmetric stationary point is a scalar saddle. A resummed large-radius expression establishes an unbounded direction for the untuned action with the inherited subtraction fixed. Numerical scans and bounded root searches supplement that analytic result but do not prove absence of all metastable extrema.

Separately, an explicit scalar-mass counterterm is chosen and held common between the two profiles. The coupled flat equations then have numerically converged small-field branches. Their retained radius/scalar Hessian and charged curvature are positive, modulo exact phase/gauge flat directions. The exact radius shift has the opposite sign from the predecessor's local scalar approximation. The counterterm and flat-vacuum subtraction are chosen inputs, not derived predictions.

## Reproduce

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 .venv/bin/python run_all.py
.venv/bin/python build_figures.py
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

The full numerical run includes a 360-point field/radius scan, twelve bounded root searches, large-radius controls, coupled solutions for both profiles, and independent checks. It may take several minutes. `run_all.py` overwrites `results.json` and `checks.json`, exiting nonzero on a failed check. Use a writable copy if preserving the sealed files. NumPy and SciPy are required; Matplotlib is needed only to regenerate figures and tables. Tested versions are pinned separately; minimum dependency versions do not promise byte-identical results across platforms.

## Files

- `Exact_Coupled_Scalar_Radius_Vacuum_2026-10-22.pdf`, `main.tex`, `tables.tex`, `images/`: note and source.
- `vacuum.py`: full spectral trace, analytic gradient/Hessian, counterterm, charged curvature, scalar kinetic metric, and resummed large-radius expression.
- `mode_sums.py`: unchanged inherited monopole and neutral-response implementation.
- `independent_checks.py`: direct matrix exponential, finite differences, independent dense angular assembly, and unbroken heat sums.
- `run_all.py`, `build_figures.py`, `seal_bundle.py`: reproduction, figures, and packaging.
- `results.json`, `checks.json`: solved branches, instability diagnostics, scans, residuals and tolerances.
- `inputs/`: preserved common-vacuum pair and predecessor scalar results.
- `ASSUMPTIONS.md`, `REVIEW.md`, `provenance.json`, `DELIVERY_VERIFICATION.json`: scope, self-audit, inputs, and delivery checks.
- `SHA256SUMS.txt`: sealed payload checksums. Verify with `shasum -a 256 -c SHA256SUMS.txt` from the extracted root.

## Scientific status

These are restricted-background stationary solutions and static stability results. Higher-harmonic tadpoles, the radion kinetic metric, full compactification stability, anomaly completion, and physical pole masses are not established. The adopted axion sector leaves a physical phase flat. No measured coupling was fitted; the measured fine-structure constant remains unexplained. The work is AI-assisted and has not undergone external peer review. See `ASSUMPTIONS.md` for the full qualifications.

This is a local research deliverable; no new publication is performed by preparing it. License: CC BY 4.0, preserving inherited attribution.
