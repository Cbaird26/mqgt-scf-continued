# Research Note 17 — Open-flavor thresholds do not switch off the heavy-quark scalar spectrum

**21 September 2026 · Author: Christopher Michael Baird · AI-assisted calculation and drafting: ChatGPT (ZoraASI).** Public technical-review draft for the *restricted* symmetric-vacuum, zero-source, common-Z2 two-singlet Higgs-portal model. This is not an observation of new particles or evidence that the symbols Φc and E measure consciousness or ethics.

## 1. Threshold repair to Notes 15–16

In the illustrative spectrum m1=10 GeV and m2=25 GeV, the virtual-Higgs invariant mass satisfies 0 ≤ sqrt(s) ≤ Δ = 15 GeV. The **open-charm D0 anti-D0** and **open-bottom B0 anti-B0** pair thresholds lie near 3.730 and 10.559 GeV. Those thresholds do *not* imply that the full charm or bottom scalar-current spectral function is zero below them. The scalar 0++ charmonium χc0(1P), near 3.415 GeV, and 0++ bottomonium χb0(1P), near 9.859 GeV, both lie below their respective open-flavor pair thresholds and within this virtuality window. A local flavor-diagonal scalar current can have overlap with compatible quarkonium and multiparticle QCD states; actual residues and interference must be computed, **not inferred from state masses alone**.

This is a methodological correction to any proposed step-function prescription Γ*_(h→cc)(M)=0 for M<2mD or Γ*_(h→bb)(M)=0 for M<2mB when those labels mean *the entire charm/bottom scalar-current response*. For *exclusive open-D/open-B pair final states*, the thresholds of course apply. Likewise, a partonic threshold 2m_q is neither a sharp physical hadron threshold nor a substitute for matched low-energy QCD. The same hadronic final state must never be counted once through quarkonium and again through an inclusive perturbative continuum.

Sources: PDG 2025 D0 mass 1864.84 MeV, https://ccwww.kek.jp/pdg/2025/listings/rpp2025-list-D-zero.pdf ; PDG 2022 χc0(1P) mass about 3414.71 MeV, https://pdg.lbl.gov/2022/listings/rpp2022-list-chi-c0-1P.pdf (historical mass listing; the threshold ordering is unaffected); PDG 2025 χb0(1P) mass about 9859.44 MeV, https://pdg.lbl.gov/2025/listings/rpp2025-list-chi-b0-1P.pdf ; B0 mass about 5279.65 MeV (PDG 2021 mass fit, https://pdg.lbl.gov/2021/listings/rpp2021-list-B-zero.pdf). For low-mass hadronic uncertainties and charmonium mixing, see Winkler, Phys. Rev. D 99, 015018 (2019), https://doi.org/10.1103/PhysRevD.99.015018, Sec. III / Appendix A. These citations motivate matching; no spectra were downloaded, digitized, or fitted here.

## 2. A rigorous spectral-input contract

Keep Note 16's fixed-width tree-level kernel, in GeV units:

Γ_had = ∫_0^{Δ²} W(s) Γ*_{had}(sqrt(s)) ds,

W(s) = v² K12² sqrt(λ(m2²,m1²,s)) sqrt(s) / [16 π² m2³ ((mh²−s)² + mh² Γh²)],

λ(a,b,c)=(a−b−c)²−4bc. The factor W(s) is nonnegative throughout the physical window. Γ*_{had} is the **absolute** width for one virtual scalar with standard-SM Higgs-current normalization and mutually exclusive physical final states. A scalar-mixing model's width must have any mixing-angle factor removed *once*, consistently; branching fractions alone cannot determine absolute widths.

Suppose a documented hadronic analysis provides, on an exhaustive collection of non-overlapping s-bins I_i, certified pointwise bounds L_i ≤ Γ*_{had}(sqrt(s)) ≤ U_i with 0 ≤ L_i ≤ U_i. Define A_i=∫_{I_i} W(s)ds ≥0. Positivity gives the exact conditional inequality

Σ_i L_i A_i ≤ Γ_had ≤ Σ_i U_i A_i.

With Γ_leptons from Note 16, corresponding bounds on the proper length are

ħc/(Γ_leptons+Σ_i U_i A_i) ≤ cτ2 ≤ ħc/(Γ_leptons+Σ_i L_i A_i).

Point samples or interpolation alone do **not** certify such pointwise bounds, especially near thresholds and narrow resonances. An unknown interval, unmatched source normalization, unbounded uncertainty, unaccounted channel, or double-counted inclusive/exclusive spectra fails the contract. In their absence the earlier Γ_total≥Γ_leptons and cτ≤17.06 cm remain the only such bounds within this restricted submodel. Additional independent amplitudes can require revisiting even these premises.

## 3. Reproducibility and next gate

`test_research_note_17.py` tests threshold ordering, kernel positivity, rigorous interval propagation, validation that gaps/overlaps/negative or nonfinite spectra are rejected, and reversed lifetime inequalities, using **synthetic, arbitrary** spectral envelopes solely as tests. Seven tests passed locally. It does *not* compute or fit hadronic widths, a total lifetime, detector efficiency, or an experimental limit.

Next input: obtain a licensable and version-pinned absolute hadronic scalar-current spectrum or reproducible code covering 0–15 GeV; audit heavy-flavor threshold matching and resonances, finite-width interference and channel exclusivity; independently recompute Γ_total and uncertainty; only then assess displaced/invisible acceptance using actual detector efficiencies. Keep this note on the open draft PR; do not merge it into a released physics prediction without the missing spectral input.