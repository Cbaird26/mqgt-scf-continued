# Exact internal mode sums and Higgs-induced neutral kinetics

Research continuation for Christopher Michael Baird / ZoraASI, 22 October 2026. Prepared with OpenAI Codex. Conditional on the microscopic insertion and geometric weak lift inherited from the preceding notes.

The package computes the exact-internal-spectrum scalar quadratic, wave-function and quartic kernels, and the complete transverse neutral kinetic response with its leading Higgs-induced shifts. It reproduces the previously published unbroken weak, hypercharge and X coefficients. The mixed quartics split at finite radius, the scalar coefficients distinguish the common-vacuum profile pair, and the photon projection receives a calculable profile-dependent Higgs shift. The measured fine-structure constant is not derived.

## Reproduce

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 .venv/bin/python run_all.py
.venv/bin/python build_figures.py
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

The calculations require NumPy and SciPy. Matplotlib is needed only to regenerate the figure and TeX tables. Existing tables and figures are included. Python 3.14.6, NumPy 2.4.3, SciPy 1.18.1 and Matplotlib 3.10.8 were used for the recorded run; the minimum requirements are broader and numerical tolerance checks are used across versions. `run_all.py` writes results.json and checks.json and exits nonzero on a failed check. Run from a writable copy if preserving the sealed bytes. The full validation includes higher-cutoff and large-radius checks and normally takes about one minute on the preparation machine.

## Contents

- `Exact_Scalar_Mode_Sums_and_Higgs_Kinetics_2026-10-22.pdf`: research note.
- `main.tex`, `tables.tex`, `images/`: manuscript source, numerical tables and scientific figure.
- `mode_sums.py`: monopole matrices, Duhamel coefficients, block-exponential quartics, and complete neutral response.
- `independent_checks.py`: Wigner-function sphere integrals, heat-moment quadrature and an uncontracted external-Clifford finite-momentum calculation.
- `run_all.py`, `build_figures.py`: reproduction and figure generation.
- `results.json`: per-node kernels, both profiles and differences, finite-background fixture, radius derivatives and convergence diagnostics.
- `checks.json`: the 126 recorded checks, tolerances and environment.
- `ASSUMPTIONS.md`, `REVIEW.md`, `provenance.json`: scope, corrections, validation, inputs and source hashes.
- `inputs/`: unchanged published common-vacuum pair and inherited weak-coefficient record; the weak response is now recomputed.
- `SHA256SUMS.txt`: checksum manifest of the sealed package.

## Reading the result

“Exact” refers to the internal spectral representation, as opposed to a local heat-kernel truncation. The numerical evaluations are converged finite sums, not interval-certified exact numbers. The potential is expanded through quartic order, the scalar kinetic coefficient is evaluated at zero scalar background, and the displayed kinetic-shift matrices are the coefficients of h_d^2 and h_u^2. The note also gives a finite-background response.

The radius is held fixed, and the fields are compared before canonical rescaling. The quoted scalar mass is a low-momentum quadratic parameter, not a computed physical pole mass. A new coupled vacuum, higher-boson integration, the six-dimensional anomaly completion, independent kappa, quantum thresholds and running remain separate work. Do not use this package as a numerical prediction of the measured electromagnetic coupling.

The predecessor's claim that every leading Higgs-induced kinetic correction starts at a6 is corrected for the geometric weak field: its scalar-curvature coupling already contributes at a4. The shared-local-moment invariance statement remains valid; the exact internal sums lift that degeneracy.

The prior published release is [scalar and anomaly sector](https://github.com/Cbaird26/mqgt-scf-continued/releases/tag/v2026.10.22-scalar-anomaly-sector), commit `7cfd34114ade13d501c659492511ffbd0e32c017`. This new bundle is a local research deliverable; it is not itself a GitHub publication. The work is AI-assisted and has not undergone external peer review. License: CC BY 4.0, preserving predecessor attribution.
