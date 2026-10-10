# Research Note 47 — Coherent three-gluon real radiation and an explicit source-normalization audit

**10 October 2026 | Scientific-development draft; not peer reviewed.** Prepared for Christopher Michael Baird with ChatGPT (ZoraASI) assistance in source checking, derivation, implementation and testing. This is a conditional calculation in the hypothetical two-real-singlet Higgs portal, not a validated Theory of Everything, a complete NLO gluonic rate, or an abundance prediction.

## 1. What this adds after Note 46

The review branch was read at `1abb5e2769dc77657ed6080e2c0c2ce1e0d77cbf`. Note 46 supplies the mass-dependent finite virtual coefficient; the two separate Note-45 lineages supply a light-pair real remainder (45-real) and RG/mass-convention consistency conditions (45-RG). This note implements the previously missing **coherent bottom/charm-loop three-gluon real-emission remainder**, retaining mass dependence in the published helicity combinations.

During source matching, a normalization inconsistency was found between the printed decay subtraction in Spira et al. [1], Eq. (C.14), and that paper's stated amplitudes and limiting formulas. The PDF was inspected directly, including printed pages 41–43; this is not merely an HTML transcription issue. We preserve the source's helicity definitions, derive the decay normalization separately, and explicitly distinguish that reconstruction from the printed formula. No author confirmation or official erratum was obtained. This is a documented source-consistency finding and proposed reconstruction, not an assertion that the authors endorsed our implementation.

The result below is a finite, subtraction-dependent part of a real correction. It is neither the positive resolved three-gluon rate nor the complete NLO correction. It must be matched to the virtual coefficient and integrated subtraction before forming a physical total.

## 2. Inputs and amplitude conventions

Retain the unfitted benchmark and frozen historical comparison inputs:

```
m1=10, m2=11.5, mh=125, fixed Gamma_h=0.0041, v=246 [GeV];
K11=K22=0.001, K12=-0.001;
alpha_s(MZ)=0.1189, MZ=91.1876 GeV;
mbar_b(10 GeV)=3.610 GeV, mbar_c(3 GeV)=0.986 GeV.
```

The inherited two-loop-truncated running and continuous four/five-flavor matching at 4.163 GeV are unchanged. These are not new fits or latest-measurement claims. The central prescription uses the inherited running mass in both the Yukawa coupling and each loop propagator at mu=Q. A separate `pole1` comparison uses Note 42's fixed auxiliary one-loop pole estimates in both positions. It is a sensitivity diagnostic, not a precision pole-mass determination. A mass redefinition of this order-alpha_s^3 real remainder changes it first at the next order, but the complete rate also requires the corresponding Born/virtual convention matching.

For the massless three-gluon final state, let

```
x=s/Q^2, y=t/Q^2, z=u/Q^2=1-x-y;  x,y,z>0,
S=s/m_q^2, T=t/m_q^2, U=u/m_q^2, rho=S+T+U=Q^2/m_q^2.
```

These x,y,z are invariant ratios, **not** the source's energy fractions x1,x2,x3 and not the incoming singlet labels 11,12,22. The linear transformation from Eq. (C.16) has unit absolute Jacobian and gives the same full triangle.

Equations (C.5)–(C.10) of [1] define four CP-even combinations C_i. Their rational coefficient matrix, triangle functions, scalar boxes, and overall `1/(2 rho^2)` are retained in `coefficients` and `helicities`. For bottom and charm loops,

```
A3 = sum_(i=1)^4 |C_i,b + C_i,c|^2,
B  = |F_b+F_c|^2,
P  = 1+x^4+y^4+z^4,
```

where the two-gluon F is normalized to one for an infinitely heavy loop quark. The source sums loop amplitudes before squaring. Our bb, cc and signed bc pieces keep that coherence; no top amplitude is included here.

## 3. Audit of the printed subtraction

Expressed in these invariant ratios, the braces of printed Eq. (C.14) are

```
[A3/B - P/2]/(x*y*z).                         [source as printed]
```

Expanding the stated CP-even combinations in the heavy-loop limit gives

```
C_1 -> x^2, C_2 -> -y^2, C_3 -> z^2, C_4 -> 1,
A3/B -> P.
```

The literal printed integrand therefore tends to `P/(2*x*y*z)`, rather than zero. It also leaves a nonzero collinear pole. This contradicts its intended use as a finite mass-dependent remainder vanishing in the heavy-quark limit. The code preserves `printed=True` solely as a failing-consistency diagnostic, not as an integrable physical result.

As a separate normalization check, using the same source amplitudes in the production formula (C.4) reproduces the independently printed heavy-mass coefficient in Eq. (42):

```
3 * integral_0^1 dv [-4+6v-4v^2+2v^3] = -11/2.
```

Thus simply rescaling all C_i by 1/sqrt(2) to hide the decay mismatch would break that production check. We do not alter the source's C_i or its historical text. The following normalization is a separate derivation, not a silent substitution into a quoted equation. No claim about all other printed formulas is made.

## 4. Independent decay normalization and finite subtraction

For two hard gluons in a color singlet, the standard soft eikonal current [2], Eqs. (4.3)–(4.5), gives the color-summed squared-amplitude ratio

```
|M3|^2/|M2|^2 -> 4*g_s^2*C_A*s12/(s13*s23),  C_A=3.
```

The soft current acts on the leading loop-induced Born amplitude; there is no lower-order Hgg tree amplitude in this full-theory sector. Since `A3/B -> 2` in that soft limit, the common normalization multiplying the stated helicity shape is

```
|M3|^2/|M2|^2 = (8*pi*alpha_s*C_A/Q^2) * (A3/B)/(x*y*z).
```

This uses the source's full momentum-dependent helicity shape, with its common normalization fixed by the soft limit; it does not approximate the full hard amplitude by its soft value.

The labeled massless phase spaces, with overall orientation integrated, are

```
Phi2 = 1/(8*pi),
dPhi3 = Q^2/(128*pi^3) dx dy,
Phi3 = Q^2/(256*pi^3).
```

Including `1/3!` for three identical gluons versus `1/2!` for the two-gluon Born final state yields

```
dGamma3/Gamma2_LO = [alpha_s*C_A/(6*pi)] * (A3/B)/(x*y*z) dx dy
                 = (a/2) * (A3/B)/(x*y*z) dx dy, a=alpha_s/pi.
```

Subtract the Born-matched heavy-limit shape **with that same normalization**. The additive coherent definition used in this note is

```
J_3g,bc(Q) = (1/2) integral_triangle dx dy [A3-P*B]/(x*y*z),
Delta S_3g,finite(Q) = (a^3*Q^2/9) J_3g,bc(Q),
S = 8*pi*v^2*Gamma/Q.
```

The additive form avoids division by a possibly vanishing coherent Born amplitude. The subtraction removes the leading soft/collinear singular terms. Its integral is a signed difference, not an event probability. The subtracted Born-like contribution is **not discarded**: it belongs in the compatible integrated-subtraction plus virtual assembly. Other finite subtraction conventions can move finite terms between pieces.

## 5. Analytic continuation and numerical controls

All dimensionless invariants use the common positive infinitesimal implied by `m_q^2 -> m_q^2-i0`. The source scalar box J is evaluated in dilogarithms, with rationalized small roots. As an independent numerical representation, we derived and checked

```
J(S,T,U) = integral_0^1 dxi {
 ln[1-S*w-i0] + ln[1-U*w-i0] - ln[1-rho*w-i0]
 }/[T+S*U*w],  w=xi*(1-xi), rho=S+T+U.
```

The separate logarithms retain their individual branches; replacing them by a single principal logarithm of their product is not generally valid. The logarithmic roots are split explicitly in the reference quadrature. A separate three-dimensional Feynman-parameter box below threshold and 55-digit triangle-function values provide additional checks. These do not independently transcribe every rational helicity coefficient or constitute an independent diagram calculation.

Bose symmetry reduces the triangle to six equal sectors `x<=y<=z`, with `0<x<1/3` and `x<y<(1-x)/2`. Integration partitions follow the internal branch points `x,y,z=4m_q^2/Q^2`. Those are loop branch points, not masses of emitted gluons. The y intervals use sine-squared maps; the x intervals use a linear map to avoid sampling excessively close to cancellation-dominated floating-point endpoints. Angular node scans, direct collinear/soft checks and infinitesimal-prescription comparisons test this numerical choice. They are convergence diagnostics, not rigorous directed-rounding or global endpoint-error certificates.

The inherited unequal-mass Maxwell–Boltzmann thermal kernel is unchanged. Hard energies are restricted to Q in [20,80] GeV, scales mu/Q in [1/2,2], and T in [1/3,0.5] GeV. Results integrate only `w=Q/T-(mi+mj)/T` in [0,90]. Generalized Gauss–Laguerre integration with scaled Bessel functions is checked against a distinct Q-variable integration with unscaled Bessel functions. No physical high-energy continuation to infinity is asserted.

## 6. Finite-window numerical results

At assumed T=0.5 GeV and central mu=Q, the fine calculation (48 angular nodes per subinterval; 32 thermal nodes) gives:

| Incoming pair | bb remainder | cc remainder | bc interference | Coherent finite three-gluon remainder |
|---|---:|---:|---:|---:|
| 11 | -6.64819e-19 | +4.73068e-20 | +3.79969e-19 | **-2.37543e-19** |
| 12 | -5.16215e-19 | +4.56887e-20 | +3.67994e-19 | **-1.02533e-19** |
| 22 | -3.80670e-19 | +4.36943e-20 | +3.55810e-19 | **+1.88344e-20** |

All entries have units GeV^-2. Pairwise thermal inputs require the declared common-temperature distributions, not an established single-equation chemical-equilibrium reduction. Only under the additional, still-unestablished equilibrium weighting do they combine to

```
bb: -6.47856965281e-19,
cc: +4.71203691952e-20,
bc: +3.78597685412e-19,
coherent finite remainder: -2.22138910673e-19 [GeV^-2].
```

The sign differences are permissible for this subtracted piece. They are not negative event counts, new observations, or a complete NLO shift. Extra numerical digits in the JSON document reproducibility rather than physical precision.

The default 32-angular/24-thermal calculation gives `-2.22139168845e-19 GeV^-2` after the same conditional weighting. Refinement changes that central sum by about 1.2 parts per million; this is only a quadrature comparison. The independent Q evaluation agrees much more closely when the same angular discretization is retained, so it cannot by itself estimate the angular integration error.

| Prescription | Conditional coherent finite remainder [GeV^-2] |
|---|---:|
| mu=Q/2, running masses | -6.63675e-19 |
| mu=Q, running masses, default quadrature | -2.22139e-19 |
| mu=2Q, running masses | -5.73360e-20 |
| mu=Q, auxiliary pole1 masses | -9.70871e-19 |

These are scale/convention sensitivities of an isolated finite component, not confidence intervals or an uncertainty envelope for a completed rate. No new completed sum with Notes 44–46 is formed.

## 7. Executed verification and provenance

The Note-46 archive was extracted without modifying its source files, and all 32 manifest entries were checked against their recorded sizes and SHA-256 values. The inherited modules remain unchanged. Four new source/reproducer files have Git blob identities:

```
three_gluon_remainder.py: e0fb6fd3964b67324289b3de86f38e7afc85e789
three_gluon_reference.py: dad9b0d56c37fb469a32d56551f923cedfd1507b
test_research_note_47.py:  b735ed15591d97c3623ed296f792939b54f8dcb7
reproduce_note47.py:      b04f5738c4f868d4818d3e0ff73e9c41444a680e
```

The first new 26-test suite had one failed assertion: a finite-x test compared the printed residual with only its asymptotic leading term too tightly. It was replaced by the exact identity `x*printed-P*B/(2*y*z)=2*x*matched`, retaining a separate small-x convergence check. The physical implementation was not changed by that repair, and no numerical integration tolerance was loosened. The failed log is preserved. An earlier synchronous long numerical run timed out before completion; the subsequent complete run produced all six prescriptions and all three pairs.

The final combined suite passed **197 tests: 26 new, 32 from Note 46, 30 from 45-RG, 33 from Note 44, 28 from Note 43, 26 from Note 42 and 22 from Note 40**. After the four new GitHub blobs returned the same identities as the local files, those matching bytes were rerun. The execution record preserves that result and runtime versions.

The live 45-real test suite and the original standalone Note-41 suite are **not** included in this count. This is not a whole-repository audit or empirical validation. No external HDECAY/HIGLU/RunDec executable, unsafe input loader, detector likelihood or Boltzmann solver was run.

```
python -m unittest -v test_research_note_40.py test_research_note_42.py test_research_note_43.py test_research_note_44.py test_note45_rg_matching.py test_research_note_46.py test_research_note_47.py
python reproduce_note47.py             # all six numerical prescriptions
python reproduce_note47.py central     # only the three central pair calculations
```

Publication is evidenced by the later commit/ref receipt, not merely by blob creation. The package includes required dependencies, test logs, complete numerical output, source hashes and an additions-only patch. Historical notes and main are not replaced.

## 8. Next assembly

The mass-dependent three-gluon finite remainder is now explicit, with a documented normalization reconstruction and its checks. The next task is a common decay assembly of the virtual term, three-gluon remainder, light-pair remainder, and universal/integrated subtraction, with the real-heavy-flavor convention matched consistently. Source-normalization review remains especially important before calling that assembled result complete.

The broader two-singlet reaction network, conversions, kinetic/cosmological history and initial conditions remain separate requirements for an abundance prediction. No Omnes input, heavier-singlet hadronic width or lifetime, H2 optical observable, detector exclusion, DOI or empirical confirmation was produced here.

## Primary sources and attribution

[1] M. Spira, A. Djouadi, D. Graudenz and P. M. Zerwas, *Higgs Boson Production at the LHC*, arXiv:hep-ph/9504378v1, Appendix C Eqs. (C.4)–(C.17), Eq. (42), and the heavy-loop limit in Sec. 2.2. https://arxiv.org/pdf/hep-ph/9504378 . Printed pages 41–43 were inspected, including the normalization at issue. The amplitudes are source-derived; the explicitly reconstructed decay normalization is not presented as the printed C.14 or an author-confirmed erratum.

[2] S. Catani and M. H. Seymour, *A General Algorithm for Calculating Jet Cross Sections in NLO QCD*, arXiv:hep-ph/9605323v3, Eqs. (4.3)–(4.5) and Sec. 4. https://arxiv.org/html/hep-ph/9605323 . Supplies the general soft current and the need for consistent subtraction, not the finite massive three-gluon calculation performed here.

[3] R. V. Harlander and P. Kant, *Higgs production and decay: Analytic results at next-to-leading order QCD*, arXiv:hep-ph/0509189, Eqs. (3.4)–(3.7). https://arxiv.org/abs/hep-ph/0509189 . Identifies the separate virtual contribution already implemented in Note 46; no complete virtual/real matching is inferred from this citation alone.

Internal lineage: Notes 40–46 at the pinned review-branch head, including the crosswalk between 45-real and 45-RG. The sources provide established QCD ingredients, not support for the proposed singlets or consciousness/ethics interpretations.
