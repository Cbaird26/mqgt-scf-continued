# E4 — Final Status After the a₄(E) Computation (Round 2)

**Date:** 2026-09-18 · **Status:** E4 **open, exclusion record complete**
**Reproduce:** `python3 mqgt_t1_e4_a4_heat.py` (exact integer/Fraction
arithmetic for all traces; controls: tr Ω²(Λ¹, S⁷) = −84, tr Ω²(Λ¹, S⁹) = −144,
both matching −2n(n−1); the Λ³/S⁷ and Λ²/S⁹ values −840 and −1008 match the
general formula −2·C(n,p)·p(n−p))

## The round-2 result

For Laplace-type operators — which include the Hodge/Beltrami sector with the
corpus's constant endomorphism shift E_p → E_p + ηE — the Gilkey heat
coefficient a₄ is a **polynomial of degree 2 in the shift**: the only
E-dependent terms in the integrand are 60 R E and 180 E². Computed exactly:

| Tower | dim Λ^p | E₀ | tr Ω² | a₄(u) = K(A + Bu + Cu²) |
|---|---|---|---|---|
| S⁷, coexact 3-forms | 35 | −12 | −840 | A = 120540, B = −63000, C = 6300 |
| S⁹, coexact 2-forms | 36 | −14 | −1008 | A = −35424, B = −25920, C = 6480 |

Therefore **a₄'''(0) = a₄''''(0) ≡ 0**, independent of bundle rank, curvature,
or η. The corpus's derivation path "S7 ∝ a₄'''(0), S7′ ∝ a₄''''(0)" is
*vacuous as stated* — zero is the only value those derivatives can take.

S7 and S7′ remain real spectral invariants — E3 confirmed them to 14 digits as
the half-determinants of the coexact towers — but their home is the spectral
determinant ζ′(0; u), which *is* non-polynomial in u. Its derivatives were
computed in round 1 (D₃ = 0.79106541282995, D₄ = 0.065144669668101 on S⁷) and
match neither the published 1/56, 1/16 normalizations nor c₃.

## Complete E4 exclusion record

| Route | Object | Result |
|---|---|---|
| Fits | 13,057-expression pre-declared topological family (frozen scan) | 58 gate-passing coincidences → uncertifiable |
| Physics | QED running from a bare α | Excluded: needs q/m_e = 1.00039, no such threshold |
| Existing invariants | Phase coefficients, determinants, 8 exact u-derivatives (M1–M3) | Nothing within 96% of c₃ |
| Heat kernel | a₄(E), corpus's own nominated object | a₄'''(0) ≡ a₄''''(0) ≡ 0 — vacuous |

## Bottom line

**The T-1 identity α⁻¹ = 137.03608245 is a 7-digit approximation** (relative
gap 6.0765×10⁻⁷ to CODATA 2022) with no known structural completion inside the
program's current operator content. E4 remains the program's principal open
theoretical problem; any future closure must introduce an invariant that is
not yet in the theory. The pinned target for any such attempt stands:
**c₃ = −1.56371823031276** on the α³ basis, produced from operator content,
factors identifiable before comparison to CODATA.
