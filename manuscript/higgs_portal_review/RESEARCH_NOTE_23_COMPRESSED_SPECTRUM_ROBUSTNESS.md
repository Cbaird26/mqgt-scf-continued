# Research Note 23 — Compressed-spectrum robustness and the missing-width scale

**21 September 2026 | Public, unreviewed scientific-development addendum.** Human author: Christopher Michael Baird. ChatGPT (ZoraASI) assisted with conditional algebra, a small numerical cross-check, and drafting. This note concerns the restricted two-real-singlet, symmetric-vacuum, zero-source collider model only. It does not establish a new particle or physical consciousness/ethics fields.

## 1. Question and inherited assumptions

Note 22 deliberately moved from `m1=10, m2=25 GeV` to an **illustrative** `m1=10, m2=11.5 GeV` point so the accessible virtual-Higgs mass lies below 1.5 GeV. That fixes the earlier 2–15 GeV extrapolation *for candidate exclusive pion/kaon channels only*, conditional on valid external source data. How robust is the compressed gap if the singlet mass matrix changes? And how much uncalculated width would shorten the previous **leptonic-only upper bound** `c*tau <= 6.448030e5 m` to a laboratory scale?

Hold `v=246 GeV`, `kappa_PhiH=.002`, `kappa_EH=0`, `gamma=+16.125 GeV^2`, and the bare second-singlet mass `mu_E^2=116.125 GeV^2` fixed. The baseline has `mu_Phi^2=55.609 GeV^2`, `A=B=116.125 GeV^2`, mass eigenvalues `100,132.25 GeV^2`. Here `epsilon` is a *hypothetical shift to the bare Phi squared-mass parameter*, `mu_Phi^2 -> mu_Phi^2+epsilon`, in GeV²; it is **not** a loop correction already calculated. The matrix is

```
M_s^2(epsilon) = [[a+epsilon, gamma], [gamma,a]],
a = 116.125 GeV^2, gamma=16.125 GeV^2.
```

## 2. Exact diagonalization and an explicit 2-GeV robustness interval

For `lambda_+ >= lambda_- > 0`,

```
lambda_± = a + epsilon/2 ± 0.5*sqrt(epsilon^2+4*gamma^2),
m_± = sqrt(lambda_±),
Delta(epsilon)=m_+ - m_-,
|sin(2theta)| = 2*|gamma|/sqrt(epsilon^2+4*gamma^2).
```

With a diagonal interaction-basis Higgs-portal matrix `diag(kappa_PhiH,kappa_EH)`, the rotated off-diagonal vertex is

```
|K12(epsilon)| = |kappa_PhiH-kappa_EH|*|sin(2theta)|/2
              = .001 * 32.25/sqrt(epsilon^2+32.25^2).
```

The rotated portal invariants are **exact** at tree level: `K11+K22=kappa_PhiH+kappa_EH` and `(K11-K22)^2+4*K12^2=(kappa_PhiH-kappa_EH)^2`. They check the rotation algebra; they do not imply that finite-mass Higgs partial widths are invariant under changes to the spectrum.

To retain the provisional `Delta <= d=2 GeV` coverage criterion with the *fixed-parameter, one-direction perturbation above*, set `Delta^2 = 2a+epsilon-2*sqrt[a*(a+epsilon)-gamma^2] = d^2`. Its two boundary solutions are

```
epsilon_± = d^2 ± 2*sqrt(a*d^2-gamma^2)
          = -24.59960664065, +32.59960664065 GeV^2  (d=2 GeV).
```

Throughout the interval between those roots the squared eigenmasses remain positive and `Delta<=2 GeV`. The **asymmetric** interval matters: a `-32.25 GeV²` bare-mass shift yields `Delta≈2.29559 GeV`, whereas a `+32.25 GeV²` shift yields `Delta≈1.99044 GeV`. The baseline `Delta=1.5 GeV` is only one illustrative point. This is neither a calculation of radiative corrections nor certification of the upstream Omnès-data grid: its actual byte content/domain are still unverified, and `2 GeV` is the paper's provisional methods window, not an authenticated accuracy boundary.

For a fixed portal and `epsilon=±16.125 GeV²`, `|K12|` becomes approximately `0.0008944272`, a 10.56% reduction in the *amplitude-level vertex*. When shifting a **portal coefficient** itself rather than a bare squared mass, BOTH the mass matrix (`delta A=v² delta kappa/2`) and the portal matrix change. It would be incorrect to apply the fixed-portal formula to that case without changing the numerator as well. This note does not quantify any UV cutoff, counterterms or fine-tuning measure.

## 3. What the 645-km ceiling does—and does not—tell us

At the *unperturbed* Note-22 point only, write `Gamma_total=Gamma_leptons+Gamma_other`, with `Gamma_leptons=3.060267688e-22 GeV` and `r=Gamma_other/Gamma_leptons >= 0`. Then the model-conditional relation is

```
c*tau_total = (6.448030e5 m)/(1+r).
```

To have a proper decay length no longer than a selected scale `L`, a **necessary total additional-width ratio** is `r >= max(0,6.448030e5 m/L-1)`. Examples: at most 1 km requires `r>=643.803`; at most 1 m requires `r>=644802`; at most 1 mm requires `r>=644802999`. These are algebraic requirements *if* that benchmark and lepton floor apply, **not** estimates of `r`, collider efficiencies, visible branching fractions, or evidence that any decay regime occurs. The total width must also inventory two-meson, other hadronic, possible photon, and other permitted modes without double-counting. Under a mass perturbation, the leptonic width and Higgs production rates must be recalculated: the baseline 645-km number cannot be reused as a new benchmark's actual bound.

## 4. Evidence boundary and next experiment-facing step

The formulas follow directly from the Note-22 declared potential and a symmetric 2×2 real mass matrix; the displayed benchmarks were checked by a local standard-library implementation, including the exact 2-GeV roots. No new third-party hadronic bytes were obtained, no source `eval` loader was executed, and no QCD width, total lifetime, detector simulation or experimental exclusion has been calculated. Before submitting a collider paper, validate the precise physical model/renormalization assumptions, obtain/authenticate the pinned four Omnès files, verify their actual grammar and domain, compute correctly normalized *exclusive* partial widths with uncertainties, add a nonoverlapping inventory of other modes, and then simulate production/decay acceptance.

**Lineage:** `RESEARCH_NOTE_22_COMPRESSED_SPECTRAL_WINDOW_BENCHMARK.md` and `near_threshold_benchmark.py` in this review branch; Notes 19–21 document the provisional 2-GeV hadronic-method window and blocked source-data access. Pinned candidate external source: Blackstone et al., *Hadronic Decays of a Higgs-mixed Scalar*, arXiv:2407.13587v1, https://arxiv.org/abs/2407.13587 ; upstream code revision `blackstonep/hipsofcobra@6a6dcfccf903317ea2104e27bb1dbbc7ad1d9fc7`. These authors did not propose or validate our two-singlet benchmark.
