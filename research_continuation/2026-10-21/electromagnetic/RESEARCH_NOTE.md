# Spectral-profile identifiability: executed continuation

**Date:** 21 October 2026. **Status:** conditional mathematical result for the stipulated common spectral action. This calculation does not select a physical action, determine its normalization, or predict the measured fine-structure constant.

## Result

The archived two-profile example extends to an exact one-parameter continuum with identical leading spectral moments. On its tracked stationary-radius branch, the endpoint inverse-hypercharge coefficient changes by **0.1279765%** and the normalization-independent gauge/gravity ratio changes by **0.3478263%**. An additional first-derivative profile datum identifies the parameter uniquely within the fixed five-exponential family.

That finite-family identification does not select a profile in a larger class. A new pair of strictly positive six-exponential profiles has exactly the **same original five-node center data through the next local heat coefficient, a8**, yet gives different compactified couplings. Their inverse-hypercharge coefficients differ by **0.005502625%**. The calculation therefore identifies both a concrete closure condition for a declared finite ansatz and its failure when that ansatz is enlarged.

All percentages compare defined mathematical actions at their separately imposed flat stationary vacua. They are not observational discrepancies or experimental forecasts. The new numerical work and exact identities are reproducible with `spectral_profile_analysis.py`; full results are in `profile_identifiability_results.json` and `profile_family_scan.csv`.

## 1. Inherited action and source boundary

The source is the supplied expanded archive, physical PDF pages **7592–7599**, “T-1: A shared spectral-action normalization test,” dated 12 October 2026 [S1]. It postulates a common bosonic functional

\[
S_{\rm sp}=\frac{\kappa}{2}\sum_i\operatorname{Tr}_{\rm Dirac}f(D_i^2/\Lambda^2),\qquad \kappa>0.
\]

The calculation retains its four copied repaired six-dimensional Weyl blocks, round internal sphere, unit X monopole flux, charge convention \(D_\mu=\partial_\mu-i(y/2)B_\mu+\cdots\), and parity-even full-Dirac trace convention. It does not rederive the block's anomaly structure or extend the external backgrounds beyond the archived hypercharge calculation.

Write \(R=\Lambda r\), and define

\[
h_n(R)=\frac n2+\sum_{p=1}^{\infty}(2p+n)e^{-p(p+n)/R^2},
\]
\[
H=12h_0+28h_1+16h_2,\qquad H_Y=\tfrac13h_0+\tfrac{32}3h_1+\tfrac43h_2.
\]

For \(f(u)=\sum_jw_je^{-a_ju}\), the inherited exact internal sums are

\[
P=\sum_j\frac{w_j}{a_j^2}H(R/\sqrt{a_j}),\quad
J=\sum_j\frac{w_j}{a_j}H(R/\sqrt{a_j}),\quad
T=\sum_jw_jH_Y(R/\sqrt{a_j}).
\]

An extra local cosmological density supplies the subtraction \(cR^2\). The flat-vacuum prescription imposes

\[
RP_R-2P=0,\qquad c=P/R^2.
\]

At this point the reported coefficients are

\[
z:=Z_Y/\kappa=T/(6\pi^2),\qquad
u:=(M_4r_*)^2/\kappa=R_*^2J/(24\pi^2),\qquad q:=z/u.
\]

The calculation uses exact internal mode sums but remains a low-external-derivative expansion. The subtraction is determined separately for each profile by the same imposed rule; a single common fixed numerical value of c is not imposed across the family. Positive \(P_{RR}-2c\) establishes positive curvature of the restricted radius potential at its flat stationary point. Without the exact radion kinetic term it does not give a physical radion mass or a full stability theorem. These qualifications are inherited directly from [S1, pp.7594–7599].

## 2. Reproduction of the archived pair

The original nodes and direction are

\[
a_j=\frac{5269}{8220}j,\qquad v=(1,-32,162,-256,125),\qquad
w_j(t)=\frac15+\frac{t v_j}{2560}.
\]

The archive's two cases are \(t=-1,+1\). Independently evaluated values agree with the displayed source table:

| Quantity | t = −1 | t = +1 |
|---|---:|---:|
| Stationary R | 1.30211764936900 | 1.30187576169391 |
| Required c | 48.3989788902990 | 48.3978806753453 |
| Restricted potential curvature | 16.0006637517561 | 16.0655185006695 |
| ZY/κ | 0.245345972549864 | 0.245467728342579 |
| M4r*/√κ | 0.685557884695684 | 0.685267055890428 |
| q = ZY/(M4r*)² | 0.522024243990561 | 0.522726714970681 |

The independent pure-exponential control reproduces \(R_*=1.3007832832273603\) and \(Z_Y/\kappa=0.3303631229653509\). Replacing \(e^{-u}\) by \(e^{-3u}\) rescales R by \(\sqrt3\) while leaving z, u, and q unchanged, verifying the source's elementary scale-redefinition control [S1, pp.7596–7598].

## 3. Continuous ambiguity with the same local data

The null identities hold exactly in rational arithmetic:

\[
\sum_{j=1}^5v_jj^{-k}=0,\qquad k=0,1,2,3.
\]

Consequently every member has

\[
f(0)=1,\quad m_1=m_2=\frac{18769}{26345},\quad
m_3=\frac{658531217359}{731399400545},
\]

where \(m_k=\sum_jw_j/a_j^k\). These are the profile factors of the six-dimensional coefficients through a6. The constraint matrix has exact rank 4 and nullity 1. Multiplying column j by \(j^3\) reduces its rows to distinct powers from 0 to 3, so its rank is also a Vandermonde consequence, not a numerical rank threshold.

Componentwise strict positivity gives exactly

\[
-\frac{256}{81}<t<2.
\]

At either closure endpoint one weight vanishes. Those endpoints are well-defined nonnegative mixtures and limits of the strictly positive family; they are not asserted to have all five weights strictly positive.

| Quantity | Lower limit t = −256/81 | Center t = 0 | Upper limit t = 2 |
|---|---:|---:|---:|
| R | 1.30238092259470 | 1.30199648681375 | 1.30175547215446 |
| ZY/κ | 0.245214958099920 | 0.245406793794817 | 0.245528775637635 |
| q | 0.521264582999461 | 0.522375570307177 | 0.523077678506052 |
| Potential curvature | 15.9308148359189 | 16.0330678717390 | 16.0980153871370 |

Across a 1,001-point grid of the closed interval, the selected near-1.3 branch has positive potential curvature and increasing z and q. The reported endpoint changes are 0.1279765% for z and 0.3478263% for q, relative to the lower endpoint. This scan supports monotonicity of the tracked branch; it is not an interval-arithmetic proof of monotonicity between every pair of grid points or of the absence of other stationary roots.

![Profile dependence of the exact coefficients](spectral_profile_sensitivity.png)

The ratio q removes the common κ. Its residual variation shows that this ambiguity cannot be absorbed solely into the common overall normalization while preserving both the gauge and gravitational-radius observables.

## 4. What additional information closes the finite ansatz?

For these five fixed nodes,

\[
f_t'(0)=-\frac{5269}{2740}-t\frac{5269}{876800}.
\]

The slope is nonzero, and adjoining this row gives exact rank 5. Thus a specified datum d gives the unique candidate

\[
t=-\frac{876800}{5269}\left(d+\frac{5269}{2740}\right),
\]

provided that value lies in the admissible interval. This is global algebraic identification **within the stipulated fixed-node five-weight model**. It is not evidence that nature supplies d or that this finite model is physically preferred. The program verifies the inverse at five independent exact rational parameter values.

An extra Mellin moment m4 also has nonzero slope,

\[
\frac{d m_4}{dt}=\frac{713357606025}{1541497376588642},
\]

and therefore would identify t in the same family. These are different types of extra input: in six dimensions the next local heat-profile factor, at a8, is \(\sum_jw_ja_j=-f'(0)\), whereas m4 is an additional Mellin integral. This follows directly by applying the local heat expansion separately to each exponential; m4 should not be described as the next six-dimensional local heat coefficient.

One can also examine local identification by hypothetical independent observables. Implicit differentiation of \(F=RP_R-2P=0\) gives

\[
\frac{dR_*}{dt}=-\frac{RP_{Rt}-2P_t}{RP_{RR}-P_R}.
\]

At t = 0, the calculation gives

\[
\frac{dR_*}{dt}=-1.20943527884\times10^{-4},\quad
\frac{dz}{dt}=6.08779891537\times10^{-5},\quad
\frac{d\log q}{dt}=6.72380989388\times10^{-4}.
\]

The Jacobian of \((\log Z_Y,\log (M_4r_*)^2)\) with respect to \((\log\kappa,t)\) has determinant \(-d\log q/dt\), nonzero at this evaluated point. Hence it is locally invertible within the two-parameter model. The derivative ranges from 0.000670786 to 0.000674920 on the grid. Locally, a fractional uncertainty δq/q propagates as approximately \(\delta t=1487.25\,\delta q/q\), before including any nuisance inputs or model discrepancy. This is a mathematical conditioning statement. No measured q, experimental precision, or attainable measurement has been assumed.

## 5. Same a8 data still do not select a general profile

Enlarge the fixed support by one node while retaining the original spacing:

\[
a_j=\frac{5269}{8220}j,\quad j=1,\ldots,6,
\]
\[
b=(1/5,1/5,1/5,1/5,1/5,0),\qquad
v_6=(-1,40,-270,640,-625,216),
\]
\[
\widetilde w_j(s)=b_j+\frac{s(v_6)_j}{7680}.
\]

Every coefficient is strictly positive for \(0<s<1536/625\). The exact identities are

\[
\sum_{j=1}^6(v_6)_j j^{-k}=0\ (k=0,1,2,3),\qquad
\sum_{j=1}^6j(v_6)_j=0.
\]

This family has the **same f(0), m1, m2, m3 and f′(0) as the original five-node center**, not just equal values between two unrelated examples. Its five-row constraint matrix has rank 5 and nullity 1. The choices s = 1 and s = 2 are both strictly interior:

| Quantity | s = 1 | s = 2 |
|---|---:|---:|
| R | 1.30210699943201 | 1.30221755151233 |
| c | 48.3985926811392 | 48.3987553947951 |
| Potential curvature | 16.0270657654678 | 16.0210836876141 |
| ZY/κ | 0.245420268242143 | 0.245433772799502 |
| M4r*/√κ | 0.685526416159451 | 0.685640629368618 |
| q | 0.522230265240659 | 0.522085021526615 |

Despite identical local profile data through a8,

\[
\Delta(Z_Y/\kappa)=1.35045573587\times10^{-5},
\]

a 0.005502625% increase relative to s = 1. The ratio q decreases by 0.027812198%. Both restricted potential curvatures remain positive.

Adding the second derivative f″(0) produces rank 6 for these six fixed nodes: its slope is \(27762361/4324377600\ne0\). That would close this particular finite family. It does not supply a microscopic rule for an unrestricted function. These two explicit constructions establish a bounded conclusion: the stated finite sets of local profile data fail to select unique exact compactified coefficients across these admissible positive mixtures. They do not prove that every conceivable additional observable or microscopic principle must fail.

## 6. Verification and precision

The run passes **38 substantive checks**, covering exact constraint ranks and null directions, positivity, the archived numerical results, the scale control, exact recovery of family parameters, finite-family identification, the new six-node counterexample, and independent numerical diagnostics.

The main scan uses analytic heat-sum derivatives and SciPy's bracketed Brent solver on R ∈ [1.2,1.4]. Independent selected evaluations use 70-digit Decimal arithmetic and Newton iteration, with separately coded heat sums. Their radii and coefficients agree with the ordinary calculation to about 2.3 × 10⁻¹⁵ at the five selected comparison points. The implicit derivative agrees with a centered difference, within the stated program tolerance.

At the center, truncation at 20 versus 40 internal radial levels changes the checked high-precision quantities by at most 10⁻⁶⁸. The integral bound from [S1, p.7598] gives, uniformly over all normalized nonnegative mixtures on the six declared nodes and R ≤ 1.4 at cutoff 40,

\[
|\Delta P|\le5.02\times10^{-226},\quad
|\Delta J|\le3.22\times10^{-226},\quad
|\Delta T|\le5.73\times10^{-228}.
\]

These are heat-value truncation bounds. They do not bound all floating-point arithmetic errors or certify complete real-root enclosures. Long decimal strings in JSON are reproducibility records, not claims that every printed digit is rigorously certified. No extra optional test campaign is needed to support the finite-family conclusions reported here.

## 7. Implication for the normalization program

This continuation replaces an unspecific “profile ambiguity” with a concrete rank calculation, a complete positive interval, a sensitivity map, an explicit extra datum that identifies a finite ansatz, and a stronger counterexample outside that ansatz. The physical missing input is still a justified rule that supplies the profile and κ, together with vacuum and quantum consistency.

The calculations do not establish a canonical radion kinetic term, full stability, a quantum prescription that protects the shared action, complete electroweak embedding, threshold matching, or running to a measured electromagnetic scale. Hypercharge normalization in this convention is not the measured photon coupling. No measured coupling has been fitted, and no arbitrary member of either family is promoted to a physical prediction.

## Source and provenance

[S1] Supplied *A Theory of Everything — Expanded Research Archive, Public Edition*, file `36-A-Theory-of-Everything-Baird-et-al-2026-Expanded-Research-Archive-Public-Edition-2026-10-20-2-.pdf`, physical PDF pp.7592–7599. Paper title and date as above. SHA-256: `4b52a5fb57716168d354b5c3dcb4bbf2ca4c0fe6744733b6ca0d3b3eae48f921`.

All new numerical values and exact algebraic identities in sections 3–6 are outputs or derivations of the accompanying script. No external publication, repository, source PDF, or existing result was modified. The source paper's historical audit counts are not represented as having been rerun here.
