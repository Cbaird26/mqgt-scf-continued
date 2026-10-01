# Research Note 44 — Signed top–bottom/charm interference at NLO and a consistent mass-scheme conversion

**30 September 2026 | Scientific-development draft; locally executed; not peer reviewed.** Human author: Christopher Michael Baird. ChatGPT (ZoraASI) assisted with source comparison, derivation, implementation, numerical checks and drafting. This is an application of published QCD ingredients to the hypothetical restricted two-real-singlet Higgs portal. It is not a validated Theory of Everything, complete gluonic or hadronic calculation, measured field, or relic-abundance result.

**Publication status:** Saved in this conversation, not pushed to GitHub. The live review branch was read at `f6d68d2ce4cdbcb2efa52691d0f6b8dd70409d1a`. A subsequent GitHub blob-write action returned `Resource not found`; rediscovery exposed read actions only. No new remote commit, PR comment, DOI, or release was created. A patch containing the four new files is supplied for that review branch; existing source files and `main` were not edited.

## 1. What is added after Note 43

Note 42 supplies the coherent leading-order top/bottom/charm-loop gluonic contribution. Note 43 supplies the top-operator-square NLO correction, distinguishing retained gluonic cuts from real heavy-quark cuts. Here the next missing sector is implemented: the **signed interference between the top-induced operator and the bottom/charm Yukawa operators**, through absolute order `alpha_s^3`, using Wang and Wang [1], Eqs. (5) and (6).

The source calculation retains cuts with at least two gluons or a gluon plus a massless light-quark pair. Real bottom/charm final-state cuts are excluded. This is the same *partonic* heavy-flavor-veto convention used for Note 43's `delta_veto`, not an experimental tagging model. The result includes the published real-plus-virtual mixed-sector coefficient, not just a virtual form factor. The source's `C1*C2` is an operator combination, not the incoming `s1*s2` particle label: it contributes to all three incoming pairs.

Top effects are treated at leading power in inverse top mass. The coherent bottom/charm-operator-square NLO correction, finite-top NLO corrections, and mixed heavy-final-state cuts remain uncomputed. A complete QCD prediction is not claimed.

## 2. Inputs, normalization and the source's mass convention

Keep the unfitted benchmark and frozen historical inputs from Notes 40–43:

```
m1=10, m2=11.5, mh=125, Gamma_h=0.0041, v=246 [GeV];
K11=+0.001, K12=-0.001, K22=+0.001;
alpha_s(MZ)=0.1189, MZ=91.1876 GeV;
mbar_b(10 GeV)=3.610 GeV, mbar_c(3 GeV)=0.986 GeV.
```

The inherited two-loop-truncated running and continuous nf=4/nf=5 matching at 4.163 GeV are unchanged. These are not latest parameter determinations, new fits, or parameters derived by the singlet proposal.

In the source's hybrid convention, `M` is an on-shell loop mass and `mY=mbar(mu)` is the already-MSbar Yukawa mass. Set

```
a = alpha_s(mu)/pi,  r=M^2/Q^2,  beta=sqrt(1-4r),
u=4r/(1+beta)^2,  ell=-ln(u),
H(r)=(1-4r)*(ell^2-pi^2)/8 - 1/2.
```

The rationalized `u` equals the source's `(z-2-sqrt(z(z-4)))/2`, where `z=1/r`, without subtractive cancellation. Equation (5) gives a per-flavor coefficient

```
Delta1_q = [4 Q M mY/(pi v^2)] H(r).
```

Using `C1=-(a/12)[1+(11/4)a]` and `C2=1+O(a^2)`, the scalar-current weight `S=8*pi*v^2*Gamma/Q` has leading interference

```
S_LO,q = -(8/3) a^2 M mY H(r).
```

It agrees with `2 Re(F_q)` times the heavy-top Born current `a^2 Q^2/9`, including the Yukawa/loop-mass ratio when they differ. There is no extra color or identical-final-state multiplier. This is an interference weight, which may have either sign, not a positive standalone decay width.

Define `B(r)` as the braces in source Eq. (6), divided by `12(1+u)^2`. The function `hard_shape` implements all of those polylogarithms through Li4; it is not a small-mass approximation. The small-mass expressions in Eqs. (8) and (10) are implemented separately for tests, not substituted into the benchmark.

### Heavy-flavor wavefunction term

Equation (5)'s `Delta1` includes **both** flavors. Applying Eq. (6)'s explicit `b <-> c` symmetrization to its final `-(ell_b+ell_c)*Delta1/6` term therefore gives

```
Delta2_wavefunction = -(ell_b+ell_c)*Delta1_total/3,
ell_q=ln(Q^2/M_q^2).
```

The per-heavy-flavor coefficient is checked separately against the last term of Eq. (10): in the printed single-heavy-flavor expansion it is `-ell*(ell^2-pi^2-4)/24`, not half that value. It also agrees with the external-gluon wavefunction factor in Eq. (4). Omitting this distinction would change the finite mixed correction.

## 3. Re-expand the loop mass without converting the Yukawa twice

The central prescription puts the inherited `mbar_q(mu)` in both mass positions, matching Note 42's central LO convention. This requires an order-consistent conversion, not just numerical replacement inside Eq. (6).

The one-loop mass relation, with the conversion direction made explicit, is

```
M = mbar(mu) [1+a d] + O(a^2),
d=4/3+ln(mu^2/mbar(mu)^2).
```

The source's Yukawa mass is **already** MSbar. Only the loop mass must be re-expanded to obtain the all-MSbar convention. At fixed Q and Yukawa mass,

```
D_loop(r) = H(r)+2r H'(r)
          = (1-12r)*(ell^2-pi^2)/8 - 1/2 - beta*ell/2.
```

Thus the loop-mass conversion adds `d*D_loop`, not an extra squared-Yukawa conversion. This additive representation stays finite when `H=0`; dividing by H to define a multiplicative correction factor would introduce an artificial singularity.

The printed Eq. (6) fixes `mu=Q`. The logarithm at general scale is derived here from the renormalization group, not read from a successfully downloaded supplement. In the source's hybrid convention the LO current contains `a^2 mbar(mu)` with a fixed loop mass. With `d a/d ln(mu^2)=-beta0 a^2`, `beta0=23/12`, and `d ln(mbar)/d ln(mu^2)=-a`, its required logarithmic coefficient is

```
(2 beta0+1)*L*H = (29/6)*L*H,  L=ln(mu^2/Q^2).
```

After conversion, write the central current as

```
S_NLO,q = -(8/3) a^2 mbar_q(mu)^2 [ H(r)+a C_q ],
C_q = B(r) - (ell_b+ell_c)*H(r)/3 + (11/4)*H(r)
      + (29/6)*L*H(r) + d*D_loop(r).
```

The `11/4` term is the *single* Wilson-coefficient matching contribution [2]. Unlike the top-square sector, it is not doubled to `11/2`. The mass-conversion relation is consistent with [3]; the explicit derivative and scale restoration above are our source-to-convention derivations.

For the auxiliary all-pole diagnostic, the loop masses remain Note 42's frozen one-loop estimates and the source Yukawa mass is converted instead: the last term becomes `-d*H`. Those auxiliary masses are not precision pole-mass measurements. Synthetic small-coupling tests show that the two re-expansions differ from their respective unexpanded hybrid expressions first at absolute order `a^4`. The residual scale derivative also begins at `a^4`, the first omitted order.

## 4. Finite-window thermal results

Insert S into the unchanged unequal-mass thermal kernel from Note 40:

```
sigma_ij(s) = Kij^2 s S(sqrt(s)) / [8*pi*D_h(s)*sqrt(lambda_ij(s))],
D_h(s) = (s-mh^2)^2+(mh*Gamma_h)^2,
lambda_ij(s)=[s-(mi+mj)^2][s-(mi-mj)^2].
```

For an interference term this formula represents its signed contribution to the cross section. The common-temperature Maxwell–Boltzmann average is evaluated over `w=Q/T-(mi+mj)/T` in `[0,90]`. Hard energies are restricted to `[20,80] GeV`, temperatures to `[1/3,0.5] GeV`, and scale ratios to `[1/2,2]`. These finite-window contributions are not a claimed physical integral to infinity.

At assumed `T=0.5 GeV` and central `mu=Q`, the results through `alpha_s^3` are:

| Incoming pair | Top–bottom interference | Top–charm interference | Signed sum |
|---|---:|---:|---:|
| 11 | +1.30667e-17 | -8.72990e-18 | +4.33676e-18 |
| 12 | +6.90922e-18 | -9.12130e-18 | -2.21208e-18 |
| 22 | +1.16881e-18 | -9.41185e-18 | -8.24304e-18 |

All entries are in `GeV^-2`. Negative entries describe destructive interference, not negative probabilities or numbers of events. Numerical digits document reproducibility, not physical precision.

Only under the still-unestablished chemical-equilibrium reduction, Note 39's full ideal-gas equilibrium weights give:

| Contribution | LO heavy-top interference | NLO increment | LO plus NLO |
|---|---:|---:|---:|
| top–bottom | +2.42994e-18 | +9.93349e-18 | +1.23634e-17 |
| top–charm | -4.25386e-18 | -4.52050e-18 | -8.77436e-18 |
| signed sum | -1.82392e-18 | +5.41300e-18 | +3.58907e-18 |

The central summed interference changes sign at this perturbative order. Its LO value is already small because of cancellation, so a ratio to that value is a poor precision or convergence diagnostic. It is also distinct from Note 42's finite-top LO interference: agreement is tested with that note's **heavy-top** limit.

## 5. Sensitivity and what can be combined

The conditional summed interference through NLO changes under the following prescriptions:

| Prescription | Signed mixed contribution [GeV^-2] |
|---|---:|
| mu=Q/2, all-MSbar | +1.23936e-17 |
| mu=Q, all-MSbar | +3.58907e-18 |
| mu=2Q, all-MSbar | -1.33849e-18 |
| mu=Q, auxiliary all-pole | +1.85731e-17 |

The scale comparison crosses zero. These are not confidence intervals; neither the sign nor a precise size of the physical mixed term is established by the central truncated calculation. Input correlations, higher orders and omitted top-power terms remain outside this exercise.

An explicitly **partial upgrade** can retain Note 42's full finite-top coherent LO result and add only the known heavy-top NLO increments:

```
coherent LO, Note 42              = 6.23608188693e-17,
top-square vetoed NLO increment  = 3.07450233950e-17,
mixed vetoed NLO increment       = 5.41299865675e-18,
partial sum                     = 9.85188409211e-17 [GeV^-2].
```

Adding increments avoids counting the LO top or mixed terms twice. It does **not** make the result complete coherent NLO: the bottom/charm-square NLO term is missing, and finite-top effects are retained only at LO. The `real_b` and `real_c` terms from Note 43 are not silently appended; those cuts need their corresponding mixed amplitudes and interference before an inclusive hadronic claim. Direct light-quark Yukawa currents are not supplied by the massless splitting flavors in [1].

## 6. Executed checks and numerical limits

The new coefficient is checked against a separately written 70-digit polylogarithm evaluation, the published small-mass expansions, the old coherent LO amplitude, and the source-to-current normalization. The Wilson factor, heavy-flavor symmetrization, mass derivative, perturbative scheme conversion, scale derivative and nonsingular behavior at the LO interference zero are checked explicitly.

One additional check uses the *rounded* on-shell Table 1 entries of [1]: auxiliary masses are inferred from two LO rows, then the NLO row is predicted without fitting to it. The result is approximately `-0.015196 MeV`, consistent with the printed `-0.0152 MeV`. This is a rounding-level consistency check, **not** retrieval of the authors' exact mass inputs or a reproduction of their four-loop running. Those inferred masses are not used in the singlet benchmark.

All six thermal contributions are checked in Q and scaled-w variables, and with generalized Gauss–Laguerre quadrature. The executed Q-versus-w absolute differences are at most about `3.1e-32 GeV^-2`. Such numerical agreement is not a QCD modeling uncertainty.

A triangle bound on the finite polylogarithm expression gives a conservative per-flavor absolute current cap of about `13.34 GeV^2` on the declared hard/scale domain. It bounds the absolute omitted contribution between the finite-window endpoint and Q=80 by approximately `8.91e-43`, `7.91e-43`, and `7.01e-43 GeV^-2` for 11/12/22. This handles the signed current by bounding its absolute value. It does not bound the physical spectrum above Q=80, and floating-point evaluations are not directed-rounding certificates.

The first combined suite passed 108 tests. Adding the separate published-table consistency check brought the final suite to **109 tests: 33 new, 22 inherited from Note 40, 26 from Note 42 and 28 from Note 43; zero failures/errors**. No physics formula or test tolerance was changed after the initial run. The original separate Note-41 suite was not rerun. These are mathematical/software checks, not independent physical validation or a whole-repository audit.

```
python -m unittest -v test_research_note_40.py test_research_note_42.py test_research_note_43.py test_research_note_44.py
python mixed_gluon_nlo.py
```

The four inherited modules match their live GitHub blob identifiers at the pinned head. The two new files have **locally calculated**, not remotely published, blob identities:

```
mixed_gluon_nlo.py:       0ffc28870c414cc8613d28549511d10bcaf30ee7
test_research_note_44.py: 4e4199ecaf308a260e2e4619557dd28198536b53
```

The package includes all required modules, complete results, logs, file hashes and a four-file patch. Its execution record distinguishes local tests from the unsuccessful publication attempt. No source supplement or external numerical program was executed; the printed source formulas were used, with the scale extension derived as above.

## 7. Remaining work

The coherent bottom/charm-square NLO correction is now the next missing gluonic amplitude sector; the remaining mixed heavy-final-state cuts require a compatible treatment. Conversion scatterings, kinetic assumptions, complete channel inventory, expansion/entropy history and initial conditions remain necessary before interpreting any coupled abundance evolution.

No new Omnes arrays, heavy-singlet hadronic width, total lifetime, H2 optical signal, experimental exclusion or empirical validation was produced. Earlier notes and archive PDFs remain unchanged.

## Primary references and source separation

[1] J. Wang and Y. Wang, *Analytic Result of Higgs Boson Decay to Gluons with Full Quark Mass Dependence*, arXiv:2503.22169v2 (2025), Eqs. (3)–(10), Table 1 and the cut definitions. https://arxiv.org/html/2503.22169v2 . Supplies the mixed-sector hard formula and independent published limits, not support for the hypothetical singlets.

[2] M. Spira, A. Djouadi, D. Graudenz and P. M. Zerwas, *Higgs Boson Production at the LHC*, arXiv:hep-ph/9504378v1, Eq. (31). https://arxiv.org/html/hep-ph/9504378 . Supplies the heavy-top Wilson matching factor, not a complete correction by itself.

[3] A. Behring and W. Bizon, *Higgs decay into massive b-quarks at NNLO QCD in the nested soft-collinear subtraction scheme*, arXiv:1911.11524v1, Sec. 2.5 and Appendix B.2. https://arxiv.org/html/1911.11524 . Used for mass-conversion conventions; its NNLO calculation is not reproduced here.

Internal lineage: Notes 39–43 in `Cbaird26/mqgt-scf-continued` at `f6d68d2ce4cdbcb2efa52691d0f6b8dd70409d1a`. The application, explicit convention/scale derivation, source checks and numerical implementation are the work of this addendum; the underlying QCD ingredients remain those of the cited authors.
