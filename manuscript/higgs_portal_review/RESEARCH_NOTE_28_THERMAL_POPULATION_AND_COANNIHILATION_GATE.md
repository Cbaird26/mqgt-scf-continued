# Research Note 28 — Thermal population and coannihilation: what stable-singlet scattering cannot establish

**21 September 2026 | Author-approved public *scientific-development draft*, not peer reviewed.** Christopher Michael Baird is the human author. ChatGPT (ZoraASI) assisted with the conditional derivation, source checking, original code and algebraic tests. The restricted two-real-singlet EFT and proposed consciousness/ethics field interpretations are hypothetical; no dark-matter abundance, experimental detection or cosmological exclusion has been established.

## 1. Separate the stable-particle claim from the abundance claim

The exact common-Z2 symmetric-vacuum branch in Notes 22–27 makes the lighter singlet `s1` stable **within the stated interactions**. Note 27's per-nucleon `sigma_SI ≈ 7.39917e-47 cm²` assumes an illustrative nucleon form factor `f_N=.30` and a local abundance fraction `xi` that has not been calculated. Stability supplies neither `xi`, a primordial production mechanism, kinetic/chemical equilibrium nor the relic density. In the same unfitted benchmark `m1=10 GeV`, `m2=11.5 GeV`, `K11=.001`, the heavy odd particle is only 15% heavier. Its potential thermal population and the portal/off-diagonal and singlet-quartic reactions are therefore relevant to any actual abundance calculation. The Omnès files required for `s2` hadronic decays are still unacquired; a complete `s2` total width is unknown.

## 2. A *partial* annihilation result from the declared Higgs-current Lagrangian

For `L_int ⊃ -(v K11/2) h s1² - (m_f/v) h fbar f`, with an SM-like virtual Higgs of illustrative `mh=125 GeV` and fixed `Gamma_h=.0041 GeV`, the spin-summed tree-level threshold annihilation cross section for a single distinct Dirac-fermion final state is

```
lim_(v_rel→0) [sigma(s1 s1 → f fbar) v_rel] =
 N_c K11² mf²/(4 pi [(4 m1² - mh²)² + mh² Gamma_h²])
 × (1 - mf²/m1²)^(3/2),   mf<m1.
```

It follows from the `h s1 s1` vertex `-i v K11`, the fermion Yukawa `-i mf/v`, two-body phase space and `Σ_spins |ubar v|²=2(s-4mf²)`. There is **no extra initial identical-particle symmetry factor** in the per-pair `sigma v` definition. The expression uses a fixed Higgs width and a zero-relative-speed, on-shell, nonrelativistic initial state. It is *not* a thermally averaged annihilation rate, nor a quark/hadronic prediction. The actual plasma-dependent Higgs spectral function, threshold effects and higher-order corrections are outside this calculation.

For electron, muon and tau final states **only**, using Note 22's lepton masses and `K11=.001`, the partial `s1 s1` sum is `1.03679016281e-15 GeV^-2`, or `1.21027614498e-32 cm³ s^-1` using `1 GeV^-2 = 0.389379338e-27 cm²` and `c=2.99792458e10 cm/s`. The tau channel dominates this *leptonic-only* number. As a **scale comparison, not a relic-density computation**, the often-quoted `3e-26 cm³ s^-1` generic WIMP reference exceeds it by `~2.47877e6`. The actual **total** annihilation rate may be much larger because quarks/hadrons, photons, coannihilation, scalar self-interactions, thermally accessible endothermic channels and other physics have not been included. Consequently this ratio **cannot** establish thermal overproduction, the observed abundance, or exclusion.

## 3. Explicit equilibrium weights—conditional, not actual populations

Only **if** both nonrelativistic singlets share a common temperature and sufficiently rapid *chemical conversion* to maintain the equilibrium ratio (e.g. verified scattering, decays/inverse decays and/or other reactions), Maxwell–Boltzmann statistics with one real degree of freedom each give

```
x=m1/T, Delta_r=(m2-m1)/m1=0.15,
r2_eq(x) = [ (1+Delta_r)^(3/2) exp(-x Delta_r) ]
          /[ 1+(1+Delta_r)^(3/2) exp(-x Delta_r) ],
r1_eq=1-r2_eq.
```

The **illustrative temperature choices**, not a derived freeze-out temperature, `x=20` (`T=0.5 GeV`) and `x=25` (`T=0.4 GeV`) give `r2_eq=0.05784749058` and `0.02818550534`. Under that same chemical-equilibrium assumption, the standard two-species rate weighting is

```
<sigma_eff v> = r1_eq² <sigma_11 v>
              + 2 r1_eq r2_eq <sigma_12 v>
              + r2_eq² <sigma_22 v>.
```

At `x=20`, the respective weights are `0.88765135`, `0.10900232`, `0.00334633`; at `x=25`, `0.94442341`, `0.05478217`, `0.00079442`. The cross term counts the two *ordered* `1,2` and `2,1` initial-state combinations once each. **No** `sigma_12`, `sigma_22`, thermal average, conversion rate, freeze-out temperature or solution to a Boltzmann network has been computed here. The formula must not be used if conversion fails or a nonthermal cosmology is selected. Since the heavy state eventually decays to the lighter under the stated interactions, its post-freeze-out history also matters. The near-degenerate/coannihilation issue is discussed in Griest and Seckel (1991); that work does **not** validate this benchmark.

## 4. A lifetime translation, and its limited cosmological meaning

The existing Note-22 heavy-state **leptonic partial width floor** is `Gamma(s2→s1 e+e-,s1 mu+mu-) = 3.060267688e-22 GeV` for the *unperturbed* 1.5-GeV-gap point. Positivity of the other partial widths gives the exact model-conditional **proper-rest-frame** limit

```
tau2 <= hbar/Gamma_leptons = 2.150831313e-3 s (~2.15 milliseconds),
c*tau2 <= ~645 km.
```

A 645-km *proper-distance ceiling* is not evidence of cosmological stability; conversely a 2.15-ms proper-time upper bound alone does **not** establish a BBN/CMB safety statement. That requires a time-dependent abundance/production history, thermal boosts, visible and electromagnetic/hadronic energy injection, and the relevant cosmological epochs. The unknown hadronic and radiative widths can shorten this lifetime, but cannot be set to values by wishful extrapolation. This temporal bound also belongs only to the unperturbed benchmark, not every neighboring mass point.

## 5. Reproducibility and strict next calculation

`thermal_population_gate.py` implements only the leptonic threshold formula, conditional equilibrium weights and lifetime unit conversion. `test_research_note_28.py` contains 13 local algebra/regression tests. These do **not** solve the coupled Boltzmann equations or run cosmological, detector, hadronic, or collider data. For an actual dark-matter fraction `xi` or a defensible exclusion, choose and disclose a cosmological history and input masses/couplings, independently calculate a **complete, nonoverlapping** annihilation/conversion/decay network with thermal averaging, check kinetic equilibrium, solve the appropriate Boltzmann system, propagate hadronic and astrophysical uncertainties, and compare with dated abundance and direct-detection likelihoods. The four pinned Omnès files remain a separate blocker for the `s2` exclusive hadronic spectrum and full lifetime.

**Source separation:** The mass/portal benchmark, previous decay floor and direct-detection result are our conditional Notes 22 and 27. The threshold leptonic annihilation equation and numerical values are *new tree-level derivations/checks for that branch*. Methodological external references: K. Griest and D. Seckel, *Three exceptions in the calculation of relic abundances*, Phys. Rev. D **43**, 3191 (1991), https://doi.org/10.1103/PhysRevD.43.3191 ; G. Steigman, B. Dasgupta and J. F. Beacom, *Precise Relic WIMP Abundance and its Impact on Searches for Dark Matter Annihilation* (2012), https://arxiv.org/abs/1204.3622 , for why a generic `3e-26` reference is not a universal threshold; and the scalar-singlet global-fit methodology https://doi.org/10.1140/epjc/s10052-017-5113-1 . None of these sources studied or endorsed our two-singlet parameters.
