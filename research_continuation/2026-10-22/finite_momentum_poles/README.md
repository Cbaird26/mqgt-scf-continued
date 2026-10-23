# Finite-momentum metric/radion/scalar response and Lorentzian pole tests

Research continuation prepared for Christopher Michael Baird / ZoraASI with OpenAI Codex on 22 October 2026. Inputs are pinned to the [radion prerelease](https://github.com/Cbaird26/mqgt-scf-continued/releases/tag/v2026.10.22-radion-kinetics-scalar-mixing), commit `1bb152dfbd6bb1e02a3e841b6d73e338f8e5fabf`.

The new calculation derives the finite-momentum metric/scalar operator of the declared warped family and tests the direct continuation `z=-s-i0`. It reproduces the previous infrared kinetic matrices, but **finds a finite-momentum obstruction: tachyonic poles with negative residues and additional non-real poles**. Positive-residue light and radion-connected timelike poles do not make this a stable vacuum. These are restricted classical quadratic kernels, not a complete compactification or causal quantum propagator.

## Reproduce

Verify the original payload before rerunning:

```bash
shasum -a 256 -c SHA256SUMS.txt
```

In a writable copy, after installing dependencies:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 .venv/bin/python run_all.py
.venv/bin/python build_figures.py
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

The computation itself uses no network. It overwrites `results.json` and `checks.json` and exits nonzero if any check fails. Complex-contour isolation may take a few minutes. Tested dependency versions are recorded separately; cross-platform byte identity is not promised.

## Contents and interpretation

- `two_point.py`: spectral kernels, entire metric form factors, bordered operator, Schur complement, analytic derivatives and residues.
- `direct_vertices.py`: independent gamma-matrix and continuum Gaussian checks.
- `poles.py`: bounded real searches, refined argument-principle counts, complex root isolation and residues.
- `run_all.py`, `results.json`, `checks.json`: reproducible numerical analysis, search domains, null vectors, residues, contour cells and tolerances.
- `mode_sums.py`, `vacuum.py`, `dynamics.py`, `all_scalars.py`: unchanged pinned predecessor code.
- `inputs/`: unchanged profiles, previous fixtures/checks and historical assumptions. Previous statements that finite-momentum gravity had not yet been computed are superseded within the scope of this note.
- `main.tex`, `sections/`, `tables.tex`, `images/`, `build_figures.py`: note and figure sources.
- `ASSUMPTIONS.md`, `REVIEW.md`, `references/SOURCES.md`, `provenance.json`, `DELIVERY_VERIFICATION.json`: complete limits, self-audit, references and verification record.

Pole searches concern the closed neutral CP-even metric/radion/amplitude sector and the transverse-traceless graviton. All nine fixed-metric scalar entries are also supplied, but charged/phase poles need vector and axion constraints not derived here. The assumed massless physical phase remains an inherited conditional statement. The full bosonic compactification spectrum, omitted tadpoles, quantum contour, loops, normalization, profile selection and measured fine-structure constant remain unresolved. The selected counterterm and flatness subtraction are inputs, not predictions.

This is an AI-assisted local research package with a same-session self-audit and no external peer review. It has not been published to GitHub by its creation. License: CC BY 4.0, preserving inherited attribution.
