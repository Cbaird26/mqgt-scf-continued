# Research Note 34 — Initial-condition memory versus number-changing chemistry

**22 September 2026 | Public scientific-development addendum, not peer reviewed.** Human author: Christopher Michael Baird; ChatGPT (ZoraASI) assisted in source comparison, mathematical derivation, limited numerical evaluation, and drafting. The two-singlet model and any consciousness/ethics interpretation are hypothetical. No observed field, dark-matter abundance, hadronic width, BBN clearance or collider exclusion is inferred.

## 1. The exact initial-condition memory hidden inside Notes 31–33

Retain **only** the conversion-only assumptions of Notes 31–33: `m1=10 GeV`, `m2=11.5 GeV`, vacuum **leptonic partial** `Gamma_l=3.060267688e-22 GeV`, ideal Maxwell–Boltzmann distributions, a common temperature, radiation domination, constant *illustrative* `g_*=g_*S=60`, `x=m1/T` increasing from 10, and a fixed comoving total odd-particle number. Define `q=n2_eq/n1_eq`, `r=q/(1+q)`, `D2=K1(m2/T)/K2(m2/T)`, and the hypothetical shared-width multiplier `c>=0`. Only under this artificial common-temperature dependence does `Lambda_c=c Gamma_l D2 (1+q)` and `k_c=Lambda_c/(x H)`.

The exact conversion-only fraction equation is `y'=-k_c(x)[y-r(x)]`. For two solutions `y_a` and `y_b` **with the same bath and rate but different prepared initial fractions**, their difference obeys `d(y_a-y_b)/dx=-k_c(y_a-y_b)`. Therefore

```
y_a(x)-y_b(x) = [y_a(10)-y_b(10)] exp[-I_c(x)],
I_c(x) = integral_10^x Lambda_c(u)/[u H(u)] du = c I_1(x).
```

This is an exact **memory-retention identity**, not a fit or a simulated particle abundance. It separates initial-condition memory from the distinct effect of an evolving equilibrium target. With the special initial choice `y(10)=r(10)`, the positive lag is instead

```
y(x)-r(x) = integral_10^x exp[-(I_c(x)-I_c(t))] [-r'(t)] dt
```

when `r` decreases over the interval. A large `I_c` can erase initial-state memory while still leaving a nonzero cooling-induced lag; the two notions should not be conflated.

## 2. Evaluate this quantity on the *same* toy background

Numerical quadrature of the previously staged `conversion_history.mb_rates(x)['dy_dx_factor']` yields `I_1(20)=0.00045188468953458` and `I_1(30)=0.0011625930884404`. The exact initial-perturbation retention factors `exp(-c I_1)` are:

| Assumed equivalent-width factor `c` | At x=20 (T=.5 GeV) | At x=30 (T=1/3 GeV) |
|---:|---:|---:|
| 1 (known leptonic partial only) | 0.9995482174 | 0.9988380825 |
| 865 (approximate instantaneous `Lambda/H=1` at x=20) | 0.6764611531 | 0.3658093359 |
| 27512 (near Note-33 *chosen* 10%-lag diagnostic at x=20) | 3.99e-6 | 1.29e-14 |
| 19616 (near the diagnostic at x=30) | 1.41e-4 | 1.25e-10 |

For example, with **leptonic conversions alone**, two different permitted initial fractions remain separated by about **99.88% of their original difference** when the toy reaches x=30. At the much larger artificial multipliers near Note 33's 10%-lag thresholds, initial-condition memory is nearly gone, but the *moving equilibrium target* can still produce the lag that defined those thresholds. These numbers rely on the assumed `g_*` history, the particular mass/partial width, and the artificial scaling `c`; they are not computed hadronic rates. The quadrature is ordinary numerical evaluation, not a rigorous interval enclosure.

## 3. Conversion cannot determine absolute relic abundance—even if it is arbitrarily fast

Every conversion in this restricted two-state operator is `s2 <-> s1 + SM`; it changes the species label but preserves **one odd particle per reaction**. If `N=n1+n2`, then `(dN/dt+3HN)_conversion=0`. Consequently `N a^3` is a freely chosen constant throughout the conversion-only toy. Sending `c -> infinity` can force `y -> r(T)` but cannot determine **that constant**, the stable-particle number density today, or its cosmic fraction `xi`. Number-changing annihilations, inverse production, initial conditions, reheating and any other production mechanism belong in the separate total-number equation. This is an exact bookkeeping obstruction, not an inference of overproduction or underproduction.

A distinct scale diagnostic can be made without pretending to have that equation. For **one real degree of freedom** with *zero chemical potential* in an ideal Maxwell–Boltzmann reference bath, `n1_eq(T)=m1^2 T K2(m1/T)/(2 pi^2)`. At the *assumed* x=20, independent evaluation with a Bessel function gives `n1_eq=1.60329212678e-9 GeV^3` and Note 29's assumed `H=2.63320146442e-19 GeV`. Multiplying this **equilibrium reference density** by Note 28's **zero-relative-speed leptonic partial**, `sigma v|_0=1.03679016281e-15 GeV^-2`, gives the formal diagnostic

```
[n1_eq * (sigma v)_leptons, v_rel=0] / H = 6.31276235e-6,
H/n1_eq = 1.64237161e-10 GeV^-2 = 1.91718946e-27 cm^3/s.
```

The first is **not** a calculated thermal annihilation-event rate, because `(sigma v)|_0` is not the needed thermal average and actual `n1` need not equal `n1_eq`. The second is merely the reference cross-section scale that would make this *formal product* equal `H`, **not** a required cross section, excluded parameter point, measured abundance, or physical freeze-out temperature. The uncomputed hadronic/quark, loop, mixed-species, thermal, and number-changing channels can change the actual reaction network. Keep the Note-28 leptonic partial, the Note-31 conversion eigenvalue, and an actual thermal annihilation reaction density as three separate quantities.

## 4. Reproduction, source boundary and release gate

The memory exposure is directly reproducible from the **existing** `conversion_history.py` in this PR with `scipy.integrate.quad(lambda x: mb_rates(x)['dy_dx_factor'], 10, x_end)` and `math.exp(-c*I_1)`; the reference equilibrium density uses `scipy.special.kv(2,20)` and the stated constants. These independent local numerical evaluations preceded an intermittent local-execution outage; **no new Note-34 code or regression test was successfully uploaded or claimed to pass**. Notes 31–33's separate 16/16 tested toy code remains unchanged. These computations use only the internally declared benchmark and conventional special functions; neither missing Omnès arrays nor third-party hadronic code were executed. The pinned four input files remain unavailable as fully authenticated local files. No total `s2` width, validated cosmological history, complete thermal network, relic density or detector prediction follows. The draft PR is not a journal submission or DOI release, and `main`/archival manuscripts remain untouched.