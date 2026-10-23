# Derivation review and numerical self-audit

This is a same-session AI-assisted self-audit. No separate agent or external referee participated.

## Derivation checks

- At constant internal background B, the metric vertices are internal identities. Therefore each internal eigenvalue contributes the massless external Dirac curvature form factors multiplied by exp(-a b_i^2). A single mixed metric/scalar insertion selects diagonal matrix elements of {B,T_A}; noncommuting scalar pairs require the two-energy Duhamel kernel.
- The spin trace includes the curvature endomorphism R/4 and spin-connection curvature. Their combination gives the local curvature-squared coefficients C_Ric(0)=-1/10 and C_R(0)=1/30; the local scalar-curvature-squared combination cancels. The transverse trace acquires nonlocal corrections at higher momentum despite that cancellation.
- Metric and mixed potential contacts are removed only by total flat stationarity. The scalar Hessian includes all local contacts, including the nonlinear radius derivative, the chosen mass term and fixed flatness subtraction. Neither counterterm has derivative or curvature vertices by assumption.
- Explicit 4x4 Dirac matrices, shifted continuum Gaussian momentum integration and Duhamel vertices provide an independent check of the conformal metric, mixed mass and transverse-traceless kernels at real Euclidean, negative real and complex momenta. The conformal calculation uses the flat-density operator exp(-sigma/2) D_flat exp(-sigma/2)+gamma5 b. The traceless check uses a volume-preserving anisotropic metric. Gaussian polynomial moments are integrated exactly by three-point Hermite rules per dimension.
- The scalar/mixed/gravity low-momentum limits reproduce the previously sealed Jordan and Einstein matrices. The rank-one Einstein addition is recovered by eliminating the transverse trace at low momentum.
- The full bordered determinant is analytic after removing its trivial metric z factor. The scalar Schur complement has poles at zeros of B(z); those are not accepted as zeros of the full operator. The representative B zero is explicitly nonsingular in the full matrix.
- Real residues use the derivative of the full operator and are independently checked against the limit of its matrix inverse. Complex null vectors and residue matrices use a transpose bilinear form, not a Hermitian norm to assign an unjustified positive/negative sign.
- The spin-two obstruction also follows analytically from positive coefficients: A(0)>0 and the large positive-z tensor kernel has a negative limit. The timelike A(-s) series has strictly positive coefficients. Thus the positive-z crossing is not an artifact of a finite derivative polynomial.
- Real pole locations and kernels are checked by increasing the fermion cutoff from 12 to 16 and the quadrature from 64 to 96. Bounded complex counts use refined contours; the representative complex zeros are isolated and refined independently of the initial multi-start search.

## Numerical search corrections

An initial multi-start complex search missed closely spaced pairs. It was replaced by adaptive argument-principle subdivision. The original subdivision depth of 20 and contour step limit were insufficient for those pairs; the final runner permits depth 40, contour refinement through 4096 points per side, and checks the isolated total against the enclosing contour count. These are numerical checks, not rigorous interval certificates. The initial incomplete search is not used to claim completeness.

## Interpretation limits

The pole result must not be turned into a successful stability claim. The light neutral and radion-connected real timelike poles have positive residues, but the same specified action has tachyonic poles and non-real poles under the declared direct continuation. The pole test therefore strengthens the caveats of the two-derivative note and reveals an obstruction to an unrestricted interpretation of that minimal action. It does not prove that every modification or ultraviolet completion of the broader program is impossible.

No alternative contour, extra gravitational counterterm, spectral-profile change, scalar retuning or additional degree of freedom is introduced to erase this outcome. Higher harmonics and other omitted bosonic modes can change the full spectrum; their stationarity and mixing remain unresolved. No full quantum propagator construction, unitarity theorem, or empirical prediction is asserted.
