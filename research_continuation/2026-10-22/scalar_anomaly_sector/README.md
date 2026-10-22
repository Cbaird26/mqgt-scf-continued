# A Microscopic Scalar and Anomaly-Complete Sector for the Shared Spectral Action

**Baird / ZoraASI Research Continuation — research note dated 22 October 2026.**
Prepared for Christopher Michael Baird with Claude. Package prepared 22 October 2026, America/New_York.

**Status:** conditional result within a declared completion of the stipulated shared spectral
action. It specifies a six-dimensional scalar sector and an anomaly-cancelling sector, derives what
the specified operator fixes, solves the coupled vacuum under stated assumptions, computes the
broken-background neutral matrices and the surviving massless generator by the null-space residue,
and sets out the quantum-matching problem. It does not determine the physical profile, the
normalization kappa, thresholds, or running, and it does not derive the measured fine-structure
constant. Preparation of this package does not itself constitute a repository publication.

## What is specified

- **Scalars (A1).** Two complex 6D scalars in the unit X flux: `Phi_d (q_Y = 1/2, x = +1)` and
  `Phi_u (q_Y = 1/2, x = -1)`. The charge |x| = 1 is forced by Yukawa charge conservation between the
  n = 2 (Q, L) and n = 1 (u, d, e) blocks and, independently, by the requirement that the lowest
  monopole harmonic be an SU(2)_W doublet (j = |x|/2). The zero-mode Yukawa overlaps are exactly
  1/(2 sqrt(pi)).
- **Higgs-dependent operator (A2).** `D_6[Phi] = D_6^(0) + Gamma_7 (x) M[Phi]`, a Connes–Chamseddine
  insertion whose square is of Laplace type with unchanged connection.
- **Anomaly sector (A7).** A Stueckelberg axion shifting only under U(1)_X (6D two-form on the flux),
  with a Bardeen counterterm protecting U(1)_Y, cancelling the exact zero-mode anomalies
  (SU(3)^2 X, SU(2)^2 X, Y^2 X, Y X^2, X^3, grav^2 X) = (1, 4, -4/3, 0, 57, 9) per block.

## What is computed

| Item | Result |
|---|---|
| Inherited pair | nodes, 95-digit weights, R_* reloaded byte-for-byte; P, P', J, c, K, z_Y reproduced to 2e-93; z_Y, z_X match predecessor printed values |
| Local scalar action (a_2, a_4) | `-8 Lambda^4 m2 tr M^2 + Lambda^2 m1 (4 tr|grad M|^2 + 4 tr M^4 + (2/3) R_6 tr M^2)`; two-doublet quartic `lam_d|H_d|^4 + lam_u|H_u|^4 + lam_A(|H_d|^2|H_u|^2 + |H_d^T i s2 H_u|^2)`; common doublet mass parameter `Lambda^2 [2 m2/m1 - 5/(6 R^2)]` |
| Invariance | every local coefficient through a_10 is identical for the published pair |
| Untuned vacuum | tachyonic doublet at R_*; largest Yukawa-weighted vev 0.860 Lambda^2 for the fixture (0.745 Lambda^2 if y_e = 0), outside the local domain; no flat stationary radius on a scan 0.1 <= R <= 30 or asymptotically |
| Tuned (hierarchical) vacuum | first-order radius shift, pair splitting proportional to K_- - K_+, induced curvature shift -8 pi^2 gamma B^2 / R_*^4 = -4.2503 (K_f = 11.72 -> 7.47); the Nb-independent stability bound gamma/K_f < R^4/(8 pi^2 B^2) holds for all Yukawa ratios (exact gamma range) |
| Neutral matrices | kernel of M^2 is (1,1,0) for all vevs and any Stueckelberg mass; `e^-2 = K_WW + K_BB + 2 K_WB`; `Delta(e^-2/kappa) = 1.5519080018e-7` at R_*, with an O(eps) radius-splitting correction at the tuned coupled vacuum (Y part computed: 27% at eps = 1e-2, 0.28% at 1e-4); massive spectrum with M_St in closed form |
| Tree matching data | `alpha^-1_tree = 4 pi kappa (z_W + z_Y) = 5.026428 kappa`; `sin^2 theta_W^tree = 0.49887`; exact one-loop coefficients b_3 = -17/3, b_2 = -5/3, b_Y = 83/9, b_X = 316/3, b_YX = 0 |
| Scalar counting | exact rational Hessian: rank 4, nullity 5, gauge-orbit rank 4, so one physical massless pseudoscalar |
| Checks | 228 recorded assertions (189 standard library only, 39 NumPy/SciPy), all passing; reruns byte-identical |
| Review | an independent AI review pass reported 14 findings; all addressed (see `REVIEW_RESPONSE.md`) |

## Files

| File | Purpose |
|---|---|
| `Scalar_Anomaly_Sector_Coupled_Vacuum_2026-10-22.pdf` | Complete thirteen-page research note |
| `research_note.tex` | Manuscript source (LaTeX; compiles with pdflatex, Latin Modern or Type1 CM fallback) |
| `ASSUMPTIONS.md` | Every inherited item (I1–I7) and declared assumption (A1, A1b, A2–A10) |
| `REVIEW_RESPONSE.md` | Independent review findings and their dispositions |
| `heatsums.py` | Shared exact-internal-mode heat sums (Decimal) |
| `inherited_inputs.py` → `inherited_inputs_results.json` | Reloads and re-verifies the published pair; recomputes Z_Y, Z_X; records inherited Z_W |
| `scalar_sector.py` → `scalar_sector_results.json` | Charges, monopole harmonics, overlaps, Clifford and heat-kernel assembly checks, local scalar action |
| `anomaly_sector.py` → `anomaly_sector_results.json` | Exact anomaly sums, Green–Schwarz couplings, Stueckelberg identity, one-loop coefficients |
| `vacuum_matching.py` → `vacuum_matching_results.json` | Coupled vacuum (untuned and tuned), neutral matrices, null space, spectrum, matching data |
| `independent_check.py` → `independent_check_results.json` | Independent NumPy/SciPy cross-check |
| `run_all.py` | Runs everything in order and reports assertion totals and byte-level reproducibility |
| `inputs/common_vacuum_pair.json` | Byte-identical copy of the published `stationary_profiles_results.json` (commit 3a8a1b0) |
| `inputs/inherited_weak_coefficients.json` | Transcript-printed Z_W values and their provenance |
| `provenance.json` | Sources, hashes, environment, result summary, scope limits |
| `SHA256SUMS.txt` | Manifest of every file in this package |
| `LICENSE` | CC BY 4.0 (destination repository license) |

## Reproduction

From this directory:

```bash
python3 run_all.py            # standard-library scripts, then independent_check.py if numpy+scipy import
python3 run_all.py --no-float # skip independent_check.py (core scripts need only the standard library;
                              # their six NumPy checks run only if NumPy is importable)
```

The four core scripts need only the Python standard library (Python 3.10+; tested on 3.13). The
independent check needs NumPy and SciPy. The run takes about half a minute. Each script overwrites
only its own result file; verify `SHA256SUMS.txt` first if checking archived bytes. The LaTeX source
compiles with `pdflatex research_note.tex` (twice).

## Scope and caveats (unchanged from the predecessors, extended)

- The scalar sector is treated in the local heat expansion (a_2–a_4) while the gauge coefficients
  and the radius potential are exact mode sums (A3). At R_* ≈ 1.28 the local coefficients are not a
  controlled approximation to the exact scalar coefficients, which are defined but not computed.
- The untuned truncated action places the electroweak scale at O(Lambda) and, on the scan and
  asymptotically, admits no flat stationary radius; a hierarchy needs an additional a_2-level input
  (A5) outside the stipulated trace. Numbers from the untuned fixture are fixtures of the truncated
  action.
- The pair difference in e^-2 is exact at R_*; at the tuned coupled vacuum it acquires an O(eps)
  correction from the radius splitting, whose W part (dz_W/dR) is not available here.
- The retained zero-mode content has four chiral generations; phenomenological viability is not
  addressed.
- The six-dimensional anomaly polynomial, the two-form reduction, and M_St are not computed.
- Z_W/kappa is inherited from the predecessor weak-response note at eighteen printed digits and is
  not recomputed.
- No radion kinetic term, no complete compactification stability, no quantum corrections, no
  thresholds, no running. The measured fine-structure constant remains unexplained unless an
  independent normalization, thresholds, and running are completed. No measured coupling is used.

## Attribution and source record

Prepared for Christopher Michael Baird with Claude assistance. The derivations and calculations were
cross-checked within this assisted workflow (exact rational and 95-digit Decimal arithmetic,
independent NumPy/SciPy code, and a separate AI review pass recorded in `REVIEW_RESPONSE.md`).
External peer review is not claimed.

Inherited definitions are pinned to the repository `Cbaird26/mqgt-scf-continued` at commit
`3a8a1b029e2923ce3fde3335fbc710ebf618a38b` (research_continuation/2026-10-22/electromagnetic and
2026-10-21/electromagnetic). The predecessor weak-response and neutral-matching notes are cited from
the shared research transcript; their bundles were not in the repository at that commit. The source
archive PDF was not accessed in this continuation. Details and hashes are in `provenance.json`.

This continuation is prepared for distribution under the Creative Commons Attribution 4.0
International license, included as `LICENSE`.
