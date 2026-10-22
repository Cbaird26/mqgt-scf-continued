# Radion kinetics and scalar mixing in the exact spectral vacuum

Research prerelease, 22 October 2026. Prepared for Christopher Michael Baird / ZoraASI with OpenAI Codex. Continues [the exact coupled scalar-radius vacuum prerelease](https://github.com/Cbaird26/mqgt-scf-continued/releases/tag/v2026.10.22-exact-coupled-vacuum), with inherited inputs pinned at commit `8ac07febf9b760720b9c5e85898499c7195e2dde`.

The declared warped-product Dirac operator determines the field-dependent gravitational coefficient, the radion kinetic term, and its mixing with all eight retained real scalar components. The full nine-field Einstein kinetic matrix is positive at all four tuned fixtures, with five positive generalized squared-mass parameters and four symmetry zeros. **These are local quadratic stability tests at two external derivatives. The radion-dominated mass parameter is near `0.91 Lambda`, without a demonstrated derivative-expansion hierarchy; it is not a verified pole of the full theory or evidence of a fully stable compactification.**

## Results and interpretation

- The fibre-volume spinor map removes the warped measure connection. Radius dependence enters the internal operator and the field-dependent gravitational coefficient. The derivation retains all internal spectral orders and all powers of the retained lowest-harmonic scalar backgrounds; numerical mode sums use finite fermion angular cutoffs.
- The Einstein transformation includes the full Higgs dependence of the gravitational coefficient. At the minus-profile `epsilon=0.01` fixture, the Jordan radial entry is approximately `-0.305924155`, while the Einstein radial entry is `+0.356376269`. A negative Jordan entry alone is not a scalar ghost diagnosis. The smallest eigenvalue of the complete nine-field Einstein kinetic matrix is approximately `0.043668076` there.
- Both profiles at `epsilon=0.01` and `0.0001` pass the retained local kinetic and potential tests. Squared-mass parameters solve `H u/(4 pi^2) = mu G_E u`, with `mu = (m^2/Lambda^2)` in the two-derivative truncation. They are not raw coordinate Hessian eigenvalues or complete-theory pole masses. Representative minus-profile parameters are:

| epsilon | charged pair (each) | light neutral | other neutral | radion dominated |
|---|---:|---:|---:|---:|
| 0.01 | 0.008154775 | 0.009906668 | 0.020157812 | 0.829596301 |
| 0.0001 | 0.000081089 | 0.000098398 | 0.000200016 | 0.832744321 |

- The two profiles have matched unbroken gravitational coefficients but retain differences in derivatives, kinetic matrices and generalized mass parameters. This does not select a physical profile.
- The radion-dominated mass parameter is about `0.91 Lambda`, above the first spectator-fermion KK scale. That KK scale is a comparison only, not a computed bosonic gap. Light scalar tuning does not create a radion-to-cutoff hierarchy.
- The supplied finite-Euclidean-momentum diagnostic holds the Jordan metric flat and fixed. Its approximately 22.6% neutral-amplitude kinetic-submatrix change at the heavy squared parameter is neither an Einstein-frame propagator calculation nor a radion pole shift or error bound.
- A neutral phase/gauge Ward identity is independently checked. With the explicitly assumed positive, independent, potential-free axion kinetic term and pure-X Stueckelberg coupling, gauge reduction leaves five massive scalar parameters and one physical massless phase. The full charged-vector and gauge/metric fluctuation system is not derived.
- The six-dimensional Einstein-Hilbert large-radius limit supplies an independent analytic sign and normalization check. Generalized masses are checked under scalar/radius coordinate changes.

The selected scalar-mass counterterm and separately selected flatness subtraction remain external inputs, held fixed when differentiating each fixture. The inherited untuned runaway remains a separate result about the untuned action. The four computed fixtures do not constitute a sampled continuation curve; figure lines only connect them.

## Reproducibility and verification

- Eight-page research note, complete LaTeX sources, Python implementation, generated figure/table, pinned inputs, full matrices/eigenvectors, results, explicit tolerances, dependency records, assumptions and same-session self-audit.
- **109/109 recorded targeted computational checks pass.** They include independent matrix-exponential quadrature, dense angular charged assembly, external round-S4 curvature normalization, gravitational finite differences, the transformed potential Hessian, neutral Ward identity, coordinate invariance and generalized-eigenvector residuals.
- The cutoff 12-to-16 comparisons give maximum changes of approximately `7.0e-15` in the Einstein kinetic matrices and `6.6e-14` in generalized squared-mass parameters. These are convergence diagnostics, not interval enclosures or a uniform spectral-tail certificate.
- During preparation, a fresh extraction reproduced `results.json` and `checks.json` byte-for-byte. Figure and table outputs also matched; a fresh two-pass LaTeX build had no warnings and all eight rendered pages matched the delivered PDF. The final numerical source/input payload matches that tested extraction.
- Tested environment: Python 3.14.6, NumPy 2.4.3, SciPy 1.18.1, Matplotlib 3.10.8. Byte identity is environment-dependent. The 109 checks test computational consistency, not empirical confirmation or independent physical predictions.
- Publication preserves the sealed PDF and ZIP unchanged, without rebuilding or rerunning the numerical calculation solely for upload. The ZIP contains 30 payload files plus their `SHA256SUMS.txt`. The repository adds three publication metadata files outside that manifest. Preparation-stage statements that publication had not occurred remain historical records, superseded by this release and `PUBLICATION.md`.

Download the PDF, ZIP and `RELEASE_SHA256SUMS.txt` into one directory, then verify:

```bash
shasum -a 256 -c RELEASE_SHA256SUMS.txt
unzip Radion_Dynamics_Reproducibility_2026-10-22.zip
cd Radion_Dynamics_2026-10-22
shasum -a 256 -c SHA256SUMS.txt
```

Follow the extracted `README.md` to rerun the numerical work and rebuild the note. Use a writable copy: reproduction overwrites the result files.

## Release asset SHA-256 checksums

```text
b84df1f00c1cbeb67a0394bbc62a225e9db18e33306a87c858301cd678568e32  Radion_Kinetics_and_Scalar_Mixing_2026-10-22.pdf
d8bab0a5f5e942e4dcf7493f4c2bd345e230c7a79cc047592f5d2e48d49df5e7  Radion_Dynamics_Reproducibility_2026-10-22.zip
```

## All stated assumptions, dynamical interpretation and limits

The complete sealed assumptions follow verbatim. The unchanged note and self-audit retain the derivation details and qualifications.

1. **Pinned operator.** The parity-even full-Dirac spectral action, microscopic scalar insertion, four copied fermion blocks, unit dimensionless Yukawas, monopole matrices and positive ten-exponential profiles are inherited from the coupled-vacuum release at commit `8ac07febf9b760720b9c5e85898499c7195e2dde`. Their uniqueness, phenomenological viability and six-dimensional ultraviolet completion are not established.
2. **Declared spacetime extension.** The torsion-free metric is `g_4(x)+r(x)^2 dOmega_2^2`, with fixed equivariant monopole connection and lowest scalar harmonics. The Hilbert-space map `chi=r psi` removes the warped spinor measure connection, leaving `D_g+gamma5 Lambda B(R,h)`. This is a classical spectral equivalence, not a quantum measure statement. `Lambda` is fixed; no dynamical cutoff dilaton is introduced.
3. **What is derived.** At two external derivatives, the field-dependent gravitational coefficient, all nine radion/real-scalar Jordan kinetic entries and Einstein-frame mixing are derived from that operator. All powers of the retained scalar amplitudes and internal spectral orders are retained. Finite fermion angular cutoffs approximate the infinite sums. This is not a complete bosonic truncation.
4. **Extra operators and subtraction.** The scalar-mass counterterm `alpha R^2 (16 |h_d|^2+12 |h_u|^2)` is a chosen extra potential term, common to both profiles. The flatness subtraction `c R^2` is selected separately per fixture and held fixed under field differentiation. Neither is derived or a solution of the cosmological constant problem. Both are assumed to add no derivative or curvature terms. No independent Einstein-Hilbert, scalar kinetic or nonminimal curvature counterterm is included. Allowing unspecified such operators would alter the answer.
5. **Frame, sign and units.** The Lorentzian two-derivative action uses signature `(-+++)` and `kappa>0`, obtained by the stated low-derivative continuation of the Euclidean action. The gravitational coefficient is `F=kappa Lambda^2 f>0`. At each fixture `f0=f_vac` defines the Einstein metric, so vacuum units match the Jordan convention. The negative Jordan radial entry alone is not a ghost diagnostic; the full Einstein matrix is tested. Changing the constant reference rescales Einstein units and does not fix a measured Planck scale.
6. **Precisely established stability.** The retained nine-field Einstein kinetic matrix is positive for both profiles at epsilon 0.01 and 0.0001. The potential Hessian has five positive directions and four symmetry zeros. Generalized squared-mass parameters are positive in the five massive directions. These are local infrared quadratic stability tests in the two-derivative scalar/gravity sector. They do not establish nonlinear stability, global minimality, uniqueness, vacuum lifetime or a complete stable compactification.
7. **Near-cutoff radion.** The radion-dominated parameter is about `0.91 Lambda`, with no demonstrated derivative-expansion hierarchy. Full momentum-dependent metric/radion mixing, Lorentzian poles and residues, reflection positivity and ultraviolet unitarity are not computed. Higher-derivative gravitational ghosts are neither established nor excluded. The light scalar parameters also remain truncation results; their smaller expansion parameters are diagnostics, not complete-propagator error certificates.
8. **Momentum diagnostic boundary.** The supplied finite-Euclidean-momentum scalar/radius kernel holds the Jordan metric flat and fixed. It checks the derivative formula and illustrates momentum dependence. It is not the Einstein-frame propagator, a Lorentzian pole calculation, or an error estimate for the physical radion mass.
9. **Omitted fields.** Higher scalar harmonics, nonspherical metric modes, other gauge/bosonic fluctuations and their tadpoles are not solved or integrated out. A restricted stationary point may not be stationary in the omitted directions. The first spectator-fermion KK mass is used only as a scale comparison, not as a computed bosonic gap.
10. **Gauge and axion assumptions.** The neutral phase/gauge Ward identity is checked, and the predecessor's positive neutral gauge kinetic matrices remain the inherited controls. A complete charged-vector response and the full gauge/metric fluctuation system are not derived. The potential-free axion is assumed to have a positive independent kinetic coefficient, a pure-X Stueckelberg coupling, and no additional independent derivative mixing. After gauge reduction one physical phase remains massless. The six-dimensional anomaly polynomial, two-form reduction, axion potential and Stueckelberg scale remain unspecified.
11. **Numerical status.** New calculations use float64/complex128 and finite internal cutoffs, with independent exponential, curvature, derivative, Ward-identity and coordinate checks. No interval enclosure or uniform spectral-tail certificate is supplied. Tiny profile differences have fewer reliable digits than absolute values. The 109 checks are computational consistency tests, not 109 physical predictions. Byte reproduction is environment-dependent.
12. **Physical claims and review.** This is a classical spectral-action calculation; independent normalization, profile selection, quantum loops, thresholds/running and the measured fine-structure constant remain unresolved. No measured coupling is fitted. The note is AI-assisted research with a same-session self-audit and independent computational paths. There was no separate-agent referee or external peer review. No claim of priority for the geometric or heat-kernel methods is made.


## Additional limits recorded in the sealed self-audit

1. The new derivation closes the missing radion kinetic term only at two external derivatives within the declared background family. It does not close the full compactification-stability problem.
2. The heavy radion parameter is close to the spectral cutoff and above the first spectator-fermion KK scale. The note does not promote it to a certified physical pole.
3. The fixed-metric finite-momentum calculation excludes metric fluctuations. Its 22.6% amplitude-submatrix change near the heavy squared parameter is not interpreted as a radion pole shift or an Einstein-frame error bound.
4. Positive retained kinetic energy and nonnegative mass parameters mean no scalar ghost/tachyon/gradient instability in that local quadratic truncation. They do not prove ultraviolet unitarity, reflection positivity, or absence of higher-derivative graviton modes.
5. The selected extra mass term and flatness subtraction supply no derivative operators by assumption. Additional allowed operators could change the kinetic matrix. The normalization and physical profile remain unselected.
6. The assumed axion kinetic coefficient is positive but unspecified. One physical massless phase remains; a strict isolated minimum is not claimed.
7. Higher-mode tadpoles, full charged-vector kinetics and the complete bosonic spectrum remain explicit open calculations.
8. The two tunings are computed fixtures. Lines in the figure connect them and do not represent a sampled continuation curve. Numerical profile differences are reported with limited meaningful precision.


## Source and attribution

- [Published source package](https://github.com/Cbaird26/mqgt-scf-continued/tree/v2026.10.22-radion-kinetics-scalar-mixing/research_continuation/2026-10-22/radion_dynamics)
- [Publication record](https://github.com/Cbaird26/mqgt-scf-continued/blob/v2026.10.22-radion-kinetics-scalar-mixing/research_continuation/2026-10-22/radion_dynamics/PUBLICATION.md)
- [Complete same-session self-audit](https://github.com/Cbaird26/mqgt-scf-continued/blob/v2026.10.22-radion-kinetics-scalar-mixing/research_continuation/2026-10-22/radion_dynamics/REVIEW.md)
- [Primary-source background and input lineage](https://github.com/Cbaird26/mqgt-scf-continued/blob/v2026.10.22-radion-kinetics-scalar-mixing/research_continuation/2026-10-22/radion_dynamics/references/SOURCES.md)

License: CC BY 4.0, preserving inherited attribution. AI-assisted conditional research; no separate-agent referee or external peer review. No measured coupling was fitted; the measured fine-structure constant remains unexplained.
