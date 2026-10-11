# Research Note 50 — Independent antenna normalization and integrated-subtraction audit

**11 October 2026 | Scientific-development draft; not peer reviewed.** Prepared for Christopher Michael Baird with ChatGPT (ZoraASI) assistance in source comparison, derivation, symbolic integration, implementation and testing. This note checks established QCD ingredients used in the hypothetical two-real-singlet Higgs-portal calculation. It does not establish the proposed fields, a Theory of Everything, a complete physical reaction network, or a cosmological abundance.

## 1. Result and current publication lineage

Note 49 established a third-source identity for the finite virtual mass-convention term. The next question was whether the independently reconstructed real-emission normalization and the universal integrated term used in Notes 47–48 are consistent with another calculation.

Here the real matrix elements of **Gehrmann-De Ridder, Gehrmann and Glover (GGG)** [1] provide that independent normalization reference. Starting from their dimensionally regulated tree expressions, rather than importing their integrated answer, we integrate the real contributions using Euler–Dirichlet moments. The resulting Laurent expansions reproduce the published answers through epsilon-squared. Combined with the source's renormalized virtual Laurent term, the double and single infrared poles cancel exactly and the finite universal coefficient is

```
U(n_f) = 73/4 - 7 n_f/6                    [SU(3), coefficient of alpha_s/pi].
```

This independently checks **the overall three-gluon factor 1/2**, the light-pair factor 1/3 per emitted flavor, and the universal finite constant used by Note 48. These are checks of normalization and subtraction ingredients, not a new full-mass real-amplitude calculation. The source is an effective local H G^2 theory: it does not independently certify every mass-dependent helicity function or scalar-box continuation inherited from the earlier Spira-based code.

The live branch was inspected at `6674e64d4edc6165bdd40617a55e93ee31a84651`. It already contains recovered Note 48 and a separately implemented Note 49, named `RESEARCH_NOTE_49_INDEPENDENT_VIRTUAL_SCHEME_IDENTITY.md`. The attached conversation archive instead contains `RESEARCH_NOTE_49_THIRD_SOURCE_FINITE_MASS_MATCHING.md` and its 26-test implementation. Both are retained as distinct records. No old recovery patch is reapplied and no live Note-49 file is replaced. This note's inherited test count refers to the attached archive, not the alternate live implementation. A separate publication receipt records whether the new files actually reach the branch.

## 2. Four-dimensional real-emission normalization

Use the source's local interaction `L_int=-(lambda/4) H F_a^{mu nu} F_{a,mu nu}`, with arbitrary normalization lambda. It cancels in the real/Born ratios. Let `x=s12/Q^2`, `y=s13/Q^2`, `z=s23/Q^2`, where `x+y+z=1`, and define `P=1+x^4+y^4+z^4`.

The source's Born spin/color sum, **already divided by 2!**, is

```
T0 = lambda^2 (N^2-1) (1-epsilon) Q^4/4.                 [1], Eq. (3.2)
```

At epsilon=0, its three-gluon spin sum, **already divided by 3!**, reduces exactly to

```
T3 = lambda^2 g_s^2 (N^2-1) N Q^2 P/(6xyz).              [1], Eqs. (4.2),(4.3)
```

The algebra is not inferred from a soft limit: using x+y+z=1, the full source expression obeys

```
(1/3)[sum_cyclic x/(yz) + sum_cyclic xy/z + 4] = P/(6xyz).
```

The labeled phase-space ratio in four dimensions is `dPhi3/Phi2=Q^2 dx dy/(16 pi^2)`. Therefore

```
dGamma3/Gamma2_LO = [alpha_s N/(6 pi)] P/(xyz) dx dy
                  = (a/2) P/(xyz) dx dy,     N=3, a=alpha_s/pi.
```

This independently reproduces the normalization reconstructed in Note 47. There is no additional symmetry factor to insert after using the already-symmetrized source T0 and T3. A doubled real normalization leaves uncanceled infrared poles in the separate integrated test below.

For one massless emitted quark flavor, the source's Eqs. (4.8),(4.9) similarly yield

```
dGamma(g q qbar)/Gamma2_LO = (a/2) (x^2+y^2)/z dx dy.
```

Set `x=(1-z)t`, `y=(1-z)(1-t)` and integrate t. The Jacobian is `1-z` and `integral_0^1 [t^2+(1-t)^2] dt=2/3`, giving

```
dGamma(g q qbar)/Gamma2_LO = (a/3) (1-z)^3/z dz.
```

That is the factor used in the 45-real light-pair remainder. Internal loop flavors b,c are not the emitted massless flavors u,d,s.

These comparisons support the explicit normalization used by our implementation. They do **not** establish an author-confirmed erratum to Spira et al., and do not require changing the historical source text or its saved diagnostic mode.

## 3. Integrate the regulated matrix elements, not only their limits

Set `d=4-2 epsilon`. Strip the common factors `alpha_s/(2 pi)`, T0, the appropriate color/flavor factor and `(Q^2)^(-epsilon)`. The normalized real densities before the phase-space weight are

```
r_g = (2/3) [sum x/(yz) + sum xy/z + 6 - 2/(1-epsilon)],
r_q = (x+y)^2/z - 2xy/[(1-epsilon)z].
```

These follow directly from the d-dimensional spin sums in [1], divided by that paper's d-dimensional T0. The phase-space weight is `(xyz)^(-epsilon)` with the MSbar factor `exp(gamma_E epsilon)/Gamma(1-epsilon)`.

Use the simplex moment

```
D(A,B,C) = integral_triangle x^(A-1) y^(B-1) z^(C-1) dx dy
         = Gamma(A) Gamma(B) Gamma(C)/Gamma(A+B+C).
```

The moments first converge for negative epsilon; their meromorphic continuations determine the Laurent expansion. Removing a common `Gamma(1-epsilon)^3/Gamma(1-3epsilon)` from the moments, the integrated rational factors are

```
R_g(e) = 4(8e^3-15e^2+11e-3) / [3e^2(e-1)(3e-2)(3e-1)],
R_q(e) = 4(e-1) / [3e(3e-2)(3e-1)].
```

Both are multiplied by

```
H(e) = exp(gamma_E e) Gamma(1-e)^2/Gamma(1-3e),
log H(e) = sum_(n>=2) (2-3^n) zeta(n) e^n/n.
```

This reproduces, without using them as integration inputs,

```
I_g = 2/e^2 + 11/(3e) + 73/6 - 7 pi^2/6 + O(e),
I_q = -2/(3e) - 7/3 + O(e).
```

The implementation also reproduces the complete epsilon and epsilon-squared coefficients printed in [1], Eqs. (4.6),(4.11). Agreement extends beyond just the finite number needed for this NLO assembly. It is not a newly calculated NNLO decay correction.

## 4. Explicit infrared cancellation and the finite constant

The renormalized local-operator virtual term from [1], Eq. (3.3), is an external input here; its loop diagrams are not recalculated. In the same `alpha_s/(2 pi)` convention, the terms through finite order are

| Piece | double pole | single pole | finite coefficient |
|---|---:|---:|---:|
| Virtual local operator | -2 N | -11 N/3 + 2 n_f/3 | +7 N pi^2/6 |
| Integrated three gluons | +2 N | +11 N/3 | N(73/6 - 7 pi^2/6) |
| Integrated light pairs | 0 | -2 n_f/3 | -7 n_f/3 |
| Sum | 0 | 0 | 73 N/6 - 7 n_f/3 |

The cancellation is exact rational/symbolic algebra. In SU(3), conversion from `alpha_s/(2 pi)` to `a=alpha_s/pi` gives `U=73/4-7n_f/6`. There is no remaining production-specific pi-squared contribution to add to this decay constant.

For a **heavy-top local-operator reference**, adding the separate Wilson matching correction `11/2` gives `95/4-7n_f/6`. For a finite-mass loop calculation, the corresponding mass-dependent virtual function supplies that role; adding another heavy-top matching factor to it would double count.

An instructive finite check concerns terms that vanish pointwise as epsilon goes to zero. Dropping the epsilon dependence of the normalized light-pair spin sum before integration would give a finite coefficient **-8/3**, instead of -7/3. The lost term has integral

```
lim_(e->0) [-2e/(1-e) D(2-e,2-e,-e)] = +1/3.
```

The pole is unchanged, but the finite subtraction changes. Thus checking soft/collinear poles or four-dimensional amplitudes alone cannot determine every finite integrated term. The present calculation retains that term.

## 5. Five running flavors versus three retained real flavors

Our benchmark excludes real b/c-pair cuts but retains five-flavor coupling running. The source's massless antenna result alone does not make that distinction. We check the conversion separately using the one-loop zero-momentum spectator/coupling matching relation in RunDec [2], Eqs. (19),(20):

```
a_3 = a_5 [1 - (a_5/6) sum_(q=b,c) ln(mu^2/m_q^2)] + O(a_5^3).
```

Squaring the coupling in the Born gluonic current generates the relative coefficient `-(1/3) sum ln(mu^2/m_q^2)`. The three-flavor universal expression has scale coefficient `2 beta0^(3)=9/2`. Writing `L=ln(mu^2/Q^2)` and `ell_q=ln(Q^2/m_q^2)`, its re-expression is

```
U_veto = 73/4 - 7*3/6 + (9/2)L - [ell_b+ell_c+2L]/3
       = 73/4 - 7*3/6 - (ell_b+ell_c)/3 + (23/6)L.
```

This is exactly Note 48's universal coefficient. The exercise concerns the zero-momentum spectator/coupling scheme term, **not** the use of a three-flavor low-energy effective theory for hard b/c loops. The source matching formula's low-energy derivation is not a license to remove the physical b/c mass dependence at Q=20–80 GeV. The massive hard form factors remain explicit, and this algebra does not independently recalculate massive virtual spectator diagrams or omitted real heavy-pair cuts. Changing the mass convention inside this order-a^3 logarithmic term first affects the next order when accompanied by consistent Born/virtual matching.

## 6. Numerical verification in the unchanged thermal kernel

Keep the inherited, unfitted comparison inputs: `m1=10`, `m2=11.5`, `mh=125`, fixed `Gamma_h=.0041`, `v=246` in GeV, portal entries `K11=K22=.001`, `K12=-.001`, and the historical running inputs of Notes 40–49. Nothing here is a new fit or latest-measurement claim.

The independently reconstructed universal function agrees with the old function at fifteen hard-energy/scale points. Integrating that function times the **coherent** Born square in the same finite Maxwell–Boltzmann window gives, at assumed T=.5 GeV and mu=Q:

| Initial pair | Verified universal/integrated contribution [GeV^-2] |
|---|---:|
| 11 | 1.47838537130e-17 |
| 12 | 1.35667974433e-17 |
| 22 | 1.23947946601e-17 |

Only under the still-unestablished chemical-equilibrium weighting, their effective contribution is **1.464473442414904e-17 GeV^-2**. It reproduces the universal term already included in Note 48. **It is not an additional contribution and must not be added again.** The assembled Note-48 candidate is not recomputed in this note; no new change to its central value is inferred.

Hard energies remain restricted to [20,80] GeV, temperatures to [1/3,.5] GeV and the reported window to w in [0,90]. The current is not extended to physical infinity. At the central point, Q- and w-variable integration agree to at most about 2.2e-15 relatively. Separate two-dimensional integrals of the regulated tree expressions at epsilon=-1,-2,-3 agree with the Gamma-function representation within about 5.3e-15 relatively. These are numerical diagnostics, not physical precision estimates. Scale variations of the isolated universal term are in the JSON and are not confidence intervals.

## 7. Executed tests and limits of independence

The attached Note-49 package was extracted and all **53 manifest entries** verified before use. Its 253-test suite passed again. The first new 24-test suite passed. No new physical formula or assertion tolerance was changed after that run. The combined execution and any command-discovery or timeout attempts are preserved separately in the execution record and logs; incomplete attempts are not counted as passes.

The new tests cover exact source normalization, Bose symmetry, phase-space/color factors, real Laurent coefficients through epsilon-squared, both pole cancellations, the finite constant, the evanescent contribution, an intentionally doubled-normalization failure, direct two-dimensional quadrature, spectator matching, thermal reproduction, and rejection of unsupported complete-rate claims.

The completed combined run passed **277 tests: 24 new and 253 inherited**, zero failures/errors, exit code 0. The returned GitHub blob identities of the new calculator and tests match the executed local bytes: `3ad02024e3abf9200bf8e9b57bf3c206a91eebe9` and `7899f4fc82a74734ec776b07663cb520455c743f`. Blob creation alone is not publication; commit/ref verification is recorded separately.

The inherited chain is the **local 253-test archive**, not the live branch's alternate 251-test chain. Neither the original standalone Note-41 suite nor the live 45-real suite is part of this count. No whole-repository audit or external-laboratory validation is claimed. The primary virtual Laurent formula is transcribed; the real integration is performed here. The massive Born form factors, running inputs, and thermal kernel are inherited. No HDECAY, HIGLU, RunDec executable, unsafe data loader or detector likelihood is run.

## 8. What is closed and what remains

**Closed at the stated ingredient level:** the independent local-operator normalization check of the three-gluon 1/2 and light-pair 1/3 factors; the dimensionally regulated real integrations and infrared cancellation; and the independent universal finite constant, with the separate five-running/three-real-flavor bookkeeping check. Note 49's finite-virtual identity and these checks strengthen different parts of the assembled candidate without introducing another fitted adjustment.

**Not supplied:** a second complete massive real-amplitude implementation across the physical phase space, a full high-energy continuation, omitted heavy-pair cuts and their interference, a full reaction network, chemical/kinetic equilibration, or cosmological abundance. The source-normalization concern is now independently checked in its overall and universal ingredients; it should not be described as wholly unresolved, but neither should that fact be inflated into independent certification of every massive amplitude. A practical next step is a channel-by-channel collision inventory and the conversion-scattering calculation, with these checked QCD ingredients explicitly separated from remaining contributions.

No new Omnes arrays, heavier-singlet hadronic lifetime, H2 optical observable, experimental exclusion, DOI or journal submission follows. The larger corpus's distinction between interpretation, formal identities, reproducible numerical calculations and physical observation is preserved.

## Primary sources

[1] A. Gehrmann-De Ridder, T. Gehrmann and E.W.N. Glover, *Gluon-Gluon Antenna Functions from Higgs Boson Decay*, Phys. Lett. B612 (2005) 49–60, arXiv:hep-ph/0502110v1. https://arxiv.org/html/hep-ph/0502110 . Eqs. (3.2),(3.3),(4.3),(4.9) supply the matrix-element inputs; Eqs. (4.6),(4.11),(4.14) are independent integrated comparison targets. PDF printed pages 3–5 were visually inspected. Two attempts to render printed page 2 failed; its virtual formula was read from arXiv HTML. No successful local PDF download or hash is claimed.

[2] K.G. Chetyrkin, J.H. Kuhn and M. Steinhauser, *RunDec*, arXiv:hep-ph/0004189, Eqs. (1),(2),(19),(20). https://arxiv.org/html/hep-ph/0004189 . Supplies coupling-running and one-loop matching conventions, not an endorsement of applying a low-energy approximation to hard b/c amplitudes.

[3] M. Spira, A. Djouadi, D. Graudenz and P.M. Zerwas, *Higgs Boson Production at the LHC*, arXiv:hep-ph/9504378, Sec. 2.2 and Appendix C. https://arxiv.org/html/hep-ph/9504378 . Earlier amplitude/decomposition source being checked; no official erratum or author communication is claimed.

Internal sources: live branch at 6674e64d4edc6165bdd40617a55e93ee31a84651, the separately supplied local Note-49 archive, and historical Notes 45-real, 47, 48 and 49. Published QCD inputs are attributed to their authors; this note's work is the source-to-convention derivation, fresh integration, explicit tests and bounded application.
