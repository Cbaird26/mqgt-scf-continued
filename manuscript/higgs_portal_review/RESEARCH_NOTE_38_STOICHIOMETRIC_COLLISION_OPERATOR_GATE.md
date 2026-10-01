# Research Note 38 — Stoichiometric collision-operator gate and conditional coannihilation reduction

**25 September 2026 | Public scientific-development addendum; not peer reviewed.** Christopher Michael Baird is the human author. ChatGPT (ZoraASI) assisted with algebra, code, exact-byte checks, tests, and drafting. The restricted two-singlet EFT remains hypothetical. This note does not calculate a relic abundance, total annihilation rate, hadronic width, detector likelihood, or empirical consciousness/ethics signal.

## 1. Reaction stoichiometry separates conversions from number-changing chemistry

Let the odd-sector species vector be `(n1,n2)`, where each `s1` or `s2` particle carries one unit of the bookkeeping count `N=n1+n2`. For a single forward reaction event, define

```
Delta N_odd = (# odd particles in final state) - (# odd particles in initial state).
```

Then the classes relevant to the restricted two-singlet discussion are structurally distinct:

- `s2 -> s1 + SM`, `s1 + SM -> s2 + SM`, and odd-sector reshufflings with the same number of odd particles have `Delta N_odd=0`.
- `s1 s1 -> SM`, `s1 s2 -> SM`, and `s2 s2 -> SM` have `Delta N_odd=-2` in the forward direction; inverse production has `+2`.

Therefore all pure conversion terms cancel when the two species equations are summed. This is the reaction-network version of the total-number obstruction identified in Notes 34 and 37: conversions can alter the composition `n2/N`, but cannot determine the absolute abundance `N`.

## 2. Pair counting fixes the mixed-channel coefficient

For thermally averaged physical cross sections `<sigma_ij v>`, define unordered forward annihilation event densities

```
R11 = (1/2) n1^2 <sigma_11 v>,
R12 =       n1 n2 <sigma_12 v>,
R22 = (1/2) n2^2 <sigma_22 v>.
```

The identical-state factors belong to the **event counts**. Each event removes two odd-sector particles, hence

```
(dN/dt + 3 H N)_forward
 = -2(R11+R12+R22)
 = - n1^2 <sigma_11 v>
   - 2 n1 n2 <sigma_12 v>
   - n2^2 <sigma_22 v>.
```

The factor of two multiplying the mixed term is therefore not an extra ordered copy of the physical `s1+s2` cross section. It arises because one mixed annihilation event removes **two total odd particles**, while `R12` itself carries no identical-pair `1/2`.

With a bath in equilibrium and detailed balance applied separately to the three channels, a convenient species-level form is

```
C1 = -<sigma_11 v>(n1^2-n1eq^2)
     -<sigma_12 v>(n1 n2-n1eq n2eq) + Jconv,

C2 = -<sigma_22 v>(n2^2-n2eq^2)
     -<sigma_12 v>(n1 n2-n1eq n2eq) - Jconv,
```

where `Jconv` is any net `s2 -> s1` conversion flux. Summing gives

```
C_N = C1+C2
    = -<sigma_11 v>(n1^2-n1eq^2)
      -2<sigma_12 v>(n1 n2-n1eq n2eq)
      -<sigma_22 v>(n2^2-n2eq^2),
```

and the conversion flux cancels exactly.

## 3. Conditional chemical-equilibrium reduction

Only if conversions are sufficiently rapid that the two species track the **same instantaneous equilibrium fractions**

```
n1 = r1 N,   n2 = r2 N,
n1eq = r1 Neq, n2eq = r2 Neq,
r1+r2=1,
```

does the summed collision term reduce algebraically to the usual one-equation coannihilation form

```
C_N = - <sigma_eff v> (N^2-Neq^2),

<sigma_eff v>
 = r1^2 <sigma_11 v>
 + 2 r1 r2 <sigma_12 v>
 + r2^2 <sigma_22 v>.
```

This reproduces the weighting written in Note 28 from the species equations rather than assuming it by inspection. The three coefficients sum to one. As a regression against Note 28's explicitly **nonrelativistic illustrative equilibrium fraction** `r2=0.05784749058` at `x=20`, the coefficients are

```
r1^2       = 0.8876513510,
2 r1 r2    = 0.1090023168,
r2^2       = 0.00334633217.
```

If the three thermal cross sections happened to be equal, the effective cross section would equal that common value exactly. This is a normalization identity, not a physical statement that the three channels are equal.

Crucially, Notes 29–34 already show that the **known leptonic conversion channel alone** is not demonstrably fast enough to justify this chemical-equilibrium reduction through the illustrative cooling history. The reduction is therefore a conditional algebraic limit, not the currently established dynamical regime of the benchmark.

## 4. What is still missing before a total-number evolution is physical

Notes 35–37 provide only the Maxwell–Boltzmann thermal treatment of the charged-lepton **partial** of `s1 s1`. The total-number equation still lacks, at minimum:

- physically valid nonoverlapping hadronic/quark contributions to `<sigma_11 v>`;
- loop/radiative final states where relevant;
- the thermal `s1 s2` and `s2 s2` annihilation/coannihilation rates;
- temperature-dependent conversion scatterings needed to test whether the one-equation reduction is dynamically justified;
- a declared `g_*(T),g_*S(T)` history and initial/reheating conditions;
- the authenticated Omnès inputs needed for the separate `s2` hadronic-decay calculation.

Accordingly, integrating the one-equation coannihilation form with placeholders for the missing rates would produce only a prepared toy trajectory. This note deliberately stops at the collision-operator structure.

## 5. Reproducibility record

Two new standard-library files were staged:

- `reaction_network_gate.py` — Git blob `298794f8d03e893482ce7671f6ee207f25986372`;
- `test_research_note_38.py` — Git blob `74ba0f2dd34724c1f43d943d93b4115f48718fa3`.

Those GitHub blob hashes match the locally executed source bytes. Running

```
python3 -m unittest -v test_research_note_38.py
```

against the matching local bytes produced **13 tests, 13 passes, 0 failures**. The tests cover stoichiometric conservation, identical/mixed pair counting, conversion cancellation, the summed species equation, Note-28 weight regression, the conditional one-equation reduction, equilibrium fixed points, and input validation. The surrounding Python environment emitted an unrelated non-fatal spreadsheet-runtime warmup warning, but the unittest process returned exit code 0. These are algebra/software tests only, not independent scientific validation.

No external QCD code, detector likelihood, unsafe upstream loader, or experimental data were executed. The review branch remains an unmerged scientific-development draft; `main`, historical PDFs, and the frozen independent-verification snapshot remain unchanged.
