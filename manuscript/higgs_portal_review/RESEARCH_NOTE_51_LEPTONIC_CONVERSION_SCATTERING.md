# Research Note 51 — Finite-mass lepton conversion scattering and the chemical-equilibrium timescale

**12 October 2026 | Scientific-development draft; not peer reviewed.** Prepared for Christopher Michael Baird with ChatGPT (ZoraASI) assistance in derivation, source comparison, implementation, numerical testing, and drafting. This calculation concerns the restricted hypothetical two-real-singlet Higgs portal. It neither establishes the particles nor supplies a Theory of Everything or a dark-matter abundance.

## 1. A physically new conversion contribution

Note 50 independently checked normalization and universal subtraction ingredients of the selected gluonic annihilation assembly. Its next task was the conversion network, not another adjustment to that QCD number. This note computes the **charged-lepton bath-scattering partial**

```
s2 + l^+/- <-> s1 + l^+/-,      l=e,mu,tau,
```

from the already declared off-diagonal Higgs portal. This is not inferred by multiplying the old leptonic decay width by an arbitrary enhancement. It is a separate tree amplitude with its own thresholds, phase space, thermal average, and reaction density.

At the inherited illustrative point and assumed T=0.5 GeV, the kinetic Maxwell–Boltzmann calculation gives a scattering population-relaxation rate **1.76277 H**, compared with **0.00115650 H** for the inherited leptonic-decay partial. Tau scattering supplies **99.1168%** of this scattering rate. Tau-pair emission in the compressed decay is forbidden, but a tau already in the bath can scatter and remain a tau. These are different kinematic questions.

This does not by itself prove chemical equilibrium. At that temperature the chosen cooling law gives an equilibrium heavy-fraction logarithmic change of **2.81786 H**, faster than this partial relaxation. At lower temperatures the computed scattering rate decreases below H. The calculation now quantitatively demonstrates why the previous decay-only timescale could not stand in for the conversion network.

## 2. Model and thermal assumptions

Retain the unfitted benchmark:

```
m1=10 GeV, m2=11.5 GeV, mh=125 GeV, K12=-0.001.
L_int contains -v K12 h s1 s2 -(ml/v) h lbar l.
me=0.00051099895, mmu=0.1056583755, mtau=1.77686 [GeV].
```

Masses and couplings are inherited fixed inputs, not new measurements, fits, or predictions of a unification theory. For the expansion comparison keep the earlier **assumed** radiation-dominated `g*=60` and non-reduced `M_Pl=1.2209e19 GeV`:

```
H(T)=sqrt(8*pi^3*g*/90) T^2/M_Pl.
```

This is not a newly computed QCD equation of state. The reported domain is `1/3 <= T <= 0.5 GeV`. The moving-target comparison additionally assumes entropy degrees of freedom constant enough that `T proportional to a_cosmic^-1`; this is a chosen cooling law, not a measured history.

Initial singlets have dilute, common-temperature kinetic MB shapes, with arbitrary number-density normalizations. The bath leptons have zero chemical potential and initially MB occupations. Final-state Pauli blocking and Fermi–Dirac bath occupations are bracketed separately in Section 6. Thermal dispersion corrections, other plasma effects, and radiative corrections are not included. The scalar momentum distributions have not been dynamically shown to be thermal.

Both lepton charges and both spin states are counted, `g_l=4` per flavor. This degeneracy belongs to the bath reaction density. It is not an extra factor in the spin-averaged cross section. These assumptions follow the same distinction between kinetic and chemical equilibrium made in the conversion literature [1,2]; the literature's model and parameter results are not transplanted into ours.

## 3. Exact tree amplitude, threshold, and integrated cross section

Let `t=(k-k')^2<=0` for the incoming/outgoing lepton momenta. The one-Higgs-exchange amplitude and initial-spin average give

```
M = K12 ml/(t-mh^2) * ubar(k')u(k),
(1/2) Tr[(kslash'+ml)(kslash+ml)] = 4ml^2-t,

|M|^2_averaged = K12^2 ml^2 (4ml^2-t)/(mh^2-t)^2.
```

The antiparticle trace gives the same result. The factors v cancel. The exchanged Higgs is spacelike; there is no propagator pole and **no timelike Higgs width is inserted**. The default calculation does not replace the propagator with a contact interaction. A contact result is retained only for comparison.

For `s_i l -> s_j l`, set `q=sqrt(s)` and

```
lambda_i(s)=[s-(mi+ml)^2][s-(mi-ml)^2],
p_i=sqrt(lambda_i)/(2q),  p_f=sqrt(lambda_j)/(2q),
E_l,i=(s+ml^2-mi^2)/(2q), E_l,f=(s+ml^2-mj^2)/(2q),

t_+/-=2ml^2-2 E_l,i E_l,f +/- 2 p_i p_f,
q0=max(mi,mj)+ml.
```

The forward endpoint is rationalized in the implementation to avoid electron-mass cancellation. At fixed initial scalar at rest, upconversion requires total lepton energy

```
E_l,min = [(m2+ml)^2-m1^2-ml^2]/(2m1)
        = 1.6125 + 1.15 ml [GeV].
```

This is not merely the 1.5-GeV rest-mass gap; recoil matters. The full thermal calculation averages both incoming momenta rather than fixing the scalar at rest.

The cross section and its smooth reduced kernel are

```
d sigma_i->j/dt = |M|^2_averaged/(16*pi*lambda_i),
W(s) := lambda_i*sigma_i->j
      = K12^2 ml^2/(16*pi) * I(s),

I(s)=integral_(t_-)^(t_+) dt (4ml^2-t)/(mh^2-t)^2.
```

I is dimensionless and W has units GeV^2. An antiderivative is

```
(4ml^2-mh^2)/(mh^2-t) - ln(mh^2-t),
```

where the logarithm's arbitrary unit cancels in the definite difference. A stable difference-of-logarithms/series implementation is independently checked by center-of-mass angular quadrature and a 60-digit direct integral.

The same physical t interval occurs in the reverse process, proving

```
lambda_2 sigma_2->1 = lambda_1 sigma_1->2 = W.
```

No identical-initial-pair factor 1/2 applies to a scalar and a lepton. The exothermic cross section can diverge as 1/p_i at the endpoint, but W vanishes there and the thermal integral is finite.

## 4. Thermal reaction density and population operator

The invariant MB reaction-density formula [1, Eq. (7); 2] becomes

```
gamma_l(T) = g_l T/(32*pi^4)
             integral_(q0^2)^infinity ds W(s)/sqrt(s) K1(sqrt(s)/T)
           = g_l T/(16*pi^4)
             integral_q0^infinity dq W(q^2) K1(q/T).

n_i,eq = mi^2 T K2(mi/T)/(2*pi^2),
Gamma_i->j = gamma_l/n_i,eq.
```

The reaction density has units GeV^4, the per-scalar rate Gamma has units GeV, and `n_i,eq` here normalizes a kinetic shape. It is **not** the assertion that the actual scalar density equals its equilibrium value. For arbitrary fugacities multiplying those shapes, the collision operator is

```
J = Gamma_down n2 - Gamma_up n1,
C1=+J, C2=-J.
```

Total odd-particle count `N=n1+n2` is conserved by these conversions. Equal forward and reverse equilibrium reaction densities imply

```
Gamma_up/Gamma_down = q_eq(T) := n2,eq/n1,eq,
Lambda_sc = Gamma_down+Gamma_up = (1+q_eq) Gamma_down.
```

Lambda_sc is the nonzero population-relaxation eigenvalue at fixed T, not the inverse-event rate per light particle. This reproduces the distinction of Note 31 using **newly calculated scattering rates**.

The primary integration uses `w=(q-q0)/T` in [0,90] and scaled Bessel functions. A separate q/CM-angle formulation uses ordinary Bessel functions and the unintegrated amplitude. Eighteen direction/flavor/temperature comparisons agree to a largest relative difference of about `3.89e-15`. They are independent numerical representations of this derived tree process, not independent physical evidence.

## 5. Rates and cooling-timescale comparison

At T=0.5 GeV, `H=2.63320146442e-19 GeV`, the per-heavy-singlet downconversion rates, including both charges and spins, are:

| Bath flavor | Gamma_down [GeV] | Gamma_up [GeV] | Gamma_down/H |
|---|---:|---:|---:|
| e | 9.06150630408e-26 | 5.49913527770e-27 | 3.44125e-7 |
| mu | 3.86472172210e-21 | 2.34537469239e-22 | 0.0146769 |
| tau | 4.33751475972e-19 | 2.63229750466e-20 | 1.64724 |

The sum is `Gamma_down=4.37616288309e-19 GeV`. The equilibrium ratio is `q_eq=0.0606867676649`, hence `Lambda_sc/H=1.76277361454`. The tau share is 0.991168490661 even though `m2-m1=1.5 < 2 mtau=3.55372 GeV`: the scattering reaction does not create a tau pair out of the mass gap.

The comparison with earlier decay work retains the inherited vacuum **e+mu partial width**, `Gamma_lep=3.060267688e-22 GeV`. Its MB time-dilation factor `K1(m2/T)/K2(m2/T)` is applied as in [1, Eq. (8)]. It is not recalculated here and is not the total vacuum width.

| T [GeV] | Lambda_sc/H | Inherited MB decay Lambda/H | Scatter + inherited decay Lambda/H | abs(d ln r2_eq/dt)/H |
|---|---:|---:|---:|---:|
| 0.5 | 1.762774 | 0.00115650 | 1.763930 | 2.817860 |
| 0.4 | 0.703797 | 0.00177471 | 0.705572 | 3.636446 |
| 1/3 | 0.291862 | 0.00253928 | 0.294402 | 4.432100 |

Under the selected cooling law, with `x_i=mi/T`,

```
abs(d ln r2_eq/dt)/H
 = [x2 K1(x2)/K2(x2)-x1 K1(x1)/K2(x1)]/(1+q_eq).
```

At T=.5, including scattering increases this selected population-relaxation partial by a factor of about **1525** compared with the prior decay-only partial. This is a ratio of calculated restricted-model rates, not an observed enhancement.

In the same restricted model the equation `(Lambda_sc+Lambda_decay)/H=1` has a numerical root `T=0.433568344577 GeV`. **This is not a freeze-out temperature or a relic-density calculation.** Hubble crossing alone does not justify rapid tracking of a changing equilibrium fraction. No coupled number evolution, initial-condition choice, or abundance fitting is performed here.

## 6. Quantum-statistical bracket and numerical versus physical uncertainty

A bound avoids silently assuming that the MB bath is exact. For on-shell zero-chemical-potential bath leptons with E,E'>=ml,

```
f_FD(E) [1-f_FD(E')]/exp(-E/T)
 = 1/[(1+exp(-E/T))(1+exp(-E'/T))],

(1+exp(-ml/T))^-2 <= ratio <= 1.
```

Multiplying by the positive squared amplitude and remaining positive phase space preserves the inequalities. Keep the scalar distributions dilute kinetic MB and their vacuum dispersion relations; no final-state scalar Bose enhancement is included. Thus the **scattering-only** population-relaxation rate with a FD bath and Pauli blocking lies within:

| T [GeV] | FD-scattering Lambda/H lower bound | MB upper bound |
|---|---:|---:|
| 0.5 | 1.656092 | 1.762774 |
| 0.4 | 0.680654 | 0.703797 |
| 1/3 | 0.284028 | 0.291862 |

This is a derived statistics bracket inside the stated dispersion/kinetic assumptions, **not** an empirical confidence interval, a complete thermal-QFT bound, or an explicit numerical integration of the full FD collision term. The inherited MB decay contribution is not included in this bracket and has not been assigned its own finite-density correction here.

At .5 GeV, the tau downconversion contact approximation is 1.00220 times the exact-propagator result. Holding the initial heavy scalar at rest instead gives 0.971296 times the kinetic-MB result. These diagnostics test different approximations and must not be presented as an uncertainty band or a demonstration of kinetic equilibrium.

For the positive mathematical tree/MB kernel the omitted integration tail can be bounded. Since `-s<=t<=0` in this mass domain,

```
I(s) <= [4 ml^2 s + s^2/2]/mh^4.
```

Also `exp(y)K1(y)` decreases with y. Integrating the resulting polynomial times exp(-w) above W gives an incomplete-Gamma-function bound. For the central tau downconversion the W=90 tail is below `2.86e-54 GeV`, roughly `6.6e-36` of the computed rate. This bounds the extension of **this mathematical vacuum-tree/MB integrand**, not neglected high-order interactions or the physical spectrum of a completed theory. Float evaluations are not directed-rounding certificates.

## 7. Collision inventory and actual next calculation

The accompanying `COLLISION_INVENTORY_NOTE_51.json` separates twelve minimal reaction classes. It is a scoped working inventory, not an exhaustive all-orders operator census.

- Number-changing: existing 11/12/22 leptonic partials; direct heavy-quark and selected gluonic contributions; missing compatible heavy cuts, light-quark and other Standard Model contributions; early Higgs production and any relevant higher-multiplicity dark reactions.
- Composition-changing: inherited leptonic decays; missing hadronic and other widths; **new charged-lepton scattering**; missing bath quark/gluon/hadron scattering; and density-dependent internal conversions such as `s2 s2 <-> s1 s1`.
- Kinetic: elastic and inelastic momentum-transfer kernels, which are not fixed by an event-count rate.

The previously computed vacuum timelike annihilation current is not automatically the spacelike, finite-temperature current required for scattering from the bath. The next calculations should treat those kinematics and the thermal medium explicitly, then check momentum relaxation rather than presuming the scalar MB shape. Initial conditions, entropy/expansion history, and a complete number-changing network remain necessary to determine the absolute abundance.

## 8. Execution, source separation, and publication

The attached Note-50 archive was extracted without source edits and all **52 manifest entries** were verified. Its 277-test inherited chain passed again. The new source is self-contained apart from SciPy and does not import the old QCD implementation. Frozen model inputs and the prior decay-width value are the explicit inherited physics inputs.

The **first 31-test new suite passed**; no new physics formula or assertion tolerance was changed afterward. The combined run passed **308 tests: 31 new plus 277 inherited, zero failures/errors**, in 35.107 seconds as reported by unittest. After new GitHub blob IDs matched local bytes, the 31 new tests were rerun successfully on those matching bytes. The three matched source identities are:

```
leptonic_conversion_scattering.py: 6ba9dcd73f7ef7325e939cebbcf0e6d482a341b3
test_research_note_51.py:          9de2313af2462d47ddaea758d325eeb844f2155c
reproduce_note51.py:              f9bfa07a278bd8e52140c6dd7d5556f6ed32865a
```

Checks include the Dirac spin trace, particle/antiparticle agreement, physical and reversed t limits, a 60-digit t integral, two thermal representations, event degeneracy, threshold behavior, detailed balance, contact and stationary diagnostics, the FD bound, number conservation, the relaxation eigenvalue, and explicit refusal of an unsupported relic-density result.

The inherited 277-test count uses the attached local Note-49 lineage, not the alternate live Note-49 implementation. Neither the original standalone Note-41 suite nor the live 45-real suite is included. This is not a whole-repository audit or experimental validation.

An initial terminal-tool request failed before execution; Python filesystem access and subprocess execution succeeded. No incomplete attempt is counted as a passing test. The execution record gives hashes, exact commands, versions, and logs. The later commit/ref receipt and clean-package validation are separate records; blob creation by itself is not branch publication. Historical notes, PDFs, and main are not rewritten.

No new Omnes arrays, heavier-singlet vacuum hadronic width or total lifetime, H2 optical response, detector likelihood, journal submission, DOI, or empirical confirmation was produced.

## Primary and internal sources

[1] M. Garny, J. Heisig, B. Lulf and S. Vogl, *Coannihilation without chemical equilibrium*, Phys. Rev. D 96 (2017) 103521, arXiv:1705.09292v2, Eqs. (3)-(8) and kinetic-equilibrium discussion. https://arxiv.org/html/1705.09292v2 . Supplies general thermal reaction-density and coupled-conversion conventions, not the two-singlet result or our tau rate.

[2] J. Edsjo and P. Gondolo, *Neutralino Relic Density including Coannihilations*, Phys. Rev. D 56 (1997) 1879, arXiv:hep-ph/9704361. https://arxiv.org/html/hep-ph/9704361 . Primary invariant thermal-averaging framework; no neutralino-model abundance is imported.

Internal: `thermal_conversion_gate.py` at live commit `451e10ae2249e12d13c2ceb1f6b41184b9e21eb8` supplies the prior decay partial and expansion convention; Notes 31,38,39 explain population versus event rates and pair bookkeeping. Note 50 and its attached package supply the verified previous state and test lineage. The new amplitude integration, FD bracket, numerical scattering rates, and inventory are this addendum's bounded extension. Standard QFT inputs do not validate the proposed singlets or interpretive field labels.
