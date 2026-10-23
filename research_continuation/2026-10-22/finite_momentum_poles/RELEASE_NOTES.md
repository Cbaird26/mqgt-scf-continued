# Finite-momentum metric, radion and scalar poles

**Research prerelease — conditional classical calculation; stability obstruction in the minimal retained action.**

The eight-page note derives the full external-momentum quadratic metric/radion/scalar operator for the declared warped round-sphere family and tests the direct analytic continuation `z=p_E^2/Lambda^2=-s-i0`. The closed CP-even neutral sector `(R,h_d,h_u)` is coupled to the transverse metric trace; the transverse-traceless graviton is tested separately. All nine fixed-metric scalar entries are supplied. Internal spectral representations are evaluated with finite numerical angular cutoffs and quadratures.

**The retained tuned fixtures fail the reported finite-momentum stability tests under that continuation.** Positive-residue light and radion-connected timelike poles coexist with negative-residue tachyonic poles and additional non-real poles. This result does not establish a stable vacuum or a causal quantum completion, and does not rule out every modification of the broader program.

## Results

- The low-momentum limits recover the predecessor's Jordan and Einstein kinetic matrices. The full bordered determinant removes the trivial metric momentum factor and avoids mistaking a Schur-complement denominator zero for a physical pole. The ordinary Einstein conformal constraint is not classified as an extra scalar ghost.
- For positive finite exponential profiles, the tensor kernel is positive near the massless origin and tends to a negative constant at large positive Euclidean momentum. A positive-Euclidean-momentum zero is therefore forced in this minimal retained action; it is not merely a finite derivative-polynomial artifact. There is no additional real timelike tensor zero under the stated assumptions.
- In the representative minus-profile `epsilon=0.01` fixture, the radion-connected squared-mass parameter shifts from approximately `0.8295963 Lambda^2` at two derivatives to `0.6565080 Lambda^2` in the retained finite-momentum operator. This is a conditional pole of an unstable restricted background, not a certified particle of a completed theory.
- The same fixture has tensor and neutral tachyonic zeros at approximately `z=10.2610119` and `z=10.9025894`, respectively, with negative residues. Four real timelike neutral poles have positive local residues. Above-cutoff poles are not empirical particle predictions.
- In the bounded square `|Re z|, |Im z| <= 20`, after removing the massless tensor and trivial metric factors, numerical counts are **7 tensor / 33 coupled zeros for both minus-profile fixtures**, and **9 tensor / 37 coupled zeros for both plus-profile fixtures**. Only the representative minus-profile `epsilon=0.01` fixture has individually isolated non-real roots: three tensor and fourteen coupled upper-half-plane zeros, with conjugate partners. Other fixtures have real-pole tests and refined enclosing counts. These are bounded floating-point calculations, not interval certificates or global zero enumerations.

## Reproducibility and release contents

The sealed preparation record contains **194/194 passing computational checks**. A fresh extraction reproduced `results.json` and `checks.json` byte-for-byte, regenerated identical figures and tables, and rebuilt an eight-page PDF whose rendered pages were pixel-identical to the inspected note. Independent explicit Dirac-matrix/Gaussian vertex checks, infrared limits, cutoff and quadrature comparisons, full-operator residue checks, and bounded contour refinements are recorded. Passing checks establish computational consistency within the assumptions, not physical validation. Numerical calculations are not rerun solely for publication.

The three release assets are:

1. `Finite_Momentum_Metric_Radion_Scalar_Poles_2026-10-22.pdf` — research note, eight pages.
2. `Finite_Momentum_Poles_Reproducibility_2026-10-22.zip` — 34 payload files plus an internal SHA-256 manifest, including code, pinned inputs, results, checks, LaTeX sources, figures, assumptions, self-audit, provenance and the same PDF.
3. `RELEASE_SHA256SUMS.txt` — checksums for the separately downloaded PDF and ZIP.

Verify the downloaded release assets in their common directory:

```bash
shasum -a 256 -c RELEASE_SHA256SUMS.txt
```

After extracting the ZIP, verify its payload from `Finite_Momentum_Poles_2026-10-22/`:

```bash
shasum -a 256 -c SHA256SUMS.txt
```

Follow the sealed README for reproduction. The original PDF, ZIP, and their 34 payload files remain unchanged. Historical statements that the package was locally prepared and not yet published are preserved as preparation-stage records; the added `PUBLICATION.md` records this later publication. The note date and tag retain the preparation date, 22 October 2026; GitHub records the actual publication timestamp.

## Release asset SHA-256 checksums

```text
0db5ed1ff98ab4c446d315c781bbea0f9d5e828b4f0bc18cc18ae70ebeaa169c  Finite_Momentum_Metric_Radion_Scalar_Poles_2026-10-22.pdf
4fa15163962e1fa6cbf815ba1d8bf8ec668ea82888507e5524848741b9b5ad33  Finite_Momentum_Poles_Reproducibility_2026-10-22.zip
```

## All stated assumptions, continuation prescription and limits

The complete sealed assumptions follow verbatim, including the historical preparation-stage publication statement.

1. **Pinned conditional model.** Inputs are inherited from the radion release at commit `1bb152dfbd6bb1e02a3e841b6d73e338f8e5fabf`. The parity-even full-Dirac spectral action, positive ten-exponential profiles, four copied fermion blocks, unit dimensionless Yukawas, monopole connection and microscopic scalar insertion are specifications. Their uniqueness, phenomenological viability and six-dimensional ultraviolet completion are not established.
2. **Declared fluctuation family.** The metric is `g_4(x)+r(x)^2 dOmega_2^2`, torsion free, with fixed internal basis and lowest scalar harmonics. The classical spinor Hilbert-space map removes the warped volume connection, leaving `D_g+gamma5 Lambda B(R,h)`. The cutoff Lambda is fixed. No quantum measure equivalence, cutoff dilaton or complete bosonic consistent truncation is asserted.
3. **Exactness at quadratic order.** The new operator retains all external momenta at quadratic order in the declared metric/radius/scalar perturbations and all internal spectral orders in its representation. Numerical fermion angular cutoffs and integration quadratures approximate that representation. It is not an all-orders calculation in fluctuation amplitude or a loop effective action. Constant backgrounds remain the four inherited tuned fixtures.
4. **Extra operators.** The selected scalar-mass counterterm and the separately selected flatness subtraction are minimally covariant potential terms, with their common volume factor. Their parameters are fixed when differentiating each fixture. Their zero-momentum metric and mixed contacts cancel only because the total potential and its first derivatives vanish. They add no independent curvature, derivative or nonlocal terms by assumption. Allowing additional Einstein-Hilbert, curvature-squared or scalar derivative terms can change the pole conclusions. Neither selected potential term solves the cosmological constant problem.
5. **Metric constraints and signs.** Euclidean kernels are reconstructed in transverse spin-two and transverse-trace projectors at nonzero momentum; diffeomorphism gauge directions are excluded. The massless spin-two sign is positive for kappa>0. The negative Einstein-Hilbert conformal entry is the ordinary gravitational constraint, not an extra scalar ghost. The neutral scalar Schur complement is used only where its metric denominator is nonzero; zeros of that denominator are checked in the full bordered operator before any pole interpretation.
6. **Lorentzian prescription.** We test the direct analytic continuation `z=p_E^2/Lambda^2=-s-i0`, with `s=(omega^2-|k|^2)/Lambda^2`. Entire kernels determine this analytic continuation of the quadratic functions but do not determine a causal quantum integration contour, path-integral Wick rotation, allowed asymptotic states, initial-value prescription, reflection positivity, temperedness or ultraviolet unitarity. Exponential growth in some complex directions prevents assuming those properties. No alternative contour or prescription is silently chosen to remove unwanted poles.
7. **Pole and residue interpretation.** A real zero z<0 is a formal timelike pole with squared mass parameter -z; z>0 is tachyonic under the stated continuation. A simple real pole has residue sign relative to the healthy Euclidean kernel `z+m^2`; complex residues have no positive/negative norm interpretation. Scalar residues are normalized with the inherited infrared Einstein metric. Tensor and neutral tachyonic poles with negative residues, and additional non-real poles, obstruct an ordinary unrestricted stable/unitary interpretation of this minimal retained action. Above-cutoff poles are not empirical particle predictions. The shifted radion pole is a result of this restricted quadratic operator, not a certified particle of a completed theory, especially because the same background has the reported instabilities.
8. **Scope of pole tests.** The closed CP-even neutral sector `(R,h_d,h_u)` is coupled to the four-dimensional metric trace; the transverse-traceless graviton is tested separately. The general all-nine-field fixed-metric scalar kernel and metric selection rules are supplied and checked. Physical charged/phase poles require charged-vector, gauge and axion constraints not derived here. The predecessor's potential-free axion, positive independent coefficient, pure-X Stueckelberg coupling and massless physical phase remain conditional assumptions, not a new finite-momentum axion result.
9. **Omitted compactification modes.** Higher scalar harmonics, nonspherical internal metric modes, other gauge/bosonic fluctuations and their tadpoles are not solved or integrated out. Their mixing can move poles. A stationary point restricted to this family need not be a stationary point of the full theory. No complete compactification stability, nonlinear evolution, global minimality, uniqueness or vacuum lifetime is proved. The untuned runaway remains a separate inherited result.
10. **Search domain and numerics.** Real searches use `-20 <= z <= 20`; complex argument-principle counts use `-20 <= Re z, Im z <= 20`. Non-real roots are individually isolated for the representative minus-profile epsilon=0.01 fixture, with conjugate partners inferred and checked from real coefficients. Other fixtures receive real-pole tests and bounded contour counts. Finite sampled contours, root refinements and cutoff/quadrature comparisons are numerical evidence, not interval-certified zero counts, global zero enumeration or uniform spectral-tail bounds. Closely spaced complex pairs require refinement. Tiny profile differences have fewer reliable digits than absolute values. Checks are consistency tests, not independent physical predictions.
11. **Normalization and phenomenology.** Kappa, Lambda and the physical profile are not selected. Vacuum-normalized units match the predecessor. Quantum loops, thresholds, matching, running, anomaly completion, two-form reduction, axion potential and Stueckelberg scale remain unresolved. No measured coupling is fitted. The measured fine-structure constant remains unexplained.
12. **Review and reproducibility.** This is AI-assisted research with a same-session self-audit and independent computational paths, without a separate agent or external peer review. Standard nonlocal heat-kernel, projector and residue methods are attributed; no methodological priority is claimed. Reproduction is environment dependent. The note and bundle are prepared locally; their creation does not publish a new GitHub release.


## Complete sealed derivation review and numerical self-audit

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


## Source and attribution

- [Published source package](https://github.com/Cbaird26/mqgt-scf-continued/tree/v2026.10.22-finite-momentum-poles/research_continuation/2026-10-22/finite_momentum_poles)
- [Publication record](https://github.com/Cbaird26/mqgt-scf-continued/blob/v2026.10.22-finite-momentum-poles/research_continuation/2026-10-22/finite_momentum_poles/PUBLICATION.md)
- [Complete assumptions](https://github.com/Cbaird26/mqgt-scf-continued/blob/v2026.10.22-finite-momentum-poles/research_continuation/2026-10-22/finite_momentum_poles/ASSUMPTIONS.md)
- [Complete same-session self-audit](https://github.com/Cbaird26/mqgt-scf-continued/blob/v2026.10.22-finite-momentum-poles/research_continuation/2026-10-22/finite_momentum_poles/REVIEW.md)
- [Primary-source background and input lineage](https://github.com/Cbaird26/mqgt-scf-continued/blob/v2026.10.22-finite-momentum-poles/research_continuation/2026-10-22/finite_momentum_poles/references/SOURCES.md)
- [Predecessor radion-kinetics prerelease](https://github.com/Cbaird26/mqgt-scf-continued/releases/tag/v2026.10.22-radion-kinetics-scalar-mixing), commit `1bb152dfbd6bb1e02a3e841b6d73e338f8e5fabf`.

License: CC BY 4.0, preserving inherited attribution. AI-assisted conditional research with a same-session self-audit, without separate-agent or external peer review. No measured coupling is fitted; the measured fine-structure constant remains unexplained.
