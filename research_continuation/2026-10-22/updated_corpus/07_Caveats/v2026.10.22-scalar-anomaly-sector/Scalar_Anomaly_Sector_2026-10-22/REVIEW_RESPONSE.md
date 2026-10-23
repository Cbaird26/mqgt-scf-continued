# Review record and responses

**Review type.** An independent review pass by a separate AI agent (Claude), run on 22 October 2026
inside the same assisted workflow. The agent had access to this bundle but not to the derivation
process. It was given a ten-item referee checklist: the Laplace-type square, the a_2/a_4 densities,
profile factors, monopole harmonics and overlaps, the 4D reduction, the coupled-radius closed forms,
anomaly and beta coefficients, the neutral matrices, scoping, and citations. **This is not external
peer review.**

The referee re-ran `run_all.py`. All checks passed, the reruns were byte-identical, and the hashes
matched. It then reported fourteen findings. Each is listed below with its disposition. Line
references are to the reviewed version of `research_note.tex`.

| # | Finding | Disposition |
|---|---|---|
| 1 | The underbrace label read "(2/3)R_6/8". The curvature-to-kinetic ratio is (2/3)R_6/4 = R_6/6 = 1/(3R^2). | **Fixed** (label only; the value 1/(3R^2) and mu^2 were already correct). |
| 2 | Boundedness follows from positivity of all quartics. The text instead attributed it to 4 lam_d lam_u − lam_3^2 > 0, which is really the condition for the two-vev stationary point to be a minimum. The recorded formula was also missing a factor of 9: the correct bracket is [27 y_d^4 + 12 y_e^4]. | **Fixed** in the note, `scalar_sector.py` and `vacuum_matching.py` (both conditions now checked separately). |
| 3 | Proposition 1 said the "gauge-boson masses coincide" for the pair, which is false. The physical vector masses solve M^2 r = m^2 K r and depend on z_W, z_Y, z_X; only M^2 coincides. "Polynomial" should be "function", and "nine retained data" should be "six profile factors". | **Fixed.** |
| 4 | M^2_max = mu^2/2 "independent of the Yukawas" holds only for y_e = 0. At the actual fixture vacuum the largest M^2 eigenvalue is 0.860 Lambda^2 (d, e sectors) and 0.688 Lambda^2 (u sector), so the expansion parameters run from 0.455 to 4.55, not 0.39 to 3.9. | **Fixed.** Computed from the vacuum in `vacuum_matching.py`. The quark block is rank one, but Phi_d and Phi_u^* peak at opposite poles, so its maximum is the larger pole value. The conclusion (outside the validity domain) is unchanged. |
| 5 | The "N_b ≥ 12" destabilisation example was wrong, because K_f and gamma both scale with N_b and so gamma/K_f does not depend on N_b. The referee also estimated gamma ≤ ~0.21 over all Yukawa ratios. | **Fixed and sharpened.** gamma depends only on t = y_e^2/y_d^2; exactly, gamma = (3 m1 Nb/16 pi^2) g(t), with 4 ≤ g ≤ 5 and the maximum 5 at t = 3/2. The maximum gives gamma/K_f = 0.01795 < R^4/(8 pi^2 B^2) = 0.04872, so the bound holds for all Yukawa ratios. Checked exactly. |
| 6 | G_H = −pi^2 gamma mu^4 R^2 was applied at R = 0.6, where mu^2 < 0 (no vev). A spurious root of the continued formula exists near R ≈ 0.35. | **Fixed** (found independently before the report arrived). G_H and its derivatives vanish for mu^2 ≤ 0 (R_c = 0.6455). The scan now covers 0.1 ≤ R ≤ 30, F_f is checked to increase via F' = R P'' − P', and F_tot < 0 throughout. The note states that this is a scan, not a certificate. |
| 7 | The leading Higgs-induced kinetic shift delta K arises at a_6, from (1/12) tr(E Omega^2) with profile factor f(0), not at a_8/a_10. | **Fixed** (also found independently). The conclusion that delta K is common to the pair is unchanged. |
| 8 | Delta(e^-2/kappa) was evaluated only at R_*, but the coupled radii split by O(eps) in the tuned regime. "Exact in any scheme with common delta K" and "leading term" overclaimed. | **Fixed and quantified.** The claim is now scoped to R_* and eps → 0. The Y part of the correction is computed exactly from dz_Y/dR = 0.22514: 27% of Delta at eps = 1e-2, 0.28% at 1e-4, 2.8e-7 relative at 1e-8, and it is cross-checked by direct evaluation at the coupled radii. The W part needs dz_W/dR (predecessor kernel), which is not available and is stated as such. |
| 9 | Assertion bookkeeping. The stdlib/NumPy split was wrong, and four checks tested nothing: a hard-coded `True`, a hard-coded 9 − 4 = 5, two literal arithmetic checks, and an overlap quadrature that assumed the lemma it tested. | **Fixed.** The trivial checks were removed or replaced: an exact rational Hessian and orbit-rank count for the pseudoscalar; a computed U(1)_Y non-anomaly condition; and zero modes integrated from the monopole Dirac equation, with exactly n normalisable modes and the overlap recomputed from those profiles. NumPy-dependent checks are now listed explicitly and counted by `run_all.py`: 228 total = 189 standard library + 39 NumPy/SciPy. |
| 10 | "Q–e" is not a Yukawa pair. | **Fixed** to "L–e and Q–u". |
| 11 | "The rank drops to one at the one-vev boundary" holds only for M_St = 0. | **Fixed.** Both cases are now stated and checked: for M_St > 0 the rank stays two and only the photon is massless. |
| 12 | b_YX = 0 removes only the logarithmic running of Y–X mixing; finite threshold mixing can remain. | **Fixed** (qualified). |
| 13 | "No vector-like addition cancels…" was misleading, because vector-like matter never contributes to anomalies. | **Fixed** (also found independently). |
| 14 | "Internal mass 1/(2r^2)" should read "mass-squared". | **Fixed.** |

## Items verified correct by the referee (summary)

- The Laplace-type square and E_Phi.
- alpha_2 = −8 tr M^2 and alpha_4 = (2/3) R tr M^2 + 4 tr M^4 + 4 tr|grad M|^2, including the cross term and curvature sign.
- The profile factors.
- The monopole-harmonic eigenvalues, zero-mode counting, the overlap 1/sqrt(4 pi), and the quartic sphere integrals.
- mu^2, Z_6, the canonical quartics, the vacuum equations, gamma = 48 m1/(13 pi^2), and tan^2 beta = 3/5.
- The normalisation V_rad = kappa Lambda^4 P/(4 pi^2), consistent with the inherited M_4 relation.
- The coupled-radius closed forms and the table values.
- The anomaly vector (1, 4, −4/3, 0, 57, 9), the Witten condition, the beta coefficients, and the SM controls.
- The neutral mass matrix, kernel, determinant identity, T and P, e^-2 = N^T K N, sin^2 theta_W, m_W, the fixtures, and the rho trend.
- The scalar spectrum and the pseudoscalar count.
- All bibliographic data.

## Not checked by the referee

- z_W and the predecessor values (inherited).
- The absolute normalisation of the Green–Schwarz couplings (only ratios checked).
- The exact mode-sum scalar coefficients and delta K (not computed in the note).
- The six-dimensional anomaly polynomial.
- PDF-versus-source agreement. This was checked separately by rendering every page.

## Additional corrections made by the author during the same pass

These were found on re-derivation:

- **E_0 prefactor.** The field-strength term is −(i/2) Gamma^{AB} F_AB with Gamma^{AB} = (1/2)[Gamma^A, Gamma^B]. It is spinor-traceless and affects no result.
- **New assumption A1b.** The n = 2 and n = 1 blocks carry opposite six-dimensional chirality. This is inferred from the predecessor's 4D orientation, not read from the source.
- **Pseudoscalar caveat.** The gauge-invariant operator mu_12^2 e^{2 i theta} H_d^dag H_u is allowed once theta is present. It is not generated by the specified operator; if it were present, it would lift the pseudoscalar.
- **Chamseddine–Connes remark.** Restated as "the a_2 Higgs mass term is of order Lambda^2, so a hierarchy needs additional input or tuning".
- **Four generations.** The retained zero-mode content has four chiral generations; its phenomenological viability is flagged as not addressed.
- **Doublet requirement.** Its agreement with Yukawa charge conservation is described as a consistency check, not an independent input.
