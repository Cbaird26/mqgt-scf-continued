# E4 Derivation Attempt — Heat-Kernel / Index Route (Round 1)

**Date:** 2026-09-18 · **Status:** E4 **remains open** — with a sharper map.
**Reproduce:** `python3 mqgt_t1_e4_derivation.py` (80-digit; exact analytic
derivative series, no finite differences, no candidate search)
**Builds on:** `mqgt_t1_e4_structure.py` (pinned target), the frozen E4 scan,
and the E3-resolved identifications.

## What was attempted

The corpus itself nominates the derivation object
(`t3_beltrami_final.py`: "S7 ∝ a₄'''(0)", E-coupling η = 0.5). We took the two
E3-resolved towers — coexact 3-forms on S⁷ (a² = 0) and coexact 2-forms on S⁹
(a² = 4) — and computed the **exact u-derivatives** of their spectral
determinants under the endomorphism shift λ → λ + u (u = ηE), using the
analytic series d^k/du^k ζ′(0) = (−1)^k Σ_m c_m Σ_{j≥k} (j−1)!/(j−k)! ·
a²^{j−k} ζ_R(2j−m). Controls passed: ½ζ′(0)|S⁷,ce3 = 1.74845220444776 (matches
S7 to 14 digits), −ζ′(0)|S⁹,ce2 = 0.413644658189679 (matches S7′), and the
ζ(0) values come out integers (+1, −1) as required.

## Results by mechanism (all pre-declared)

| Mechanism | Verdict |
|---|---|
| **M1** — correction already inside the universal phase (existing coefficients ζ(3)·13/24π, ζ(5)/4π², S7/56, S7′/16 vs needed X = 1.5637187) | **Excluded** — all off by ≥ 87%. |
| **M2** — corpus derivation path: published normalizations 1/56, 1/16 vs the determinants' shift-derivatives (S7·56 = 97.91 vs D₃ = 0.791; S7′·16 = 6.62 vs D₄ = −0.0588) | **Not reproduced in this realization.** Caveat: D_k are log-determinant derivatives, not the heat coefficient a₄(E) itself; the a₄(E) claim proper remains untested and is the named next computation. |
| **M3** — is c₃ = −1.56371823031276 *any single invariant* of the existing operator content (2 determinants + 8 derivatives, all pre-declared)? | **No.** Closest candidate is off by 96%; nothing within light-years of the 10⁻⁸ gate. |

## What this establishes

1. The E4 correction is **not a recombination of the program's existing
   spectral invariants**. Any closure requires a genuinely new invariant.
2. The corpus's nominated object — the heat coefficient **a₄(E) of the
   Beltrami operator with E-coupling** — is now the *only* standing candidate
   path, and it is computable with the machinery already in this repo (the
   degeneracy polynomials and stabilized Hurwitz evaluation are in
   `mqgt_t3_reverse_search.py`; the Gilkey a₄ integrand is quoted in
   `t3_beltrami_final.py`).
3. The pinned target from round 1 stands: c₃ = −1.56371823031276, produced
   from operator content, with every factor identifiable before comparison to
   CODATA.

## Next computation (named, not promised)

Compute a₄(E) for the Beltrami operator B = ⋆d on S⁷ with endomorphism
E_p → E_p + ηE directly from the Gilkey integrand, extract a₄'''(0) and
a₄''''(0), and check (a) whether they reproduce S7 and S7′ under *some*
pre-declared normalization — which would finally derive T-3 from first
principles — and (b) whether the same coefficient structure yields
c₃ = −1.56371823031276. Both outcomes are informative: success closes E4;
failure excludes the last nominated object and the honest report becomes
"the T-1 identity is a 7-digit approximation with no known structural
completion."
