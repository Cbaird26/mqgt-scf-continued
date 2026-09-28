# Research Note 40 — A leading-power bottom/charm QCD contribution to two-singlet thermal annihilation

**28 September 2026 | Public scientific-development addendum; not peer reviewed.** Human author: Christopher Michael Baird. ChatGPT (ZoraASI) assisted with source review, derivation, implementation and numerical checks. This is a conditional calculation in the restricted two-singlet Higgs-portal model, not a validated Theory of Everything, new-particle observation, complete hadronic calculation or relic-density prediction.

## 1. Two different energy ranges require different hadronic inputs

Note 39 supplied the charged-lepton thermal contributions for initial pairs 11, 12 and 22. Here we calculate an approximate bottom- and charm-quark scalar-current contribution for those same pairs. It uses published perturbative-QCD coefficients and newly implemented running, rather than an invented missing hadronic spectrum.

The inherited illustrative masses are m1=10 GeV and m2=11.5 GeV. Their annihilation energies begin at Q=sqrt(s)=20, 21.5 and 23 GeV. In contrast, the compressed heavy-state decay s2 -> s1 + X allows the produced SM system only Q <= m2-m1=1.5 GeV. Blackstone et al. [1] study low-energy pion/kaon channels up to approximately 2 GeV. Their Omnes data must not be extrapolated into the annihilation range.

The complete pinned Omnes files were still not obtained in this step: public raw retrieval was blocked, and a container acquisition attempt failed DNS resolution. Therefore no heavy-state hadronic decay width or change to its previous lifetime ceiling follows from this note. The higher-energy annihilation calculation is a separate task.

## 2. Declared external inputs and approximation order

Keep Note 24/39's unfitted portal benchmark:

```
m1=10, m2=11.5, mh=125, Gamma_h=0.0041, v=246 [GeV];
K11=+0.001, K12=-0.001, K22=+0.001.
```

For this reproducible comparison, choose the historical central inputs from Chetyrkin et al., arXiv:0907.2110v2, Section IV [2]:

```
alpha_s(MZ)=0.1189, MZ=91.1876 GeV;
mbar_b(10 GeV)=3.610 GeV; mbar_c(3 GeV)=0.986 GeV.
```

These are explicitly fixed historical inputs, not the latest determinations, parameters derived by MQGT-SCF, or a new fit. Input uncertainties and their correlations are not propagated. Use a declared bottom matching scale of 4.163 GeV, four active flavors below it and five above, with continuous coupling/mass matching. Higher-order threshold matching is omitted.

Implement the first two beta and mass-anomalous-dimension coefficients in [3], with a=alpha_s/pi and t=ln(mu^2):

```
da/dt = -beta0*a^2 - beta1*a^3;
d ln(mbar)/dt = -gamma0*a - gamma1*a^2;
beta0=(11-2*nf/3)/4; beta1=(102-38*nf/3)/16;
gamma0=1; gamma1=(202/3-20*nf/9)/16.
```

The implicit coupling solution and integrated mass ratio are checked against a separate differential-equation solver. Exactness of an implicit solution refers only to these truncated equations, not to exact QCD. At mu=20 GeV this implementation gives alpha_s=0.1548302, mbar_b=3.308101 GeV and mbar_c=0.738035 GeV.

The hard scalar-current correction is retained only through next-to-leading order (NLO) in alpha_s and at leading power in the quark-mass-to-energy ratio. The high-energy coefficient in [4] gives R=1+(17/3)a at mu=Q. Renormalization-group invariance of mbar(mu)^2 R restores the scale logarithm:

```
R_q(Q,mu)=1 + alpha_s(mu)/pi * [17/3 + 2 ln(mu^2/Q^2)],
S_q(Q,mu)=3 mbar_q(mu)^2 R_q(Q,mu),  q=b,c.
```

The factor 3 is color multiplicity. The logarithm cancels the leading scale derivative of the squared running mass; this cancellation is tested. The inclusive correction contains the real/virtual q qbar(g) contribution at this order. Adding a separate q qbar g rate to the same contribution would double count it. Gluon-current, higher-order interference and other omitted contributions are not supplied by this coefficient.

## 3. Insert the scalar-current weight into the inherited thermal kernel

Use Note 39's single-Higgs-exchange amplitude and define

```
D(s)=(s-mh^2)^2+(mh Gamma_h)^2,
lambda_ij(s)=[s-(mi+mj)^2][s-(mi-mj)^2].
```

Replacing its leptonic weight mf^2 beta_f^3 by S_q gives the leading-power quark-current approximation

```
sigma_ij^(q)(s)=Kij^2 s S_q(sqrt(s),mu)
               /[8 pi D(s) sqrt(lambda_ij(s))].
```

Equivalently, a unit Higgs-current partial width Gamma_h*(Q)=Q S_q/(8 pi v^2) gives the same normalization through the spectral formula. This equality and recovery of the previous leptonic kernel are checked separately. No additional identical-incoming-particle factor is inserted into the cross section; Note 38's event counting remains unchanged.

The ideal Maxwell-Boltzmann thermal average is

```
<sigma_ij v>_q = 1/[8 mi^2 mj^2 T K2(mi/T) K2(mj/T)]
  * integral ds sigma_ij^(q)(s) lambda_ij(s)/sqrt(s) K1(sqrt(s)/T).
```

Here K1 and K2 are Bessel functions, not portal entries. We integrate both a scaled-Bessel variable w=Q/T-mi/T-mj/T and the original Q variable, with their respective Jacobians. The numerical window is 0<=w<=90. The implementation deliberately restricts T to [1/3,0.5] GeV and the hard-current evaluation to Q in [20,80] GeV; it rejects use for the low-energy heavy-state decay.

## 4. Numerical results at the assumed T=0.5 GeV

At the central renormalization scale mu=Q, the new implementation gives the following **leading-power NLO approximations**, in GeV^-2:

| Initial pair | Bottom-current contribution | Charm-current contribution | Bottom + charm |
|---|---:|---:|---:|
| 11 | 1.33539e-14 | 6.64666e-16 | 1.40185e-14 |
| 12 | 1.33352e-14 | 6.63739e-16 | 1.39990e-14 |
| 22 | 1.32247e-14 | 6.58237e-16 | 1.38829e-14 |

Extra digits in the machine-readable output document reproducibility, not physical precision. These are neither full massive-NLO rates nor rigorous lower bounds on the physical total.

Only under the additional, still-unestablished chemical-equilibrium reduction of Notes 38-39 do their equilibrium weights combine these into

```
<sigma_eff v>_(b+c), LP NLO = 1.40159797222e-14 GeV^-2.
```

This is about 14.35 times Note 39's conditional three-lepton effective contribution. Adding that known lepton contribution gives approximately 1.49925e-14 GeV^-2 for the **selected leptons + approximate b/c subset**. Neither number is the complete effective annihilation rate, nor does either establish the required chemical equilibrium.

The pairwise rates remain usable as conditional collision inputs without making that one-equation reduction, provided their common-temperature kinetic assumptions and approximation limits are retained.

## 5. Physical approximation errors outweigh quadrature errors

A common scale scan, changing mu/Q in the masses, coupling and hard logarithm together, gives these conditional bottom/charm effective contributions:

| Prescription | Effective b+c contribution [GeV^-2] |
|---|---:|
| mu=Q/2, leading-power NLO | 1.51870e-14 |
| mu=Q, leading-power NLO | 1.40160e-14 |
| mu=2Q, leading-power NLO | 1.29081e-14 |
| mu=Q, running masses but Born hard coefficient | 1.09783e-14 |
| mu=Q, NLO coefficient times a massive-Born phase diagnostic | 1.20791e-14 |

The last row multiplies S_q by [1-4 mbar_q(mu)^2/Q^2]^(3/2). It is a deliberately non-systematic sensitivity diagnostic for omitted mass dependence, **not a full finite-mass NLO treatment**. Its roughly 13.8% reduction shows why small numerical integration errors must not be confused with a precise physical prediction. The scale range 1.29-1.52e-14 is not a confidence interval or guaranteed error envelope; it does not cover all modeling uncertainties.

All six b/c pair integrals agree between the Q and w evaluations to approximately 2.5e-15 relative in this execution. That checks numerical implementation, not independent QFT correctness. A formal positive high-w remainder bound uses decreasing S_q, y^2 sqrt(lambda_dimensionless)<=y^4, decreasing scaled K1, and D>=(mh Gamma_h)^2. The resulting remainders are of order 1e-42 GeV^-2 for the **formal five-flavor continuation of this approximation only**. They do not certify QCD across further flavor thresholds or bound missing physical processes. No claim of a fully controlled physical error budget is made.

## 6. Executed reproducibility record

The new source and test files have Git blob identifiers

```
heavy_quark_thermal.py: 40d51657a26fb20851be2bafa0ea6b3efe05ddfb
test_research_note_40.py: 7ce8c3172a8434a54be4e2217796e3a9ea8452cc
```

The locally executed bytes match those GitHub identifiers. After correcting a test-file transcription error during transfer, a hash-matched rerun produced **22 tests, 22 passes, 0 failures/errors**, exit code 0. No physics formula changed in that transfer correction. The runtime was Python 3.13.5, NumPy 2.3.5 and SciPy 1.17.0.

The suite checks RG boundary values and independent ODE evolution, matching, scale-log cancellation, spectral normalization, earlier leptonic results, both thermal variables for all six contributions, finite-window sensitivity, input-domain rejection and the distinction between central and phase-diagnostic calculations. These are software/mathematical checks, not independent scientific review.

```
python -m unittest -v test_research_note_40.py
python heavy_quark_thermal.py
```

The execution record and machine-readable results accompany the note. No HDECAY or RunDec executable, upstream eval-based loader, Omnes amplitudes, detector likelihood or full Boltzmann evolution was run.

## 7. Remaining calculation and source separation

The immediate physics extension is a systematically finite-mass heavy-quark treatment with consistent matching, followed by the omitted gluon/light-quark and relevant electroweak contributions without double counting. The complete conversion network, kinetic assumptions, entropy/expansion history, initial conditions and coupled yield equations must then be treated before an abundance is inferred. The low-energy s2 decay calculation remains separately blocked by the unauthenticated Omnes inputs.

Our contribution here is the explicitly limited application and reproducible calculation in the inherited two-singlet benchmark. The external papers provide QCD ingredients, not support for the proposed new fields or an endorsement of this benchmark. The draft branch is not merged; historical notes, the frozen verification archive and main were not edited in this step.

### Primary references

[1] P. Blackstone et al., *Hadronic Decays of a Higgs-mixed Scalar*, arXiv:2407.13587v1 (2024), https://arxiv.org/html/2407.13587v1 . Used only to distinguish the low-energy two-meson problem; no numerical arrays obtained.

[2] K. G. Chetyrkin et al., *Charm and Bottom Quark Masses: an Update*, Phys. Rev. D 80, 074010 (2009), corrected arXiv:0907.2110v2 (2015), Section IV, https://arxiv.org/html/0907.2110v2 . Historical input values, not a reproduced mass fit.

[3] K. G. Chetyrkin, J. H. Kuhn and M. Steinhauser, *RunDec: a Mathematica package for running and decoupling of the strong coupling and quark masses*, arXiv:hep-ph/0004189 (2000), Eqs. (1),(2),(6),(7), https://arxiv.org/abs/hep-ph/0004189 . Published RG coefficients only; code implemented separately.

[4] P. A. Baikov, K. G. Chetyrkin and J. H. Kuhn, *Scalar Correlator at O(alpha_s^4), Higgs Decay into b-quarks and Bounds on the Light Quark Masses*, Phys. Rev. Lett. 96, 012003 (2006), arXiv:hep-ph/0511063v2, Eq. (3), https://arxiv.org/abs/hep-ph/0511063 . Only the leading-power O(alpha_s) hard coefficient is retained here.

Internal lineage: Notes 24, 38 and 39 under manuscript/higgs_portal_review/, read at inherited head d44b673ae56c283071bc87e506f29a8cce3c403d. Earlier dated notes remain unchanged.
