# Research Note 35 — Maxwell–Boltzmann thermal averaging of the *leptonic-only* singlet annihilation partial rate

**22 September 2026 | Public scientific-development addendum; not peer reviewed.** Christopher Michael Baird is the human author. ChatGPT (ZoraASI) assisted with the derivation, source comparison, numerical quadrature and drafting. The two-singlet EFT and any consciousness/ethics interpretation remain hypotheses. This note neither establishes relic abundance nor detects dark matter or calculates hadronic annihilation.

## 1. Upgrade a formal reference product without changing its meaning

Note 28 calculated the **zero-relative-speed, tree-level leptonic partial** `s1 s1 -> e+e-, mu+mu-, tau+tau-`, `sum(sigma*v)_0 = 1.03679016281e-15 GeV^-2`, at the *illustrative* `m1=10 GeV`, `K11=0.001`, `mh=125 GeV`, `Gamma_h=0.0041 GeV`. Note 34 multiplied this threshold quantity by a hypothetical **zero-chemical-potential equilibrium density**; it explicitly called that product **formal**, not a thermal reaction rate. The next narrowly answerable question is: what happens if the same *three leptonic channels only* are thermally averaged with an ideal Maxwell–Boltzmann bath? Neither this average nor the equilibrium reference density is an actual total reaction density without a justified cosmological history and the other channels.

For `s >= 4m1^2`, `beta_i(s)=sqrt(1-4m1^2/s)`, `beta_f(s)=sqrt(1-4mf^2/s)`, and `D(s)=(s-mh^2)^2+mh^2 Gamma_h^2`, the Note-28 interaction `L_int ⊃ -(v K11/2) h s1^2 -(mf/v) h fbar f` yields for each Dirac lepton (`N_c=1`)

```
[sigma*v_Moller]_COM(s) = K11^2 mf^2 beta_f(s)^3 / [4*pi*D(s)],
sigma(s) = [sigma*v_Moller]_COM(s) / [2 beta_i(s)].
```

The second expression is singular *as a cross section* exactly at the initial-state threshold, but its product with the flux/phase-space factor in the thermal integral is finite. The first expression at `s=4m1^2` recovers Note 28's threshold partial rate. Do not add an extra `1/2` to the cross section for identical incoming real scalars: the pair-counting factor in a reaction density is a separate bookkeeping convention.

For an ideal, common-temperature, zero-chemical-potential **Maxwell–Boltzmann reference bath** with `x=m1/T`, use the relativistic one-dimensional thermal-average formula of Gondolo and Gelmini (1991):

```
<sigma*v>(T) = [1/(8 m1^4 T K2(x)^2)]
  * integral_(4m1^2)^infinity ds sigma(s) (s-4m1^2) sqrt(s) K1(sqrt(s)/T).
```

Here `K1,K2` are modified Bessel functions, not the portal matrix `K_ij`; the momentum-dependent cross section uses the *same fixed-width tree-level Higgs model* as Note 28. This is a **leptonic partial thermal average**, not a complete freeze-out cross section. For a numerically stable change of variable `w=sqrt(s)/T-2x`, `y=2x+w`, `s=T^2 y^2`, `kve_nu(z)=exp(z) K_nu(z)`, the same integral is

```
<sigma*v>_f = [1/(8 x^4 kve_2(x)^2)]
 * integral_0^infinity dw exp(-w) sqrt(w)
   [sigma*v_COM]_f(T^2(2x+w)^2)
   (2x+w)^3 sqrt(4x+w) kve_1(2x+w).
```

This is also suitable for independent generalized Gauss–Laguerre quadrature with weight `exp(-w)*sqrt(w)`; no upstream hadronic loader or Omnès numerical data is involved.

## 2. Numerical cross-check, with its precision boundary

At the declared point, adaptive quadrature over `0 <= w <= 90` and independent 32-/64-node generalized Gauss–Laguerre evaluation agree for the **tau-only** partial at the displayed precision (agreement at about `1e-15` relative for `x=10,20,30,50` in the local comparison). The tau values in `GeV^-2` are approximately:

| x = m1/T | T (GeV) | tau-only thermal <sigma*v> | tau-only zero-speed reference |
|---:|---:|---:|---:|
| 10 | 1 | 9.19878793e-16 | 1.03295820409e-15 |
| 20 | 0.5 | 9.70342862e-16 | 1.03295820409e-15 |
| 30 | 1/3 | 9.89733829e-16 | 1.03295820409e-15 |

For the **sum of all three charged-lepton channels** at x=20 the evaluated thermal partial is **approximately `9.74e-16 GeV^-2`**, or about **94%** of Note 28's threshold partial; do not use the extra digits of the initial finite-window exploratory sum as a numerical uncertainty estimate. At the same *assumed* `T=.5 GeV`, the Note-34 reference `n1_eq=1.60329212678e-9 GeV^3` and `H=2.63320146442e-19 GeV` produce the purely conditional **equilibrium-reference** product `n1_eq * <sigma*v>_leptons / H ≈ 5.93e-6`, rather than the zero-speed-formal `6.31276235e-6`. Thus the previous formal estimate is refined, not refuted: both are extremely incomplete inputs to the true number-changing problem.

The `w<=90` adaptive evaluation is a finite-window numerical calculation, *not a claimed exact integration to infinity*. For the quoted parameters a conservative high-energy tail bound follows from `sigma*v_COM <= K11^2 mf^2/[4*pi*(mh*Gamma_h)^2]`, `sqrt[w(4x+w)] <= (2x+w)`, and decreasing `kve_1(2x+w)`: the neglected positive tail is bounded by the same prefactor times `kve_1(2x+90)*integral_90^infinity exp(-w)*(2x+w)^4 dw`. The bound is negligible at the **quoted three-significant-figure** precision, including the distant Higgs pole. This is not a full numerical error budget, a QCD modeling uncertainty, or an improved observational constraint. The local tau quadrature comparison was completed; **no new Note-35 regression suite or independent all-channel software audit is claimed**.

## 3. Remaining physical gate and source/provenance distinction

An actual annihilation calculation must also include physically valid nonoverlapping hadronic final states, loop-induced channels, relevant `s1 s2`/`s2 s2` channels and any singlet self-reactions; it must establish species distributions, kinetic and chemical equilibrium, the thermal history and initial conditions, then solve the appropriate coupled number equations. The four upstream Omnès files are **not yet authenticated and safely parsed in full**; the restricted tau/e/mu computation does not substitute for them. A thermal average of a partial channel is *not* the complete number-changing collision operator, a freeze-out temperature, a value of the local dark-matter fraction `xi`, or an exclusion.

**Sources and convention checks:** Note 28's declared tree-level amplitude and masses, Note 34's *explicitly formal* threshold-rate diagnostic, and P. Gondolo & G. Gelmini, *Cosmic abundances of stable particles: improved analysis*, Nucl. Phys. B **360** (1991) 145–179, DOI: https://doi.org/10.1016/0550-3213(91)90438-4 , for the exact one-dimensional Maxwell–Boltzmann thermal-average method. That paper does **not** study or endorse this hypothetical benchmark. The code comparisons above are mathematical checks only; no archival manuscript, frozen independent-verification snapshot, or `main` branch was modified.
