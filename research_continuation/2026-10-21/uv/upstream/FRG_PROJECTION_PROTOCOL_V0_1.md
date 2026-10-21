# FRG projection protocol v0.1

This protocol applies only to the declared reconstruction basis in
`DECLARED_TRUNCATION_V0_1.md`.

## Fixed conventions

- Euclidean signature; `t = ln(k/k0)`.
- Background split: `g = gbar + h`; background-covariant gauge fixing with
  gauge parameters recorded as part of each run.
- Faddeev-Popov ghost contribution is retained in the supertrace.
- Baseline regulator (optimized/Litim form for each fluctuation sector):
  `R_k(z) = Z_k (k^2-z) theta(k^2-z)` where `z` is the relevant background
  Laplacian eigenvalue. Tensor, vector, scalar, fermion, and ghost regulators
  must be written individually before evaluation.
- Projection backgrounds: constant `H`, `Phi_c`, and `E`; flat background for
  potential/portal terms; constant-curvature background for `R`, `R^2`,
  curvature-scalar, and cosmological projections; gauge backgrounds for
  `F^2` portals.

## Derivation pipeline

1. Write `Gamma_k` from the 41-coordinate basis plus gauge fixing and ghosts.
2. Compute the Hessian `Gamma_k^(2)` in every field sector.
3. Add the sector regulator and invert the block operators.
4. Evaluate the supertrace by a heat-kernel or spectral expansion with all
   thresholds and normalizations retained.
5. Project the result onto every basis operator, yielding `beta_1..beta_41`.
6. Numerically solve the simultaneous system and require
   `max_i |beta_i(g*)|` below a declared tolerance.
7. Construct the finite-difference or analytic `41 x 41` Jacobian, publish its
   eigenvalues and eigenvectors, and state the critical-exponent convention.
8. Repeat under at least one regulator/gauge variation. A reported fixed point
   is provisional if it is not stable under this variation.

## Stop conditions

No result may be called a 41-coupling fixed point if any Hessian block,
regulator term, ghost contribution, operator projection, residual vector, or
stability spectrum is omitted.

The existing Python code has the numerical end of steps 6-7. Steps 1-5 are the
remaining symbolic/functional derivation, and are intentionally not replaced
by guessed coefficients.
