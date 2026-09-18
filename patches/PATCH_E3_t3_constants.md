# PATCH E3 — T-3 constants: correct spectral identifications

**Erratum:** E3 (resolved; constants identified, all quoted digits confirmed)
**Frozen record:** `mqgt-scf-independent-verification`, `MQGT_SCF_ERRATA_2026-09-17.md` §E3
**Targets:** `t3_beltrami_final.py` (primary), `t3_beltrami_exact.py`,
`t3_beltrami_complete.py`, `CRITICAL_ASSESSMENT.md`, `LITERATURE_SEARCH_T1_T3.md`

## Why

The audit assigned S7′ to "ζ′_Δ₂(0) on S⁷". That assignment is wrong — the
coexact 2-form ζ′(0) on S⁷ is −0.61982401, which matches nothing in the
program. The constants are in fact spectral determinants on the **two spheres
of the program's Hopf structure**, and both identifications are now confirmed
by a third independent method (stabilized Hurwitz numerics, 80-digit):

| Constant | Correct identification | Value |
|---|---|---|
| S7  | ½ ζ′(0) of **coexact 3-forms on S⁷** | 1.74845220445 (all 7 quoted digits ✓) |
| S7′ | −ζ′(0) of **coexact 2-forms on S⁹** | 0.41364465819 (all 5 quoted digits ✓) |

## `t3_beltrami_final.py` — docstring (lines 5–7)

OLD:
```
The values S7=1.748452 and S7'=0.41364 are the paper-quoted spectral constants
from the TUFT paper (Nielsen 2026), verified by the audit:
ζ'_Δ₂(0) = -0.41364
```

NEW:
```
The values S7=1.748452 and S7'=0.41364 are the paper-quoted spectral constants
from the TUFT paper (Nielsen 2026), now identified (erratum E3, resolved):
  S7  = +(1/2) ζ'(0) of coexact 3-forms on S^7 = 1.74845220445
  S7' = -      ζ'(0) of coexact 2-forms on S^9 = 0.41364465819
(The earlier "ζ'_Δ2(0) on S^7" assignment was incorrect: that determinant is
-0.61982401 and matches nothing in the program.)
```

## `t3_beltrami_final.py` — verification print (line 30)

OLD:
```
print(f"  ζ'_Δ₂(0) = -0.41364 (matches S7' = {nstr(S7p, 6)})")
```

NEW:
```
print(f"  -ζ'_coexact-2form(S9)(0) = 0.41364465819 (matches S7' = {nstr(S7p, 6)})")
print(f"  (1/2)ζ'_coexact-3form(S7)(0) = 1.74845220445 (matches S7 = {nstr(S7, 6)})")
```

## `t3_beltrami_final.py` — closing summary (lines 69, 77)

Replace both "Verified by audit: ζ'_Δ₂(0) = -0.41364 → S7' = 0.41364 ✓" /
"Audit: ζ'_Δ₂(0) = -0.41364 ✓" lines with:
```
Identified (E3): S7 = (1/2)ζ'_coex3(S7)(0), S7' = -ζ'_coex2(S9)(0) ✓
```

## Markdown files

In `CRITICAL_ASSESSMENT.md` and `LITERATURE_SEARCH_T1_T3.md`, wherever
"ζ′_Δ₂(0)" appears as the source of S7′, append:
"(superseded by erratum E3: S7′ = −ζ′(0) of coexact 2-forms on S⁹ =
0.41364465819; ζ′_Δ₂(0) on S⁷ = −0.61982401 is a different operator on a
different sphere)".

**Independent confirmation behind this patch:**
`mqgt_t3_independent.py` + `mqgt_t3_reverse_search.py` (verification repo);
numerics note: sphere-zeta computations that subtract a finite head from
ζ_R(w) are catastrophically unstable for w ≳ dps/0.301 — the reverse-search
script documents and fixes this (hybrid direct-sum Hurwitz for w > 40).
