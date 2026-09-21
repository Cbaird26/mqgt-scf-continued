# Research Note 15 — Off-shell Higgs spectral factorization and an idealized detector bound

**2026-09-21 | Exploratory, conditional, unreviewed calculation.** Extends Research Note 14's symmetric-vacuum, zero-source, common-Z2 two-singlet submodel. No discovery or validation of the proposed scalar fields, consciousness, ethics, or H2 dynamics is claimed. All dimensions use natural units except decay lengths.

## Derive the inclusive decay expression

The fixed interaction is `L ⊃ -v K12 h s1 s2`; set `m2 > m1`, `Delta=m2-m1<mh`, and `q²` to the invariant squared mass of an inclusive Standard Model final state `X`. Define `lambda(a,b,c)=(a-b-c)^2-4bc`, and let `Gamma_h*(sqrt(q²); X)` mean the physical, channel-specific width of a hypothetical Higgs scalar with mass `sqrt(q²)` and the corresponding Standard Model couplings/form factors. Tree-level factorization gives

```
dGamma(s2 -> s1 X)/dq²
 = [v² K12² sqrt(lambda(m2²,m1²,q²)) / (16 pi m2³)]
   * [sqrt(q²) Gamma_h*(sqrt(q²); X) / (pi D_h(q²))],
D_h(q²)=(mh²-q²)²+mh² Gamma_h².
```

Integrate over physical thresholds through `0 <= q² <= Delta²` and sum over *non-overlapping* final states. The constant-width propagator is numerically immaterial far below the Higgs pole; a fully consistent high-precision treatment would use a matched off-shell propagator. As a cross-check, inserting `Gamma_h* -> f fbar = Nc mf² sqrt(q²)/(8 pi v²) [1-4mf²/q²]^(3/2)` reproduces the explicit free-fermion differential expression in Note 14 exactly. For hadronic `X`, this formula requires physical QCD-inclusive spectral information or a validated perturbative calculation with thresholds, running masses, and corrections; plugging uncorrected free b/c-quark widths into the sum would not establish a total width.

## What can be established without a hadronic model

Freeze only the *illustrative* Note-14 point `m1=10 GeV`, `m2=25 GeV`, `mh=125 GeV`, `v=246 GeV`, `Gamma_h=0.0041 GeV`, `theta=pi/4`, `kappa_PhiH=0.002`, `kappa_EH=0`, so `K11=K22=0.001` and `K12=-0.001`. Its `s2 -> 3s1` channel remains kinematically closed. Standard-library composite-Simpson quadrature yields tree-level leptonic partial widths (GeV): electron `1.17526e-22`, muon `5.02081e-18`, tau `1.151478228e-15`; hence

```
Gamma_total >= Gamma_e + Gamma_mu + Gamma_tau = 1.156499157e-15 GeV,
c tau_total <= hbar*c / Gamma_leptons = 0.1706244 m.
```

These are *internal toy-model* bounds conditional on those couplings; they do not determine the hadronic contribution, complete lifetime, or physical parameter viability. Additional channels may shorten the lifetime.

For this same point, corrected tree-level Higgs partial widths (GeV) are `Gamma_11=4.75366954e-6`, `Gamma_12=9.17934993e-6`, `Gamma_22=4.41367137e-6`, with total `1.83466908e-5` and conditional pair-production branching fraction `0.004455` when the only other Higgs width is `0.0041 GeV`.

**Idealized geometry, not LHC acceptance.** Suppose an at-rest Higgs, a spherical detection boundary at 1 m, independent exponential decay lengths, and *every* `s2` decay within that boundary being fully detectable. Then the leptonic width floor implies survival ceilings `P12 <= 0.08545` for the heavy state in `h -> s1 s2`, and `P22 <= 0.07747` for each heavy state in `h -> s2 s2`. The potentially invisible width in this explicitly ideal model obeys

```
Gamma_invisible,ideal <= Gamma_11 + P12 Gamma_12 + (P22)^2 Gamma_22
                      <= 5.565e-6 GeV.
```

These percentages are *not* a collider constraint or a reliable estimate of invisibility in ATLAS/CMS: real boosts, acceptance, soft/displaced tracks, branching fractions, trigger thresholds, detector geometry and possible invisible additional interactions invalidate the toy classification. The robust conclusion is the **spectral-function route to a total width** and a narrow, well-labeled leptonic lower bound, not a real-world detector efficiency.

## Reproducibility and next gate

`test_research_note_15.py` (standard library) exercises the spectral/fermion identity, old tau integral, lepton bound, Higgs pair arithmetic, and idealized survival bound. Five local tests passed on 2026-09-21. An independent SciPy quadrature check of the spectral formula also reproduced the tau width. Neither is independent experimental validation. The next necessary input is a cited, matched low-energy Higgs hadronic spectral function, followed by a full decay inventory and detector simulation; leave the working paper's total-lifetime and collider-acceptance claims open until then.

**Attribution:** Christopher Michael Baird, human author. ChatGPT (ZoraASI) assisted with calculation, checking, manuscript drafting, and implementation; it is not an independent referee or coauthor.
