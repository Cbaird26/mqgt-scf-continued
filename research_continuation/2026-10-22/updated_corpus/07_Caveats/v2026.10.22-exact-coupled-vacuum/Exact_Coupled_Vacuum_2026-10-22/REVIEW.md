# Derivation review and numerical self-audit

This record describes the same assistant session using independent numerical methods. There was no separate agent referee or external peer review.

## Main checks

- The full potential at zero scalar background reproduces the inherited heat sum, its first and second radius derivatives, the stationary subtraction, and the scalar Hessian. The potential includes each fermion sector exactly once.
- The full finite-field trace is evaluated by eigenvalues and independently by matrix exponentials. The analytic divided-difference gradient/Hessian is checked by finite differences at a nonzero background.
- Untuned field scans record the common scalar dilation derivative, with increasing angular cutoffs at large fields/radii. Bounded optimizer searches preserve unsuccessful endpoints and residuals. A solver termination flag alone is not treated as a vacuum.
- The large-radius runaway is derived from the resummed leading heat trace, retaining the scalar mass exponentials. Finite-radius calculations check its approach; they are not the proof of the asymptotic statement.
- Both tuned profiles use exactly the same scalar-mass counterterm. Their flatness subtraction is then selected separately and reported. A separate fixed-subtraction calculation has nonzero potential and is explicitly not presented as a flat spacetime vacuum.
- The full radius/amplitude Hessian and scalar-relaxed Schur complement are evaluated at the coupled solutions. Cutoffs 12 and 16 are compared for both coordinates and Hessians.
- Charged relative-orientation curvature is calculated from spectral derivatives and checked against a separately assembled dense angular operator at finite angle. This supplements the neutral-amplitude Hessian rather than assuming charged stability from it.
- The finite-background two-amplitude scalar metric and complete neutral gauge kinetic matrix are checked for positivity. The missing radion kinetic metric is explicitly excluded from the stability claim.
- The near-critical profile split is derived from the common-counterterm quadratic coefficients and positive effective quartic. It is not described as a numerical solution at a tiny unresolved vev.

## Findings and distinctions retained in the note

1. A positive quartic truncation does not establish a finite-field scalar minimum of the exact trace. The untuned quartic candidate is checked against the full gradient.
2. Global unboundedness at fixed inherited subtraction excludes a ground state in the declared family; it does not exclude every possible metastable extremum.
3. The optional scalar tuning is extra input. Its radius dependence is specified because it controls scalar/radius mixing. It cannot be silently replaced by an arbitrary radius-dependent canonical mass shift.
4. The exact mass-slope combination has the opposite sign from the local expression, reversing the tuned radius shift. The relaxed curvature has a different small-tuning limit.
5. Potential-Hessian eigenvalues are coordinate-dependent curvature parameters. Only their inertia is used for the static test; no canonical masses or physical poles are claimed.
6. Gauge and phase zeros are symmetry directions. With the adopted potential-free axion, one physical phase remains flat. Full dynamical stability, higher-harmonic tadpoles, and nonspherical/other bosonic fluctuations remain unresolved.
7. Numerical “exact” means an untruncated spectral representation in the retained amplitudes evaluated at finite fermion cutoffs. It does not mean interval-certified arithmetic, a complete bosonic action, or a quantum loop potential.
8. The common counterterm can put the two profiles on opposite sides of the local symmetry-breaking threshold. A broken-branch comparison is not uniform as the tuning approaches zero.

All executed numerical metrics and tolerances are recorded in `checks.json`; figures and manuscript tables are generated from `results.json`. Delivery checks and fresh-extraction reproduction are recorded in `DELIVERY_VERIFICATION.json` when sealing the package.
