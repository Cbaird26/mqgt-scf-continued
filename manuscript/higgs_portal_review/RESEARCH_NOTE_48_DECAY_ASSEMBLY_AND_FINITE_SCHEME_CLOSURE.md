# Research Note 48 — Common decay assembly and a finite mass-convention closure test

**10 October 2026 | Scientific-development draft; not peer reviewed.** Prepared for Christopher Michael Baird with ChatGPT (ZoraASI) assistance in source comparison, algebra, numerical implementation, tests and drafting. This is a calculation within the hypothetical restricted two-real-singlet Higgs portal. No new field, validated Theory of Everything, complete physical annihilation rate, or relic abundance is established.

**Publication status:** Saved locally in this conversation. The attempted GitHub blob write returned `Resource not found`; subsequent discovery exposed no code-creation action. The installed GitHub integration was rediscovered but no working code-upload alternative was obtained. No remote blob, commit or ref update succeeded in that attempt. An additions-only patch is supplied. A later publication receipt records separately whether a discussion comment succeeds.

## 1. Main finding and correction to the preceding interpretation

The live review branch was checked at `94093121a33a3486a8c5e74c0a1fbcf496654d74`, containing Note 47. The attached Note-47 package was extracted and all 36 entries of its manifest were verified before using its unmodified modules.

This note attempts the common decay assembly of the virtual coefficient, three-gluon remainder, light-pair remainder, and universal/integrated subtraction. It introduces an important cross-check that the separate component tests did not perform: replace one loop by a heavy-top probe and compare the assembled top–bottom/charm interference with the different closed coefficient already implemented in Note 44 from Wang and Wang [1].

The **literal assembly of Note 46's virtual convention does not close that comparison**. Its discrepancy follows a specific Born-amplitude mass derivative. Adding the finite matching term `Delta G_q=(8/3) D_q F_q` reconciles the independently represented mixed coefficients at all fourteen flavor/checkpoint comparisons performed here. This is the finite term associated with the one-loop `4/3` mass-boundary conversion, not a fitted overall correction factor.

Consequently, Note 46's statement that its source's mass label by itself justified the common MSbar interpretation was too strong. Its recorded numerical block remains a reproducible *literal source-convention block*, but it must not be used unchanged as the matched virtual contribution in this assembly. This addendum keeps the old source, tests and results intact, returns both literal and matched constructions, and records the finite difference explicitly.

There is no author-confirmed erratum. The assignment of the discrepancy to a particular published convention still merits independent source/code review. Note 47's separately reconstructed three-gluon normalization also remains a review item. The assembled numbers below are therefore **source-matched candidate results**, not a claim that every outstanding normalization or physical-model question has been settled.

## 2. Inputs and the common partonic definition

Keep all inherited unfitted comparison inputs:

```
m1=10, m2=11.5, mh=125, fixed Gamma_h=0.0041, v=246 [GeV];
K11=K22=0.001, K12=-0.001;
alpha_s(MZ)=0.1189, MZ=91.1876 GeV;
mbar_b(10 GeV)=3.610 GeV, mbar_c(3 GeV)=0.986 GeV.
```

The inherited two-loop-truncated running and continuous four/five-flavor matching at 4.163 GeV remain unchanged. These are historical fixed inputs, not latest measured values or parameters predicted by the singlet model. The central prescription uses the running mass in both the Yukawa coupling and loop propagators at `mu=Q`.

Retained partonic cuts are `gg`, `ggg`, and `g q qbar` for massless emitted `q=u,d,s`, with the virtual terms needed for this convention. Real bottom/charm final-state cuts are excluded. Five flavors remain in the coupling running and bottom/charm virtual spectator terms. This is a theoretical cut definition, not an experimental heavy-flavor-tagging model. The emitted light flavors do not supply their direct Yukawa currents.

Hard energies are restricted to Q in [20,80] GeV, scales mu/Q in [1/2,2], temperatures T in [1/3,0.5] GeV. Thermal quantities integrate only `w=Q/T-(mi+mj)/T` in [0,90]. No physical high-energy continuation or bound above Q=80 is asserted.

## 3. Candidate assembly before finite mass matching

Write `a=alpha_s(mu)/pi`, `A=F_b+F_c`, `B=|A|^2`, where the one-loop form factors are normalized to one in the infinitely heavy-quark limit. The additive virtual numerator is `V=Re[(G_b+G_c) A*]`, using the literal Note-46 G until the matching step below. Coherence is retained throughout.

From the decay decomposition and heavy-loop limit in Spira et al. [2], combined with the real-heavy-flavor-veto convention of [1] and Note 43, the common universal coefficient is

```
U_veto = 73/4 - 7*n_l/6 - (ell_b+ell_c)/3 + (23/6)*L,
n_l=3, ell_q=ln(Q^2/m_q^2), L=ln(mu^2/Q^2).
```

The 73/4 is the heavy-top inclusive 95/4 coefficient with the mass-dependent virtual heavy limit 11/2 separated. The heavy virtual logarithms distinguish five running flavors from three retained massless real-splitting flavors. No real b/c cut is appended to this definition.

Use Note 47's reconstructed additive three-gluon remainder and the 45-real light-pair remainder:

```
J_3 = (1/2) integral_triangle dx dy [A3-(1+x^4+y^4+z^4) B]/(xyz),
J_p = integral_0^1 dz (1-z)^3/z [|F_b(z)+F_c(z)|^2-B].
```

Here A3 is the coherent sum over the published three-gluon helicity combinations. The b/c loop branch points are resolved in each numerical integral. The common candidate current is

```
S_literal = (Q^2/9) {a^2 B + a^3 [V_literal + U_veto B + J_3 + (n_l/3) J_p]}.
```

The factor n_l/3 equals one for this note. These remainders subtract their Born-like singular shapes; the universal term restores the compatible integrated contribution in the candidate assembly. A finite change that adds a function times B to a subtracted remainder must remove that same function from the corresponding integrated term. A synthetic relocation test checks that algebra, without treating its arbitrary function as new QCD input.

The heavy-top probe has `F_t=1`, `G_t=11/2`, and helicities `(x^2,-y^2,z^2,1)`. Its finite real remainders vanish and `G_t+U_veto` reproduces Note 43's top-operator-square NLO coefficient. That check passes without any finite shift. The production-specific universal pi-squared term is not imported into the decay coefficient.

## 4. Cross-sector discrepancy and the finite derivative that removes it

For each heavy-top–q mixed component, with q=b or c, compare the *absolute order-a^3 increment*, not LO plus NLO, against Note 44's independently transcribed closed polylogarithm expression from [1]. Inputs and running are shared, but the hard coefficient is represented differently: virtual-plus-real integrals here versus a closed mixed coefficient there.

At Q=20 GeV, mu=Q, the current-level values in GeV^2 are:

| Mixed component | Literal assembled increment | Note-44 closed reference | Literal minus reference |
|---|---:|---:|---:|
| top–bottom | +0.0274829256 | +0.0374927645 | -0.0100098388 |
| top–charm | -0.0128148944 | -0.0137490764 | +0.0009341820 |

These are signed current contributions, not standalone event rates. Their mismatch is far larger than the numerical integration differences. It has the structure

```
S_literal,tq - S_reference,tq
 = -(a^3 Q^2/9) (8/3) Re[D_q F_q],
D_q = m_q partial/partial m_q,
```

to the tested numerical accuracy. D acts on both the Yukawa and propagator-mass dependence of the amplitude. No division by the Born amplitude is needed at a zero or cancellation.

The standard one-loop pole/MSbar relation [3] contains the finite boundary term

```
M_q = mbar_q(mu) [1+a*(4/3+ln(mu^2/mbar_q^2))] + O(a^2).
```

Spira et al. [2], Eq. (7), explicitly distinguish their pole-normalized running mass from the MSbar running mass. Harlander and Kant [4], printed page 3, use an MSbar label, and Eqs. (3.4)-(3.7) give the coefficient transcribed in Note 46. The labels alone do not establish that our direct combination of these formula conventions is consistent. We retain this source-level tension rather than asserting an official correction to either paper.

At cross-section-numerator level, the finite 4/3 shift gives

```
Delta G_q = (8/3) D_q F_q,
Delta V_bc = Re[(Delta G_b+Delta G_c) A*]
           = (4/3)(D_b+D_c) B.
```

The factor two arises because G is a cross-section-level coefficient, as specified by [4]. This is a mass-convention matching term, not new emitted radiation. The resulting explicit candidate is

```
S_matched = S_literal + (a^3 Q^2/9) Delta V_bc.
```

Equivalently, keeping Note 46's rational G1 expression, the matched numerators are `G1+2[ln(mu^2/mbar^2)+4/3]DF` in the common running-mass convention and `G1` in the corresponding pole diagnostic. The old literal versions are not overwritten.

Fourteen comparisons cover both b and c at Q=20,23,40,65 GeV centrally, scales Q/2 and 2Q at Q=20, and the auxiliary pole prescription at Q=23. With 32 angular nodes the largest relative matched/reference difference is about **1.06e-9**. No masses, couplings or finite constants were fitted in these checks. They identify a tightly constrained finite matching discrepancy, but are not an independent complete diagram calculation or proof of an author-confirmed erratum.

For the b/c-square sector the same term follows by differentiating the *coherent* Born square, not by estimating it from the mixed-sector percentages. A separate finite-difference check verifies the derivative. A synthetic mass re-expansion shows that its residual begins at a^4, the next omitted absolute order.

## 5. Finite-window candidate results

At assumed T=0.5 GeV, central mu=Q, using 32 angular and 32 thermal nodes:

| Incoming pair | Coherent b/c-square LO | Finite matching shift | Assembled matched b/c-square NLO candidate |
|---|---:|---:|---:|
| 11 | 2.67595e-17 | +4.27755e-18 | 6.12645e-17 |
| 12 | 2.51272e-17 | +4.04590e-18 | 5.75965e-17 |
| 22 | 2.34521e-17 | +3.79368e-18 | 5.38335e-17 |

All entries are in GeV^-2. They require the stipulated common-temperature Maxwell–Boltzmann momentum distributions, but not the further one-equation chemical-equilibrium reduction.

Only under that **still-unestablished** chemical-equilibrium reduction do the inherited ideal-gas weights give the following candidate assembly:

```
LO b/c square:                    2.65726141679e-17,
literal virtual block:           1.57699987285e-17,
universal/integrated term:        1.46447344241e-17,
three-gluon finite remainder:   -2.22139168845e-19,
light-pair finite remainder:    -1.71707392988e-19,
finite matching shift:           4.25097349932e-18,
matched NLO increment:           3.42718600901e-17,
LO plus matched increment:       6.08444742581e-17 [GeV^-2].
```

Without the finite matching shift the corresponding sum is 5.65935007588e-17 GeV^-2; the shift changes that candidate by 7.51%. This does not mean a newly observed 7.51% effect. The matched candidate is 2.28974 times its LO reference; the size of that order correction and prescription dependence prohibit a precision claim.

| Prescription | Conditional assembled b/c-square candidate [GeV^-2] |
|---|---:|
| mu=Q/2, running masses | 8.74697e-17 |
| mu=Q, running masses | 6.08445e-17 |
| mu=2Q, running masses | 4.32751e-17 |
| mu=Q, auxiliary pole1 masses | 9.47016e-17 |

These are prescription-sensitivity comparisons, not confidence intervals or guaranteed error envelopes. Auxiliary pole masses are the frozen low-order estimates from Note 42, not precision pole-mass determinations.

The raw output also records heavy-top probe-square and mixed components so the closure can be reproduced. Their sum is not advertised as a full finite-top physical prediction. No additional sum with the direct quark-current or lepton network is interpreted as total annihilation or abundance.

## 6. Numerical controls and execution

The default 24-angular/24-thermal central candidate is 6.08444732625e-17 GeV^-2. Refining both to 32 changes the conditional candidate by approximately 1.64e-8 relatively. A different Q-variable thermal quadrature agrees with the default candidate to about 4.4e-16 relatively when the same angular rule is retained. That agreement cannot estimate the angular integration error or physical uncertainties.

The reconstructed light-pair evaluator reproduces the 45-real hard checkpoint J_bc(20 GeV)=-0.0773301160 and its thermal contribution. The extended six-component three-gluon implementation reproduces Note 47's unchanged b/c pieces. Old modules remain byte-identical; the new module extends their helicity assembly only by an explicit heavy-top probe. It uses no external executable, fitted numerical table or unsafe data loader.

The first new 30-test run had one failure: a 24-angular-node cross-sector comparison at high Q differed by 1.39e-7 relatively, exceeding its unchanged 2e-8 tolerance. The closure test was refined to 32 angular nodes; neither its tolerance nor the physical formula was changed. The original failed log is preserved. This numerical-test repair is separate from the finite physical-convention discrepancy, which is deliberately retained as a detected-discrepancy test.

The corrected combined suite passed **227 tests: 30 new and the 197-test inherited chain**, zero failures/errors, exit code 0. The chain includes Notes 40,42,43,44,45-RG,46,47. It does **not** include the original standalone Note-41 or 45-real suites and is not a whole-repository audit.

```
python -m unittest -v test_research_note_40.py test_research_note_42.py \
  test_research_note_43.py test_research_note_44.py test_note45_rg_matching.py \
  test_research_note_46.py test_research_note_47.py test_research_note_48.py
python reproduce_note48.py --full
```

The full run completed all six prescriptions and seven hard checkpoints. The execution record and package contain source hashes, full numerical output, the failed and successful test logs, and reproduction commands. Publication and final clean-package validation are recorded separately after those operations occur; a local file or Git blob is not by itself proof of branch publication.

## 7. Remaining review and physics

This is the first explicit common candidate assembly in this development chain, with an independently represented mixed-sector closure test and a finite mass-boundary correction. It is a substantial step beyond listing separate pieces. It does not erase the source-normalization and finite-convention review requirements. `complete_physical_rate` deliberately rejects requests to treat the candidate as an independently certified completed observable.

Next, independently check the identified finite boundary and reconstructed real normalization against a third full-order implementation or source derivation. Then consistently include the omitted real-heavy-flavor cuts and their interference, remaining direct light-quark/electroweak channels, conversion scatterings and kinetic/cosmological inputs. A complete abundance calculation also requires specified initial conditions and a coupled number evolution.

No new Omnes arrays, heavy-singlet hadronic width or lifetime, H2 optical prediction, detector exclusion, journal submission, DOI or empirical confirmation follows. Historical notes and main are not rewritten by this additive correction record.

## Primary sources and attribution

[1] J. Wang and Y. Wang, *Analytic Result of Higgs Boson Decay to Gluons with Full Quark Mass Dependence*, arXiv:2503.22169v2 (2025), Eqs. (4)-(6) and the real-heavy-flavor cut definition. https://arxiv.org/html/2503.22169v2 . The closed mixed coefficient supplies a cross-check, not endorsement of the hypothetical singlets.

[2] M. Spira, A. Djouadi, D. Graudenz and P. M. Zerwas, *Higgs Boson Production at the LHC*, arXiv:hep-ph/9504378v1 (1995), Eq. (7), Sec. 2.2, and Appendix C. https://arxiv.org/html/hep-ph/9504378 . The explicit pole-normalized/non-MSbar distinction is relevant to finite matching. Note 47 documents the separate reconstructed decay normalization; neither finding is an author-confirmed erratum.

[3] K. G. Chetyrkin, J. H. Kuhn and M. Steinhauser, *RunDec*, arXiv:hep-ph/0004189, Eq. (13). https://arxiv.org/html/hep-ph/0004189 . Supplies the finite 4/3 one-loop mass conversion. No RunDec executable was run.

[4] R. V. Harlander and P. Kant, *Higgs production and decay: Analytic results at next-to-leading order QCD*, arXiv:hep-ph/0509189v1, printed page 3 and Eqs. (3.4)-(3.7). https://arxiv.org/pdf/hep-ph/0509189 . The formula pages were visually checked; the mass-label sentence was available in parsed text but its page-image fetch failed. The cross-section-level normalization and rational coefficient are source-derived; the finite convention tension is expressly left for independent review.

Internal lineage: live Notes 40-47 at 94093121a33a3486a8c5e74c0a1fbcf496654d74. The common assembly, probe extension, closure diagnosis and additive matching record are developed here. Established QCD ingredients remain attributable to their source authors.
