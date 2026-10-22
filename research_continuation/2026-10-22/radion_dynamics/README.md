# Radion kinetics and scalar mixing in the exact spectral vacuum

Research continuation for Christopher Michael Baird / ZoraASI, prepared with OpenAI Codex on 22 October 2026. Continues the [exact coupled-vacuum prerelease](https://github.com/Cbaird26/mqgt-scf-continued/releases/tag/v2026.10.22-exact-coupled-vacuum), pinned at commit `8ac07febf9b760720b9c5e85898499c7195e2dde`.

The warped-product Dirac operator determines the field-dependent gravitational coefficient and the complete radion/lowest-scalar kinetic metric. The Jordan radial entry is negative, but the Einstein-frame metric is positive on all nine retained real directions for both profiles at both supplied tunings. The generalized two-derivative mass problem has five positive parameters and four gauge zeros. An assumed positive, potential-free axion sector leaves one physical massless phase after gauge reduction.

**The radion-dominated parameter is near `0.91 Lambda`, so it is not a certified pole of the full momentum-dependent theory.** Higher external derivatives, metric response, Lorentzian continuation and omitted bosonic modes remain unresolved. The result establishes restricted infrared quadratic stability tests; it does not establish full compactification or ultraviolet stability. The mass counterterm and flatness subtraction remain selected inputs. No measured coupling is fitted; the measured fine-structure constant remains unexplained.

## Reproduce offline after installing dependencies

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 .venv/bin/python run_all.py
.venv/bin/python build_figures.py
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

`run_all.py` exits nonzero on any failed check and overwrites `results.json` and `checks.json`. It performs 109 targeted checks. Use a writable copy if preserving the sealed payload. The numerical run generally takes under several minutes on the preparation host. Figure generation needs Matplotlib; the numerical calculation needs NumPy and SciPy. The tested versions are in `requirements-tested.txt`. The minimum requirements do not promise byte identity across versions or platforms. No network access is used by the computation itself.

Verify the sealed payload before rerunning:

```bash
shasum -a 256 -c SHA256SUMS.txt
```

## Files and conventions

- `Radion_Kinetics_and_Scalar_Mixing_2026-10-22.pdf`: research note.
- `main.tex`, `sections/`, `tables.tex`, `images/`: manuscript and figure sources/output.
- `dynamics.py`: neutral/radion kernels, nonminimal gravitational coefficient, Einstein transformation, finite-momentum fixed-metric diagnostic, coordinate transformation.
- `all_scalars.py`: all eight real scalar tangents plus radius, potential Hessian and kinetic matrices. Up coordinates refer to the conjugate-up Yukawa insertion.
- `independent_checks.py`: direct matrix exponential quadrature, independent dense charged assembly, external round-S4 curvature control and finite differences.
- `mode_sums.py`, `vacuum.py`: unchanged inherited numerical operators.
- `run_all.py`, `build_figures.py`, `seal_bundle.py`: computation, figure/table generation and packaging.
- `inputs/`: unchanged 95-digit common-profile data and previous sealed branch/check records.
- `results.json`, `checks.json`: full numerical matrices, modes, diagnostics, checks and tolerances.
- `ASSUMPTIONS.md`, `REVIEW.md`, `references/SOURCES.md`, `provenance.json`, `DELIVERY_VERIFICATION.json`: scope, self-audit, primary sources, input lineage and delivery checks.

The Lorentzian convention is `(-+++)`, `kappa>0`, with `F=kappa Lambda^2 f`. Kinetic matrices multiply `kappa Lambda^2/2`. At each flat fixture the Einstein reference is `f0=f_vac`, so the vacuum units agree with the original Jordan units. Reported squared masses solve `H u/(4 pi^2)=mu G_E u`; they are parameters of the two-derivative truncation, not complete-theory poles. Matrices and masses are numerical finite-cutoff values, not interval certificates.

This is a local prepared research package. Its creation does not publish a new GitHub release. The work is AI-assisted and has a same-session self-audit, with no separate-agent referee or external peer review. License: CC BY 4.0, preserving inherited attribution.
