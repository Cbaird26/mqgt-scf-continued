# Research Note 45 — Coherent bottom/charm radiation: a finite collinear-subtracted light-pair remainder

**1 October 2026 | Public scientific-development addendum; not peer reviewed.** Human author: Christopher Michael Baird. ChatGPT (ZoraASI) assisted with source comparison, derivation, implementation, numerical tests and drafting. This calculation concerns the hypothetical restricted two-real-singlet Higgs portal. It does not establish new fields, a Theory of Everything, a complete NLO QCD rate, or a relic abundance.

## 1. Scope and recovery of the preceding work

The live review branch was read at `f6d68d2ce4cdbcb2efa52691d0f6b8dd70409d1a`, containing Note 43. Note 44 had been packaged locally but not pushed during a publishing-action outage. Its original code, tests, note and execution record are retained byte-for-byte for publication alongside this addendum. Their 30 September statements about the failed publication attempt remain historical statements; this dated addendum and the later publication record document recovery rather than backdating it.

Note 44 supplies the mixed top–bottom/charm correction. The coherent bottom/charm-square NLO sector remains unfinished. This note calculates one finite part of that sector: the collinear-subtracted real-emission remainder for

```
s_i s_j -> h* -> g q qbar,  q = u,d,s treated as massless,
```

induced by the **internal bottom and charm loops**, coherently. The emitted light flavors and internal loop flavors are different labels. No top-loop term, direct light-quark Yukawa amplitude, real heavy-pair contribution, finite virtual remainder or three-gluon remainder is supplied by this calculation. In particular, a finite subtracted contribution is not a separately measurable decay channel or a complete NLO correction.

## 2. Inherited inputs and declared finite domain

Retain the unfitted benchmark and historical inputs of Notes 40–44:

```
m1=10, m2=11.5, mh=125, Gamma_h=0.0041, v=246 [GeV];
K11=+0.001, K12=-0.001, K22=+0.001;
alpha_s(MZ)=0.1189, MZ=91.1876 GeV;
mbar_b(10 GeV)=3.610 GeV, mbar_c(3 GeV)=0.986 GeV.
```

The inherited two-loop-truncated running and continuous four/five-flavor matching at 4.163 GeV are unchanged. These are fixed comparison inputs, not new or latest measurements or values derived by the singlet proposal.

The central prescription uses `mu=Q` and the inherited running mass in both the Yukawa coupling and propagators of each loop. The scale comparison uses `mu/Q=1/2,1,2` consistently in the coupling and masses. The separate `pole1` diagnostic uses the frozen auxiliary one-loop estimates from Note 42, approximately 4.30717 and 1.27132 GeV, in both positions. They are not precision pole-mass determinations. For unequal Yukawa and loop masses the amplitude would require the explicit factor `mY/m_loop`; that alternative is not silently used here.

The hard domain is `20 <= Q <= 80 GeV`, with `1/3 <= T <= 0.5 GeV`. Thermal results integrate `w=Q/T-(mi+mj)/T` only in `[0,90]`. The endpoints at T=0.5 GeV are Q=65,66.5,68 GeV for 11,12,22. Window and quadrature comparisons are numerical diagnostics, not a proof bounding the unknown physical spectrum to infinity. No numerical low-energy Omnes input is needed or used for this distinct hard-energy subcalculation.

## 3. Source-matched off-shell loop amplitude

The real amplitude requires one on-shell gluon and one timelike gluon that splits into the light pair. Set `tau=Q^2/(4m_loop^2)` and `z=k_pair^2/Q^2`. Spira et al. [1], Appendix C, Eq. (C.5), give the corresponding triangle through their `A_qqg(S)`. With `S=z*rho`, `rho=4*tau`, define `F(tau,z)=-3 A_qqg/4` so that its on-shell value agrees with the normalized form factor of Note 42:

```
F(tau,z) = -3/[2 tau (z-1)] * {
  1 - 2z [g(z tau)-g(tau)]/(z-1)
    - [1+1/(tau (z-1))] [f(z tau)-f(tau)] },
F(tau,0) = (3/2)[tau+(tau-1)f(tau)]/tau^2.
```

Here f and g are the published timelike functions of [1], Appendix A. For tau<=1,

```
f(tau)=asin(sqrt(tau))^2,
g(tau)=sqrt((1-tau)/tau)*asin(sqrt(tau)).
```

For tau>1, with `beta=sqrt(1-1/tau)` and `Z=ln[(1+beta)/(1-beta)]-i*pi`, they are `f=-Z^2/4`, `g=beta*Z/2`. Their continuous zero limits are f(0)=0 and g(0)=1. The internal branch points in the real-emission variable are `z=1/tau_b` and `1/tau_c`. They are not thresholds for the emitted massless u/d/s pair.

Both loops feed the same final state. Therefore use

```
B(z) = |F(tau_b,z)+F(tau_c,z)|^2,
```

including `2 Re(F_b F_c*)`, not a sum of two probabilities. The code keeps bb, cc and the signed bc interference separately and checks their sum.

Independent checks use a separately written 65-digit evaluation and the logarithmic parameter representations

```
f(t) = -(1/2) integral_0^1 dx ln[1-4t x(1-x)-i0]/x,
g(t) = 1+(1/2) integral_0^1 dx ln[1-4t x(1-x)-i0].
```

The latter require explicit splitting at their real logarithmic roots. They check a different integral representation of the same loop, not independent experimental evidence or a second derivation of all QCD.

## 4. Derive the real phase-space normalization and subtraction

The transverse amplitude tensor can be taken as `V_mn=(p.k)g_mn-k_m p_n`, with p the real-gluon momentum and k the conserved pair current. Contracting the massless fermion trace, using color trace `T_R=1/2`, and factorizing three-body phase space into two two-body factors gives, per emitted flavor,

```
dS_real/dz = a^3 Q^2/27 * (1-z)^3/z * B(z),
a=alpha_s(mu)/pi.
```

The scalar-current convention remains `S=8*pi*v^2*Gamma/Q`. Equivalently the real/Born ratio for a pointlike unit amplitude is `(a/3)(1-z)^3/z`. The identical-two-gluon factor is already in the Born denominator. No extra color-three or one-half is inserted. A tensor-contraction and phase-space test checks this normalization explicitly.

The real-emission integral alone diverges at z=0 in the massless emitted-flavor approximation. We therefore define an explicitly **subtraction-dependent** finite quantity:

```
J_bc(Q) = integral_0^1 dz (1-z)^3/z * [B(z)-B(0)],
Delta S_real,finite(Q) = n_l a^3 Q^2 J_bc(Q)/27,  n_l=3.
```

The difference B(z)-B(0) is O(z), so this integral is finite. A negative value is permissible because this is a difference of contributions, not an event probability. The subtracted B(0) term is not discarded from the full theory: it must be restored in a compatible integrated-subtraction and virtual calculation. Other finite subtraction prescriptions redistribute finite pieces. This J must not be added to an inclusive published current that already contains it.

For an arbitrary resolution epsilon,

```
C(epsilon)=integral_epsilon^1 dz (1-z)^3/z
 = -ln(epsilon)-11/6+3epsilon-(3/2)epsilon^2+epsilon^3/3,
R(epsilon)=integral_epsilon^1 dz (1-z)^3/z B(z),
R(epsilon)-B(0) C(epsilon) -> J_bc.
```

At Q=20 GeV in the central prescription:

| epsilon | Positive resolved real integral R | Positive subtracted term B(0)C | Difference |
|---|---:|---:|---:|
| 1e-3 | 4.01013 | 4.08978 | -0.0796449 |
| 1e-5 | 7.71942 | 7.79677 | -0.0773532 |
| 1e-7 | 11.4288 | 11.5061 | -0.0773303 |

The difference converges to `J_bc=-0.0773301160` while the two positive terms grow logarithmically. This is a mathematical subtraction check; epsilon is not a detector parameter or a fitted cutoff.

## 5. Stable endpoints and numerical evaluation

The derived collinear derivative is

```
partial_z F(tau,0) = 3/(2tau) * [4-tau-2g(tau)+(1-2/tau)f(tau)].
```

At the opposite endpoint,

```
F(tau,1)=3/(4tau) * [1+(2tau-1)f'(tau)].
```

A quadratic expansion about z=1 avoids cancellation in the closed expression, and the analytic collinear derivative is used in a tiny z<1e-9 interval. The small-tau expansion, used only for tests rather than the physical b/c rates, is

```
F(tau,z)=1+(7+11z)tau/30
          +(10+16z+22z^2)tau^2/105+O(tau^3).
```

The default real integral uses vectorized Gauss-Legendre quadrature on three intervals separated by the b/c branch points. Sine-squared maps smooth the square-root behavior at those interval endpoints. Direct adaptive z quadrature and adaptive quadrature on the mapped intervals provide cross-checks; 64/128/256-point comparisons are convergence diagnostics, not rigorous error bounds. The inherited thermal integral is checked in invariant Q and scaled w variables and with generalized Gauss-Laguerre quadrature.

## 6. Signed finite-window results

At assumed T=0.5 GeV, central mu=Q, the thermal contributions of this **finite real remainder only**, in GeV^-2, are:

| Incoming pair | Signed finite real remainder |
|---|---:|
| 11 | -1.65256e-19 |
| 12 | -2.22012e-19 |
| 22 | -2.65559e-19 |

The pairwise results assume common-temperature Maxwell-Boltzmann distributions. Only under the additional, still-unestablished chemical-equilibrium reduction do Note 39's equilibrium weights combine them into

```
Delta <sigma_eff v>_real,finite = -1.71707392988e-19 GeV^-2.
```

The corresponding signed decomposition is

```
bb remainder:               +1.03053461635e-19,
cc remainder:               -2.07938288484e-20,
bc interference remainder:  -2.53967025775e-19 [GeV^-2].
```

Their sum is the coherent result. The destructive interference is essential; keeping only the two squares would even change the sign of this remainder. The ratio to the inherited leading-order bc-square group, 2.65726141679e-17 GeV^-2, is -0.6462%. This ratio describes one finite subpiece, **not** the size of the complete missing bc-square NLO correction or a precision estimate.

| Prescription | Conditional finite real remainder [GeV^-2] |
|---|---:|
| mu=Q/2, running masses | -1.77245e-19 |
| mu=Q, running masses | -1.71707e-19 |
| mu=2Q, running masses | -1.37075e-19 |
| mu=Q, auxiliary pole1 masses | +5.70147e-21 |

These are prescription sensitivities, not confidence intervals. The auxiliary mass prescription changes the sign. Neither the sign of a standalone physical correction nor the full rate can be inferred from this isolated, subtraction-dependent piece. No new complete sum is formed with Note 44's partial upgrade.

## 7. Executed checks and provenance

The original Note-44 package was unpacked and its 109-test suite rerun successfully before this extension. A first nested-adaptive prototype was too slow and timed out without producing results; the default implementation was replaced by the mapped vectorized quadrature described above.

The first new 29-test suite exposed two failed assertions and one integration error. A high-precision check found cancellation near z=1; the endpoint implementation was improved to a quadratic expansion over 1-z<1e-3, with tests at the new transition, without loosening its tolerance. The independent logarithmic-parameter test was repaired to split a double root at t*z=1 and use a stable quadratic polynomial there. An arbitrary closeness-to-one test was replaced by the explicitly derived small-tau expansion and its scaling test. The initial failed log is retained in the package.

After these repairs, all 29 new tests passed. The combined suite then passed **138 tests: 29 new and 109 inherited (22 Note 40, 26 Note 42, 28 Note 43, 33 Note 44), zero failures/errors**. The original separate Note-41 test suite was not rerun; its unchanged module is checked by inherited tests. This is not a whole-repository audit.

The new source identities returned by GitHub blob creation match local bytes:

```
bc_real_radiation.py:      7a1404c8cc99b335b376f943c3a4abc2e1963a15
test_research_note_45.py: 3d9c4c46de547b4b503be9a0326041c8047e0495
```

The recovered Note-44 source/test identities likewise match 0ffc28870c414cc8613d28549511d10bcaf30ee7 and 4e4199ecaf308a260e2e4619557dd28198536b53. After matching these remotely created objects, another execution of the matching local bytes passed all 138 tests in 6.291 seconds, exit code 0. Runtime: Python 3.13.5, NumPy 2.3.5, SciPy 1.17.0 and mpmath 1.3.0. The same blob objects are selected for the additions-only review-branch commit. The accompanying publication record distinguishes this sequence from the earlier Note-44 failed write.

```
python -m unittest -v test_research_note_40.py test_research_note_42.py test_research_note_43.py test_research_note_44.py test_research_note_45.py
python bc_real_radiation.py
```

The package supplies inherited dependencies, new code, complete results, original failure and successful execution logs, and hashes. These are mathematical/software checks, not independent QCD validation or experimental observations. No external HDECAY/RunDec executable, unsafe upstream loader, Omnes data, detector likelihood or Boltzmann abundance solver was executed.

## 8. Remaining completion

The next bc-square pieces are the finite virtual correction and the coherent three-gluon real remainder, combined with the compatible integrated subtraction. Their interference structure must be retained before declaring this sector complete. The other missing heavy-final-state cuts, direct light-quark/electroweak contributions, conversion network, kinetic assumptions, expansion history and initial conditions remain separate tasks.

This step does not change the heavier singlet's hadronic width, lifetime, cosmological abundance or any H2 optical observable. It neither freezes the broader research program nor establishes its hypotheses. Historical source equations and archive PDFs are preserved; this addendum is limited to a specified testable-model calculation.

## Primary references and source separation

[1] M. Spira, A. Djouadi, D. Graudenz and P. M. Zerwas, *Higgs Boson Production at the LHC*, arXiv:hep-ph/9504378v1 (1995), Appendix A loop functions and Appendix C Eq. (C.5), with the virtual/real decomposition in Sec. 2.2 and Appendix C. https://arxiv.org/html/hep-ph/9504378 . Supplies the massive off-shell triangle; its complete NLO calculation has not been reproduced by this isolated real remainder.

[2] J. Wang and Y. Wang, *Analytic Result of Higgs Boson Decay to Gluons with Full Quark Mass Dependence*, arXiv:2503.22169v2 (2025), operator and final-state-cut definitions, especially Eqs. (3)–(7). https://arxiv.org/html/2503.22169v2 . Used for continuity of the sector/cut bookkeeping in Notes 43–44; no missing bc-square NLO coefficient is inferred from the paper's leading-order Eq. (7).

Internal lineage: Notes 40–43 and unchanged modules at f6d68d2ce4cdbcb2efa52691d0f6b8dd70409d1a; the original Note-44 conversation package. The source-to-current normalization, explicit subtraction convention, endpoint algebra and benchmark implementation are this addendum's work. External authors supply established QCD ingredients and do not endorse the proposed singlets or their interpretations.
