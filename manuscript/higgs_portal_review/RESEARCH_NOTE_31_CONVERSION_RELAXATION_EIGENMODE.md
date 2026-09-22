# Research Note 31 — From inverse-decay event counts to the chemical relaxation eigenmode

**22 September 2026 | Public scientific-development addendum, not peer reviewed.** Human author: Christopher Michael Baird; ChatGPT (ZoraASI) assisted with algebra, limited source review, numerical checks and drafting. This is a hypothetical restricted two-singlet EFT, not a dark-matter discovery, a measured abundance, or a computed cosmological history.

## 1. A distinction left open in Note 29

Note 29 reports, under a deliberately assumed radiation era with `T=0.5 GeV` and `g_*=60`, a *leptonic inverse-decay event rate per equilibrium light singlet* of `6.61689217e-5 H`. It **explicitly says this is not a chemical relaxation eigenvalue**. Comparing each light-particle event count separately to `H` can be excessively demanding when the equilibrium heavy population is small: the relevant question for a conversion-only two-state system is how rapidly a perturbation of its *relative population* relaxes. Here we derive that eigenvalue, without computing the missing hadronic and scattering conversion channels.

All numerical inputs are the *unfitted illustrative benchmark* of Notes 22, 28 and 29: `m1=10 GeV`, `m2=11.5 GeV`, `Gamma_l(s2->s1 e+e-, s1 mu+mu-)=3.060267688e-22 GeV`. Assume one common kinetic temperature, Maxwell–Boltzmann ideal-gas equilibrium densities, a zero-chemical-potential Standard Model bath, inverse reactions related by detailed balance, the vacuum leptonic decay matrix element without plasma corrections, and no number-changing reactions when isolating this eigenmode. The source Bessel conventions are `q(T)=n2eq/n1eq=(m2/m1)^2 K2(m2/T)/K2(m1/T)` and `D2(T)=K1(m2/T)/K2(m2/T)`; the thermally averaged forward decay rate per heavy particle is `A_l=Gamma_l D2`.

## 2. Exact conversion-only two-state relaxation at fixed temperature

At fixed temperature and fixed total `N=n1+n2`, write the leptonic decay/inverse-decay number-density equations, omitting common Hubble dilution (which cancels in the fraction),

```
(d n2/dt)_conv = -A_l*n2 + A_l*q*n1,
(d n1/dt)_conv = -(d n2/dt)_conv.
```

In the vector `(n1,n2)` the conversion matrix is `A_l*[[-q,1],[q,-1]]`, with eigenvalues `0` (conserved total) and `-A_l*(1+q)` (relative-population relaxation). Defining `y=n2/N`, `r_eq=q/(1+q)` gives **exactly** at constant `T` and `N`:

```
dy/dt = -Lambda_l*(y-r_eq),
Lambda_l = Gamma_l * D2 * (1+q)
         = (forward decays per heavy) + (inverse events per light).
```

Thus the inverse event count `q*Gamma_l*D2` is only one term of `Lambda_l`; demanding it alone exceed `H` is **not** a necessary general criterion for this simplified mode. This refines, rather than contradicts, Note 29's explicitly limited statement. The decays/inverse decays still fail even the less stringent `Lambda_l >= H` comparison at the chosen point.

## 3. Illustrative numbers and two DIFFERENT timescale questions

At *assumed* `T=0.5 GeV`, `g_*=60`, `M_Pl=1.2209e19 GeV` (nonreduced), fixed effective radiation degrees of freedom and radiation domination, the same ideal-gas Bessel conventions yield:

```
q=0.0606867676649; r_eq=0.0572145986119; D2=0.938176870693;
H=2.63320146442e-19 GeV;
Gamma_l*D2/H=0.001090335245;
q*Gamma_l*D2/H=0.00006616892167;
Lambda_l/H=0.00115650416636.
```

If *all conversion* could be represented by a temperature-independent effective decay width with the same thermal factor and equilibrium bath, the width that would give `Lambda=H` **at this one assumed temperature** is `Gamma_equiv,H=H/[D2*(1+q)]=2.64613633e-19 GeV`, about `865` times the already calculated leptonic partial width. The corresponding additional **equivalent conversion width**, conditional on this common thermalization assumption, would be `2.64307606e-19 GeV`. These figures are **requirements within a simplified rate parametrization**, *not* computed hadronic widths, a physical bound on the actual total vacuum width, or a relic-density constraint. The separate hypothetical criterion `inverse events per light = H` instead demands about `15113*Gamma_l`, illustrating why the two tests must not be conflated.

Even `Lambda >= H` is only a rough timescale comparison, not a guarantee of close chemical tracking: the *target* equilibrium fraction changes as the bath cools. **Additionally** assume adiabatic radiation cooling `d ln T/dt=-H`, which requires an approximately constant entropy-effective degree count over the illustrative interval; this approximation is not certified near the QCD crossover. Differentiating the ideal-gas `q(T)` gives

```
d ln q / d ln T = z2*K1(z2)/K2(z2) - z1*K1(z1)/K2(z1), z_i=m_i/T,
|d ln r_eq/dt|/H = (1-r_eq) * d ln q/d ln T = 2.81786005815
```

at `T=.5 GeV`. If no other source changes the total population or fraction, the moving-target deviation `delta=y-r_eq` obeys `d delta/dt = -Lambda_l*delta - d r_eq/dt`. The **quasistatic estimate** for a small fractional lag is `|delta|/r_eq ≈ |d ln r_eq/dt|/Lambda_l`; with the tiny leptonic-only rate this formula yields about `2437` and is **outside its own small-lag regime**, so it must NOT be treated as an actual population fraction or solution. A width giving `Lambda=|d ln r_eq/dt|` in the identical simplified decay parametrization would be `7.45644187e-19 GeV`, about `2437*Gamma_l`; close tracking would require a still larger rate. No freeze-out temperature or thermal-history solution follows.

The two-state conversion-only eigenmode is not the full Boltzmann system. Hadronic/radiative decays, `s1+SM <-> s2+SM` scatterings, dark-sector number-changing processes, annihilations, evolving `g_*S`, plasma dispersion and initial conditions can alter the relevant eigenvalues and time-dependent forcing. Do **not** substitute a missing zero-temperature total decay width into the formula without demonstrating its thermal detailed-balance partner and in-medium corrections.

## 4. Source and reproducibility boundary

These values are direct algebraic consequences of Note 29's *conditional* benchmark rates plus a **new two-by-two conversion operator**. The displayed Bessel and derivative numbers were checked numerically against `scipy.special.kv`; this is a local arithmetic cross-check, not an external physical validation. At the time of staging, the container stopped accepting further commands while preparing a standalone regression script, so **no new Note-31 test file is claimed to have passed or been uploaded**. The source four Omnès inputs are still not downloaded, authenticated or parsed; no hadronic width, total lifetime, chemical-equilibrium conclusion, relic abundance, or detector exclusion is claimed.

Methodological context: Garny, Heisig, Lülf and Vogl, *Coannihilation without chemical equilibrium*, Phys. Rev. D **96**, 103521 (2017), https://doi.org/10.1103/PhysRevD.96.103521 , shows why coupled chemical-equilibration assumptions need checking; this publication does **not** study or endorse our benchmark. Notes 22, 28 and 29 are the source for our *illustrative* masses, leptonic partial width and radiation-era conventions. Original archive and `main` remain unchanged.