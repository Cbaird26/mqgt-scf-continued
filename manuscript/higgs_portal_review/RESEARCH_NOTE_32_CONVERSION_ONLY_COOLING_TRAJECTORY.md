# Research Note 32 — A conversion-only cooling trajectory, not a relic-density prediction

**22 September 2026 | Public scientific-development addendum, not peer reviewed.** Human author: Christopher Michael Baird. ChatGPT (ZoraASI) assisted with the conditional derivation, independent numerical comparison, code and drafting. The restricted two-real-singlet EFT and consciousness/ethics interpretations are hypothetical; none of the numerical results here measures a field, determines dark-matter abundance, or establishes a cosmological history.

## 1. What the Note-31 eigenvalue cannot determine

Note 31 established that, for a *fixed* temperature and fixed total particle number, the leptonic decay/inverse-decay relative-population eigenvalue is `Lambda_l=Gamma_l [K1(m2/T)/K2(m2/T)] (1+q)`, with `q=n2eq/n1eq`. At the **assumed** `T=0.5 GeV`, it is only `0.00115650416636 H`. A ratio evaluated at one temperature is not a time-dependent trajectory. Note 31's quasistatic small-lag estimate becomes self-inconsistent when its purported fractional lag is much larger than one. This addendum therefore solves a deliberately narrower, well-specified time-dependent **conversion-only** example and labels its initial condition. It does **not** solve the physical coupled annihilation/conversion Boltzmann system.

Keep the prior *unfitted illustrative* parameters `m1=10 GeV`, `m2=11.5 GeV`, and the previously calculated **vacuum leptonic partial width** `Gamma_l=3.060267688e-22 GeV` for `s2 -> s1 e+e-, s1 mu+mu-`. Assume an ideal Maxwell–Boltzmann gas, a common kinetic temperature with the SM bath, zero bath chemical potentials, vacuum matrix elements unaffected by plasma, radiation domination, `M_Pl=1.2209e19 GeV` (nonreduced), **constant illustrative** energy and entropy degrees of freedom `g_*=g_*S=60`, and no number-changing reactions or additional conversion channels. Do not read constant `g_*S=60` over `T=1` to `1/3 GeV` as a physically established approximation near the QCD crossover. The total comoving odd-particle number is fixed **by construction**, so this calculation cannot determine its absolute number or relic density.

## 2. Derivation and exact formal solution

Set `x=m1/T`, `N=n1+n2`, `y=n2/N`, `q(x)=(m2/m1)^2 K2(m2/T)/K2(m1/T)` and `r(x)=q/(1+q)`. At fixed temperature, detailed balance gives the forward heavy decay rate `A(x)=Gamma_l K1(m2/T)/K2(m2/T)` and inverse events per light particle `B(x)=q(x) A(x)`. The conversion source equations, including common Hubble dilution, are

```
dn2/dt + 3H n2 = -A n2 + B n1;
dn1/dt + 3H n1 = +A n2 - B n1;
dN/dt  + 3H N  = 0;
dy/dt = -(A+B)[y-r(x)].
```

With the **additional assumed** adiabatic cooling law `dT/dt=-HT`, one has `dx/dt=xH` and therefore

```
dy/dx = -k(x)[y-r(x)],
k(x) = Gamma_l D2(x)[1+q(x)]/[x H(x)],
D2(x)=K1(m2/T)/K2(m2/T),
H(x)=sqrt(8*pi^3*g_*/90)*T^2/M_Pl.
```

If `J(x)=integral_{x0}^x k(u) du`, the exact integrating-factor solution is

```
y(x)=exp[-J(x)] y(x0)
    + integral_{x0}^x exp[-(J(x)-J(u))] k(u) r(u) du.
```

Because `k>=0` and `0<=r<=1`, this formula preserves `0<=y<=1` for every valid initial fraction and displays **initial-condition dependence** explicitly. It also shows that setting `Gamma_l=0` freezes `y` while `r(x)` still changes; a large `y/r` does not imply an excess **total** abundance. The source-free solution assumes `N` is already present, not that it was thermally produced.

## 3. One explicitly prepared illustrative trajectory

Choose the **hypothetical preparation** `y(x0)=r(x0)` at `x0=10` (`T=1 GeV`) and evolve to `x=30` (`T=1/3 GeV`). Nothing in the available model calculation establishes that this preparation or these thermal assumptions ever occurred in the early universe. At the benchmark leptonic partial width, standard fourth-order Runge–Kutta with 400 steps in `x` and an independently implemented exponential-midpoint update give the following numerical *toy fractions* (not relic fractions):

| `x` | `T` (GeV) | equilibrium `r(x)` | leptonic-only toy `y(x)` | `Lambda_l/H` |
|---:|---:|---:|---:|---:|
| 10 | 1 | 0.212042535905 | 0.212042535905 (initial condition) | not used as a tracking claim |
| 20 | 0.5 | 0.0572145986119 | 0.211998004152 | 0.00115650416636 |
| 30 | 1/3 | 0.0134099205463 | 0.211868008080 | 0.00253927800704 |

An independent `scipy.integrate.solve_ivp` calculation gives `y(30)=0.21186800807494`, versus RK4 `0.21186800807996` and exponential midpoint `0.21186800807104`. An independent `scipy.special.kve` comparison of scaled Bessel functions at `x=10,20,30` agreed with the standalone positive-integral quadrature to floating-point precision at the reported points. **These are numerical cross-checks of one truncated mathematical system, not physical validation.** No mathematically certified global integration-error interval is claimed.

The **same** toy equations yield `y(30)=0.00007184811597` if one *instead assumes* `y(10)=0`, and `y(30)=0.499490889347` if one *instead assumes* `y(10)=0.5`. This initial-condition sensitivity is a concrete reason why the leptonic partial width and mass gap cannot establish an actual post-freeze-out composition. It does not imply the actual cosmology is initial-condition sensitive once all physical reactions are included.

## 4. What is missing and what was actually checked

`conversion_history.py` implements bounded, standard-library positive-integral evaluations of scaled Bessel functions and two deterministic integration algorithms for this illustrative conversion-only equation. The local baseline trajectory and independent SciPy cross-check above were computed before a subsequent local execution outage. **No new stand-alone Note-31/32 regression test suite is claimed to have passed in this staging step.** Do not substitute `y(x)` from this deliberately fixed-total exercise into an `Omega_DM` or `xi` forecast. A physical calculation must first specify initial abundances and cosmological thermal history, calculate thermally averaged and mutually nonoverlapping `11`, `12`, `22` annihilations, hadronic/radiative `s2` decays and inverse processes, relevant `s1+SM <-> s2+SM` conversions and possible dark self-interactions, then solve the coupled comoving-number equations with variable `g_*(T),g_*S(T)` and independently evaluated hadronic uncertainties. The four pinned Omnès files have not been fully downloaded, authenticated or parsed. No total `s2` width, relic density, detection, exclusion, or empirical evidence of MQGT-SCF is inferred.

**Source provenance:** The branch's Notes 22 and 28–31 supply the illustrative masses, leptonic partial width and conditional equilibrium/cosmology conventions. The non-equilibrium coannihilation literature supplies methodological context, not this benchmark: Garny, Heisig, Lülf and Vogl, *Coannihilation without chemical equilibrium*, *Phys. Rev. D* **96**, 103521 (2017), https://doi.org/10.1103/PhysRevD.96.103521 . This new integrating-factor equation and numerical example are our explicitly delimited mathematical extension, not a result quoted from that publication. Original archival work and `main` remain untouched.
