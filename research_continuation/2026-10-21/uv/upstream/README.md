# UV reconstruction: 41-coordinate FRG scaffold

This is an auditable reconstruction framework, not a recovered historical solver.

The supplied archives report a 41-running-coupling, dimension-`<= 6` FRG truncation but do not supply its operator list, complete beta-functional system, fixed-point vector, or `41 x 41` stability matrix. This project therefore makes the missing choices explicit and refuses to fabricate unknown loop coefficients.

The primary PDF also says its Wilsonian operator inventory is restricted rather
than complete and corrects earlier dimension-counting errors. See
`SOURCE_AUDIT.md`; no current registry in this folder is represented as the
historical 41-operator basis.

`DECLARED_TRUNCATION_V0_1.md` is the new versioned basis used for the
reconstruction. It makes the action content and validation conditions explicit
before any full FRG coefficient is claimed.

`FRG_PROJECTION_PROTOCOL_V0_1.md` fixes the reproducibility contract for the
Hessian, ghosts, Litim regulator, operator projections, residuals, and
regulator-dependence checks needed before running the full solver.

`scalar_frg_lpa.py` implements the first concrete Hessian block: the six-real-
scalar constant-background mass matrix and its d=4 Litim-regulated Wetterich
potential trace. It does not include gauge, fermion, metric, or ghost traces.

## What is implemented

- A declared 41-coordinate registry covering gravity, Standard Model gauge/Yukawa/Higgs, two real singlets (`Phi_c`, `E`), non-minimal curvature terms, and dimension-six placeholder operators.
- A beta-system protocol: canonical scaling is populated only where unambiguous; quantum terms must be supplied in a coefficient file or a derived projection module.
- Fixed-point residual, finite-difference stability matrix, critical-exponent calculation, and the exact gravity invariant:

  `beta_gN = (2 + eta_N) gN`; hence, any nonzero `gN*` requires `eta_N* = -2`.

## Deliberate limitation

`model.py` does **not** claim to compute a physical 41-coupling FRG flow. Calling `beta()` without a complete projected quantum contribution raises `IncompleteFlowError`. That failure is the scientifically correct outcome until the Hessian/regulator projection is derived.

## Run

Any Python 3.10+ interpreter with NumPy works (set `PY` to yours):

```sh
PY=python3
$PY -m unittest discover -s tests -v
$PY solve.py --check-reported
```

The reported-point check validates only the necessary gravitational condition. It cannot certify the reported fixed point without all 41 beta functions.

## Explicit derived core

`scalar_core.py` implements the one-loop MS-bar flow for the two-real-scalar,
massless quartic sector in the stated potential normalization. It proves a useful
negative result: that isolated real one-loop core has only the Gaussian fixed
point. Any non-Gaussian scalar point must therefore come from supplied gravity,
gauge, Yukawa, or higher-operator terms; this code does not assume them.

`higgs_two_singlet_core.py` extends this using the one-loop quartic tensor
contraction to four real Higgs components plus `Phi_c` and `E`. This eliminates
hand-entered portal combinatorics; it is still scalar-loop-only and cannot
establish a gravity-matter fixed point.

`sm_gauge_core.py` implements the isolated one-loop Standard Model gauge flow
under the source-stated assumption that both new scalars are gauge singlets. It
correctly produces a positive hypercharge beta function and asymptotic freedom
for `SU(2)` and `SU(3)`; it cannot yield an interacting nonzero one-loop gauge
fixed point.

`perturbative_matter_baseline.py` couples the derived scalar tensor flow to
one-loop SM gauge flow and the dominant top-Yukawa/Higgs terms, with an RK4
integrator. It is a testable matter baseline, not an FRG gravity calculation.

`canonical_scaling.py` supplies the exact engineering-dimension contribution
for every coordinate. Quantum projections are still required before those
canonical terms form a complete beta system.

`einstein_hilbert_litim_benchmark.py` implements a separate, pure-gravity
Einstein-Hilbert optimized-cutoff benchmark from Litim. Its coupling
normalization is deliberately kept distinct from this reconstruction's `gN`.
It includes the benchmark stability matrix and critical exponents.
Run `run_einstein_hilbert_benchmark.py` to reproduce its checked values.

## Verified derived blocks and joint fixed point

Every module below declares its regulator, gauge, and projection convention in
its docstring and in `DECLARED_TRUNCATION_V0_1.md`; nothing is guessed.

| Block | Module | Convention label | Status |
|---|---|---|---|
| Einstein-Hilbert + SM matter (DEP) | `gravity_matter_coupling.py` | arXiv:0705.3059, type-II cutoff, table convention | Verified: FP `(2 Lambda_tilde*, G_tilde*) = (-4.7975095, 1.7621271)`, exponents (3.961, 1.644) |
| Scalar LPA (mass^2, quartic, Z, xi_4) | `scalar_frg_lpa.py` | Litim cutoff, constant background | Verified: Gaussian fixed point; step-plateau convergence |
| Nonminimal curvature `xi_i` | `scalar_tensor_nonminimal_np.py` | NP-DE-DONDER-TYPEA, arXiv:0911.0386, GMFP background | Verified: GMFP (0.00862, 0.02375), theta = 2.143 +- 2.879i, eigenvector (0.3557 +- 0.3776i, 0.8549) |
| Dimension-six scalar potentials | `sextic_lpa.py` | same Litim trace, factor `1/2^(a+b+c)` | Verified: zero-sextic limit matches quartic flow; stencil checks |
| R^2 sector | `r2_gravity_cpr.py` | arXiv:0805.2909, one-loop | Negative result recorded: `beta_{a_C2} = 133/(320 pi^2) > 0` constant, no fixed point |
| 33-coordinate joint flow + spectrum | `partial_flow_41.py`, `joint_fixed_point_stability.py` | DEP gravity + Gaussian matter + NP xi + LPA dim-6 | Verified below |

### Joint fixed point and stability spectrum (33 derived coordinates)

The joint fixed point of the derived 33-coordinate flow is the DEP SM fixed
point with Gaussian matter: `(lambdaN, gN) = (-4.7975095, 1.7621271)`, all
other derived coordinates zero.  Residuals: gravity/matter exact, `xi_i` ~1e-16,
dimension-six ~1e-11 (stencil noise floor).

Critical exponents `theta = -eigenvalue` of the quantum + canonical Jacobian
(`joint_fixed_point_stability.stability_spectrum`):

| Classification | theta | Count | Directions |
|---|---|---|---|
| Relevant | +3.9609 | 1 | Lambda_tilde |
| Relevant | +2.8554 | 3 | mH2, mPhi2, mE2 |
| Relevant | +2.0000 | 3 | xiH, xiPhi, xiE |
| Relevant | +1.6436 | 1 | G_tilde |
| Marginal | 0.0000 | 12 | g1, g2, g3, yt, yb, ytau, six quartics |
| Irrelevant | -0.0756 | 3 | Z_h, Z_phi, Z_E |
| Irrelevant | -2.0000 | 10 | dimension-six entries |

The two gravity eigenvalues reproduce the DEP table-convention exponents
(3.961, 1.644).  Excluded: `a_R2`/`a_C2` (NaN at the Gaussian point; the
one-loop R^2 block has no fixed point) and the six pending derivative/gauge-
portal coordinates (`c_HBox`, `c_PhiBox`, `c_EBox`, `c_HF2`, `c_PhiF2`, `c_EF2`).

**Verdict:** within the declared truncation, the reconstructed flow has a
UV-attractive joint fixed point with **8 relevant**, 12 marginal, and 13
irrelevant directions.  This is a reconstruction result of the declared
conventions, not a reproduction of the historical 41-point claim (8 of the 41
coordinates remain undriven and are recorded as pending).

## Status and license

Theoretical reconstruction and software-validation work; no experimental result is claimed. Text, notes and data: CC BY 4.0 (see `LICENSE`); code may be reused under the same terms.
