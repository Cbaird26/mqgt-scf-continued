# Research Note 39 — Unequal-mass leptonic coannihilation partials and a conditional effective rate

**27 September 2026 | Public scientific-development addendum; not peer reviewed.** Christopher Michael Baird is the human author. ChatGPT (ZoraASI) assisted with the unequal-mass thermal derivation, numerical implementation, cross-checks, tests, and drafting. The restricted two-singlet EFT remains hypothetical. This note does not calculate a relic abundance, total annihilation rate, hadronic width, detector likelihood, or empirical consciousness/ethics signal.

## 1. Extend the thermal calculation from 11 to 12 and 22

Notes 35–36 thermally averaged only the charged-lepton partial of `s1 s1`. Note 38 then derived the two-species total-number operator and showed that a physical coannihilation calculation additionally needs `<sigma_12 v>` and `<sigma_22 v>`. This note computes the same restricted **electron + muon + tau partial only** for all three initial pairs at the illustrative Note-24 benchmark

```
m1 = 10 GeV,  m2 = 11.5 GeV,
K11 = +0.001, K12 = -0.001, K22 = +0.001,
mh = 125 GeV, Gamma_h = 0.0041 GeV.
```

The portal interaction is

```
L_int superset -(v/2) h [K11 s1^2 + 2 K12 s1 s2 + K22 s2^2]
                 -(mf/v) h fbar f .
```

For initial masses `mi,mj`, define

```
lambda_ij(s) = [s-(mi+mj)^2][s-(mi-mj)^2],
beta_f(s) = sqrt(1-4 mf^2/s),
D(s) = (s-mh^2)^2 + mh^2 Gamma_h^2 .
```

The isotropic tree-level cross section for `s_i s_j -> f fbar` is

```
sigma_ij->ff(s)
 = Kij^2 mf^2 s beta_f(s)^3
   / [8 pi D(s) sqrt(lambda_ij(s))] .
```

No extra initial-state `1/2` is inserted into this physical cross section. The identical-pair factors belong to event-density bookkeeping, as derived in Notes 37–38.

For a common-temperature ideal Maxwell–Boltzmann bath, the unequal-mass invariant thermal average is

```
<sigma_ij v>(T)
 = 1/[8 mi^2 mj^2 T K2(mi/T) K2(mj/T)]
   * integral_((mi+mj)^2)^infinity ds
     sigma_ij(s) lambda_ij(s)/sqrt(s) K1(sqrt(s)/T).
```

For `mi=mj=m1` this reduces algebraically to the equal-mass formula used in Notes 35–36. The implementation evaluates a scaled-Bessel `w=sqrt(s)/T-mi/T-mj/T` form and separately evaluates the original invariant integral in `q=sqrt(s)` as a numerical cross-check.

## 2. Charged-lepton partials at the illustrative T = 0.5 GeV point

At `T=0.5 GeV` (`m1/T=20`, `m2/T=23`), the three charged-lepton thermal partials are

| initial pair | electron | muon | tau | e+mu+tau total |
|---|---:|---:|---:|---:|
| `s1 s1` | `8.39081761e-23` | `3.58677985e-18` | `9.70342862e-16` | **`9.73929725784e-16`** |
| `s1 s2` | `8.53804435e-23` | `3.64978778e-18` | `9.93179396e-16` | **`9.96829268711e-16`** |
| `s2 s2` | `8.61485399e-23` | `3.68268259e-18` | `1.00691241496e-15` | **`1.01059518370e-15`** |

All entries are in `GeV^-2`. The `11` result reproduces Note 36. The sign of `K12` drops out of this single-Higgs-exchange rate because the rate is proportional to `K12^2`; that does not imply the sign is irrelevant in amplitudes where other diagrams interfere.

The transformed and direct invariant integrals agree for the tau channel for all three initial pairs at better than the displayed precision; the mixed-channel electron/muon/tau comparisons also agree within the regression tolerances. A positive finite-`w` tail bound at `W=90` gives summed three-lepton upper tails of approximately

```
11: 2.12e-43 GeV^-2,
12: 1.88e-43 GeV^-2,
22: 1.67e-43 GeV^-2,
```

for this fixed-width kernel, about `10^-28` of the corresponding quoted partials. These bounds do **not** constrain omitted hadronic, radiative, plasma, or other physical channels.

## 3. Conditional leptonic-only effective coannihilation partial

Using the full ideal-gas Maxwell–Boltzmann equilibrium densities

```
n_i^eq = mi^2 T K2(mi/T)/(2 pi^2)
```

with one real degree of freedom per species gives at `T=0.5 GeV`

```
r2 = n2eq/(n1eq+n2eq) = 0.0572145986119,
r1 = 0.942785401388.
```

The corresponding exact-MB weights are

```
r1^2      = 0.888844313070,
2 r1 r2   = 0.107882176635,
r2^2      = 0.00327351029432.
```

These differ slightly from Note 28's explicitly nonrelativistic approximation because Note 29 already replaced that approximation with the full Bessel-function ideal-gas fraction.

**Only if** chemical conversion is sufficiently rapid to justify the one-equation reduction of Note 38, the three charged-lepton partials combine as

```
<sigma_eff v>_leptons
 = r1^2 <sigma_11 v>_lep
 + 2 r1 r2 <sigma_12 v>_lep
 + r2^2 <sigma_22 v>_lep
 = 9.76520203072e-16 GeV^-2.
```

The weighted pieces are approximately

```
11 contribution = 8.65671898093e-16 GeV^-2,
12 contribution = 1.07540111242e-16 GeV^-2,
22 contribution = 3.30819373723e-18 GeV^-2.
```

Within this **leptonic-only, equilibrium-assumed** construction, the effective partial is only `1.00265982` times the `s1 s1` leptonic partial. That small numerical shift does not imply coannihilation is physically negligible: the missing hadronic and other channels can have different relative sizes in `11`, `12`, and `22`, and the conversion analysis in Notes 29–34 has not established that equilibrium tracking actually holds.

## 4. Reproducibility and exact-byte record

Two new files were staged:

- `coannihilation_leptons.py` — Git blob `c349c38a126a9c01e77766661d6757ad20de16f4`;
- `test_research_note_39.py` — Git blob `e9059d6b2f72609138d486bfd5a2ca17b8a9427c`.

Those GitHub blob identifiers match the locally executed source bytes. The first local test pass exposed a test-call typo and an over-tight direct-integral tolerance for the tiny electron mixed-channel partial; those **test assertions only** were corrected without altering the thermal formulas or reference outputs. The final exact-byte-matched suite produced **13 tests, 13 passes, 0 failures** in approximately **0.060 s**.

The tests cover recovery of Note 36, all three pair totals, transformed-versus-direct invariant integration, full-MB equilibrium fractions, exact effective weights, the conditional effective partial, portal-sign invariance of the single-diagram rate, positive tail bounds, and invalid-input rejection. They are mathematical/software checks, not independent scientific validation.

## 5. Remaining physical gate

This note fills only the **charged-lepton portion** of the `11/12/22` number-changing network. A physical total-number evolution still requires nonoverlapping hadronic/quark contributions, loop/radiative channels where relevant, temperature-dependent conversion scatterings, a declared thermal history, and the coupled Boltzmann solution. The four authenticated Omnès inputs remain separately required for the heavy-state exclusive hadronic-decay calculation.

No external QCD code, detector likelihood, unsafe upstream loader, journal submission, DOI, or experimental data were used. The review branch remains an unmerged scientific-development draft; `main`, historical PDFs, and the frozen independent-verification snapshot remain unchanged.
