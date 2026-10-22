# Exact scalar-radius vacuum: instability and tuned stationary branches

Research prerelease, 22 October 2026. Prepared for Christopher Michael Baird / ZoraASI with OpenAI Codex. Continues [the exact scalar mode-sum prerelease](https://github.com/Cbaird26/mqgt-scf-continued/releases/tag/v2026.10.22-exact-scalar-mode-sums), whose inherited inputs are pinned at commit `12fa25fc3f35b0ea0b65aa870a93fa0c501957d9`.

The full finite-background spectral potential is evaluated without a polynomial expansion in the retained lowest scalar harmonics. **The untuned inherited action has a scalar saddle and an analytically established unbounded direction at fixed subtraction.** Numerically converged coupled scalar/radius stationary branches appear after adding an **explicitly chosen positive scalar-mass counterterm** and separately selecting the flat-vacuum subtraction. These are conditional results in a restricted background family, not a completed physical vacuum construction.

## Results

- At the inherited symmetric radius, the radial curvature is positive but both neutral scalar curvatures are negative. A positive quartic truncation does not stabilize the full potential; its candidate is checked against the full gradient.
- A resummed large-radius heat-trace expression establishes the untuned runaway. For the minus profile along fixed `h_d=h_u=2`, `W/R^2` tends to approximately `-6.06641572` with the inherited subtraction held fixed. The plus profile has the same sign. This excludes a ground state within the declared family, while leaving possible metastable extrema unresolved. The bare spectral trace remains positive; the negative direction is for the subtracted action.
- A 360-point scalar/radius scan and twelve bounded root searches supplement the analytic result. Their unsuccessful endpoints and residuals are preserved. They are numerical exclusions at tested points and starts, not a global nonexistence theorem.
- With the optional mass counterterm held common between profiles, flat coupled solutions are obtained at `epsilon=0.01` and `0.0001`. The minus-profile values are:

| epsilon | R | h_d | h_u | scalar-relaxed radial curvature |
|---|---:|---:|---:|---:|
| 0.01 | 1.2781645588 | 0.2091273511 | 0.1943861736 | 11.6408747464 |
| 0.0001 | 1.2784693163 | 0.0208600895 | 0.0193927039 | 11.7012706697 |

- The retained radius/neutral-amplitude Hessian, charged curvature, two-amplitude scalar kinetic matrix, and neutral gauge kinetic matrix are positive for the tuned fixtures. Gauge/phase flat directions remain; the assumed potential-free axion leaves one physical phase flat. Potential-Hessian eigenvalues are coordinate-dependent curvatures, not canonical masses or physical poles.
- The exact scalar mass slope reverses the radius-shift sign relative to the predecessor's local scalar approximation. The scalar-relaxed radial curvature approaches approximately `11.70187946` near criticality.
- With a common counterterm, the profiles cross the local symmetry-breaking threshold at different tuning values; the threshold separation corresponds to `epsilon` approximately `3.4178723e-8`. This near-critical conclusion follows from quadratic coefficients and a positive effective quartic; it is not a numerical tiny-vev solution.
- Holding the inherited subtraction fixed instead gives nonflat restricted stationary diagnostics. They are not self-consistent curved-spacetime solutions.

The complete equations, numerical results, residuals, failed-search diagnostics, and tolerances are in the note and `results.json` / `checks.json`.

## Reproducibility and verification

- Seven-page research note, LaTeX source, figure source, Python implementation, pinned inputs, results, dependency records, assumptions, and self-audit.
- **51/51 recorded targeted numerical checks pass.** These include independent matrix exponentials, analytic derivatives checked by finite differences, charged curvature checked by an independently assembled dense angular operator, and cutoff comparisons. These checks establish computational consistency within the declared scope, not empirical confirmation of the theory.
- A fresh extraction reproduced `results.json` and `checks.json` byte-for-byte in the preparation environment. The final numerical source/input payload matches that tested extraction. Tested environment: Python 3.14.6, NumPy 2.4.3, SciPy 1.18.1, Matplotlib 3.10.8. Byte identity is not promised across platforms or dependency versions.
- The PDF was compiled twice without warnings and all seven rendered pages were inspected during preparation. Publication preserves the sealed PDF and ZIP without rebuilding them or rerunning the numerical calculation solely for upload.
- The ZIP contains 23 original payload files plus their `SHA256SUMS.txt`. Repository publication metadata is additional and outside that original manifest. Preparation-stage statements that publication had not yet occurred are historical and are superseded by the separate publication record and this release.

Download the PDF, ZIP, and `RELEASE_SHA256SUMS.txt` into one directory and run:

```bash
shasum -a 256 -c RELEASE_SHA256SUMS.txt
unzip Exact_Coupled_Vacuum_Reproducibility_2026-10-22.zip
cd Exact_Coupled_Vacuum_2026-10-22
shasum -a 256 -c SHA256SUMS.txt
```

Follow the extracted `README.md` to rerun the numerical work and rebuild the note. Use a writable copy: reproduction overwrites the result files.

## Release asset SHA-256 checksums

```text
ca898789296461ebb2448d38db21728cb88fd62d61e790f08011219125828f04  Exact_Coupled_Scalar_Radius_Vacuum_2026-10-22.pdf
4f7ca65a1a9bc25fd7a83f255c3a16628ac9d24adb72b01c30d5e7ef6d887242  Exact_Coupled_Vacuum_Reproducibility_2026-10-22.zip
```

## All stated assumptions, branch choices, and limits

The complete sealed assumptions are reproduced below; the unchanged note and `REVIEW.md` provide the derivation and same-session audit details.

1. **Pinned theory input.** The parity-even, full-Dirac spectral action and microscopic Yukawa insertion are inherited from commit `12fa25fc3f35b0ea0b65aa870a93fa0c501957d9` of `Cbaird26/mqgt-scf-continued`. The monopole matrix implementation and 95-digit common-vacuum profiles are copied unchanged. Their specification is conditional; uniqueness and a six-dimensional ultraviolet completion are not established.
2. **Retained background family.** Four copied fermion blocks, unit dimensionless down/lepton/up Yukawas, a round sphere of radius `R=Lambda r`, fixed equivariant monopole connection, and two lowest scalar harmonics are used. Neutral amplitudes are `h_i=H_i/(Lambda R)`. The calculation keeps every power of these amplitudes in the spectral potential. Fermion angular sums use finite cutoffs; this does not mean that every bosonic mode has been retained.
3. **Potential and subtraction.** `W=4 pi^2 V/(kappa Lambda^4)=P+alpha R^2(16 h_d^2+12 h_u^2)-c R^2`. The untuned inherited action has `alpha=0`, with the inherited subtraction `c_star` fixed when testing global stability. In the flat tuned fixtures, `c` is selected separately after solving the flat stationary equations. It is a coupling, not a dynamical scalar. Retuning it is an additional flat-vacuum prescription, not a solution of the cosmological constant problem.
4. **Explicit optional tuning.** The positive scalar-mass counterterm is a specified extra operator, proportional to the sphere volume times the squared scalar amplitudes. Its coefficient `alpha` is chosen to make the minus-profile symmetric-background quadratic mass parameter `-epsilon Lambda^2` at the inherited radius. Exactly the same `alpha` is used for the plus profile. This externally chosen counterterm is not generated or selected by the exact spectral action. In the predecessor's local convention, `alpha=m1 delta2/(4 pi)`.
5. **What is solved.** The flat equations are `P_hd+2 alpha R^2 16 h_d=0`, `P_hu+2 alpha R^2 12 h_u=0`, and `R P_R-2P=0`, with `c=(P+alpha R^2(16 h_d^2+12 h_u^2))/R^2`. The counterterm cancels from the last equation only at fixed `h`. Scalar stationarity makes this consistent with using radius-dependent coordinates in the original fields. Separate fixed-`c_star` stationary diagnostics have nonzero potential and are not solutions of a self-consistent curved-spacetime problem.
6. **Stability meaning.** The full radius/neutral-amplitude potential Hessian, its Schur complement, and charged relative-orientation curvature are checked. Exact gauge and phase flat directions are counted. The two-amplitude scalar kinetic matrix and full neutral gauge kinetic matrix are positive in the numerical fixtures. The radion kinetic term and its scalar mixing are not derived, so no full dynamical-stability or physical pole-mass claim is made.
7. **Omitted directions.** Higher scalar harmonics, nonspherical metric modes, other gauge/bosonic fluctuations, and their tadpoles are not computed or integrated out. A stationary point in the retained family need not be stationary in those directions. Positivity of a restricted Hessian cannot establish full compactification stability, global minimality, or vacuum lifetime.
8. **Anomaly sector.** A potential-free axion with a pure-X Stueckelberg coupling is inherited as an assumption. Its constant value does not change these vacuum equations. With two nonzero neutral scalar amplitudes there are five potential-flat phase/gauge directions in the scalar-plus-axion sector: four are gauge directions and one physical phase remains flat. A six-dimensional anomaly polynomial, explicit two-form reduction, axion potential and Stueckelberg mass remain unspecified.
9. **Global versus local statements.** A resummed leading large-radius heat-trace expression proves a negative asymptotic direction for the untuned action at fixed inherited `c_star`. This is global unboundedness within the declared family, not a proof that every possible metastable extremum is absent. The finite scalar scan and bounded root searches are only numerical exclusions at the tested points and starts. Tuned branches are local minima modulo exact flat directions in the retained potential; global uniqueness is not asserted.
10. **Precision and physical interpretation.** New results use float64/complex128. Cutoff, independent exponential, derivative, and dense charged-orientation checks are supplied; no interval enclosure or universal tail certificate is claimed. Small profile differences have fewer trustworthy digits than absolute values. These are classical spectral-action calculations. Independent normalization, profile selection, quantum thresholds/running and the measured fine-structure constant remain unresolved. This is AI-assisted research with a same-session self-audit, without external peer review.


## Source and attribution

- [Published source package](https://github.com/Cbaird26/mqgt-scf-continued/tree/v2026.10.22-exact-coupled-vacuum/research_continuation/2026-10-22/exact_coupled_vacuum)
- [Publication record](https://github.com/Cbaird26/mqgt-scf-continued/blob/v2026.10.22-exact-coupled-vacuum/research_continuation/2026-10-22/exact_coupled_vacuum/PUBLICATION.md)
- [Full same-session self-audit](https://github.com/Cbaird26/mqgt-scf-continued/blob/v2026.10.22-exact-coupled-vacuum/research_continuation/2026-10-22/exact_coupled_vacuum/REVIEW.md)

License: CC BY 4.0, preserving the inherited attribution. AI-assisted research; no separate-agent referee or external peer review. No measured coupling was fitted, and the measured fine-structure constant remains unexplained.
