# Research Note 26 — Optical two-singlet thresholds and the vacuum-response gate

**21 September 2026 | Public scientific-development draft; not peer reviewed.** Christopher Michael Baird is the human author. ChatGPT (ZoraASI) assisted with the conditional kinematic derivation, code, tests, and drafting. Restricted, symmetric-vacuum, zero-source, exact common-Z2 two-real-singlet EFT of Notes 22 and 25. Neither the fields nor consciousness/ethics interpretations have been established experimentally. The 2-eV photon below is deliberately **illustrative, not a verified H2 hardware specification**.

## 1. Symmetry-allowed is not kinematically open

Note 25 establishes that an even photon-only initial state cannot produce exactly one odd singlet under exact unbroken common Z2; two singlets are symmetry-allowed. For the separate, unfitted compressed Note-22 point `m1=10 GeV, m2=11.5 GeV`, the on-shell free-two-singlet thresholds are:

| Final state | Minimum sqrt(s) | s threshold | Equal-energy head-on photons: energy each |
|---|---:|---:|---:|
| s1s1 | 20 GeV | 400 GeV² | 10 GeV |
| s1s2 | 21.5 GeV | 462.25 GeV² | 10.75 GeV |
| s2s2 | 23 GeV | 529 GeV² | 11.5 GeV |

For two freely colliding real photons of energies `omega_a,omega_b` and relative direction angle `vartheta`, exactly `s_gamma_gamma = 2 omega_a omega_b (1-cos(vartheta)) <= 4 omega_a omega_b`; the massive final pair needs `s >= (m_i+m_j)^2`. Two hypothetical 2-eV photons, even head-on, have `sqrt(s)=4 eV=4e-9 GeV`, a factor **5 billion below** the 20-GeV light-pair threshold in invariant energy (`s/s_threshold=4e-20`). Therefore that isolated optical two-photon vacuum process cannot produce any on-shell 10/11.5-GeV singlet pair, regardless of uncalculated amplitude `C_gamma`. Collinear real photons have `s=0`; a single isolated real photon with `k²=0` also cannot decay into two massive singlets in empty vacuum. These are kinematic statements, independent of the missing hadronic data.

An ordinary *static* electromagnetic background may supply spatial momentum but not the missing energy when time translation is preserved: one 2-eV photon cannot produce a >=20-GeV pair merely by crossing a static B-field. A time-dependent drive, energetic matter, pre-existing odd singlet, active boundary, or sufficiently energetic multiphoton environment requires a new energy budget and is **not** ruled out by this narrow argument.

## 2. A symbolic allowed operator does not imply optical dephasing

Note 25 conditionally introduced `L ⊃ [C_gamma(q²)/(4v)] h F_mu_nu F^mu_nu`. Tree-level low-energy elimination of the physical Higgs in the declared normalization gives

`L_eff ⊃ -C_gamma/(8 mh²) [K11 s1² + 2 K12 s1s2 + K22 s2²] F_mu_nu F^mu_nu`.

`C_gamma` is still uncalculated. In a homogeneous Lorentz-invariant vacuum, a spacetime-*constant* renormalized expectation of the singlet bilinear only shifts the coefficient of the local Maxwell kinetic term `-Z F²/4`. For constant `Z>0`, the source-free Maxwell equation is unchanged after division by Z; plane waves still satisfy `omega²=|k|²` in c=1 units. **This constant F² term alone predicts neither a refractive-index shift nor visibility loss.** The composite expectation itself is not computed.

In the strictly *free* massive singlet vacuum, the connected normal-ordered bilinears `:s1²:`, `:s1s2:`, `:s2²:` have leading two-particle spectral thresholds of 20, 21.5 and 23 GeV. This is **not** a claim that the full interacting SM-plus-singlet correlator is gapped there: SM light channels, charged/photonic higher loops, possible bound states, external media, matter populations, finite temperature, and nonstationary forcing need their own calculation. Virtual analytic effects can survive below the on-shell threshold.

Neither the symbolic pair operator nor pair thresholds provide a value, sign or positive lower bound for the archived instrument-level visibility parameter in `V/V0=exp[-Gamma_H2*T*(Delta x)^2]`. The note excludes a **particular on-shell vacuum optical-pair mechanism** at the stated illustrative energies; it is *not* a universal optical null result or a calculated H2 dephasing rate.

## 3. Explicit remaining model-to-observable gates

To attribute an actual optical phase or visibility result to this EFT, pin the real photon energy/bandwidth and geometry, the energy supplied by any background/target/drive, the gauge-complete photon/singlet amplitude and `C_gamma(q²)`, the singlet/environment state and connected spectrum, and a microscopic map into the instrument visibility estimator with nuisance controls. A lighter or parity-breaking scalar branch must redo its vacuum, symmetry, thresholds and constraints rather than reuse this benchmark. Separately authenticate all four Omnès inputs and calculate nonoverlapping hadronic channels before quoting the heavy singlet's full lifetime.

`optical_threshold_gate.py` and `test_research_note_26.py` implement pure kinematic and constant-F² algebra. **12 local regression tests passed**, without experiments, third-party spectral data, loop amplitude matching, a collider exclusion or H2 rate. The conditional Note-22 leptonic-only `c*tau2 <= ~645 km` and Note-24 idealized pair-production envelope remain unchanged.

**Lineage:** [Research Note 22](https://github.com/Cbaird26/mqgt-scf-continued/blob/research/two-singlet-higgs-portal-2026-09-21/manuscript/higgs_portal_review/RESEARCH_NOTE_22_COMPRESSED_SPECTRAL_WINDOW_BENCHMARK.md) supplies the toy spectrum; [Research Note 25](https://github.com/Cbaird26/mqgt-scf-continued/blob/research/two-singlet-higgs-portal-2026-09-21/manuscript/higgs_portal_review/RESEARCH_NOTE_25_Z2_PHOTON_SELECTION_AND_H2_MATCHING_GATE.md) supplies the symmetry and operator convention. The specifically qualified threshold conclusions are this note's derivation, not an outside experimental claim.