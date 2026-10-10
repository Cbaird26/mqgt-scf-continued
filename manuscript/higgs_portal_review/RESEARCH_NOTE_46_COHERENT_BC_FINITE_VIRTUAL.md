# Research Note 46 — A finite virtual coefficient for coherent bottom/charm gluonic currents

**10 October 2026 | Scientific-development draft; not peer reviewed.** Prepared for Christopher Michael Baird with ChatGPT (ZoraASI) assistance in literature comparison, source-to-model algebra, implementation, testing and drafting. This concerns the hypothetical restricted two-real-singlet Higgs portal. It does not establish new fields, a Theory of Everything, a complete NLO gluonic decay rate, or a cosmological abundance.

## 1. Advance and two distinct Note-45 lineages

The live review branch was read at `994b7f12af99e228bda0fe0e9dcaa5dae2d8dff4`. It contains the recovered Note 44 and **RESEARCH_NOTE_45_COHERENT_BC_FINITE_REAL_RADIATION.md**, which calculates a collinear-subtracted light-pair real remainder. The conversation also contains a different, locally saved **RESEARCH_NOTE_45_COHERENT_BC_RG_AND_MATCHING.md**, which fixes scale logarithms and mass-convention differences but not the finite coefficient. These are complementary documents with a numbering collision, not interchangeable versions. A separate dated crosswalk preserves both. The local RG test file is published as `test_note45_rg_matching.py` to avoid replacing the live real-radiation test.

This note implements the previously uncalculated **mass-dependent finite virtual coefficient c_H** from Harlander and Kant [1], Eqs. (3.4)–(3.7), including coherent bottom/charm interference. The source already regularizes its virtual contribution using the infrared-singular part of real emission. The extracted c_H is therefore a convention-defined building block, not an unregularized virtual probability and not the entire finite decay coefficient requested by the RG note.

The source's production formula also contains a universal pi-squared term and a coupling-scale logarithm. We keep the latter separately for an RG check, and do not import the former as a complete decay correction. Compatible three-gluon real terms, integrated subtraction and the desired real-heavy-flavor convention remain to be assembled. No new complete NLO sum is asserted.

## 2. Inputs and published normalization

Retain the unfitted benchmark and historical comparison inputs:

```
m1=10, m2=11.5, mh=125, fixed Gamma_h=0.0041, v=246 [GeV];
K11=K22=0.001, K12=-0.001;
alpha_s(MZ)=0.1189, MZ=91.1876 GeV;
mbar_b(10 GeV)=3.610 GeV, mbar_c(3 GeV)=0.986 GeV.
```

The inherited two-loop-truncated running and continuous four/five-flavor matching at 4.163 GeV are unchanged. No new parameter fit, latest-measurement claim, or singlet-derived quark mass is made. The central prescription uses `mu=Q`, running masses in both the Yukawa and loop positions, and a common ideal Maxwell–Boltzmann temperature.

Define `r_q=mbar_q(mu)^2/Q^2`, `tau_q=1/(4r_q)`, and the normalized one-loop form factor F_q of Note 42. In [1] this is `F0^H`. The timelike continuation uses

```
beta=sqrt(1-4r),
theta=(beta-1)/(beta+1)+i0 = -4r/(1+beta)^2+i0.
```

Equation (3.7) of [1] gives the complex product `G1_q=F0^H B1^H` in logarithms, ordinary polylogarithms through order four, and one harmonic polylogarithm. Its complete expression is implemented in `hk_expression`; the printed equation was inspected directly. This is use of a published exact mass-dependent formula, not a new two-loop diagram calculation.

A critical convention check is [1], printed page 3: its quark mass is already MSbar. Equations (2.7) and (3.6) imply, with `D_q=m_q*d/dm_q`,

```
F0 C2 = D_q F_q,
B2 = 2 C2,
G_MS,q = G1_q + 2 D_q F_q ln(mu^2/mbar_q(mu)^2).
```

There is no additional Yukawa conversion to perform. Also, [1] defines B at the cross-section level, so another interference factor of two would double count its normalization.

For fixed real Yukawa probe multipliers, form

```
A = kappa_b F_b + kappa_c F_c,
G = kappa_b G_MS,b + kappa_c G_MS,c,
V_bc = Re(G A*).
```

Away from A=0 this equals `|A|^2 Re(G/A)`, the source's normalized coefficient times the Born square. The additive expression stays finite at cancellations. Its components are

```
V_bb = Re(G_b F_b*),
V_cc = Re(G_c F_c*),
V_interference = Re(G_b F_c* + G_c F_b*).
```

Thus the signed mass-dependent current contribution is

```
Delta S_virtual(Q,mu) = Q^2/9 * [alpha_s(mu)/pi]^3 * V_bc.
```

It includes neither the source's universal production pi-squared term nor the full real-emission correction. Interference and finite subtracted terms need not be positive separately.

## 3. Numerical implementation of the additional special function

The harmonic polylogarithm in Eq. (3.7), with its standard kernels, has the defining representation

```
H(1,0,-1,0;theta)
 = integral_0^theta dt/(1-t) [-ln(t) Li2(-t)+2 Li3(-t)].
```

Expanding the convergent integrand gives the separately derived evaluation formula

```
H = sum_(j=2)^infinity theta^j/j * {
 (1/j-ln(theta))*sum_(n=1)^(j-1) (-1)^n/n^2
 + 2*sum_(n=1)^(j-1) (-1)^n/n^3 }.
```

The production calculation uses 48 terms on `|theta|<=0.1`; ordinary polylogarithms use their defining convergent series on the same domain. These are special-function evaluations, not a truncation of the physical mass dependence. The hard benchmark lies inside this domain. Threshold behavior outside the declared domain is rejected.

`virtual_reference.py` instead evaluates the one-dimensional H integral and polylogarithms with mpmath at high precision. It shares the rational published coefficient expression with the production implementation. Accordingly this is an independent **numerical special-function evaluation**, not an independent transcription of every rational coefficient or another QFT derivation. Additional checks include the derivative of H, the defining-series remainder, the source's mass derivative, and the heavy-mass limit c_H -> 11/2. The below-threshold heavy-limit check uses the reference evaluator only, not an extension of the production domain.

## 4. Matching and scale checks

The pole/MSbar relation through first order is `M=mbar(1+a*d)`, where `a=alpha_s/pi` and `d=4/3+ln(mu^2/mbar^2)`. Since the full Born square depends on both mass positions, its scheme shift is `sum_q d_q D_q |A|^2`, as derived independently in the local RG Note 45.

At the same numerical mass argument, the corresponding pole-convention finite numerator is

```
G_OS,q = G1_q - (8/3) D_q F_q.
```

The difference `Re[(G_MS-G_OS) A*]` is exactly `sum_q d_q D_q |A|^2`. This identity checks the conversion direction and prevents converting already-running Yukawas twice. A physical prescription change must change the Born masses and hard terms together; the isolated shift is not an added final state.

The separately identified universal coupling-scale term is

```
2 beta0 L |A|^2,  beta0=23/12,  L=ln(mu^2/Q^2).
```

Together with the explicit mass logarithms, its slope is the RG Note-45 condition `K=2 beta0 B+(D_b+D_c)B`, where `B=|A|^2`. Synthetic small-coupling tests show that scheme-reexpansion and residual-scale differences start at absolute order a^4. This fixes normalization and running consistency, not the missing real/subtraction completion.

## 5. Finite-window thermal results

Insert the signed current in the unchanged spectral normalization and unequal-mass thermal kernel:

```
sigma_ij(s) = Kij^2 s Delta S_virtual(sqrt(s))
              /[8*pi*D_h(s)*sqrt(lambda_ij(s))],
D_h(s)=(s-mh^2)^2+(mh Gamma_h)^2,
lambda_ij(s)=[s-(mi+mj)^2][s-(mi-mj)^2].
```

This equation represents the contribution of a finite virtual coefficient, not a standalone positive scattering probability. Hard energies remain Q in [20,80] GeV, scales mu/Q in [1/2,2], and temperatures T in [1/3,0.5] GeV. Reported values integrate only `w=Q/T-(mi+mj)/T` in [0,90]. No physical infinity-domain integral or bound above Q=80 is claimed.

At assumed T=0.5 GeV and mu=Q:

| Incoming pair | bb virtual piece | cc virtual piece | bc interference | Coherent finite virtual piece |
|---|---:|---:|---:|---:|
| 11 | 1.19444e-17 | 3.60285e-19 | 3.54170e-18 | **1.58464e-17** |
| 12 | 1.14538e-17 | 3.30402e-19 | 3.39702e-18 | **1.51812e-17** |
| 22 | 1.09085e-17 | 3.02280e-19 | 3.22887e-18 | **1.44396e-17** |

All entries are in GeV^-2. Extra digits in the machine output document numerical reproduction, not physical precision. Only under the still-unestablished chemical-equilibrium reduction do the inherited ideal-gas weights combine these into

```
bb: 1.18880581129e-17,
cc: 3.56871389826e-19,
bc: 3.52506922579e-18,
coherent finite virtual: 1.57699987285e-17 [GeV^-2].
```

The same implementation reproduces the previous conditional LO b/c-square reference `2.65726141679e-17 GeV^-2`. Comparing the virtual piece with that reference is not a physical NLO enhancement claim, because the remaining real and subtraction terms have not been assembled.

For the explicitly labeled **virtual plus universal coupling-scale-log** diagnostic, the effective values at mu/Q=1/2,1,2 are respectively `7.68710e-18`, `1.57700e-17`, `1.56805e-17 GeV^-2`. The central scale log is zero. A separate auxiliary-pole prescription gives a virtual-only central piece `-6.15910e-19 GeV^-2`. The sign change illustrates the non-observable nature of an isolated convention-dependent piece; it is not a negative event rate or a confidence interval for the completed physical rate.

No new sum with the local RG correction, live real-radiation remainder or Note-44 partial upgrade is advertised as complete. Those pieces require a compatible subtraction and cut convention.

## 6. Executed verification and limits

The first new suite passed **32 tests, zero failures/errors**. The combined suite passed **171 tests: 32 new, 30 from the local RG Note 45, 33 from Note 44, 28 from Note 43, 26 from Note 42 and 22 from Note 40**. The new tests cover high-precision special functions, published normalization, coherent algebra, mass/scale matching, numerical integration variables, quadrature order, window changes, invalid domains and explicit refusal to return a completed NLO rate.

The live real-radiation Note-45 suite and the original standalone Note-41 suite are **not included** in this count. Their existence is not a claim of execution in this step. This is not a whole-repository audit or empirical validation.

All twelve component/pair integrals were checked in invariant Q and scaled w; their largest absolute difference was about `5.55e-32 GeV^-2`. Generalized Gauss-Laguerre, node-order, finite-window and lower-temperature comparisons passed. These are numerical diagnostics, not rigorous physical uncertainty bounds. An early exploratory high-precision heavy-limit call exceeded its time budget; targeted reference checks and all final tests completed. No successful external HIGLU/HDECAY download or executable run is claimed.

The accompanying execution record gives hashes, commands, versions and test logs. New source identities are `fd2af360cc4eae7a838f2d93a16c003627b533a5` (calculator), `00eda0258365a8cdb7d2e8bd8d210d694f40630e` (reference evaluator), and `007c1d4331386c78a0bf5a822b195fb00282c8bd` (new tests). The original local RG source and renamed test retain their bytes; the dated crosswalk separates historical publication statements from current recovery.

## 7. Next assembly

The mass-dependent finite virtual function is now explicit rather than an unknown callback. The coherent three-gluon real remainder and compatible integrated subtraction are still needed, along with matching the real-heavy-flavor convention. The live light-pair remainder and this c_H use separately stated decompositions; adding them without that matching would not close the calculation.

The broader reaction network still needs the remaining channels, conversion scatterings, kinetic and cosmological assumptions before a coupled abundance calculation. No new Omnes arrays, heavier-singlet hadronic width or lifetime, H2 optical observable, detector exclusion, DOI or empirical confirmation follows. Historical notes, archive PDFs and main are not rewritten by this addendum.

## Primary sources

[1] R. V. Harlander and P. Kant, *Higgs production and decay: Analytic results at next-to-leading order QCD*, JHEP 12 (2005) 015, arXiv:hep-ph/0509189v1, printed page 3 and Eqs. (2.7),(3.4)–(3.7). https://arxiv.org/pdf/hep-ph/0509189 . The source supplies the exact virtual coefficient and its mass convention, not a new singlet model or a complete decay calculation reproduced here.

[2] M. Spira, A. Djouadi, D. Graudenz and P. M. Zerwas, *Higgs Boson Production at the LHC*, arXiv:hep-ph/9504378v1, Sec. 2.2 and virtual/real decomposition. https://arxiv.org/html/hep-ph/9504378 . Used to separate the mass-dependent coefficient, universal terms, decay assembly and flavor definitions.

[3] K. G. Chetyrkin, J. H. Kuhn and M. Steinhauser, *RunDec*, arXiv:hep-ph/0004189, RG coefficients and mass-conversion convention. https://arxiv.org/abs/hep-ph/0004189 . Running code is inherited; no external executable is run.

Internal lineage: live Notes 40–45 at 994b7f12af99e228bda0fe0e9dcaa5dae2d8dff4, plus the separately saved RG Note 45. The special-function evaluation, convention checks and source-to-model application are developed here. These sources do not endorse the hypothetical singlets or consciousness/ethics interpretations.
