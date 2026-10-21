# Declared truncation v0.1 - reconstruction convention

Status: **new, declared reconstruction basis**. It is not a transcription of a
historical 41-coupling calculation.

## Fields and conventions

Euclidean background-field FRG in four dimensions with fields
`g_mu_nu`, Standard Model fields, and real gauge-singlet scalars `Phi_c` and
`E`. The flow is the Wetterich equation

`partial_t Gamma_k = 1/2 STr[(Gamma_k^(2) + R_k)^(-1) partial_t R_k]`.

Use background-covariant gauge fixing and Faddeev-Popov ghosts. A regulator
choice, gauge parameters, and projection backgrounds must be recorded with
every numerical result; no coefficient in this project is valid without them.

## Coordinate basis

The 41 coordinates follow `model.NAMES` in order:

1. `gN`: dimensionless Newton coupling; Einstein-Hilbert `R`.
2. `lambdaN`: dimensionless cosmological term.
3. `a_R2`: `R^2`.
4. `a_C2`: Weyl-tensor squared.
5-7. `g1`, `g2`, `g3`: Standard Model gauge kinetic terms.
8-10. `yt`, `yb`, `ytau`: third-generation Yukawas.
11-12. `lambdaH`, `mH2`: Higgs quartic and mass.
13-14. `lambdaPhi`, `mPhi2`: `Phi_c` quartic and mass.
15-16. `lambdaE`, `mE2`: `E` quartic and mass.
17. `kappaPhiE`: `Phi_c^2 E^2`.
18-19. `kappaHPhi`, `kappaHE`: `|H|^2 Phi_c^2`, `|H|^2 E^2`.
20-22. `xiH`, `xiPhi`, `xiE`: `R|H|^2`, `R Phi_c^2`, `R E^2`.
23-25. `Z_h`, `Z_phi`, `Z_E`: kinetic normalizations (projected as anomalous dimensions).
26-35. scalar dimension-six potentials: `|H|^6`, `Phi^6`, `E^6`,
`|H|^4 Phi^2`, `|H|^4 E^2`, `|H|^2 Phi^4`, `|H|^2 E^4`,
`Phi^4 E^2`, `Phi^2 E^4`, `|H|^2 Phi^2 E^2`.
36-38. derivative dimension-six operators: `|H|^2 Box |H|^2`,
`Phi^2 Box Phi^2`, `E^2 Box E^2`.
39-41. gauge-strength portals: `|H|^2 F^2`, `Phi^2 F^2`, `E^2 F^2`.

Implementation names for entries 26-41 are, respectively: `c_H6`, `c_Phi6`,
`c_E6`, `c_H4Phi2`, `c_H4E2`, `c_H2Phi4`, `c_H2E4`, `c_Phi4E2`, `c_Phi2E4`,
`c_H2Phi2E2`, `c_HBox`, `c_PhiBox`, `c_EBox`, `c_HF2`, `c_PhiF2`, `c_EF2`.

## Convention labels and fixed points (recorded, not guessed)

- Litim type-A Einstein-Hilbert benchmark (`gravity_frg.py`, hep-th/0606044,
  alpha -> infinity, g_eq = c_d gN with c_4 = 24 pi): fixed point
  `(lambdaN, gN) = (0.25, 1/(1536 pi))`, `eta_N* = -2`,
  `theta = 5/3 +- i sqrt(167)/3`.
- DEP gravity-matter block (`gravity_matter_coupling.py`, arXiv:1311.2898,
  type-II cutoff, alpha = rho = 1, table ghost factor 2*2^{[d/2]}): in the
  scaffold coordinates `gN = G_tilde` and `lambdaN = 2 Lambda_tilde`, so
  `beta_gN = beta_G_tilde` and `beta_lambdaN = 2 beta_Lambda_tilde`.
  Verified pure-gravity fixed point `(Lambda_tilde, G_tilde) = (0.01046,
  0.7725)` and SM row `(-2.399, 1.762)`; the coupled SM joint fixed point in
  scaffold coordinates is `(gN, lambdaN) = (1.7621, -4.7975)` with the matter
  sector at its Gaussian point.  These numbers are regulator/gauge dependent.
- The earlier claimed `(gN* ~ 0.27, lambdaH* ~ 0.038)` is **superseded**: it
  matches no recorded regulator, gauge, or projection convention, and it is
  not reproduced by any verified block above.
- Narain-Percacci nonminimal-coupling block (`scalar_tensor_nonminimal_np.py`,
  arXiv:0911.0386, convention label NP-DE-DONDER-TYPEA, d = 4, de-Donder
  gauge, optimized/Litim-shape cutoff, single scalar): the `xi_2` flow of the
  closed-form five-coupling system (Appendix A, eqs. A1-A5) is evaluated on
  the paper's GMFP gravity background `(lambda_0*, xi_0*) = (0.00862,
  0.02375)` with `eta = 2`, using the per-species mapping
  `lambda_2 = m_i^2`, `xi_2 = xi_i`, `lambda_4 = lambda_i/4`.  Verified
  against the paper: GMFP fixed point, critical exponents `2.143 +- 2.879 i`,
  and eigenvector `(0.3557 +- 0.3776 i, 0.8549)` (numerical Jacobian).
  Recorded paper-internal inconsistency: the printed closed-form entries of
  the stability matrix `M_00` are not the numerical derivatives of the
  Appendix A flows at the GMFP (the flow-derived Jacobian reproduces the
  published exponents and eigenvectors; the `M_00` closed forms do not).
  Note this block is a different gauge/cutoff convention from the DEP block;
  the two are never mixed in one solve (the `xi` entries sit on the NP GMFP
  background by construction).
- Sixth-order scalar LPA block (`sextic_lpa.py`): the same Litim-regulated
  Wetterich trace as the mass-squared block, projected at zero field onto the
  ten scalar dimension-six operators of the basis.  Convention: every
  monomial `(h^2)^a (Phi^2)^b (E^2)^c` with `a+b+c = 3` carries a factor
  `1/2^(a+b+c)` (the same "2 per invariant factor" rule that fixes the
  quartic sector `lambda_H/4 (h^2)^2`, `p/4 (h^2) Phi^2`); radial projections
  then read `c_H6 = d^6 flow/dh^6 / 90`, `c_H4Phi2 = d^4 d^2 flow/(dh^4
  dPhi^2) / 6`, `c_H2Phi2E2 = d^2 d^2 d^2 flow/(dh^2 dPhi^2 de^2)`, with
  the O(4) combinatorics fixed by the sextic tensor
  `c_000000 = 90 c_H6`, `c_0000PhiPhi = 6 c_H4Phi2`,
  `c_00PhiPhiEE = c_H2Phi2E2`.  Scalar loops only; step choice
  `step = 5e-2` gives a convergence plateau (values at step 3e-2 and 7e-2
  agree to a few percent).
- With the DEP SM gravity fixed point and Gaussian matter (all masses,
  quartics, Yukawas, `xi`, and dimension-six couplings zero), every
  currently derived entry vanishes: the `xi_i` entries exactly (verified
  residual ~1e-16) and the dimension-six entries to the stencil noise floor
  (~1e-11).
- Joint fixed point and 33-dimensional stability spectrum
  (`joint_fixed_point_stability.py`): the joint fixed point is the DEP SM
  fixed point `(lambdaN, gN) = (-4.7975095, 1.7621271)` (table convention,
  `improved=False`, ghost factor `2*2^{[d/2]}`) with all 31 other
  coordinates zero.  The numerical Jacobian of the derived flow (quantum +
  canonical terms for `m_i^2` and the `c_*` entries) gives 33 critical
  exponents `theta = -eigenvalue`: **8 relevant** (`+3.9609`, `+2.8554 x3`
  for `mH2/mPhi2/mE2`, `+2.0000 x3` for `xiH/xiPhi/xiE`, `+1.6436`),
  **12 marginal** (`0.0000 x12`: the gauge, Yukawa, and six quartic
  couplings of the SM block, all Gaussian), **13 irrelevant**
  (`-0.0756 x3` from `eta_s = -0.076`, `-2.0000 x10` the dimension-six
  entries).  The two gravity eigenvalues reproduce the DEP table exponents
  (3.961, 1.644).
- **R^2-sector record (negative result, not papered over)**: in the
  Codello-Percacci-Rahmede one-loop block
  `beta_{a_C2} = 133/(320 pi^2) ~ +0.04211` is strictly positive and
  constant, so the Weyl-squared direction runs away and this block has no
  fixed point for `a_C2`.  `beta_{a_R2}` vanishes on the two lines
  `a_R2 = 2 x a_C2` with `x in {0.0295207, 0.4704793}`, but because `a_C2`
  never stops the `(a_R2, a_C2)` subsystem has no true fixed point either.
  `a_R2`/`a_C2` are therefore NaN at the Gaussian point (singular
  parametrization) and are excluded from the stability spectrum.
- The remaining undriven coordinates `c_HBox`, `c_PhiBox`, `c_EBox`
  (derivative dimension-six operators, not projectable by a
  constant-background LPA), and `c_HF2`, `c_PhiF2`, `c_EF2` (gauge-strength
  portals, require a dressed-gauge-sector trace) are recorded as
  **pending**; no flow value is fabricated for them.

## Exclusions and controls

- Four-derivative scalar operators are dimension eight and are excluded from
  this dimension-six basis, consistent with the primary-source correction.
- Redundant operators must be removed only by the declared integration-by-parts,
  equation-of-motion, and field-redefinition convention.
- Every result must include the operator table, gauge parameters, regulator,
  projection background, numerical residual `max_i |beta_i|`, and the full
  stability spectrum.

## First non-negotiable checks

1. `beta_gN=(2+eta_N)gN`; nonzero `gN*` requires `eta_N*=-2`. This holds
   for the Litim type-A convention; under the DEP convention label the
   entries 0/1 are instead `beta_gN = beta_G_tilde` and
   `beta_lambdaN = 2 beta_Lambda_tilde` with `eta_h ~ 0.27 != -2` at the
   fixed point.
2. A proposed point must make every one of the 41 beta residuals small.
3. Critical exponents are the eigenvalues of the declared 41x41 Jacobian,
   with the sign convention stated alongside the result.
