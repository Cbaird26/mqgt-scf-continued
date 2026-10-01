# Research Note 33 — Finite-time conversion sensitivity, and an executed Notes 31–32 regression audit

**22 September 2026 | Public scientific-development addendum; not peer reviewed.** Human author: Christopher Michael Baird. ChatGPT (ZoraASI) assisted with mathematics, calculations, code verification and drafting. All field and cosmological interpretations remain hypothetical. This note reports neither a dark-matter abundance nor a calculated hadronic width, an experimental constraint, or a validated theory of everything.

## 1. Close an outstanding reproducibility gate before another inference

Local execution returned. The previously staged **exact repository source** `conversion_history.py` and **exact repository tests** `test_research_notes_31_32.py` were copied into one local directory, and their Git blob hashes were independently checked against the GitHub `fetch_file` metadata at the approved PR head. They match respectively `ea8f181c93af00f5445eecf20047a7d157174c7f` and `6a49d2e2fe89e698aa2375d8b5b01137c531ce9a`. Running `python -m unittest test_research_notes_31_32 -v` against those exact bytes produced **16 tests, 16 passes, 0 failures, in 2.558 s**. These are algebra, reference-number, convergence, positivity, and input-validation tests for an *assumed* conversion-only model; they do not supply missing physical reactions or observational validation. Earlier Notes 31–32 accurately stated that the tests were *unexecuted at the time of staging*; this dated note records their subsequent execution without silently rewriting those historic statements.

## 2. Exact structure of the restricted toy problem

Retain the Note-32 assumptions only: m1=10 GeV, m2=11.5 GeV, known vacuum **leptonic partial** Gamma_l=3.060267688e-22 GeV, equilibrium Maxwell–Boltzmann ideal-gas ratio q(T), common kinetic temperature, constant illustrative radiation/entropy degrees g*=g*S=60, radiation domination, zero bath chemical potentials, T=m1/x proportional to inverse scale factor, and a fixed *comoving total number* of odd singlets. At x0=10 choose y0=r(x0)=0.2120425359054555, where y=n2/(n1+n2) and r=q/(1+q). The equilibrium condition at x0 is an **initial condition chosen for illustration**, not an inferred primordial history.

For a deliberately *hypothetical*, temperature-independent equivalent conversion-width multiplier c>=0, assume every missing conversion contributes in precisely the same *effective* two-state detailed-balance structure and time-dilation factor as the leptonic decay/inverse decay. Define A(x)=c Gamma_l K1(m2/T)/K2(m2/T), B(x)=q(x)A(x), Lambda=A+B and k_c(x)=Lambda/[x H(x)]. The fraction then obeys

```
dy/dx = -k_c(x) [y-r(x)] ;  y(x0)=r(x0).
```

The exact integrating-factor representation, for any nonnegative integrable k, is

```
I(x) = integral_(x0)^x k(u) du,
y(x) = exp[-I(x)] y0
     + integral_(x0)^x exp[-(I(x)-I(t))] k(t) r(t) dt.
```

The positive coefficients sum to one, so 0<=y<=1 for 0<=y0,r<=1. On a cooling interval where r(x) is nonincreasing and y0=r(x0), this equation gives r(x)<=y(x)<=y0. If k_c=c k_1 with c increased at every x, the solution y_c(x) is nonincreasing in c: the deviation y_c-r is initially zero, remains nonnegative, and comparing the two linear equations yields a nonnegative difference for the smaller-c trajectory. These are **structural conditional claims**, not data-driven bounds on the actual universe. This is a bounded one-variable integration, not the full coupled annihilation/chemical/entropy Boltzmann system.

## 3. Finite-history thresholds are not instantaneous rates

Numerical integration of the *existing* repository `conversion_history.py` `evolve(..., method='exp-mid')` with c multiplying the fixed Gamma_l gives the following illustrative y values, all with x0=10 and y0=r(10):

| c (multiples of known leptonic partial width) | y(20) | y(30) |
|---:|---:|---:|
| 0 | 0.21204253591 | 0.21204253591 |
| 1 | 0.21199800416 | 0.21186800807 |
| 865 | 0.17863671319 | 0.10898568840 |
| 1,000 | 0.17424218582 | 0.09916572013 |
| 2,437 | 0.13774896736 | 0.04382876958 |
| 10,000 | 0.07709857006 | 0.01642523129 |
| 30,000 | 0.06240702793 | 0.01425109647 |

The **instantaneous target** is r(20)=0.0572145986119 and r(30)=0.0134099205463. Thus even c≈865—the Note-31 *single-temperature* value giving Lambda(20)≈H(20)—leaves a history-dependent, very substantial population lag. The equilibrium fraction is not the simulated actual or observed particle fraction.

Define a *chosen diagnostic*, not an observational criterion: `y(x_end)/r(x_end) - 1 <= 0.10`. Solving this one-dimensional root in the same conversion-only toy gives approximate minimum **effective multipliers** c≈2.75e4 at x_end=20 (T=.5 GeV) and c≈1.96e4 at x_end=30 (T≈.333 GeV). For the x=20 ten-percent threshold, exponential-midpoint step counts 200, 400, 800 yield c=27522.75, 27513.86, 27511.64; for x=30 they give c=19650.97, 19622.89, 19615.90. These are **mesh-convergence diagnostics**, not certified error intervals; the precision of the last digits is not a physics uncertainty. The effective 10%-lag widths are roughly 8.42e-18 GeV and 6.00e-18 GeV respectively **if** one elects to parameterize all conversions with the exact artificial c Gamma_l factor. No 10%-lag observational requirement was supplied; alternate initial conditions, time-dependent widths, plasma effects and g* changes invalidate this specific numerical inference.

A width inferred from instantaneous Lambda/H, or from one inverse-decay event count per equilibrium light particle, cannot substitute for integrating the moving-target dynamics. Conversely, these artificial multiplier thresholds **cannot** be presented as necessary physical hadronic widths, a measured or calculated total s2 width, a lower bound on actual dark-matter abundance, or a BBN/CMB limit. Non-decay 2-to-2 bath scatterings generally possess distinct phase-space, temperature and detailed-balance dependence. The original four pinned upstream Omnès files have **not** been fully authenticated or parsed, and no exclusive pion/kaon amplitude or partial width has been evaluated here.

## 4. Reproduction and outstanding work

Run `python -m unittest test_research_notes_31_32 -v` alongside the two verified source files under `manuscript/higgs_portal_review/`. To reproduce the displayed width sensitivity, vary `width=c*GAMMA_LEP` in `evolve(steps=400,method='exp-mid',width=...)` and read indices 200 (x=20) and 400 (x=30); rerun with 200 and 800 integration steps for a mesh check, and use bisection on `evolve(x1=x_end,...)[-1][1]/mb_rates(x_end)['r']-1.10` to locate each illustrative 10%-lag point. These steps reuse the **verified previous test file**, not an invented new Note-33 test suite. An attempted additional independent SciPy comparison was interrupted by a local execution error; **do not claim it passed**. The next physical release gate is independently verified complete temperature-dependent annihilation and conversion reaction densities, with authentic hadronic source files, and a coupled Boltzmann solution for a declared cosmological history and initial condition.

Source separation: Notes 22, 28–32 provide the hypothetical benchmark, known leptonic partial width, Bessel conventions and prior assumptions. This addendum derives the integrating-factor and comparison statements and reports numerical evaluations of that existing toy. No third-party hadronic code was executed; no new DOI, journal submission, or merge into `main` occurred.