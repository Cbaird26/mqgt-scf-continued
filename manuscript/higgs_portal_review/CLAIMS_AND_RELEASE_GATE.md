# Higgs-portal research note: claims, source map, and release gate

**Date:** 2026-09-21. **State:** public working draft on a review branch. Human author approved GitHub staging. The independent-verification snapshot, original corpora, and `main` remain unchanged. No DOI, release, journal submission, new experimental data, or independent technical peer review is claimed.

## Exact model branch
The paper assumes two real singlets; portal potential `V ⊃ (κ_ΦH/2) Φ²H†H + (κ_EH/2) E²H†H`; bilinear `γ Φ E`; zero effective sources; stationary symmetric singlet vacuum; Standard Model electroweak vacuum. Stability statements are local unless explicitly strengthened by positive-definite bare singlet masses, nonnegative quartics, and nonnegative quadratic portals. The source framework admits additional backgrounds, effective sources, and measurement dynamics that this paper does NOT derive or address.

## Source-to-claim map

| Claim | Primary source / check | Boundary |
|---|---|---|
| Portal `-κ s²H†H/2` and inconsistent printed `8πm_h` width | C. M. Baird, *A Completed Theory of Everything* (2026), collider-facing Sec. 3.1, Eqs. (10)–(11); original PDF retained in user's research corpus | Correct width for that normalization is `κ²v²/(32πm_h)` times phase-space factor. Original archival equation must NOT be silently overwritten. |
| Companion versus ultralight benchmarks | March 2026 anchor reproduced in *All + ToE_Part.9*, benchmark card in section 4 | Benchmark is not a measurement or a globally vetted viable region. |
| Mass eigenvalues and three Higgs-pair channels | Algebra derived from the declared potential, reproduced in collider draft | Conditional tree-level result; does not imply lifetime or invisible detection. |
| Basis-independent massless summed width | Trace identity `tr(Rᵀ diag(κ) R)² = κ_Φ²+κ_E²` | Finite mass phase space spoils angle independence. |
| Invisible Higgs limit of 0.107 | ATLAS Collaboration, *Phys. Lett. B* 842 (2023) 137963, DOI `10.1016/j.physletb.2023.137963`, arXiv `2301.10731`; observed 95% CL, SM Higgs production | Dated ATLAS result; not a global or necessarily latest constraint; likelihood reanalysis needed. |
| Initial illustrative rates | `higgs_portal_checks.py`; illustrative `v=246 GeV`, `m_h=125 GeV`, `Γ_h^SM=4.1 MeV` | Software checks are NOT independent peer review or data. |
| Notes 14–21's leptonic, spectral and source checks | Read individual dated note and corresponding source/test | Source files unavailable; no QCD rate, full lifetime or detector constraint. |
| Note 22's *different* compressed point | `RESEARCH_NOTE_22_COMPRESSED_SPECTRAL_WINDOW_BENCHMARK.md` | `m1=10,m2=11.5 GeV` gives provisional `Delta=1.5 GeV` and conditional leptonic-only `c*tau<=~645 km`, not a total-lifetime prediction. |
| Note 23's squared-mass perturbation interval and width-ratio requirements | `RESEARCH_NOTE_23_COMPRESSED_SPECTRUM_ROBUSTNESS.md`; `spectrum_robustness.py` | Exact tree-level 2×2 algebra on a fixed bare-mass perturbation slice. `Delta<=2 GeV` is a provisional method criterion, NOT actual grid certification. No radiative computation or missing-width estimate. |

## Items intentionally withheld from verified-result claims

- A complete heavy-scalar lifetime, branching fractions or collider acceptance: no independently certified nonoverlapping all-channel width, validated hadronic data, or detector simulation.
- H2 thermal Langevin, vacuum spectral-gap, and photon-scalar conversion toy models: no demonstrated mapping from this portal action to the H2 detector estimator.
- Ultralight naturalness: no full renormalization, protection, cosmological or fifth-force joint analysis.
- Ethics, consciousness, and AI qualia interpretations: no independently established operational correspondence or empirical detection.

## Completed checks and remaining gates

Earlier draft work corrected the historical normalization issue, checked the dated ATLAS citation and ran local toy-model algebra/numerical tests detailed in each development note. Note 23's matrix roots were locally cross-checked, but no third-party Omnès grid or radiative calculation has been executed. Test scripts verify only declared toy assumptions; they do not substitute for independent scientific review.

**Before formal release/submission:** pin precise source editions, independently check vertex factors and renormalization scheme; certify the complete singlet vacuum/radiative analysis; obtain and authenticate the four pinned Omnès inputs, safely parse their actual grammar and verify domain/units; compute nonoverlapping exclusive and remaining inclusive/radiative widths with uncertainty; separately simulate detector acceptance and analyze current applicable collider/cosmology likelihoods; independently match any H2 observables to this action; compile a publication-ready manuscript with bibliography; confirm human authorship, AI-use disclosure, third-party software/data licenses, and DOI/release metadata. Do not present a 2023 limit as a 2026 global constraint.

**GitHub process:** staged on `research/two-singlet-higgs-portal-2026-09-21` for a draft PR against `main`; do not modify `mqgt-scf-independent-verification`, mass-edit historical PDFs, merge this draft to `main` as final science, or mint a Zenodo DOI merely because toy code runs.
