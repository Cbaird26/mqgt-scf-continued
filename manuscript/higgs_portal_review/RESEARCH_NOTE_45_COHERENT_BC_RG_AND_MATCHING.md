# Research Note 45 — RG-fixed logarithms and mass-scheme matching for coherent bottom/charm-square gluonic currents

**1 October 2026 | Scientific-development draft; locally executed; not peer reviewed.** Prepared for Christopher Michael Baird with ChatGPT (ZoraASI) assistance in source checking, derivation, implementation, testing and drafting. This is a conditional calculation in the restricted two-real-singlet Higgs portal. It neither establishes the hypothetical particles nor completes their gluonic rate, total reaction network, or cosmological abundance.

**Publication status:** Notes 44 and 45 are local packages, not branch commits. The live review branch was read at `f6d68d2ce4cdbcb2efa52691d0f6b8dd70409d1a`, the Note-43 snapshot. A fresh attempt to upload the Note-44 calculator through `GitHub.create_blob` returned `Resource not found`; subsequent discovery returned no code-creation actions. No remote blob or branch write succeeded. An attempted PR status comment also returned `Resource not found`; no comment was posted. The installed GitHub integration was rediscovered; no working code-upload alternative was obtained. Historical notes and `main` were not changed. The package contains separately applicable Note-44 and Note-45 patches and a combined additions-only patch.

## 1. The calculation that is—and is not—performed

The Note-44 archive was read, extracted without source edits, and checked against all byte counts and SHA-256 values in its manifest. Its 109-test suite passed again. Its top–bottom/charm mixed contribution remains unchanged.

The next missing gluonic sector is the square of the coherent bottom/charm Yukawa amplitude, including bottom–charm interference. Wang and Wang [1], Eq. (7), supply this sector at its leading nonzero order only. Their mixed-sector Eq. (6) does not determine the independent higher-order square-sector coefficient. This note calculates the **required explicit NLO renormalization-scale logarithm and the mass-scheme conversion terms** of that square sector. It does **not** calculate its finite NLO real-plus-virtual matching function.

The distinction is operational: the implementation refuses to return a completed NLO current without a separately supplied finite coefficient. It never assumes that this coefficient vanishes in a physical prediction. An optional callback is an input contract, not certification of the physics supplied to it.

All numerical inputs remain those of Notes 40–44: `m1=10`, `m2=11.5`, `mh=125`, fixed `Gamma_h=0.0041`, `v=246` in GeV; portal entries `K11=K22=0.001`, `K12=-0.001`; historical inputs `alpha_s(MZ)=0.1189`, `MZ=91.1876 GeV`, `mbar_b(10)=3.610 GeV`, `mbar_c(3)=0.986 GeV`. The inherited two-loop-truncated running and continuous flavor matching remain unchanged. These are not new fits or claims about the latest measurements.

## 2. Differentiate the coherent amplitude, not an incoherent sum

Set `a=alpha_s(mu)/pi`, `L=ln(mu^2/Q^2)`, `r_q=mbar_q(mu)^2/Q^2`. The one-loop form factor, normalized to one for an infinitely heavy quark, can be written above threshold as

```
beta = sqrt(1-4r),  ell = ln[(1+beta)/(1-beta)],
z = ell-i*pi,  f = -z^2/4,
F(r) = 6r [1+(1-4r)f].
```

This is an algebraic rewrite of the form factor used in Note 42 and of the amplitude in [1], Eq. (7); Yukawa and propagator masses are both in the declared running-mass prescription. There are no additional gluon-color or identical-final-state factors.

Introduce independent **real Yukawa multipliers** `kappa_b,kappa_c` as algebraic probes. They do not change quark masses, active flavors, vacuum-polarization loops or the running coupling. Define

```
A = kappa_b F(r_b)+kappa_c F(r_c),
B = |A|^2 = B_bb+B_cc+B_bc,
B_bc = 2 Re[kappa_b F_b (kappa_c F_c)*].
```

Here `bc` is a loop-flavor interference label, not the incoming singlet pair `12`.

At fixed Q, the exact logarithmic mass derivative of the one-loop form factor is

```
D_q F_q := m_q dF_q/dm_q = 2r_q dF_q/dr_q,
D F = 12r [1+(1-8r)f + beta*z/2].
```

Since `d ell/dr=-1/(r beta)`, this follows directly by differentiating F. It includes both the Yukawa-mass and loop-mass dependence. Consequently

```
D_q B = 2 Re[(kappa_q D_q F_q) A*].
```

It is incorrect to differentiate `|F_b|^2+|F_c|^2` and omit the derivative of their interference. The additive derivative remains finite when a coherent amplitude or interference component cancels; no division by a vanishing LO quantity is introduced.

## 3. Determine the explicit NLO logarithm

The QCD conventions in RunDec [2], Eqs. (1),(2),(6),(7), give for five active flavors

```
da/dL = -beta0 a^2 + O(a^3),   beta0=23/12,
d ln(mbar_q)/dL = -gamma0 a + O(a^2),   gamma0=1.
```

We consider the pure Yukawa-square gluonic-cut sector with the same real-heavy-flavor veto as Note 44. Its renormalized scalar Yukawa operators are treated with their QCD mass renormalization; no top-operator Wilson matching factor is inserted into this sector.

The leading current is

```
S_LO(Q,mu) = (Q^2/9) a^2 B(r_b,r_c).
```

At fixed Q its scale derivative through absolute order a^3 is

```
dS_LO/dL = -(Q^2/9) a^3 [2 beta0 B + gamma0(D_b+D_c)B] + O(a^4).
```

Therefore a consistently renormalized NLO completion must have the form

```
S_NLO = (Q^2/9) { a^2 B + a^3 [C_fin(r_b,r_c) + L K(r_b,r_c)] } + O(a^4),
K = 2 beta0 B + gamma0(D_b+D_c)B.
```

**K is determined here; C_fin is not.** `C_fin` contains the finite virtual-plus-real contribution with the chosen cuts. It may itself contain mass-ratio logarithms; “finite” means after the required cancellations and renormalization, not free of logarithms.

The identity holds componentwise for `bb`, `cc`, and the signed `bc` interference. Higher beta/gamma coefficients enter the residual derivative at a^4, beyond the hard order being fixed. This result does not upgrade the inherited running prescription to complete higher-order QCD.

### Why RG consistency cannot set the central finite answer

For any smooth finite function `H(r_b,r_c)`, replacing `C_fin` by `C_fin+H` changes the central current at order a^3 but its scale derivative only at a^4. Thus infinitely many central values obey the same NLO scale-cancellation equation. This is a boundary-data freedom of the RG equation, not a no-go result about calculating the physical coefficient.

Tests demonstrate this with explicitly synthetic choices. No synthetic choice is used as QCD input or reported as a physical NLO rate. A scale-log repair alone cannot turn Note 44's partial sum into a complete coherent NLO calculation.

## 4. Mass-scheme matching is fixed independently

The one-loop mass conversion from [2], Eq. (13), inverted through first order, is

```
M_q = mbar_q(mu) [1+a d_q]+O(a^2),
d_q = 4/3+ln(mu^2/mbar_q(mu)^2) = 4/3+L-ln(r_q).
```

Starting with an all-on-shell amplitude, re-expanding the full Born square gives the additive coefficient shift

```
Delta C_OS->MSbar = d_b D_b B + d_c D_c B.
```

At `L=0` this determines the finite **difference between two conventions**:

```
C_fin,MSbar = C_fin,OS + sum_q [4/3-ln(r_q)] D_q B.
```

Neither finite coefficient is determined by this difference alone. The explicit L in the conversion combines with the all-on-shell scale coefficient `2 beta0 B`, reproducing the K derived above.

The source's hybrid convention requires a different intermediate derivative. With the Yukawa mass held fixed, an individual amplitude is `(mY_q/M_q)F(M_q)`, so its loop-mass derivative is `D_q F_q-F_q`. The summed derivative of the square is therefore `(D_b+D_c)B-2B`. The hybrid scheme has scale coefficient `(2 beta0+2)B` because its two Yukawa factors run. Adding the loop-only conversion again gives `2 beta0 B+(D_b+D_c)B`. This cross-check avoids converting an already-running Yukawa twice.

A large numerical convention shift is not a newly predicted physical correction. It must accompany the corresponding change of Born masses and finite hard coefficient.

## 5. Finite-window thermal values

We integrate the known terms with the unchanged unequal-mass Maxwell–Boltzmann kernel. Temperatures are restricted to `[1/3,0.5] GeV`, hard energies to `[20,80] GeV`, and scale ratios to `[1/2,2]`. The reported window is `w=Q/T-(mi+mj)/T` in `[0,90]`. There is no new claim about the physical spectrum above Q=80 or a physical infinity-domain integral.

At assumed `T=0.5 GeV`, central `mu=Q`, and `kappa_b=kappa_c=1`:

| Incoming pair | Coherent b/c-square LO | Required NLO coefficient of L | Finite OS-to-MSbar conversion term |
|---|---:|---:|---:|
| 11 | 2.67595e-17 | 8.22568e-18 | 1.73281e-17 |
| 12 | 2.51272e-17 | 7.68145e-18 | 1.68291e-17 |
| 22 | 2.34521e-17 | 7.12780e-18 | 1.61679e-17 |

All columns have units `GeV^-2` after integration. **The second and third columns are not complete NLO rates and must not be added as new independent final states.** The second is the coefficient of the explicit dimensionless logarithm. The third is a mass-convention conversion term, not the unknown physical hard correction.

Only if the still-unestablished chemical-equilibrium reduction applies, the inherited equilibrium weights give

```
coherent b/c-square LO:                 2.65726141679e-17 GeV^-2,
required NLO coefficient of L:          8.16337116395e-18 GeV^-2,
finite OS-to-MSbar convention shift:    1.72704293682e-17 GeV^-2.
```

The LO value reproduces the unchanged Note-42 `bb+cc+bc` components. The explicit-log slope is 0.30721 times that LO contribution per unit L; this is **not a 30.7% change of the physical rate**. At the central scale L=0 its explicit contribution vanishes. When the scale changes, masses and coupling change as well, and the log cancels their leading scale dependence. The finite convention shift is 0.64993 times the LO value, but likewise is not a 65.0% physical enhancement.

For the known terms, invariant-Q and scaled-w integrals agree within an absolute difference of approximately `8.1e-32 GeV^-2` in this execution. Independent generalized Gauss–Laguerre and finite-window checks pass. Numerical agreement does not bound missing finite matching, higher QCD orders, input covariance, plasma effects, or the incomplete reaction inventory.

## 6. A concrete extraction contract for the remaining finite coefficient

At fixed masses, coupling, flavor content and cuts, an exact-order calculation with top Yukawa set to zero has a quadratic dependence on the two Yukawa multipliers:

```
R(kb,kc)=kb^2 R_bb+kc^2 R_cc+kb kc R_bc.
```

Here `R_bc` includes the full interference factor of two. The three values

```
R_bb=R(1,0),   R_cc=R(0,1),
R_bc=R(1,1)-R(1,0)-R(0,1)
```

recover the sector, with the independent checks

```
R_bc=[R(1,1)-R(1,-1)]/2,   R(0,0)=0.
```

The new `polarize` checker implements this contract, including signed NLO increments. Setting a quark mass to zero is **not** an acceptable way to turn off its Yukawa contribution: that also changes loop kinematics, spectator loops, matching and possibly the active-flavor prescription. All those inputs must remain fixed between probes. Satisfying the algebraic checks does not independently certify the external implementation.

The full massive NLO literature [3] supplies a route to a direct calculation, but its treatment of real splitting flavors must be matched to the present veto convention. An inclusive five-massless-splitting-flavor number is not automatically our vetoed observable. We identified the official HDECAY source listing as a candidate [4], but its `hgg.f` retrieval failed; no executable, interpolation grid or NLO probe data were obtained or run here. We do not claim the finite result is absent from all literature or numerical programs.

The direct amplitude route instead requires the coherent two-loop virtual contribution and the coherent one-loop real-emission contributions, with infrared subtraction and compatible cuts. A finite virtual form factor alone does not give the inclusive decay correction. The extraction contract makes the remaining missing data precise without supplying them by assumption.

## 7. Execution, failure record and artifact provenance

The Note-44 package manifest was verified and its full 109-test suite rerun successfully before this extension. The new suite contains 30 tests: independent 70-digit amplitude derivatives, coherent component identities, exact cancellation behavior, RG orders, mass conversions, both thermal variables, independent quadrature, finite-domain checks, extraction algebra, and explicit rejection of an absent finite hard coefficient.

The initial 30-test run had one failure. A test attempted to measure a quartic residual by a ratio at `L=0` with a zero finite matching fixture and one-loop running. At that special point the residual vanishes identically, so its floating-point ratio was meaningless. The test was corrected to evaluate at nonzero `L=0.4`; its tolerance was not loosened and the physics implementation was not changed. The initial failure log is retained. The corrected suite passed 30/30; the combined baseline plus new suite passed **139/139**, with zero failures/errors. The original separate Note-41 suite is not included or claimed to have run.

```
python -m unittest -v test_research_note_40.py test_research_note_42.py \
  test_research_note_43.py test_research_note_44.py test_research_note_45.py
python coherent_bc_rg.py
```

The execution record supplies byte counts, Git-style local blob identities, SHA-256 values and software versions. New identities are **local**; no remote publication succeeded. A clean extraction of the finished package was hash-verified and the same 139-test command rerun. The complete repository was not audited. These are mathematical/software checks, not independent empirical validation.

No new Omnes inputs were acquired. The heavier-singlet hadronic width/lifetime, total annihilation network, actual chemical equilibrium, relic abundance, H2 signal and detector exclusions remain outside the results of this note.

## References and separation of sources from this derivation

[1] J. Wang and Y. Wang, *Analytic Result of Higgs Boson Decay to Gluons with Full Quark Mass Dependence*, arXiv:2503.22169v2, Eqs. (1)–(7) and the cut definitions. https://arxiv.org/html/2503.22169v2 . Supplies the operator organization, LO coherent b/c square and hybrid mass convention, not the missing square-sector finite NLO coefficient.

[2] K. G. Chetyrkin, J. H. Kuhn and M. Steinhauser, *RunDec: a Mathematica package for running and decoupling of the strong coupling and quark masses*, arXiv:hep-ph/0004189, Eqs. (1),(2),(6),(7),(13). https://arxiv.org/html/hep-ph/0004189 . Supplies RG and mass-conversion conventions; no RunDec executable was run.

[3] M. Spira, A. Djouadi, D. Graudenz and P. M. Zerwas, *Higgs Boson Production at the LHC*, arXiv:hep-ph/9504378v1, Sec. 2.2, Eqs. (23)–(26) and the real-splitting-flavor discussion. https://arxiv.org/html/hep-ph/9504378 . Identifies a massive-NLO calculation route and a final-state convention that must be reconciled, not numerical data imported here.

[4] Official PSI HDECAY repository, source listing `zzz/hgg.f`, viewed 1 October 2026: https://gitea.psi.ch/ltpth/HDECAY/src/branch/main/zzz . Listing inspected only; source/data download unsuccessful.

Internal lineage: Notes 40–43 at the live pinned head above; Note 44 from its attached reproducibility ZIP. The coherent derivative, explicit RG-log specialization, mass-convention cross-check, extraction contract and numerical implementation are developed in this note. The underlying QCD ingredients remain those of the cited authors. No source endorses the proposed singlets or consciousness/ethics interpretations.
