# Derivation review and numerical self-audit

This records a same-session AI-assisted review. No separate agent or external referee participated.

## Derivation checks

- The warped fibre has dimension two, so the Dirac measure connection is one times the derivative of `ln r`. The unitary map between the two spinor measures cancels this term. Radius dependence then enters the internal operator and the four-dimensional gravitational coefficient. No extra radion term is silently added.
- The action's `kappa/2` factor, four external spin components and sector multiplicities are tracked. The curvature coefficient reproduces the inherited `F/(kappa Lambda^2)=J/(24 pi^2)`. A separate exact external-S4 Dirac sum checks this normalization and its sign.
- The mixed kinetic kernel follows from the two-insertion expansion, including both the spin-derivative vertex and the derivative of the shifted Gaussian. The second derivative of the nonlinear radius insertion is a momentum-independent contact term; it is included in the potential Hessian and does not add a kinetic term.
- The unbroken diagonal heat sums and the independent six-dimensional Einstein-Hilbert reduction agree on the large-radius Jordan coefficient. This provides an analytic sign/factor check outside the finite-background matrix implementation.
- The Einstein transformation includes derivatives of the full Higgs-dependent gravitational coefficient. The Jordan metric is not used as the physical scalar ghost test. A negative Jordan entry is cured by the calculated conformal contribution at the supplied fixtures.
- The flat-vacuum Hessian is differentiated with `c` and `alpha` fixed. Because both the potential and its gradient vanish at the fixture, the field-dependent Weyl factor does not alter its Hessian in vacuum-normalized units. Finite differences of the transformed potential check this statement.
- The full eight-scalar tangent assembly includes neutral real/imaginary and charged real/imaginary directions. Hermitian conjugates are used in complex matrix products. The neutral amplitude block reproduces the earlier implementation; a separately assembled dense angular operator checks the charged metric.
- Phase covariantization reproduces the independent spectral neutral gauge mass response. This supports the phase conventions and low-momentum gauge interpretation without purporting to derive the unknown axion sector.
- Generalized eigenvalues, rather than raw Hessian eigenvalues, define the two-derivative mass parameters. Eigenvector residuals, kinetic normalization and invariance under radius-dependent original scalar coordinates are checked.

## Limits retained in the note

1. The new derivation closes the missing radion kinetic term only at two external derivatives within the declared background family. It does not close the full compactification-stability problem.
2. The heavy radion parameter is close to the spectral cutoff and above the first spectator-fermion KK scale. The note does not promote it to a certified physical pole.
3. The fixed-metric finite-momentum calculation excludes metric fluctuations. Its 22.6% amplitude-submatrix change near the heavy squared parameter is not interpreted as a radion pole shift or an Einstein-frame error bound.
4. Positive retained kinetic energy and nonnegative mass parameters mean no scalar ghost/tachyon/gradient instability in that local quadratic truncation. They do not prove ultraviolet unitarity, reflection positivity, or absence of higher-derivative graviton modes.
5. The selected extra mass term and flatness subtraction supply no derivative operators by assumption. Additional allowed operators could change the kinetic matrix. The normalization and physical profile remain unselected.
6. The assumed axion kinetic coefficient is positive but unspecified. One physical massless phase remains; a strict isolated minimum is not claimed.
7. Higher-mode tadpoles, full charged-vector kinetics and the complete bosonic spectrum remain explicit open calculations.
8. The two tunings are computed fixtures. Lines in the figure connect them and do not represent a sampled continuation curve. Numerical profile differences are reported with limited meaningful precision.

`checks.json` contains all executed checks, errors and tolerances. `DELIVERY_VERIFICATION.json` records fresh-extraction reproduction and final PDF inspection when sealing is complete.
