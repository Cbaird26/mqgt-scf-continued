# Research Note 27 — Stable-singlet nucleon scattering and collider/direct-detection crossing

**21 September 2026 | Public scientific-development draft; not peer reviewed.** Human author: Christopher Michael Baird. ChatGPT (ZoraASI) assisted with derivation, source-convention checks, original code, tests and drafting. The two-singlet EFT and proposed field interpretations are hypothetical; this note reports no dark-matter detection, relic-density determination or experimental exclusion.

## 1. A separate interface from the missing `s2` hadronic width

Use the restricted symmetric-vacuum, exact common-Z2 branch of Notes 22–26. At the *illustrative, unfitted* point `m1=10 GeV`, `m2=11.5 GeV`, `mh=125 GeV`, `v=246 GeV`, `kappa_PhiH=0.002`, `kappa_EH=0`, and `theta=pi/4`, the light state has `K11=0.001`. It is stable within this EFT if there is no lighter odd state, but stability **does not establish any Galactic abundance** or guarantee detector invisibility. Its leading nucleon scattering can be evaluated without the four missing Omnès files or `s2` total lifetime.

Declare the interactions `L ⊃ -(v*K11/2) h*s1^2 - (f_N*m_N/v) h*Nbar*N`, where the second term is an *additional*, conventional effective Higgs–nucleon matrix element, **not** derived from the MQGT-SCF archive. Use illustrative proton mass `m_N=0.9382720813 GeV` and `f_N=0.30`; assume a single SM-like Higgs mediator, low momentum transfer, elastic nonrelativistic scattering and no competing amplitudes. The `h*s1*s1` vertex is `-i*v*K11` (no leftover 1/2).

## 2. Tree-level formulas and a coupling-elimination identity

With standard nonrelativistic spinor normalization, `|M|≈2*|K11|*f_N*m_N^2/mh^2`. The zero-momentum spin-independent **per-nucleon** cross section is

```
sigma_SI = K11^2*f_N^2*m_N^4/[4*pi*mh^4*(m1+m_N)^2]  GeV^-2.
```

Convert by `1 GeV^-2 = 0.389379338e-27 cm^2`. Independently the identical-pair width from the same portal convention is

```
Gamma_11 = v^2*K11^2*beta/(32*pi*mh),
beta = sqrt(1-4*m1^2/mh^2),  2*m1<mh.
```

Eliminating `K11^2` produces this **model-conditional, tree-level crossing check** (for an open pair channel and nonzero portal):

```
sigma_SI/Gamma_11 =
 [8*f_N^2*m_N^4/(v^2*mh^3*(m1+m_N)^2*beta)]
 * (0.389379338e-27 cm^2/GeV^-2),
```

in `cm^2/GeV`. The result uses a common coupling; it is not an independent prediction or observation. Near `2*m1=mh`, the Higgs pair width vanishes and the displayed ratio is no longer a finite usable map. Additional light mediators, modified Higgs–nucleon couplings or interference can change this result. To obtain `Gamma_11` from a measured *branching fraction* would also require the **full Higgs width**, including all open exotic channels, not simply `Gamma_h^SM`.

## 3. Numeric example and rate/abundance caveat

For the chosen benchmark and `f_N=0.30`:

```
Gamma_11 = 4.75366954175e-6 GeV,
sigma_SI = 7.39917378137e-47 cm^2,
sigma_SI/Gamma_11 = 1.55651833102e-41 cm^2/GeV.
```

Illustratively setting `f_N=0.25` or `0.35` changes the cross section to `5.1383e-47` or `1.0071e-46 cm^2`, respectively; **these are sensitivity settings, not a statistical confidence interval**. If `xi=rho_s1/rho_totalDM` denotes an *unknown local* abundance fraction and velocity distributions are assumed identical, event rates scale as `xi*sigma_SI`. That rate-equivalent quantity is **not a change to the particle's microscopic cross section**. Neither `xi`, thermal production, coannihilation, a detector event count, an updated experimental likelihood nor exclusion status has been calculated. Actual rate forecasts need a Galactic velocity model, target-nucleus response, exposures, thresholds and detector efficiency.

The off-diagonal `K12` mediates possible *inelastic* `s1+N -> s2+N`, not a second leading elastic Higgs tree diagram. For a **free proton target at rest**, the exact laboratory incident-`s1` kinetic threshold is `[(m2+m_N)^2-m1^2-m_N^2]/(2*m_N)-m1 ≈ 18.68585 GeV`; ordinary nonrelativistic halo scattering cannot reach that threshold. Nuclei, boosted populations and extra interactions require separate analyses.

## 4. Reproducibility, sources and remaining gates

`stable_singlet_direct_detection.py` and `test_research_note_27.py` implement and regression-test these algebraic claims (12 local tests). No external detector data, Omnès file, relic density or current cross-section limit was evaluated. This *different* hadronic input `f_N` must eventually be sourced and assigned uncertainty; the four still-unavailable Omnès inputs are relevant to `s2` decay, not the leading `s1` elastic amplitude.

External sources: [1] *Status of the scalar singlet dark matter model*, EPJ C 77 (2017), https://doi.org/10.1140/epjc/s10052-017-5113-1 , Eq. (8), conventional scalar Higgs-exchange spin-independent nucleon expression and detector-response discussion; that article did **not** evaluate our two-singlet benchmark. [2] *The Higgs-portal for dark matter: effective field theories versus concrete realizations*, EPJ C 81 (2021), https://doi.org/10.1140/epjc/s10052-021-09411-2 , Sec. 2, definitions and relic-density assumptions. [3] LZ Collaboration publications, https://lz.lbl.gov/publications/ , for selecting a future **dated** experimental likelihood; no LZ comparison or exclusion is asserted here. Technical lineage: Notes 22, 24 and 26 in this unmerged draft PR. No peer review, journal submission, DOI or observational verification is claimed.
