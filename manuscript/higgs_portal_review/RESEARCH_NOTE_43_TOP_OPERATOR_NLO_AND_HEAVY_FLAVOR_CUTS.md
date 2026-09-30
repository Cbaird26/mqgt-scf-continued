# Research Note 43 — NLO top-operator current, massive real cuts, and the limits of a gluon upgrade

**30 September 2026 | Public scientific-development addendum; not peer reviewed.** Human author: Christopher Michael Baird. ChatGPT (ZoraASI) assisted with source comparison, derivation, implementation, numerical checks and drafting. This concerns the hypothetical restricted two-real-singlet Higgs-portal model. It is not a validated Theory of Everything, complete QCD calculation, field observation or relic-density result.

## 1. What the next published ingredient actually supplies

The live review branch was read at `384d2773bc857a171fd5b00ca83d5b6c239e9315`. Note 42 supplies the leading, coherent top/bottom/charm-loop two-gluon contribution. Here the next-to-leading-order (NLO) correction is calculated for the **top-induced operator-square sector**, including an explicit separation of real heavy-quark final states. No old note or source module is changed.

There is an important scope distinction in the external source. Wang and Wang [1] give higher-order top-operator and mixed-operator terms, but keep the bottom/charm-operator-square term at its leading nonzero order, Eq. (7). Its smallness in their on-shell-Higgs example does not establish smallness at our different invariant masses. Using Note 42's unchanged amplitudes and assumed equilibrium weights, the coherent bottom/charm-loop-square group is

```
weighted |F_b+F_c|^2 contribution = 2.65726141679e-17 GeV^-2,
weighted |F_t+F_b+F_c|^2 total    = 6.23608188693e-17 GeV^-2,
ratio                           = 0.426110731862.
```

Thus this group accounts for **42.61% of the chosen leading-order gluon result**. This is an amplitude-group ratio inside that conditional calculation, not a measured branching fraction or a fraction of all annihilation. It includes bottom-charm interference. It prevents us from importing a claim of complete NLO accuracy while leaving this group's NLO correction unspecified. The top-bottom/top-charm NLO interference is also not implemented in this note.

Operator labels in [1] must not be confused with incoming species labels: its `C1*C1` denotes a top-induced operator sector, not specifically the initial pair `s1*s1`. Every operator sector contributes to each of the three incoming pairs through the corresponding portal coupling.

## 2. Source-matched top-induced correction

Retain the unfitted benchmark and frozen historical inputs of Notes 40–42:

```
m1=10, m2=11.5, mh=125, Gamma_h=0.0041, v=246 [GeV];
K11=+0.001, K12=-0.001, K22=+0.001;
alpha_s(MZ)=0.1189, MZ=91.1876 GeV;
mbar_b(10 GeV)=3.610 GeV, mbar_c(3 GeV)=0.986 GeV.
```

Keep the inherited two-loop-truncated running and continuous matching prescription. These are not latest parameter determinations or predictions of the singlet theory.

Let `a=alpha_s(mu)/pi`, `Q=sqrt(s)`, and `L=ln(mu^2/Q^2)`. Integrating out the top at leading power in `Q^2/M_t^2` gives an operator `O_g=(H/v) G^a_mn G^a_mn`, with Wilson coefficient in our sign convention

```
C_g = -(a/12) [1+(11/4)a] + O(a^3).
```

The coefficient is supplied by [2], Eq. (31). Squaring it contributes **11/2**, not 11/4, to the relative NLO rate coefficient. This matching contribution must be combined with the real/virtual operator matrix element; the Wilson coefficient alone is not the full NLO rate.

With three massless real-splitting flavors `n_l=3` (u,d,s) but five flavors in the running coupling, Eq. (4) of [1] plus the matching term yields

```
E_veto = 95/4 - 7*n_l/6 - (l_b+l_c)/3 + (23/6)*L,
l_q    = ln(Q^2/m_q^2),
S0     = alpha_s(mu)^2 Q^2/(9*pi^2),
S_top,veto^NLO = S0 [1+a E_veto].
```

The retained cuts are `gg`, `ggg`, and `g u ubar / g d dbar / g s sbar`, together with their required virtual terms. Real `g b bbar` and `g c cbar` cuts are excluded from this convention; massive b/c virtual loops remain. “Veto” is only a partonic final-state definition here, not an experimental tagging or jet-veto calculation.

The central numerical prescription uses inherited `mbar_q(mu)` in the mass-dependent NLO coefficients. The source states them with on-shell kinematic masses. In this top-operator-square sector the Born current is independent of the b/c masses, so an O(a) mass conversion changes the O(a^3) current first at O(a^4). A separate calculation uses Note 42's frozen auxiliary one-loop pole estimates. Neither prescription defines a physical hadron threshold at twice a running mass, and neither is used for the low-energy singlet decay. Finite-top NLO power corrections are not included.

## 3. Calculate the excluded massive real cuts rather than changing a flavor count

The following is our phase-space derivation from the local operator, not an additional result attributed to Eq. (4). Let `r=m_q^2/Q^2` and `z=q_pair^2/Q^2`. For the **top-operator amplitude alone**,

```
Gamma(O_g -> g q qbar) / Gamma(O_g -> gg)_LO = (a/3) I(r),
I(r) = integral_(4r)^1 dz/z (1-z)^3 sqrt(1-4r/z) (1+2r/z).
```

The normalization follows from the conserved vector-current trace, factorized three-body phase space and `T_R=1/2`. In the quark-pair rest frame, the transverse spin trace has angular factor

```
1+cos(theta)^2 + (4m_q^2/q_pair^2) sin(theta)^2.
```

Its angular integral is `(8/3)(1+2m_q^2/q_pair^2)`. The ratio includes the identical-two-gluon factor in the Born denominator. No extra color-three or identical-final-state one-half is applied. The tests independently integrate the squared local-operator amplitude and both two-body phase-space factors to check this normalization.

With `B=sqrt(1-4r)`, elementary integration gives

```
I(r) = (1-18r^2+8r^3) ln[(1+B)/(1-B)] - (7/2+r) B^3.
```

One derivation sets `beta=sqrt(1-4r/z)` and integrates the rational function

```
beta^2 (3-beta^2) (1-beta^2-4r)^3 / (1-beta^2)^4
```

from zero to `B`. Both this representation and logarithmic-z quadrature independently check the closed form. Close to `B=0`, the implementation uses a nonsingular fixed-interval quadrature rather than subtracting nearly equal closed-form terms. The mathematical threshold behavior is `I~(16/105)B^9`; this is not a QCD threshold-resummation claim.

Including the two massive real cuts gives the top-induced inclusive coefficient

```
E_inclusive = E_veto + [I(r_b)+I(r_c)]/3,
S_top,inclusive^NLO = S0 [1+a E_inclusive].
```

This is inclusive over the specified top-induced partonic cuts, not over every Higgs-current interaction. The small-mass identity

```
I(r) = ln(1/r) - 7/2 + 18r + O(r^2 ln r)
```

shows explicitly how the real heavy-flavor cuts cancel the mass logarithms of the vetoed result. Consequently

```
E_inclusive -> 95/4 - 7*5/6 + (23/6)L
```

as both masses become small. This recovers the independently published five-flavor heavy-top coefficient in [2], Eq. (26). Simply replacing `n_l=3` by five in the vetoed formula would not produce this massive-cut calculation.

## 4. Thermal results for the same illustrative masses

Insert the new current in the unchanged Note-40/42 thermal kernel:

```
sigma_ij(s) = Kij^2 s S(sqrt(s)) / [8*pi*D(s)*sqrt(lambda_ij(s))],
D(s)=(s-mh^2)^2+(mh*Gamma_h)^2,
lambda_ij(s)=[s-(mi+mj)^2][s-(mi-mj)^2].
```

The ideal Maxwell–Boltzmann average uses the finite window `w=Q/T-(mi+mj)/T` in `[0,90]`. The hard domain is `Q in [20,80] GeV`, temperatures `[1/3,0.5] GeV`, and scales `mu/Q in [1/2,2]`. The pair rates assume a common thermal momentum distribution; they do not require the further one-equation chemical-equilibrium reduction.

At the **assumed** `T=0.5 GeV` and central `mu=Q`, the top-operator-square rates are:

| Incoming pair | LO heavy-top reference | NLO excluding real b/c pairs | Added real b/c cuts | NLO including real b/c pairs |
|---|---:|---:|---:|---:|
| 11 | 3.69671e-17 | 6.73128e-17 | 2.28824e-18 | 6.96010e-17 |
| 12 | 4.20495e-17 | 7.58887e-17 | 2.73893e-18 | 7.86276e-17 |
| 22 | 4.71046e-17 | 8.43201e-17 | 3.21142e-18 | 8.75316e-17 |

All entries are in `GeV^-2`. The LO reference reproduces Note 42's **heavy-top-only** result, not its coherent three-loop-flavor result.

Only under the still-unestablished chemical-equilibrium reduction, applying Note 39's full ideal-gas equilibrium weights gives

```
LO top-operator effective reference:       3.75486248578e-17 GeV^-2,
NLO top-operator effective, b/c vetoed:     6.82936482528e-17 GeV^-2,
NLO top-operator effective, b/c included:   7.06335310505e-17 GeV^-2.
```

The last number is **88.11% larger than its own top-only LO reference**. It is not an 88% correction to all gluon loops, to the complete annihilation network, or to the earlier lepton-plus-quark result. The included real heavy-flavor cuts account for 3.31% of this NLO top-sector result.

The separately known, veto-convention NLO increment is `3.07450233950e-17 GeV^-2`. Adding only this increment to Note 42's coherent LO result would give `9.31058422643e-17 GeV^-2`, but the code explicitly labels that operation a **partial upgrade, not a complete coherent NLO prediction**. It does not duplicate the already present LO top amplitude.

## 5. Uncertainty and bookkeeping boundaries

The conditional top-induced inclusive effective result varies as follows:

| Prescription | Effective top-sector rate [GeV^-2] |
|---|---:|
| mu=Q/2, central mass prescription | 8.71159e-17 |
| mu=Q, central mass prescription | 7.06335e-17 |
| mu=2Q, central mass prescription | 5.81376e-17 |
| mu=Q, auxiliary pole-mass prescription | 7.08036e-17 |

These are sensitivity comparisons, not confidence intervals. The small 0.24% difference in the last row does not establish small physical uncertainty: this is only the top-operator sector, and scale dependence, top-power corrections, input uncertainty and the other amplitude sectors remain.

The new top-induced `g b bbar` and `g c cbar` terms share final states with Yukawa-induced amplitudes. They are separately identified **coupling-sector contributions**, not disjoint experimental channels. Their interference with direct quark-current amplitudes must be included at the appropriate order before claiming a complete rate. Similarly, an inclusive published width cannot be added on top of its own already-counted real cuts.

The massless u/d/s splitting contributions in the top sector do not supply direct light-quark Yukawa currents. The source's higher-order mixed top–b/c term, higher-order coherent b/c-square term, and consistent remaining cuts still need calculation. A single universal multiplicative correction applied to `|F_t+F_b+F_c|^2` would assume those results rather than derive them.

## 6. Executed numerical controls and provenance

The real-cut normalization is checked with explicit three-body phase space; the closed integral is checked with two independent variables and 60-digit arithmetic. The inclusive massless limit reproduces [2]; the scale logarithm agrees with five-flavor running; synthetic small-coupling checks verify that residual scale and mass-scheme effects begin at the next omitted order. These checks concern formulas, not experimental observations.

The thermal contributions agree between the invariant-Q and scaled-w integrations and with generalized Gauss–Laguerre quadrature within the test tolerances. Window and lower-temperature checks are included. A positive analytic current cap of `8.161 GeV^2` on the declared hard/scale domain bounds the omitted interval from the `w=90` endpoint to `Q=80` by at most approximately `5.45e-43`, `4.84e-43`, and `4.29e-43 GeV^-2` for pairs 11/12/22. It does not bound the unknown physical spectrum above 80 GeV. Displayed floating-point cap values are not directed-rounding certificates.

New GitHub blob identities match the locally executed source bytes:

```
top_operator_nlo.py:       cf2c5f0fa09802330dfdf401e15ed1c1d78b9ab3
test_research_note_43.py:  bfbf2cfc0e3cf83fdb443b0f5e561a2c057f6d61
```

After the matching GitHub blob objects were created, the matched local suite ran **76 tests: 28 new, 22 inherited from Note 40 and 26 inherited from Note 42; zero failures/errors, exit code 0**. The same objects are selected for the branch commit. The first run also passed; no test tolerance or physical formula needed correction after it. The original separate Note-41 suite was not rerun; its unmodified module and selected results are checked by inherited Note-42 tests. This is not a claim to have tested the entire repository.

```
python -m unittest -v test_research_note_40.py test_research_note_42.py test_research_note_43.py
python top_operator_nlo.py
```

The execution record preserves hashes and software versions; the companion package contains all required modules, full results and test logs. No external HDECAY/RunDec program, unsafe data loader, full Boltzmann evolution, detector likelihood or Omnes input was run.

## 7. Next calculation

The next higher-order tasks are the mixed top–bottom/charm sector and the coherent bottom/charm-square correction with compatible final-state cuts. They should be combined at their stated perturbative orders before labeling a gluonic result complete. The conversion network and cosmological inputs remain separate requirements for abundance evolution.

No low-energy Omnes data were obtained in this step. The compressed heavy-singlet hadronic width and lifetime are unchanged. There is no new abundance, H2 optical signal, DOI, journal submission or empirical validation. Historical notes, `main`, and the frozen verification archive are unchanged by this addendum.

## Primary references

[1] J. Wang and Y. Wang, *Analytic Result of Higgs Boson Decay to Gluons with Full Quark Mass Dependence*, arXiv:2503.22169v2 (2025), Eq. (4), Eq. (7), Table 1 and the final-state-cut discussion. https://arxiv.org/html/2503.22169v2 . The paper's on-shell numerical predictions and higher-order mixed coefficient are not substituted into our benchmark.

[2] M. Spira, A. Djouadi, D. Graudenz and P. M. Zerwas, *Higgs Boson Production at the LHC*, arXiv:hep-ph/9504378v1 (1995), Eqs. (26),(31) and Sec. 2.2. https://arxiv.org/html/hep-ph/9504378 . Supplies the independent heavy-top matching coefficient and inclusive massless limit.

[3] Internal lineage: Notes 39–42 and their source files at `Cbaird26/mqgt-scf-continued@384d2773bc857a171fd5b00ca83d5b6c239e9315`. The phase-space algebra and source-to-model application are developed here; the QCD ingredients are established literature, not evidence for the hypothetical field interpretation.
