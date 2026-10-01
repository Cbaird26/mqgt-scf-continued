# Research Note 41 — Finite-mass QCD currents and consistent mass-scheme matching

**29 September 2026 | Public scientific-development addendum; not peer reviewed.** Human author: Christopher Michael Baird. ChatGPT (ZoraASI) assisted with literature comparison, derivation, implementation, numerical checks and drafting. This is a conditional calculation in the restricted two-real-singlet Higgs-portal model, not a validated Theory of Everything, observed field, complete hadronic spectrum or relic-density prediction.

## 1. Replace a diagnostic with an order-consistent calculation

Note 40 supplied a leading-power, next-to-leading-order (NLO) bottom/charm scalar-current contribution. Its separate massive-Born phase-space multiplier was explicitly a diagnostic, not the full finite-mass NLO coefficient. Here we implement the published finite-mass nonsinglet coefficient through O(alpha_s), consistently re-express both the Yukawa mass and the kinematic mass in the MSbar convention, and insert that current into the inherited thermal kernel.

The original contribution is this limited application, scheme derivation and reproducible implementation; the QCD ingredients are established published results, not new QCD discoveries or endorsements of the hypothetical singlets.

Retain the unfitted benchmark and fixed historical inputs of Note 40:

```
m1=10, m2=11.5, mh=125, Gamma_h=0.0041, v=246 [GeV];
K11=+0.001, K12=-0.001, K22=+0.001;
alpha_s(MZ)=0.1189, MZ=91.1876 GeV;
mbar_b(10 GeV)=3.610 GeV; mbar_c(3 GeV)=0.986 GeV.
```

The inherited two-loop-truncated running and continuous nf=4/nf=5 matching at 4.163 GeV are unchanged. These are not newly fitted or latest measured inputs. Higher-order matching and input covariance are not included. The calculation is NLO in its hard coefficient with that inherited running prescription, not a complete NNLO result.

## 2. Published on-shell coefficient and normalization

Let Q be the invariant mass of the produced Standard Model system, M the pole quark mass, a=alpha_s(mu)/pi, C_F=4/3 and beta_M=sqrt(1-4M^2/Q^2). In the current normalization used in Note 40, the inclusive nonsinglet contribution is

```
S_OS(Q) = 3 M^2 beta_M^3 [1 + a C_F Delta_H(beta_M)] + O(a^2).
```

The factor three counts colors. The associated unit-Higgs-current width is Q*S/(8*pi*v^2). The finite-mass real-plus-virtual correction is given in Djouadi [1], Eqs. (2.13)-(2.15), printed pages 76-77:

```
p=(1-beta)/(1+beta), L=ln[(1+beta)/(1-beta)],
Delta_H(beta) = A(beta)/beta
  + (3+34 beta^2-13 beta^4)*L/(16 beta^3)
  + 3*(7 beta^2-1)/(8 beta^2),
A(beta) = (1+beta^2)*[4 Li2(p)+2 Li2(-p)
  -3 L ln(2/(1+beta))-2 L ln(beta)]
  -3 beta ln(4/(1-beta^2))-4 beta ln(beta).
```

This contains the inclusive q qbar(+g) contribution at this order. A separate addition of the same real q qbar g process would double count it. It is not the gluon-current contribution, a differential jet prediction, or a threshold-resummed calculation.

## 3. Convert the whole Born factor, not just the Yukawa coupling

The one-loop pole/MSbar mass relation can be written as

```
M = mbar(mu)*[1+a*d] + O(a^2),
d = 4/3 + ln[mu^2/mbar(mu)^2].
```

Behring and Bizon [2], Sec. 2.5 and Appendix B.2, provide the conversion convention. Their phenomenological implementation converts the Yukawa coupling while retaining pole-mass kinematics. Our expression below is a separately derived **all-MSbar re-expansion**, not a claim that their hybrid implementation uses it.

At fixed Q, define r=mbar(mu)^2/Q^2 and beta=sqrt(1-4r). The Born factor depends on the mass through both the squared Yukawa factor and phase space:

```
G(r) = d ln[mbar^2*(1-4mbar^2/Q^2)^(3/2)] / d ln(mbar)
     = 2 - 12r/(1-4r).
```

Expanding the complete pole expression through first order in a gives

```
C_MS(r,mu/Q) = C_F*Delta_H(beta) + d*G(r),
S_MS(Q,mu) = 3*mbar(mu)^2*beta^3*[1+a*C_MS(r,mu/Q)] + O(a^2).
```

Converting only the Yukawa prefactor would supply 2d instead of d*G(r) and omit the phase-space derivative. Replacing the pole mass numerically everywhere without this re-expansion would also fail to implement the stated perturbative convention.

Two independent checks constrain the result. Its massless coefficient tends to 17/3+2 ln(mu^2/Q^2), recovering Note 40. Taking the imaginary parts of the separate MSbar correlator expansion in Harlander and Steinhauser [3], Eqs. (3),(4),(6),(7), gives at mu=Q

```
S_MS/(3*mbar^2) = 1-6r+O(r^2)
               + a*[17/3-40r+O(r^2 ln r)] + O(a^2).
```

In contrast, multiplying the leading-power NLO coefficient by beta^3 gives -34a*r, not -40a*r. The missing -6a*r term demonstrates algebraically why the Note-40 diagnostic was not the full finite-mass correction. Tests compare the exact expression with the independently published expansion through r^4, as well as checking the mass derivative and O(a^2) scheme-reexpansion remainder.

The all-MSbar re-expansion is used away from threshold. It does not identify 2*mbar(mu) as a physical hadronic threshold and must not be extrapolated into a near-threshold or low-energy decay calculation.

## 4. Thermal integration and domain

Use the same single-Higgs-exchange normalization as Notes 39-40:

```
D(s)=(s-mh^2)^2+(mh*Gamma_h)^2,
lambda_ij(s)=[s-(mi+mj)^2]*[s-(mi-mj)^2],
sigma_ij(s)=Kij^2*s*S_MS(sqrt(s),mu)/[8*pi*D(s)*sqrt(lambda_ij(s))].
```

The unequal-mass Maxwell-Boltzmann thermal kernel is inherited unchanged. Numerical results below integrate the finite window w=Q/T-(mi+mj)/T in [0,90]. A second implementation uses Q directly; a third uses generalized Gauss-Laguerre quadrature. They compare different numerical representations of the same current and amplitude, not three independent QFT derivations.

The implementation rejects hard energies outside Q in [20,80] GeV, scale ratios outside mu/Q in [1/2,2], and temperatures outside T in [1/3,0.5] GeV. At T=0.5 GeV the three windows end at Q=65,66.5,68 GeV. These are finite-window thermal contributions, not a claimed integration of the physical spectrum to infinity.

## 5. Results at the assumed T=0.5 GeV

At the central scale mu=Q, the finite-mass NLO contributions are:

| Initial pair | Bottom current [GeV^-2] | Charm current [GeV^-2] | Bottom + charm [GeV^-2] |
|---|---:|---:|---:|
| 11 | 1.12898e-14 | 6.59483e-16 | 1.19493e-14 |
| 12 | 1.15673e-14 | 6.59310e-16 | 1.22266e-14 |
| 22 | 1.17058e-14 | 6.54439e-16 | 1.23602e-14 |

Digits beyond the physical approximation's precision document numerical reproducibility only. These partial contributions are not rigorous bounds on a physical total.

Only under the still-unestablished chemical-equilibrium reduction of Notes 38-39 do the full ideal-gas equilibrium weights combine them into

```
<sigma_eff v>_(b+c), finite-mass NLO = 1.19805650414e-14 GeV^-2.
```

This is **14.52% below** Note 40's leading-power value 1.40159797222e-14 and **0.816% below** its phase-only diagnostic 1.20791269963e-14. The diagnostic happened to be close here; its numerical proximity is not a general justification for using it.

A consistent variation of mu in the running masses, coupling and conversion coefficient gives:

| Scale prescription | Conditional effective b+c contribution [GeV^-2] |
|---|---:|
| mu=Q/2 | 1.28624e-14 |
| mu=Q | 1.19806e-14 |
| mu=2Q | 1.11684e-14 |

This is a scale-sensitivity comparison, not a confidence interval or guaranteed uncertainty envelope. Adding Note 39's conditional three-lepton contribution gives 1.29570852444e-14 GeV^-2 for the **selected leptons plus NLO b/c subset**, not the complete effective annihilation rate. The pairwise rates do not require the one-equation chemical-equilibrium reduction, but retain their common-temperature kinetic assumptions.

## 6. Finite-domain remainder and physical uncertainties

An analytic triangle bound on the logarithm/dilogarithm expression, together with monotonic inherited mass/coupling running, gives a conservative current cap S<328.94 GeV^2 throughout the declared hard/scale domain. This is not a maximum inferred from sampled points. Bounding the positive thermal kernel using D>=(mh*Gamma_h)^2, y^2*sqrt(lambda_dimensionless)<=y^4 and decreasing scaled K1 gives per-flavor omitted contributions between the window endpoint and Q=80 bounded numerically by

```
11: 2.20e-41, 12: 1.95e-41, 22: 1.73e-41 [GeV^-2].
```

The mathematical bounding envelope is integrated to infinity only to bound that **finite interval**. Neither the cap nor those numbers bounds the unknown physical spectrum above Q=80. Displayed floating-point bounds are not directed-rounding certificates. The full infinity-domain thermal integral remains outside this note's claims.

Finite-mass NLO matching removes one identified approximation, not all uncertainties. Higher QCD orders, gluon/light-quark and relevant electroweak contributions, threshold matching, input correlations, plasma effects, kinetic distributions and the expansion history remain separate issues. No relic abundance or detector likelihood follows.

## 7. Executed verification and provenance

The on-shell coefficient evaluated at the independent published check point M=4.78 GeV, Q=125.09 GeV yields Delta_H=-7.44664783295, agreeing with the -7.446648 coefficient in Table 2 of [2]. Those numbers are a formula check, not replacement inputs for our benchmark. The code also agrees with a 60-digit dilogarithm evaluation and the independent MSbar large-momentum expansion in [3]. No external HDECAY or RunDec executable was run.

At T=0.5 GeV all six current contributions agree between Q and w integration within 2.6e-15 relative in the executed floating-point comparison. This is numerical agreement, not a physical error estimate. Window, scale, lower-temperature and independent quadrature-order checks are included.

The new committed source/test blobs are

```
finite_mass_quark_thermal.py: 117fd5d3abb650f05334d8bff6f88115c63e09da
test_research_note_41.py:     66bad882f07db816d266c102e168efae641ac6fa
```

They match the locally executed bytes at code/test commit 86289fcf7825090282b579b0e1ff400e79497239. The inherited heavy_quark_thermal.py remains byte-identical to blob 40d51657a26fb20851be2bafa0ea6b3efe05ddfb. After checking these identities, the combined suite ran **46 tests: 24 new and 22 inherited, zero failures/errors, exit code 0**. Runtime: Python 3.13.5, NumPy 2.3.5, SciPy 1.17.0 and mpmath 1.3.0.

```
python -m unittest -v test_research_note_40.py test_research_note_41.py
python finite_mass_quark_thermal.py
```

The execution record, full results and logs accompany this note. Tests are software/mathematical checks, not independent empirical validation. The four low-energy Omnes inputs were not obtained in this step; no s2 hadronic-decay width or lifetime was updated. No Boltzmann abundance evolution, journal submission, DOI or release is claimed. Historical notes, main and the frozen verification archive were not edited.

## Primary references

[1] A. Djouadi, *The Anatomy of Electro-Weak Symmetry Breaking. I: The Higgs boson in the Standard Model*, arXiv:hep-ph/0503172v2, Eqs. (2.13)-(2.15), https://arxiv.org/pdf/hep-ph/0503172 . The full massive O(alpha_s) coefficient is used, not the higher-order predictions discussed elsewhere in the review.

[2] A. Behring and W. Bizon, *Higgs decay into massive b-quarks at NNLO QCD in the nested soft-collinear subtraction scheme*, arXiv:1911.11524v1, Sec. 2.5, Appendix B.2 and Table 2, https://arxiv.org/html/1911.11524 . Used for mass-conversion conventions and an on-shell NLO benchmark; its NNLO computation was not reproduced here.

[3] R. Harlander and M. Steinhauser, *Higgs Decay to Top Quarks at O(alpha_s^2)*, arXiv:hep-ph/9704436v1, Eqs. (3),(4),(6),(7), https://arxiv.org/pdf/hep-ph/9704436 . Used for the generic-mass scalar-current expansion as an independent NLO check, not for top-quark production at our benchmark.

Internal lineage: Notes 24, 38-40 at inherited head 160016eb2798a11e6cced984951cd5331bc614bb. Source authors provide established ingredients; none studied or endorsed the proposed two-singlet interpretation.
