# Research Note 37 — Exact-byte Note-36 execution audit and the number-equation gate

**24 September 2026 | Public scientific-development addendum; not peer reviewed.** Christopher Michael Baird is the human author. ChatGPT (ZoraASI) assisted with exact-byte verification, local test execution, bookkeeping derivation, and drafting. The restricted two-singlet EFT remains hypothetical. This note does not determine a relic abundance, total annihilation rate, hadronic width, experimental exclusion, or observed consciousness/ethics field.

## 1. Close Note 36's committed-byte reproducibility gap

Note 36 correctly recorded that its 14 tests had passed on the local working implementation *before* GitHub transfer, while an exact-byte rerun of the committed files had not yet been completed. That historical statement remains untouched.

On 24 September 2026, the two files were fetched from the approved review branch through the GitHub connector and copied into the local execution directory without source edits:

- `thermal_leptons_repro.py`: Git blob `48739229762c6d477e43e608532eade6a649539f`
- `test_thermal_leptons_repro.py`: Git blob `acf79b129678032d3c84dbc75a25e27b164b8368`

Local `git hash-object` returned those same two blob identifiers. Running

```
python3 -m unittest -v test_thermal_leptons_repro.py
```

against those exact bytes produced **14 tests, 14 passes, 0 failures** in approximately **0.040 s**. This closes only the software-reproducibility gap identified by Note 36. It is not independent physics validation, a detector result, or evidence that the omitted physical channels are negligible.

## 2. Why pair counting does not insert an extra one-half into the number-loss equation

For an identical self-conjugate real scalar species `s1`, define the annihilation event density for unordered incoming pairs as

```
R_11 = (1/2) n1^2 <sigma v>_11 .
```

Each annihilation event removes **two** `s1` particles, so the forward number-loss contribution is

```
(d n1/dt + 3 H n1)_forward = -2 R_11
                              = - n1^2 <sigma v>_11 .
```

If the Standard-Model bath is in equilibrium and detailed balance is used for the inverse process, the corresponding restricted one-species equation is

```
d n1/dt + 3 H n1 = - <sigma v>_11 [n1^2 - n1,eq^2].
```

Thus the `1/2` used to avoid double-counting identical **events** is exactly canceled by the two particles removed per event. Multiplying the cross section itself by another `1/2` would double-count that convention. This is bookkeeping, not a new interaction.

For entropy-conserving evolution with `Y1=n1/s_entropy`, `x=m1/T`, and constant entropy degrees of freedom, the same restricted equation becomes

```
dY1/dx = - [s_entropy <sigma v>_11 /(H x)]
          [Y1^2 - Y1,eq^2].
```

This equation is only as complete as the collision term supplied to it.

## 3. The two-singlet total-number equation is still not closed

Notes 31–34 treated conversions such as `s2 <-> s1 + SM`. Those reactions change the species label but preserve one odd-sector particle, so they cancel in the equation for

```
N = n1 + n2 .
```

The total abundance is instead controlled by genuinely number-changing reactions: at minimum `s1 s1`, `s1 s2`, and `s2 s2` annihilation/inverse-production channels, plus any additional singlet self-reactions or production mechanisms allowed by the declared EFT and cosmological history.

Only the three charged-lepton **partial** of `s1 s1` has received the Maxwell–Boltzmann thermal treatment of Notes 35–36. The following are still missing or physically incomplete:

- nonoverlapping hadronic/quark final states and their thermal treatment;
- loop-induced and radiative channels where relevant;
- `s1 s2` and `s2 s2` annihilation/coannihilation rates;
- temperature-dependent conversion scatterings;
- authenticated and safely parsed Omnès inputs for the separate heavy-state hadronic-decay problem;
- a declared `g_*(T), g_{*S}(T)` history, reheating/initial condition, and coupled Boltzmann solution.

Therefore a numerical integration using only the Note-36 charged-lepton partial would be a **prepared toy history**, not a prediction of `xi`, `Omega h^2`, freeze-out, or present-day density. The correct next physical gate is to complete the collision operator before interpreting a yield trajectory.

## 4. Scope and provenance

The number-equation bookkeeping is consistent with the pair-counting convention already stated in Note 36 and with the Maxwell–Boltzmann thermal-average convention cited there from Gondolo and Gelmini (1991). That reference does not study or endorse this two-singlet benchmark. No new external hadronic code, detector likelihood, unsafe upstream loader, or experimental data were executed for this note.

The review branch remains a public scientific-development draft. `main`, the frozen independent-verification snapshot, historical PDFs, and archival source equations remain unchanged. No DOI, release, peer review, journal submission, or empirical validation is claimed.
