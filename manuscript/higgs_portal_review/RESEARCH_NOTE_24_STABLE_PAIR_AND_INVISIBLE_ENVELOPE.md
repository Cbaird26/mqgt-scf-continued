# Research Note 24 — Stable-pair Higgs production and a conditional invisible-event envelope

**21 September 2026 | Public scientific-development draft, not peer reviewed.** Human author: Christopher Michael Baird. ChatGPT (ZoraASI) assisted with the derivation, cross-check code, tests and drafting. The two singlets, and their suggested consciousness/ethics interpretations, are hypothetical and have not been established experimentally.

## 1. A calculable collider quantity despite the missing hadronic spectrum

Notes 19–23 focus on the missing external pion/kaon form-factor input needed for the heavier singlet's total width. A different, **already calculable** question is how much Higgs production creates a pair of the lighter singlets *within the restricted model*. Use Note 22's illustrative, unfitted point: `m1=10 GeV`, `m2=11.5 GeV`, `mh=125 GeV`, `v=246 GeV`, `Gamma_h^SM=0.0041 GeV`, `K11=K22=0.001`, `K12=-0.001`. Assume common Z2 is exact, SM fields even, both singlets odd, the lighter singlet has no lighter odd decay product, and the only Higgs widths are the stated SM reference and three two-singlet channels. The light singlet is then stable within this EFT. Real-detector invisibility additionally requires interaction/acceptance analysis.

From the portal normalization `L_int ⊃ -(v/2)h[K11 s1²+2K12 s1s2+K22 s2²]`, the tree-level widths are

```
Gamma_ii = v² Kii²/(32 pi mh) * sqrt(1 - 4 mi²/mh²), if 2 mi < mh;
Gamma_12 = v² K12²/(16 pi mh)
         * sqrt([1-(m1+m2)²/mh²][1-(m2-m1)²/mh²]), if m1+m2 < mh.
```

These production partial widths do **not** depend on the unknown `s2` lifetime or Omnès files. The independent standard-library calculation gives `Gamma_11=4.75366954175e-6`, `Gamma_12=9.48719983776e-6`, `Gamma_22=4.73348800319e-6` GeV, sum `1.89743573827e-5 GeV`, reproducing Note 22's total. This is *production*, not a calculated displaced or invisible yield.

## 2. What the missing heavier-singlet lifetime cannot change

Within the stated Higgs-width inventory, the denominator `Gamma_h^SM + Gamma_11+Gamma_12+Gamma_22 = 0.00411897435738 GeV`. The light-pair branch is

```
BR(h -> s1 s1) = Gamma_11/Gamma_h^tot = 0.001154090589 = 0.1154091%.
```

The entire exotic pair branch is `BR(h -> any pair) = 0.004606573321 = 0.4606573%`. Both numbers follow from the toy potential and assumed SM reference Higgs width. **Uncertainty in s2's hadronic widths cannot erase h -> s1 s1 or change its tree-level partial width.** With exact Z2 and no lighter odd states, `h -> s1 s1` contains two stable neutral singlets independently of `s2`'s decays.

Introduce abstract, **unmeasured** event-classification probabilities `p12,p22 ∈ [0,1]` for the two topologies with heavier singlets. Treat the `h -> s1 s1` topology as invisible only under an additional idealized detector assumption that both stable `s1` escape undetected. Then

```
Gamma_invisible,ideal = Gamma_11 + p12 Gamma_12 + p22 Gamma_22;
0.1154091% <= BR_invisible,ideal <= 0.4606573%.
```

This interval is **not** a prediction of actual LHC selection efficiency, invisible branching, displaced-track acceptance or experimental exclusion. The two probabilities are not calculated. A lifetime alone does not determine either without boosts, geometry, daughter modes, thresholds and triggers. If additional Higgs partial widths exist, the branching denominator increases and **even the numerical 0.1154% lower fraction no longer follows**; `Gamma_11` remains the tree-level partial width for the declared portal. If Z2 breaks or new lighter odd states exist, revisit the lighter singlet's stability premise.

## 3. Experimental-interface discipline and next gate

The stable-pair production channel is a separate calculable model deliverable while the hadronic-data gate is closed, but it cannot be compared directly to a search limit without dated source, production assumptions, acceptance and likelihood. The larger exotic production can produce invisible, visible, displaced or mixed final states depending on uncomputed heavier-singlet decays. No signal yield, present-day ATLAS/CMS exclusion or parameter fit is asserted. Note 22's 645-km *leptonic-only upper bound* is not a lifetime or detector-escape prediction.

Next: authenticate all four pinned Omnès bytes, safely inspect and parse them without the upstream `eval` loader, calculate exclusive pion/kaon widths with source uncertainties and nonoverlapping complementary modes, and map a full width and daughter distributions into a detector model. Independently check vacuum/radiative/broader constraints and publication metadata before formal submission. No third-party hadronic input or detector simulation was used here.

**Reproducibility:** `invisible_channel_envelope.py` computes the tree-level widths and conditional range; `test_research_note_24.py` checks Note-22 numeric recovery, thresholds, portal-sign invariance, abstract probability bounds, invalid-input rejection and additional-Higgs-width sensitivity. Twelve local tests passed: software checks of stipulated toy equations, not independent scientific review or experimental evidence.

**Lineage:** Research Notes 12, 15 and 22–23, especially `RESEARCH_NOTE_22_COMPRESSED_SPECTRAL_WINDOW_BENCHMARK.md`. No third-party data or code is redistributed.