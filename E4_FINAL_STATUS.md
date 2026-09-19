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

## Correction (2026-09-18, ChatGPT round 11 — verified, applied)

The round-2 table above labeled its bundles "coexact" but computed the
**full Λ^p bundle** (dim C(n,p)). The coexact tower's heat trace follows
by the alternating sum of full-form traces (exact p-forms are isospectral
to coexact (p−1)-forms; the scalar-zero-mode constant does not touch a₄).
Corrected coexact certificates (exact integer arithmetic, reproduced by
the correction block in `mqgt_t1_e4_a4_heat.py`):

| Tower | leading multiplicity | coexact a₄(u) = K(A + Bu + Cu²) |
|---|---|---|
| S⁷, coexact 3-forms | 20 (full Λ³: 35) | A = 94080, B = −40320, C = 3600 |
| S⁹, coexact 2-forms | 28 (full Λ²: 36) | A = −24192, B = −34560, C = 5040 |

**The no-go result is unchanged:** coexact a₄(u) remains degree-2 in the
shift (an alternating sum of quadratics), so a₄'''(0) ≡ a₄''''(0) ≡ 0 on
the coexact towers too. What changed is the numerical certificate, not
the exclusion.

Also on record from the same review: (i) shift-convention harmonization —
this script shifts the endomorphism by +u (eigenvalues −u); the
determinant script shifts eigenvalues by +u; u_heat = −u_det; (ii)
higher heat coefficients as a *limited* negative result — for
D_u = D₀ + u, A_{2k}(u) = Σ_j (−u)^j/j! A_{2(k−j)}(0), so
∂_u³A₆|₀ = −A₀ and ∂_u⁴A₈|₀ = +A₀ are nonzero but reduce to the leading
coefficient (volume × principal-symbol multiplicity); they do not derive
c₃ or the T-3 normalizations; (iii) CODATA anchor — this file's
137.035999178 is an internal rounding of NIST 137.035999177(21);
re-anchor queued in `LEDGER.md` §5 (manuscript v1.2+ pins …177 with both
pin sets footnoted).

## Bottom line

**The T-1 identity α⁻¹ = 137.03608245 is a 7-digit approximation** (relative
gap 6.0765×10⁻⁷ to CODATA 2022) with no known structural completion inside the
program's current operator content. E4 remains the program's principal open
theoretical problem; any future closure must introduce an invariant that is
not yet in the theory. The pinned target for any such attempt stands:
**c₃ = −1.56371823031276** on the α³ basis, produced from operator content,
factors identifiable before comparison to CODATA.
