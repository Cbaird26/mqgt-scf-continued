# Higgs-portal research note: claims, source map, and release gate

**Date:** 2026-09-21. **State:** public working draft on a review branch. Human author approved GitHub staging. The independent-verification snapshot, original corpora, and `main` remain unchanged. No DOI, release, journal submission, new experimental data, or independent technical peer review is claimed.

## Exact model branch
The paper assumes two real singlets; portal potential `V ⊃ (κ_ΦH/2) Φ²H†H + (κ_EH/2) E²H†H`; bilinear `γ Φ E`; zero effective sources; stationary symmetric singlet vacuum; Standard Model electroweak vacuum. Stability statements are local only. The source framework admits additional backgrounds, effective sources, and measurement dynamics that this paper does NOT derive or address.

## Source-to-claim map

| Claim | Primary source / check | Boundary |
|---|---|---|
| Portal `-κ s²H†H/2` and inconsistent printed `8πm_h` width | C. M. Baird, *A Completed Theory of Everything* (2026), collider-facing Sec. 3.1, Eqs. (10)–(11); original PDF retained in user's research corpus | Correct width for that normalization is `κ²v²/(32πm_h)` times phase-space factor. Original archival equation must NOT be silently overwritten. |
| Companion versus ultralight benchmarks | March 2026 anchor reproduced in *All + ToE_Part.9*, benchmark card in section 4 | Benchmark is not a measurement or a globally vetted viable region. |
| Mass eigenvalues and three Higgs-pair channels | Algebra derived from the declared potential, reproduced in this paper | Conditional tree-level result; does not imply lifetime or invisible detection. |
| Basis-independent massless summed width | Trace identity `tr(Rᵀ diag(κ) R)² = κ_Φ²+κ_E²` | Finite mass phase space spoils angle independence. |
| Invisible Higgs limit of 0.107 | ATLAS Collaboration, *Phys. Lett. B* 842 (2023) 137963, DOI `10.1016/j.physletb.2023.137963`, arXiv `2301.10731`; observed 95% CL, SM Higgs production | Dated ATLAS result; not a global or necessarily latest constraint; likelihood reanalysis needed. |
| Numerical examples | `higgs_portal_checks.py`, with illustrative `v=246 GeV`, `m_h=125 GeV`, `Γ_h^SM=4.1 MeV` | Unit tests are software checks, NOT independent peer review or data. |

## Items intentionally withheld from verified-result claims

- Research Note 13's numerical three-body lifetime and detector classification: no independently verified phase-space integral, all-channel decay width, hadronic treatment, or detector simulation.
- H2 thermal Langevin, vacuum spectral-gap, and photon-scalar conversion toy models: no demonstrated mapping from this portal action to the H2 detector estimator.
- Ultralight naturalness: no full renormalization, protection, cosmological or fifth-force joint analysis.
- Ethics, consciousness, and AI qualia interpretations: no independently established operational correspondence or empirical detection.

## Checks performed and still required

**Performed in draft development:** verified the old source's conflicting portal/width expressions; verified ATLAS article citation, date, and abstract's 0.107 observed figure; independently computed the example widths and coupling norm; locally ran six standard-library unit tests covering trace invariance, massless total width, equal-portal transition, example branching ratios, illustrative norm, and channel thresholds. No laboratory experiment or independent physics referee was involved.

**Before formal release/submission:** pin precise edition/page/commit of the March anchor action and historical source; obtain an independent calculation of vertex factors and all widths; complete singlet potential vacuum/stability and radiative checks; compute scalar decay channels and detector acceptance; assess updated collider and cosmological constraints and full applicable likelihoods; compile a publication-ready manuscript with bibliography; confirm author, AI-use, license, DOI/release metadata, and scientific claims. Do not call this paper peer-reviewed or present a 2023 result as a 2026 global constraint.

**GitHub process:** staged on `research/two-singlet-higgs-portal-2026-09-21` for a draft PR against `main`; do not modify `mqgt-scf-independent-verification`, mass-edit the 6,926-page PDF, merge this draft to `main` as final science, or mint a Zenodo DOI merely because the code tests pass.

## Addendum — Research Note 21 (21 September 2026)

Notes 19–21 propose a possible partial pion/kaon spectral interface but **no upstream Omnès input data have been retrieved or numerically parsed**. The original `safe_omnes_manifest.py` checks four source-file identities offline with length and Git blob SHA-1, and records raw SHA-256 only after a matching local acquisition; its 15 passing local regression tests use synthetic fixtures and algebra. Note 20's `0.004138912` is exclusively a toy *kinematic-weight* fraction below 2 GeV, not a hadronic width fraction. Note 21 derives a general weighted-mean spectral-ratio identity: obtaining a hypothetical 50% low-window contribution would require `R ≈ 240.6094`; no actual QCD ratio is established. Do not infer hadronic suppression or dominance from the toy kinematic number. Source data verification, safe grammar-specific parsing, absolute spectral normalization, and nonoverlapping full-domain channel matching remain blocking. The conditional leptonic-only `c*tau <= approximately 17.06 cm` is unchanged. This public draft remains unmerged and unreviewed.
