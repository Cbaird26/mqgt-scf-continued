# Research Note 16 — Hadronic spectral matching: a bounded propagator error, not a claimed total lifetime

**21 September 2026 · Public technical-review draft.** Author: Christopher Michael Baird; AI assistance: ChatGPT (ZoraASI) for analysis, writing, and internal computational checks. Neither the underlying fields nor their interpretations as consciousness/ethics observables have been experimentally established. This note extends the *restricted* symmetric-vacuum, zero-source, common-Z2 companion model of Notes 12–15; it is not the full September Part-0 hidden-sector action.

## 1. What Note 15 actually requires

With the interaction L ⊃ −v K12 h s1 s2, set s=q², Δ=m2−m1 and define a **channel-specific**, appropriately matched virtual-Higgs width Γ*_X(√s). In the tree-level propagator approximation,

Γ_X = ∫_[s_threshold, Δ²] [v² K12² sqrt(λ(m2²,m1²,s))/(16π m2³)] × [sqrt(s) Γ*_X(sqrt(s))/(π D(s))] ds,

where D(s)=(mh²−s)²+mh² Γh² and λ(a,b,c)=(a−b−c)²−4bc. Sum only **mutually exclusive physical final states**. A 125-GeV Higgs branching-ratio table cannot supply Γ*_X across 0–15 GeV. Higgs-mixed light-scalar phenomenology must be translated to the SM scalar-current normalization without multiplying by the mixing angle twice; branching ratios alone also lack the absolute width normalization.

**External methodology, not evaluated for this benchmark:** Djouadi, Kalinowski, Mühlleitner and Spira, *HDECAY: Twenty++ years after*, Comput. Phys. Commun. 238, 214–231 (2019), https://doi.org/10.1016/j.cpc.2018.12.010, describes higher-order QCD and multi-body Higgs widths; its running-mass and renormalization-scale implementation is documented at https://gitea.psi.ch/ltpth/HDECAY/src/branch/main/CHANGES. Winkler, *Decay and detection of a light scalar boson mixing with the Higgs boson*, Phys. Rev. D 99, 015018 (2019), https://doi.org/10.1103/PhysRevD.99.015018, addresses nonperturbative issues particularly in the lower-GeV regime. Neither program nor meson form factors were executed or digitized here.

## 2. Exact result within the fixed-width propagator approximation

At the frozen illustrative masses m2=25 GeV, m1=10 GeV, mh=125 GeV, Γh=0.0041 GeV, every virtuality satisfies 0≤s≤Δ²=225 GeV². D(s) decreases throughout this interval, and the inclusive physical spectral numerator is nonnegative. Replacing 1/D(s) by its contact-limit value 1/D(0) gives, **for any nonnegative matched spectrum**,

**Γ_X(contact) ≤ Γ_X(full) ≤ [D(0)/D(225)] Γ_X(contact) = 1.02943424 Γ_X(contact).**

Thus the propagator's contact approximation affects the width by at most **2.9435%** in this fixed-width toy calculation, irrespective of the unknown hadronic spectral shape. This says **nothing** about the size or precision of the QCD width, additional amplitudes, or momentum-dependent Higgs self-energy. For general Δ<mh replace 225 by Δ², checking the whole interval stays below the pole. The spectral numerator and normalization, rather than the distant propagator variation, are the main outstanding calculations for this benchmark.

## 3. A lifetime parametrization, not a hadronic estimate

For K12=−0.001 in this conditional point, the internally checked electron + muon + tau width is Γ_leptons≈1.15650×10⁻¹⁵ GeV. Define the **unknown** nonnegative ratio r=Γ_nonleptonic/Γ_leptons. If no additional amplitudes alter these leptonic rates and all other decays are counted in Γ_nonleptonic,

**cτ2=ħc/[Γ_leptons(1+r)]≈17.06 cm/(1+r).**

This parameter is not measured or computed. Illustrations r=1 and r=10 would imply 8.53 cm and 1.55 cm; those are *not* lifetime predictions. The previous cτ≤17.06 cm is a floor-derived bound for this restricted model only. Real-detector acceptance requires branching fractions, boosts, detector response, and hadronic matching.

As an integration diagnostic, approximately **73.94% of the tau-only width's q-weight** comes from √s>10 GeV; this is **not a hadronic branching fraction**. For the one-active-portal point, det K=K11 K22−K12²=κ_ΦH κ_EH=0 provides an independent check on the coupling convention: K12 is not freely adjustable while keeping both diagonal couplings fixed.

## 4. Reproducible handoff and stop condition

`test_research_note_16.py` implements seven internal, standard-library tests: nonnegative spectral-function bounds, a direct tau cross-check, integration-window weighting, lifetime scaling, toy survival, and the portal rank-one identity. Seven tests passed locally on 2026-09-21. These do not calculate QCD, demonstrate an experiment, or constitute independent review.

A legitimate next step requires an accessible **absolute** Γ*_(h→X)(M) table or code for the full relevant mass interval, with provenance, mutually exclusive channel definitions, renormalization scheme, thresholds and uncertainties. Calculate and independently check the inclusive sum, then simulate detector response. **Do not report a central hadronic width, total lifetime or physical invisible branching fraction without those inputs.** Keep this note separate from any released paper pending review.