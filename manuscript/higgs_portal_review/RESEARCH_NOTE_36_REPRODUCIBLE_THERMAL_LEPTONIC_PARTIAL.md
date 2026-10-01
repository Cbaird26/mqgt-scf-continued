# Research Note 36 — Reproducing the full three-lepton thermal partial and bounding the omitted integration tail

**22 September 2026 | Public scientific-development addendum; not peer reviewed.** Christopher Michael Baird is the human author; ChatGPT (ZoraASI) assisted with source comparison, algebra, code, numerical checks, and drafting. This note treats a hypothetical restricted symmetric-vacuum two-singlet EFT. It does not report a discovered field, a relic abundance, an exclusion, or the full annihilation rate.

## 1. Reproducibility question left by Note 35

Note 35 evaluated a Maxwell–Boltzmann thermal average of the *leptonic-only* `s1 s1 -> e+e-, mu+mu-, tau+tau-` partial process, but only the tau channel received an independent quadrature comparison. This note supplies a separately staged `thermal_leptons_repro.py` and `test_thermal_leptons_repro.py` covering **each of the three charged leptons**, a mathematically explicit upper bound on the finite-`w` tail, and regression against Notes 28, 34 and 35. No external hadronic input is acquired or inferred.

Exactly retain the unfitted illustrative inputs `m1=10 GeV`, `K11=.001`, `mh=125 GeV`, fixed `Gamma_h=.0041 GeV` and electron/muon/tau masses from Note 28. Let `D(s)=(s-mh²)²+mh² Gamma_h²`, `beta_f(s)=sqrt(1-4mf²/s)`, `beta_i(s)=sqrt(1-4m1²/s)`. The declared tree-level interactions give

```
[sigma*v_Moller]_COM(s) = K11² mf² beta_f(s)^3 / [4*pi*D(s)],
sigma(s) = [sigma*v_Moller]_COM(s) / [2*beta_i(s)],
<sigma*v>_f = [1/(8*m1^4*T*K2(m1/T)^2)]
              integral_(4*m1²)^infinity ds sigma(s)(s-4*m1²)sqrt(s)K1(sqrt(s)/T).
```

This is the standard single-species Maxwell–Boltzmann thermal-average convention of Gondolo and Gelmini (1991), DOI `10.1016/0550-3213(91)90438-4`, applied to the **declared restricted model**. It is not a thermal average of the complete two-species network. The identical-incoming-particle factor `1/2` belongs in the annihilation *event density* `R_11=n1²<sigma*v>_11/2` when counting unordered pairs; the corresponding number-loss term is `-2R_11=-n1²<sigma*v>_11` if inverse production is neglected. Multiplying the cross section itself by another `1/2` would double-count that convention.

Set `x=m1/T`, `w=sqrt(s)/T-2x`, `y=2x+w` and `kve_nu(z)=exp(z)K_nu(z)`. An algebraic change of variables gives the stable integral

```
<sigma*v>_f = [1/(8*x^4*kve_2(x)^2)]
             integral_0^infinity dw exp(-w)*sqrt(w)*
             [sigma*v]_f(T² y²)*y³*sqrt(4x+w)*kve_1(y).
```

The reproducer evaluates `0<=w<=90` by adaptive QUAD and separately evaluates the transformed `0<=w<infinity` integral by generalized Gauss–Laguerre quadrature with weight `exp(-w)*sqrt(w)`. These are distinct numerical algorithms applied to the same derived kernel, not an independent QFT derivation.

## 2. Explicit numerical results; fixed assumptions only

The output of the local implementation, in `GeV^-2`, is:

| Assumed x=m1/T | electron partial | muon partial | tau partial | total *leptonic partial* |
|---:|---:|---:|---:|---:|
| 10 | 7.92758411e-23 | 3.38880316e-18 | 9.19878793182e-16 | 9.23267675618e-16 |
| 20 | 8.39081761e-23 | 3.58677985e-18 | 9.70342862021e-16 | **9.73929725784e-16** |
| 30 | 8.56853155e-23 | 3.66273160e-18 | 9.89733829231e-16 | 9.93396646522e-16 |

All three x=20 charged-lepton partials agree between adaptive integration and 64-node generalized Gauss–Laguerre within approximately `1e-15` *relative* in the local floating-point comparison; corresponding tau checks at x=10,20,30 also agree. The x=20 total is `0.9393701452` times the **zero-speed three-lepton partial** of Note 28. With the *assumed zero-chemical-potential reference* `n1_eq=1.60329212678e-9 GeV³` and **assumed** radiation-era `H=2.63320146442e-19 GeV`, `n1_eq*<sigma*v>_leptons/H=5.93002048073e-6`. This latter quantity is an equilibrium-reference **partial** interaction-to-expansion diagnostic; an actual event or depletion rate additionally depends on the actual density and inverse reactions. It is neither an inferred total annihilation rate nor a freeze-out or abundance calculation.

## 3. Derive a transparent high-energy tail bound

At this *fixed-width Higgs-only* benchmark, positive `beta_f<=1` and `D(s)>=(mh*Gamma_h)^2` give `0 <= [sigma*v]_f(s) <= K11² mf²/[4*pi*(mh*Gamma_h)^2] = Vmax_f`. For `w>=W=90`, `sqrt[w(4x+w)]<=2x+w` and the positive scaled `kve_1(2x+w)` decreases with w. Thus the omitted positive tail obeys

```
Tail_f(W) <= Vmax_f * kve_1(2x+W)/(8*x^4*kve_2(x)^2)
             * sum_(j=0)^4 binomial(4,j)*(2x)^(4-j)*Gamma(j+1,W),
Gamma(j+1,W)=integral_W^infinity exp(-w)*w^j dw.
```

The sum of three computed **model-conditional numerical upper bounds** at W=90 is approximately `7.98e-43`, `2.12e-43`, and `1.09e-43 GeV^-2` for x=10,20,30 respectively, many orders below the quoted partial rates. The inequality is algebraic for the specified fixed-width kernel, but the displayed floating-point bound is not a certified directed-rounding interval, and it does **not** bound missing physical channels, parameter errors, QCD, plasma effects or cosmological assumptions. For x=10 the remote Higgs-pole region lies beyond W=90; it is nevertheless covered by this coarse maximum-based tail inequality. No extrapolation to resonance-adjacent dark-matter masses is licensed by these numbers.

## 4. Test and provenance record; remaining gates

The local working-copy suite first exposed one **overly tight decimal-rounding regression tolerance** for the Note-34 displayed equilibrium density; that tolerance was corrected to `7e-21 GeV³` without changing the calculation. Subsequently **14 of 14 local regression tests passed** (threshold normalization, three-channel/three-temperature quadrature comparison, quadrature order, positive fixed-model tail, reference density, finite-window checks and invalid-input rejection). These tests were executed on the local working implementation before its source was transferred into this branch through the GitHub connector; **an exact-byte Git-blob comparison or a fresh test run against the committed files has not been completed**. The tests are software checks, not independent scientific verification. SciPy/NumPy are required by the reproducer; no Omnès data, upstream `eval` loader, detector likelihood, or full Boltzmann solver was run.

The four pinned Omnès arrays remain missing as completely authenticated and safely parsed local inputs; hadronic final states, off-diagonal and heavy-state processes, a consistent thermal history and the full total-number equation are still open. Source separation: Notes 28, 34 and 35 supply this illustrative benchmark and its conditional previous quantities; Gondolo and Gelmini supply the general thermal-average formalism, not an endorsement of MQGT-SCF. The original archival papers and `main` are unchanged; this remains an unmerged draft scientific-development note.
