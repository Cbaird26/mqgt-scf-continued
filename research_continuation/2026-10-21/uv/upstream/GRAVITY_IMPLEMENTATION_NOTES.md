# Gravity-block implementation notes

The next derivation is restricted to an Einstein-Hilbert test block
`(gN, lambdaN)` before extending it to `R^2` and `C^2`.

Primary references selected for the exact gauge/parametrization/regulator
formulae:

- M. Reuter and F. Saueressig, *Renormalization Group Flow of Quantum Gravity
  in the Einstein-Hilbert Truncation*, arXiv:hep-th/0110054.
- D. Litim, *On fixed points of quantum gravity*, arXiv:hep-th/0606044.
- D. Benedetti, *Asymptotic safety goes on shell*, arXiv:1107.3110.

## Required implementation order

1. Choose linear or exponential metric split and record it.
2. Write the background-covariant gauge-fixing and Faddeev-Popov operator.
3. Decompose metric fluctuations into tensor/vector/scalar modes.
4. Derive the regulated Hessian, including ghost signs and all threshold
   functions, in precisely that convention.
5. Project first onto `sqrt(g)` and `sqrt(g) R`, solve the two-coordinate
   test system, and verify `eta_N=-2` at any non-Gaussian `gN` root.
6. Add the `R^2` and `C^2` blocks; repeat regulator/gauge variation before
   coupling the matter and dimension-six operators.

No numerical coefficients are copied into the solver until all six steps are
completed in one convention. Results from another parametrization, gauge, or
cutoff are comparison data rather than coefficients for this reconstruction.
