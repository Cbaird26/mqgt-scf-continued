# Research Note 22 — Compress the mass gap to remove the unmodeled 2–15 GeV tail

**21 September 2026 | Public technical-development draft; not peer reviewed.** Human author: Christopher Michael Baird. ChatGPT (ZoraASI) assisted with the model-branch construction, calculations, numerical cross-check and drafting. This is an illustrative, unfitted companion-sector benchmark, not a discovery, consciousness/ethics measurement, experimental constraint, or complete MQGT-SCF prediction.

## 1. A way around *one* obstacle in Notes 19–21

Notes 19–21 could not turn a pion/kaon calculation provisionally restricted to virtual masses at most ~2 GeV into a complete partial width for the previous `m1=10, m2=25 GeV` point, where `sqrt(s)` can reach **15 GeV**. That limitation is fundamentally kinematic. Instead of inventing a high-energy continuation of the two-meson amplitudes, change the *illustrative model point* while keeping the same coupling normalization:

```
m1=10 GeV,  m2=11.5 GeV,  Delta=m2-m1=1.5 GeV,
mh=125 GeV, v=246 GeV, Gamma_h=0.0041 GeV,
theta=pi/4, kappa_PhiH=0.002, kappa_EH=0,
K11=K22=0.001, |K12|=0.001; all effective sources = 0.
```

For `s2 -> s1 + X` through `h*`, phase space forces `0 <= sqrt(s) <= Delta=1.5 GeV`. Thus **the entire virtual-mass domain for each pion/kaon *exclusive* partial width lies inside the earlier provisional ~2-GeV methodological window**, conditional on an independent check that the actual upstream grid covers thresholds through 1.5 GeV. This removes the specific *unmodeled 2–15 GeV tail in those channels*, not the missing source-file identity, source uncertainty, or uncounted final states. The 2-GeV figure is a paper/method window, not an authenticated shipped-grid endpoint (Notes 19–21).

Two-pion and two-kaon thresholds are open using the upstream's *approximate isospin reference masses* (`2*0.134=0.268 GeV`, `2*0.497=0.994 GeV`). The tau-pair threshold `2*1.77686=3.55372 GeV` is closed; the electron/muon channels are open. Other low-mass final states, e.g. multipion, eta-containing, photons and hadronic channels, require an **independent nonoverlapping inventory**; two-meson form factors alone still cannot give the total heavy-state lifetime. A model-dependent radiative channel is not implicitly zero simply because we have not computed it. The `s2 -> 3s1` channel is closed at `11.5 < 30 GeV`.

## 2. Realization in the stated symmetric-vacuum branch

Use the branch's mass matrix after electroweak symmetry breaking, `M_s²=[[A,gamma],[gamma,B]]`, where `A=mu_Phi²+kappa_PhiH*v²/2`, `B=mu_E²+kappa_EH*v²/2`. A 45-degree mass rotation yielding eigenmasses 10 and 11.5 GeV has `A=B=(100+132.25)/2=116.125 GeV²` and `|gamma|=(132.25-100)/2=16.125 GeV²`. With the portal coefficients above, one explicit choice is:

```
mu_Phi² = 55.609 GeV²,    mu_E² = 116.125 GeV²,
|gamma| = 16.125 GeV²,
mu_Phi²*mu_E² - gamma² = 6197.5795 GeV^4 > 0.
```

The bare singlet quadratic form is positive definite. **If, additionally**, singlet quartics and their cross-quartic are nonnegative, no odd singlet terms/sources are present, and the only singlet–Higgs interactions are the stated nonnegative quadratic portals, then the singlet-dependent part of the potential is nonnegative at any `H`, with equality at `Phi=E=0`. Under those explicitly stronger assumptions, the singlet-zero electroweak minimum is globally stable *at tree level*. This does **not** establish radiative naturalness, cosmological viability or a minimum for the unrestricted source action. The common Z2 leaves the lighter state stable within the stated interactions.

## 3. Leptonic floor and production, freshly calculated

Integrate Note 15's exact tree-level lepton kernel with `s` between `4 mf²` and `Delta²`. The implementation uses the endpoint-smoothing substitution `s=4 mf²+(Delta²-4 mf²)sin²(pi*t/2)`, `0<=t<=1`, and composite Simpson quadrature; an independent direct-`s` SciPy integration reproduces the muon width at the new point to relative difference `5.53e-15`. The following are conditional toy calculations, NOT measured lifetimes or estimates of hadronic widths:

| `Delta` (GeV), `m1=10 GeV` | Leptonic-only width floor (GeV) | Corresponding **upper bound** on `c tau2`, *if* the branch applies |
|---:|---:|---:|
| 0.8 | `1.282657495e-23` | `1.538423e7 m` |
| **1.5** | **`3.060267688e-22`** | **`6.448030e5 m` (~645 km)** |
| 2.0 | `1.198307792e-21` | `1.646714e5 m` |
| 15.0 (previous benchmark) | `1.156499157e-15` | `0.1706244 m` |

For the 1.5-GeV-gap point specifically, `Gamma_mu=3.060190637e-22 GeV`, `Gamma_e=7.705062302e-27 GeV`, `Gamma_tau=0`. The enormous *leptonic-only upper bound* is **not a prediction of a 645-km decay length or of detector escape**: any additional physically allowed decay modes shorten `c tau` and can radically change the final-state classification. The previous 17.06-cm conditional upper bound belongs to the **different**, 15-GeV-gap benchmark and cannot be carried over unchanged.

At the same new point, the corrected tree-level Higgs rates are `Gamma_11=4.753669542e-6 GeV`, `Gamma_12=9.487199838e-6 GeV`, `Gamma_22=4.733488003e-6 GeV`. Summed pair width `1.897435738e-5 GeV`; conditional pair-production branching fraction `0.0046065733` (~0.461%) **if** the only other Higgs width is the illustrative SM `0.0041 GeV`. No ATLAS/CMS exclusion or invisible/displaced acceptance follows from this number; the altered lifetime requires a fresh detector analysis. The constant-width off-shell propagator differs from the simple `1/mh⁴` contact denominator by no more than a ~`0.02881%` multiplicative enhancement over `0<=s<=2.25 GeV²` (up to a negligible Higgs-width correction). This controlled propagator estimate does **not** control QCD form-factor or missing-channel error.

## 4. Reproducibility and strict remaining gates

Files: `near_threshold_benchmark.py` and `test_research_note_22.py` (standard library). **13 regression tests passed locally** for thresholds, amplitude-squared portal scaling, endpoint quadrature convergence, contact bounds, recovery of the old 15-GeV-gap lepton result, the reconstructed positive bare mass matrix and Higgs-pair arithmetic. An independent direct-variable SciPy quadrature agrees with the new muon result; no experimental data, third-party form factors, or detector simulation were used.

The four pinned external Omnès files **remain unavailable in this runtime**; direct raw-file retrieval also failed here. Run Note 21's `safe_omnes_manifest.py` on an independently obtained local upstream checkout before reading numerical data, then safely inspect the grammar and certify actual grid coverage through 1.5 GeV and form-factor normalization, including extrapolated portions and uncertainties. Evaluate exclusive `pi pi` and `K K-bar` widths only within a verified domain. Construct the other-channel inventory without counting the same hadronic state twice; validate matching, uncertainty and the *full* total width before any lifetime or collider exclusion claim. Keep the existing draft PR unmerged, without a new DOI or journal-submission claim.

**Sources/lineage:** restricted model and kernel in Notes 12, 15; paper-to-code matching in Note 19; data gate and low-bin sensitivity in Notes 20–21. Primary external hadronic source: Blackstone et al., *Hadronic Decays of a Higgs-mixed Scalar*, arXiv:2407.13587v1 (2024), https://arxiv.org/abs/2407.13587 . Pinned package: https://github.com/blackstonep/hipsofcobra/tree/6a6dcfccf903317ea2104e27bb1dbbc7ad1d9fc7 . The compressed two-singlet point and calculations here are our conditional derivations, not results claimed by that paper.