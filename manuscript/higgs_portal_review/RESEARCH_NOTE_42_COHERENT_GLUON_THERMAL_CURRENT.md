# Research Note 42 — Coherent quark-loop gluon annihilation and perturbative-order bookkeeping

**29 September 2026 | Public scientific-development addendum; not peer reviewed.** Human author: Christopher Michael Baird. ChatGPT (ZoraASI) assisted with source comparison, derivation, implementation, numerical checks and drafting. This is a conditional calculation in the restricted two-real-singlet Higgs-portal model. No observed new field, validated Theory of Everything, total QCD rate or relic abundance is claimed.

## 1. Live-source reconciliation and the next collision channel

The live review branch was read at `4fbcef5ff7e42f1962c75529d2bbc94c083a05e0`. It already contained Note 41, although the last conversation summary stopped at Note 40 and the PR-description heading still stopped at Note 39. Rather than duplicate that work, this note retains Note 41 and extends it to the previously omitted two-gluon final state.

The inherited Note-40 running module and Note-41 finite-mass module were reconstructed or extracted locally and matched to their published Git blob identities. Re-evaluation reproduces Note 41's conditional effective bottom/charm contribution, `1.19805650413715e-14 GeV^-2`. This is a rerun of the implementation and a regression, not independent empirical validation. The separate original 24-test Note-41 suite was not rerun in this step; the executed suite below includes Note-41 source identity, central-value and published-coefficient checks.

The new process is `s_i s_j -> h* -> g g`, for initial pairs `11`, `12`, `22`. Its leading nonzero rate is O(alpha_s^2). We include the complete one-loop mass dependence and complex interference of top, bottom and charm loops. Up/down/strange loops and higher-order gluon corrections are not included.

## 2. Inherited inputs and explicit loop-mass convention

Retain the unfitted masses, portal couplings, fixed Higgs propagator and historical QCD inputs of Notes 40-41:

```
m1=10, m2=11.5, mh=125, Gamma_h=0.0041, v=246 [GeV];
K11=+0.001, K12=-0.001, K22=+0.001;
alpha_s(MZ)=0.1189, MZ=91.1876 GeV;
mbar_b(10 GeV)=3.610 GeV, mbar_c(3 GeV)=0.986 GeV.
```

The sole additional mass input is `M_t=172.69 GeV`, selected from the historical numerical prescription in Wang and Wang [2], Eq. (12). This is not a latest-mass claim or a parameter derived by the singlet framework. Their other numerical inputs are not substituted for ours.

The central prescription uses the inherited two-loop-truncated, five-flavor running coupling at `mu=Q`, bottom/charm running masses `mbar_q(mu)` in both the Yukawa coupling and loop propagators, and the same fixed top mass in both its Yukawa coupling and propagators. Varying `mu/Q` changes alpha_s and the b/c masses together. Djouadi [1] states the form factor with pole masses; using the same MSbar mass in both places is our explicitly declared leading-order scheme prescription. A mass-scheme conversion changes this leading O(alpha_s^2) width at O(alpha_s^3), which is not computed here. No partial conversion counterterm is misrepresented as a complete NLO gluon correction.

A separate diagnostic uses one-loop auxiliary pole estimates at the frozen input anchors:

```
M_q^(1) = mbar_q(mu0)*[1+(alpha_s(mu0)/pi)*(4/3+ln(mu0^2/mbar_q(mu0)^2))],
mu0_b=10 GeV, mu0_c=3 GeV;
M_b^(1)=4.30717304 GeV, M_c^(1)=1.27132167 GeV.
```

These are low-order conversion estimates, not precision pole-mass determinations. Both loop and Yukawa masses change together in this diagnostic. With unequal Yukawa and loop masses, each form factor instead requires the explicit multiplier `m_Yukawa/m_loop`.

## 3. Coherent amplitude and source-to-model normalization

Use [1], Eqs. (2.46)-(2.48),(2.58), with `tau_q=Q^2/(4m_q^2)` and a form factor normalized to one for an infinitely heavy quark:

```
F(tau) = (3/2)*[tau+(tau-1)*f(tau)]/tau^2,
f(tau) = asin(sqrt(tau))^2                                      (tau<=1),
f(tau) = -(1/4)*[ln((1+sqrt(1-1/tau))/(1-sqrt(1-1/tau)))-i*pi]^2  (tau>1).
```

The auxiliary unit-Higgs-current width and the inherited scalar-current weight are

```
Gamma_gg(Q) = alpha_s(mu)^2*Q^3/(72*pi^3*v^2)*|F_t+F_b+F_c|^2,
S_gg(Q) = 8*pi*v^2*Gamma_gg(Q)/Q
        = alpha_s(mu)^2*Q^2/(9*pi^2)*|F_t+F_b+F_c|^2.
```

The published normalization already includes final gluon colors and identical-final-state counting. It must not be multiplied by an extra factor of three or one-half.

The incoming portal then gives

```
sigma_ij^gg(s) = Kij^2*s*S_gg(sqrt(s))
                /[8*pi*D(s)*sqrt(lambda_ij(s))],
D(s)=(s-mh^2)^2+(mh*Gamma_h)^2,
lambda_ij(s)=[s-(mi+mj)^2]*[s-(mi-mj)^2].
```

We apply the same unequal-mass Maxwell-Boltzmann thermal integral as Notes 39-41, retaining its original pair-counting convention. The numerical window is `w=Q/T-(mi+mj)/T` in `[0,90]`. Code rejects hard energies outside `[20,80] GeV`, scale ratios outside `[1/2,2]`, and temperatures outside `[1/3,0.5] GeV`.

All three loops lead to the *same final state*. Accordingly, `|sum F|^2` must be used, not `sum |F|^2`. The terms `2 Re(F_q F_r*)` are signed interference terms, not separately positive decay channels. As a separate normalization check, the infinite-top limit agrees with the leading operator-basis pieces of [2], Eqs. (4),(5),(7), using `C1=-alpha_s/(12*pi)` and `C2=1`. The higher-order coefficients of that paper are not implemented.

## 4. Numerical results at the assumed T=0.5 GeV

Central finite-window results, in `GeV^-2`, are:

| Initial pair | Coherent gg contribution from t/b/c loops |
|---|---:|
| 11 | 6.23489e-17 |
| 12 | 6.24469e-17 |
| 22 | 6.27542e-17 |

Only under the still-unestablished chemical-equilibrium reduction do the full ideal-gas equilibrium weights from Note 39 produce

```
<sigma_eff v>_gg, leading order = 6.23608188693e-17 GeV^-2.
```

This is 0.5205% of the inherited finite-mass NLO bottom/charm effective contribution. Combining it with that result and the inherited Note-39 lepton contribution gives `1.30194460633e-14 GeV^-2` for the **selected leptons + NLO nonsinglet b/c + leading gg subset**. That subset sum is not the total effective rate, not a uniformly NNLO QCD result, not a lower bound on a physical total, and not an abundance prediction.

The conditional effective gluon decomposition is:

| Amplitude term | Signed thermal contribution [GeV^-2] |
|---|---:|
| top squared | 3.76138e-17 |
| bottom squared | 2.19506e-17 |
| charm squared | 3.44055e-19 |
| top-bottom interference | +2.43192e-18 |
| top-charm interference | -4.25754e-18 |
| bottom-charm interference | +4.27801e-18 |

The coherent result is 65.79% larger than the finite-top-only result at this chosen low-invariant-mass benchmark. Summing loop probabilities without interference would give `5.99084e-17`, 4.09% below the coherent result when the difference is measured relative to that incoherent sum. Neither percentage is transferable to the physical 125-GeV on-shell Higgs. For example, the central top-bottom interference changes sign between `Q=20` and `Q=23 GeV` in this implementation.

Keeping b/c loops and replacing the finite top form factor by its heavy-top limit changes the effective result by about -0.102%. This distinguishes a good top-mass expansion here from the unjustified omission of the bottom/charm amplitudes.

## 5. Scale and scheme sensitivity are larger than numerical errors

| Prescription | Conditional effective gg contribution [GeV^-2] |
|---|---:|
| mu=Q/2; running b/c masses | 9.77601e-17 |
| mu=Q; running b/c masses | 6.23608e-17 |
| mu=2Q; running b/c masses | 4.27578e-17 |
| mu=Q; auxiliary one-loop pole b/c masses | 1.07027e-16 |

The scale shifts are approximately +56.8% and -31.4%, and the auxiliary-pole diagnostic is 71.6% above the central prescription. These large variations explicitly prevent a precision claim for this leading-order gluon term. They are not confidence intervals or guaranteed error envelopes. The cancellation-sensitive loop amplitudes depend on the mass convention; true higher-order corrections and input uncertainties remain necessary.

The chosen scale ratios are applied consistently within each prescription; they are not fitted to produce agreement with previous numbers. The code checks that an infinitesimal one-loop mass redefinition changes the leading gluon width first at cubic order in alpha_s.

## 6. What may be added, and what must not be double counted

At the orders retained, Note 41's nonsinglet final states `b bbar(+g)` and `c cbar(+g)` and this note's two-gluon final state are distinct. Thus their selected contributions may be displayed together. Top/bottom/charm interference *within gg* must first be included coherently.

This does not supply all O(alpha_s^2) corrections to a total hadronic width: quark-current NNLO terms, singlet/interference contributions in other final-state cuts, and light-quark and electroweak modes remain absent. For NLO gluon work, real `ggg` and `g q qbar` cuts and operator mixing must be assigned consistently. An inclusive published QCD width must not simply be added on top of the channels it already contains. Reference [2] specifically distinguishes these cuts; its NLO calculation is a possible next ingredient, not a result reproduced here.

## 7. Numerical controls and executed provenance

The form factors agree with an independent 60-digit evaluation; below threshold they also agree with a direct Feynman-parameter integral. Thermal rates agree between the `Q` and scaled-`w` integrals within `2.4e-15` relative in the executed comparison. Generalized Gauss-Laguerre and window/order checks also pass. These are checks of the numerical formulas, not independent physical experiments.

An initial high-precision test exposed cancellation at `tau=1e-4`: the direct closed form differed by `3.0347e-12`, just above the unchanged `3e-12` test tolerance. The implementation was improved by extending its fourth-order heavy-mass Taylor branch from `tau<1e-4` to `tau<1e-3`, and adding checks at the new transition. The physical benchmark rates were unchanged. The initial failed log is preserved in the downloadable package; no failure was hidden by loosening the test tolerance.

After this change, **48 tests passed: 26 new Note-42 tests and 22 inherited Note-40 tests, with zero failures/errors**. The Note-41 module remains byte-identical, and its conditional central value and an on-shell published-coefficient check are included in the new tests. This does not claim execution of the separate original Note-41 test suite.

An analytic amplitude triangle bound gives `S_gg<92.93 GeV^2` throughout the declared hard/scale domain for the two specified mass prescriptions. It is not a maximum inferred from a scan. This gives omitted finite-interval bounds between the `w=90` endpoint and `Q=80 GeV` of approximately `6.21e-42`, `5.51e-42`, `4.88e-42 GeV^-2` for `11/12/22`. Those inequalities do not bound the unknown physical spectrum above `80 GeV`, and floating-point bound evaluations are not directed-rounding certificates.

New source/test identities:

```
gluon_loop_thermal.py:    c49c6fab4baa2d9c01c64f9fd8c2fdb7f018d50c
test_research_note_42.py: 16b989d17622647f6e75a135ecb45e9d08243c3d
```

The accompanying execution record separates local execution, GitHub byte verification, inherited files, runtime versions and physical limitations. The package includes full numerical output and test logs.

## 8. Remaining physics

The two-gluon term is now an explicit leading-order input rather than an unspecified omission. The full reaction network still needs higher-order gluon treatment with consistent final-state bookkeeping, light-quark/electroweak channels where relevant, conversion scatterings, kinetic assumptions, a specified expansion/entropy history and initial conditions before a coupled abundance evolution can be interpreted physically.

No low-energy Omnes data were obtained or evaluated in this step. The compressed `s2` hadronic width and lifetime are unchanged. No abundance curve, detector exclusion, H2 signal, journal submission or DOI was produced. Historical notes, main and the frozen verification archive are not modified by this addendum.

## Primary references

[1] A. Djouadi, *The Anatomy of Electro-Weak Symmetry Breaking. I: The Higgs boson in the Standard Model*, arXiv:hep-ph/0503172v2, Eqs. (2.46)-(2.48),(2.58), printed pages 89 and 94. https://arxiv.org/pdf/hep-ph/0503172 . Only the leading quark-loop formula is used here.

[2] J. Wang and Y. Wang, *Analytic Result of Higgs Boson Decay to Gluons with Full Quark Mass Dependence*, arXiv:2503.22169v2 (15 September 2025), Eqs. (4),(5),(7),(12) and final-state-cut discussion; Phys. Lett. B 869 (2025) 139865. https://arxiv.org/html/2503.22169v2 . Its NLO numerical predictions are not copied into our lower-Q benchmark or claimed to have been reproduced.

[3] Internal source lineage: Research Notes 39-41 at `Cbaird26/mqgt-scf-continued@4fbcef5ff7e42f1962c75529d2bbc94c083a05e0`. Their parameters, running and thermal kernels are inherited with the stated restrictions. External authors supply established ingredients, not support for the proposed singlet interpretation.
