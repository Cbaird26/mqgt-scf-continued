# Research Note 29 — Leptonic conversion versus cosmic expansion: a conditional coannihilation gate

**21 September 2026 (US Eastern time) | Public scientific-development draft, not peer reviewed.** Christopher Michael Baird is the human author; ChatGPT (ZoraASI) assisted with this conditional derivation, independent numerical checks, code and text. The two-singlet fields are hypothetical. This note neither establishes a cosmological history nor detects dark matter or consciousness/ethics fields.

## 1. Question left open by Note 28

Note 28 reports the *conditional*, nonrelativistic Maxwell–Boltzmann fraction `n2_eq/(n1_eq+n2_eq)=0.05784749058` at an **assumed** `x=m1/T=20`. The effective coannihilation formula requires the states to maintain chemical equilibrium, which Note 28 did not check. Here we compare the **previously calculated, vacuum leptonic partial decay width only** to an **assumed radiation-dominated Hubble rate** at the same illustrative temperatures. This does not calculate all conversions or infer an actual freeze-out temperature.

Use the unfitted Note-22 point `m1=10 GeV`, `m2=11.5 GeV`, `Gamma_l(s2 -> s1 e+e-, s1 mu+mu-)=3.060267688e-22 GeV`. For the following *illustrative cosmology only*, choose the nonreduced Planck mass `M_Pl=1.2209e19 GeV`, `g_*(T)=60`, negligible new-sector contribution to radiation density, and radiation domination, giving

```
H(T) = sqrt(8*pi^3*g_*/90) T^2/M_Pl
     = approximately 1.66 sqrt(g_*) T^2/M_Pl.
```

`g_*=60` is a **sensitivity setting**, not a calculated Standard Model equation-of-state value near the QCD crossover. Use `hbar=6.582119569e-25 GeV s` only to convert units. We do not substitute `H` for a detector timescale or use this approximation for nonradiation cosmologies.

At the assumed `T=0.5 GeV`, `H=2.63320146442e-19 GeV` and `H^-1=2.49966425e-6 s`, while `Gamma_l/H=0.00116218517`. At `T=0.4 GeV`, `H=1.68524893723e-19 GeV`, `H^-1=3.90572539e-6 s` and `Gamma_l/H=0.00181591433`. Across merely illustrative `g_* = 10...100` at `T=.5 GeV`, the rest-frame leptonic ratio is `0.00284676...0.000900225`, still below unity. **These are comparisons for the partial leptonic process, not bounds on the unknown total conversion rate.** The full `Gamma_2` is at least `Gamma_l`, potentially much larger; no hadronic, radiative or plasma scattering width was supplied.

## 2. Thermal time dilation and detailed balance

If both singlets and a zero-chemical-potential lepton bath obey Maxwell–Boltzmann equilibrium distributions, if medium corrections to the vacuum leptonic matrix element are neglected, and if the decays/inverse decays use the same interaction, the equilibrium reaction density for the *leptonic* channel is

```
R_D,l = n2_eq * Gamma_l * D2(T),
D2(T)=<m2/E2>_MB=K1(m2/T)/K2(m2/T),    0 < D2 < 1.
R_inverse,l = R_D,l  (detailed balance at equilibrium),
R_inverse,l/n1_eq = (n2_eq/n1_eq) * Gamma_l * D2.
```

The inverse rate per equilibrium light particle is a *reaction-density normalization*, **not** a complete chemical relaxation eigenvalue; a coupled Boltzmann system is required for that. The approximate Note-28 nonrelativistic density ratio is

`q_NR=(m2/m1)^(3/2) exp[-(m2-m1)/T]`.

For more accurate **ideal-gas Maxwell–Boltzmann** number densities, use `q_MB=(m2/m1)^2 K2(m2/T)/K2(m1/T)`. `K1` and `K2` denote modified Bessel functions; the supplied dependency-free code integrates their positive representation. The resulting exact-MB values at the *same illustrative point* are:

| Assumed T | q_MB | heavy equilibrium fraction q_MB/(1+q_MB) | D2 | leptonic decay per heavy / H | leptonic inverse per light / H |
|---|---:|---:|---:|---:|---:|
| 0.5 GeV | 0.06068676766 | 0.05721459861 | 0.9381768707 | 0.001090335245 | 0.00006616892167 |
| 0.4 GeV | 0.02873090418 | 0.02792849332 | 0.9500172197 | 0.001725149879 | 0.00004956511588 |

Thus Note 28's 5.7847% at `T=.5 GeV` is the **nonrelativistic approximation**; the full MB ideal-gas value is **5.7215%** under the same equilibrium premise. The discrepancy (~1.1% relative) is a controlled ideal-gas refinement, not a determination of the real population. As a dependency-free upper bound *within these assumptions*, `D2<=1` and `q_NR` give `R_inverse,l/(n1_eq H) <= 7.13573386e-5` at `T=.5 GeV`; the exact-MB evaluation gives `6.61689217e-5`.

## 3. Conclusion's narrow scope

**The calculated vacuum leptonic decay and inverse-decay channels by themselves do not meet the conventional `Gamma_conversion >> H` rapid-conversion criterion at either *assumed* temperature.** This is a quantitative insufficiency result for **that deliberately incomplete subset**, not proof that the full two-singlet theory ever departs from equilibrium: the unknown `s2` hadronic width, thermal inelastic scatterings `s1+SM <-> s2+SM`, dark-sector pair conversions, plasma effects, thermal history and the actual `g_*(T)` can change the result. Nor does `Gamma_l/H <<1` establish that the stable `s1` makes all, some, or none of Galactic dark matter. The **actual total `s2` lifetime is not fixed** by the leptonic upper lifetime bound.

Before applying Note 28's `sigma_eff` formula, calculate the full, nonoverlapping **temperature-dependent reaction-density matrix**, including conversions and their detailed-balance partners, and test chemical/kinetic equilibrium across the relevant epoch. If rapid conversion fails, solve the separate species Boltzmann equations, not the one-equation effective approximation. Independently authenticate the four missing Omnès source files before deriving a QCD hadronic partial width; do not execute the upstream `eval` input loader. This note does not change `main`, release a preprint, make a collider/BBN exclusion, or claim independent peer review.

## 4. Reproducibility and external methodological sources

`thermal_conversion_gate.py` implements the assumed radiation-era `H`, earlier leptonic rate, detailed-balance expression, and numerical Bessel integral. `test_research_note_29.py` includes 16 locally passing **mathematical and regression tests**, with an additional independent SciPy Bessel-function cross-check of the numerical values; neither test set analyzes experimental data. All energy values are GeV in natural units. The earlier `Gamma_l` is taken from Note 22 as recorded in Note 28, not recomputed here from new external data.

- Radiation-era Friedmann expression, equilibrium Bessel-number densities and assumptions for the coannihilation single-equation treatment: *Revisiting the averaged annihilation rate of thermal relics at low temperature*, Eur. Phys. J. C **84**, 751 (2024), https://doi.org/10.1140/epjc/s10052-024-13108-7 . That paper does **not** study this benchmark.
- Thermal decay time-dilation factor and equilibrium reaction-density conventions: *Boltzmann Equation and Its Cosmological Applications*, Symmetry **17**, 921 (2025), https://www.mdpi.com/2073-8994/17/6/921 . Formulae were adapted with the explicitly stated *per heavy/per light particle* normalization; no external numerical data were imported.
- Origin of the benchmark, leptonic floor, conditional nonrelativistic population and missing channels: Notes 22 and 28 in this **unmerged** public development PR.
