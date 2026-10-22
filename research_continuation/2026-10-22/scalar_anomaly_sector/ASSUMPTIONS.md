# Explicit assumptions and declared conventions

Every statement in the research note is conditional on the items below. They are
numbered so that the note, the scripts, and the results files can refer to them.
Inherited items are taken from the pinned predecessor notes without re-derivation.

## Inherited (not re-derived here)

- **I1. Shared spectral action.** `S_sp = (kappa/2) sum_i Tr_Dirac f(D_i^2/Lambda^2)`, kappa > 0,
  `R = Lambda r`, with admissible profiles `f(u) = sum_j w_j exp(-a_j u)`, a_j > 0 distinct, w_j > 0,
  sum w_j = 1. Parity-even full-Dirac trace convention. Four copied repaired six-dimensional
  Weyl blocks, round internal sphere S^2_r, unit U(1)_X monopole flux with monopole index n = x.
- **I2. External gauge coupling convention.** `D_mu = d_mu - i (J_a W^a_mu + q_Y B_mu + x X_mu)`,
  `q_Y = y/2`. SU(2)_W is the sphere isometry (geometric); U(1)_Y and U(1)_X are external.
- **I3. Zero-mode charge table (one block).** Q(3,2,1/6;x=2), L(1,2,-1/2;2), u(3,1,2/3;1), d(3,1,-1/3;1),
  e(1,1,-1;1) with u,d,e physical right-handed; n = 0 colour-triplet spectator (q_Y = 1/6, x = 0) with
  no chiral zero modes. Sector weights D_n = (12,28,16), Y_n^2 = (1/3,32/3,4/3), X_n^2 = (0,28,64).
- **I4. Flat-vacuum prescription.** `F(R) = R P'(R) - 2P(R) = 0`, `c = P/R^2`, `K = P'' - 2c`;
  `(M_4 r)^2/kappa = R^2 J/(24 pi^2)`.
- **I5. Published common-vacuum pair.** Ten nodes `a_j = (178939/338184) j`, weights
  `w^+- = 1/10 -/+ v_j/20`, common radius `R_* = 1.27847241204397865...`, 95-digit data copied
  byte-for-byte from `stationary_profiles_results.json` (commit 3a8a1b0).
- **I6. Weak coefficients.** `Z_W/kappa` for both profiles are the eighteen-digit values printed in the
  predecessor weak-response note (transcript); they are **not** recomputed here. `Z_Y/kappa` and
  `Z_X/kappa` are recomputed from the heat sums and agree with the predecessors' printed values.
- **I7. Unbroken kinetic matrix.** `K^(0) = kappa diag(z_W, z_Y, z_X)`; the exact Y-X trace mixing
  vanishes sector by sector; SU(2) invariance excludes WY and WX terms at the unbroken background.

## Declared in this note

- **A1. Microscopic scalar content.** Two complex six-dimensional scalars on M^4 x S^2_r in the same
  unit X flux: `Phi_d: (SU(3) singlet, q_Y = 1/2, x = +1)`, `Phi_u: (singlet, q_Y = 1/2, x = -1)`.
  No other scalars. Justification: Yukawa charge conservation (Sec. 3.1) and the doublet requirement
  (Sec. 3.2) both force |x| = 1; a Y-charged X-neutral scalar would be an isometry singlet.
- **A2. Higgs-dependent operator (Connes-Chamseddine insertion).** `D_6[Phi] = D_6^(0) + Gamma_7 (x) M[Phi]`
  with `M` the Hermitian block-off-diagonal Yukawa map between the n = 2 and n = 1 blocks of each
  copied block (generation-diagonal Yukawas y_d, y_e, y_u, dimension mass^-1 in six dimensions;
  `y_6 = yhat/Lambda`). The insertion anticommutes with the Clifford generators, so the squared operator
  is of Laplace type with unchanged connection. On the chiral subspaces Gamma_7 acts as a sign, so the
  fermionic Yukawa terms are the standard ones up to a phase.
- **A3. Local scheme for the scalar sector.** Phi-dependent terms are computed from the Seeley-DeWitt
  coefficients a_2 and a_4 of D_6[Phi]^2 in six dimensions (Vassilevich conventions, R = 2/r^2 > 0 on
  the sphere), multiplied by the profile factors Lambda^4 m_2 and Lambda^2 m_1. The Phi-independent
  radius potential and the gauge kinetic coefficients retain the inherited **exact** internal mode
  sums. This is a mixed scheme, declared as such. The exact mode-sum Phi-dependent coefficients are
  defined in the note (Duhamel two-insertion form) but **not computed**.
- **A4. Validity domain.** The local scheme is controlled only for Yukawa-weighted vevs
  `M^2 << Lambda^2/a_j` and is in any case an expansion in 1/R^2 ~ 0.6; a_6 and higher Phi-dependent
  terms are dropped. The untuned truncated minimum violates the first condition; its numbers are
  fixtures of the declared truncated action, not controlled predictions.
- **A5. Hierarchical tuning parameter.** `mu^2/Lambda^2 = 2 m_2/m_1 - delta_2 - 5/(6 R^2)`, where
  delta_2 >= 0 parametrises additional a_2-level contributions from sectors outside the stipulated
  trace (as in the Chamseddine-Connes treatment of the Higgs mass term). delta_2 = 0 is the untuned
  action. The 1/R^2 term (curvature coupling plus the exact lowest-harmonic eigenvalue 1/(2 r^2)) is
  kept at full strength in both cases.
- **A6. Lowest-harmonic truncation.** The four-dimensional scalar fields are the j = 1/2 monopole
  harmonics of Phi_d and Phi_u (the SU(2)_W doublets H_d, H_u). Higher harmonics (j >= 3/2, all
  non-tachyonic at R_*) are not integrated out; their O(v^2) sourcing is neglected.
- **A1b. Six-dimensional chirality of the blocks.** The n = 2 fields (Q, L) and the n = 1 fields
  (u, d, e) carry opposite six-dimensional chirality. With both fluxes of the same sign this is what
  makes Q, L left-handed and u, d, e right-handed in four dimensions (the predecessor's conventional
  orientation), and it is what a scalar Yukawa coupling between them requires. The source archive's
  chirality column was not accessed; this is inferred, not read.
- **A7. Anomaly-cancellation mechanism.** A single Stueckelberg axion theta, shifting only under
  U(1)_X (`theta -> theta + lambda_X`), with couplings theta tr G Gdual, theta tr W Wdual, theta B Bdual,
  theta X Xdual, theta R Rdual fixed by the exact zero-mode anomaly coefficients, a Bardeen
  (generalized Chern-Simons) counterterm that moves the Y^2 X consistent anomaly onto the X leg, and a
  Stueckelberg mass term `(M_St^2/2)(d theta - X)^2`. Its six-dimensional origin is a two-form with a
  Green-Schwarz coupling reduced on the monopole flux; the reduction and the six-dimensional anomaly
  polynomial of the repaired blocks are **not** computed. M_St is a free parameter of the sector.
- **A8. Aligned electroweak vacuum.** Both doublet vevs in the Q_em-neutral component; justified by the
  derived positive coefficient of |H_d^T i sigma_2 H_u|^2. CP conserved at tree level.
- **A9. Broken-background kinetic shifts.** `K = K^(0) + delta K(v)`, with `delta K = O(v^2/Lambda^2)`.
  In the local scheme the leading shift comes from the a_6 term `(1/12) tr(E Omega_AB Omega^AB)`, which
  contains `-(1/12) tr(M^2 Omega_{mu nu} Omega^{mu nu})` (profile factor f(0)), followed by a_8 and a_10
  (factors -f'(0), f''(0)). Through a_10 delta K is therefore a polynomial in the retained local data
  and identical for the published pair. Its exact mode-sum value is not computed. All numerical
  kinetic matrices in this note use delta K = 0 and state so.
- **A10. Tree level only.** No loop corrections, thresholds, or running are computed. The matching
  section is a specification of what must be computed, with the model's exact one-loop coefficients
  supplied as inputs to it. No measured coupling enters any construction.

## Numerical-method statements

- Decimal arithmetic at 95 significant digits; 40 internal levels checked against 60 near R_*;
  adaptive levels (a_1 L^2/R^2 >= 60) for the large-radius scan at 30 digits.
- Exact rational arithmetic (Fraction) for charges, anomaly sums, sphere Beta integrals, and the
  Stueckelberg determinant identity (checked at 200 random rational points).
- The NumPy/SciPy cross-check is independent code, double precision only.
- Nothing here is an interval certificate; the published seed certificate of the predecessor is not
  rerun.
