# Research Note 14 — Mixed-singlet decay inventory and leptonic cross-check

**2026-09-21 | Public development draft; not peer reviewed or an experimental result.** This note extends the symmetric-vacuum, zero-source, common-Z2 two-singlet submodel in `COMPREHENSIVE_WORKING_PAPER_2026-09-21.md` (§§2–4). It does not establish either hypothetical field's physical existence or interpretation.

## Higgs-mediated three-body channel

With `(Phi,E)^T=R(theta)(s1,s2)^T` and `R=[[c,-s],[s,c]]`, the anchor-normalized portals yield `L ⊃ -v K12 h s1 s2` where `K12=(kappa_EH-kappa_PhiH)*s*c`. The Standard Model Yukawa interaction is `L ⊃ -(mf/v) h fbar f`. For `s2 -> s1 h* -> s1 f fbar`, define `q²=(pf+pfbar)²` and `lambda(x,y,z)=(x-y-z)²-4yz`. The tree-level free-fermion differential width is

```
dGamma_f/dq² = [Nc K12² mf²/(128 pi³ m2³)]
    * q² sqrt(lambda(m2²,m1²,q²)) (1-4 mf²/q²)^(3/2)
    / [(q²-mh²)²+mh² Gammah²]
```

integrated over `4mf² <= q² <= (m2-m1)²`. It follows by summing fermion spins and factorizing the three-body phase space. Hadronic channels need QCD treatment: a free-b-quark integral is not a detector prediction.

## Previously omitted quartic-mediated channel

For `V4=lambda_Phi Phi^4/4 + lambda_E E^4/4 + kappa Phi²E²/2`, the coefficient of `s1³ s2` in the rotated potential is

```
C1112=c*s*(-lambda_Phi*c²+lambda_E*s²+kappa*(c²-s²));
g2111=6*C1112.
```

Consequently `s2 -> 3s1` can occur for `m2>3m1` if its effective coupling is nonzero. Exact common Z2 forbids `s2 -> 2s1`, but does not generally stabilize the heavier state.

## Internally rechecked illustrative point (not fitted)

For `m1=10 GeV`, `m2=25 GeV`, `theta=pi/4`, `kappa_PhiH=0.002`, `kappa_EH=0`, `mh=125 GeV`, `Gammah=0.0041 GeV`, `m_tau=1.77686 GeV`, one has `|K12|=0.001`. A positive singlet mass matrix can be arranged with `A=B=362.5 GeV²`, `|gamma|=262.5 GeV²` and eigenvalues `100,625 GeV²`. In the defined portal convention with `v=246 GeV`, the corresponding diagonal bare masses squared are `301.984,362.5 GeV²`, respectively. This confirms local singlet-direction positivity only, not global vacuum or phenomenological viability.

The `s2 -> 3s1` mode is closed here (`25<30 GeV`). Independent SciPy quadrature and a standard-library composite-Simpson implementation give

```
Gamma(s2 -> s1 tau+ tau-) = 1.151478228e-15 GeV;
hbar*c/Gamma_tau = 0.17137 m.
```

Because total width is at least the tau partial width, **`c*tau_total <= 0.17137 m` in this toy model**. This is not a claim that the total lifetime equals the tau-only figure; accessible hadronic modes and other channels may shorten it.

For an at-rest 125-GeV Higgs with `h -> s1 s2`, the toy heavy state has `E2=64.6 GeV` and `beta*gamma=2.38266`. Its mean flight is bounded above by `0.40831 m`; survival past an *idealized* 1-m boundary is at most `0.0864`. This is not a real collider acceptance or an ATLAS/CMS likelihood: Higgs boosts, angular coverage, material, branching fractions, and reconstruction must be simulated.

**Status/gates:** The tau partial-width algebra and toy arithmetic are internally rechecked; a complete lifetime and detector classification remain unverified. Complete hadronic/QCD, leptonic, loop-mediated and quartic modes as applicable, and investigate any extra EFT operators before updating the manuscripts or reinterpretating an invisible-Higgs limit. The H2 dephasing coefficient is not derived from this decay calculation.

**Attribution:** Human author Christopher Michael Baird. ChatGPT (ZoraASI) assisted with derivation, manuscript drafting, and internal computational checks; no independent referee or experimental result is claimed.
