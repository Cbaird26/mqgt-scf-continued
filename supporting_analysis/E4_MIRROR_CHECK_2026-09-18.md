# Middle-Tower Mirror Check + D1 Closed Form — 2026-09-18

**Record-side computation.** Script: `mqgt_mirror_check.py` (workspace root),
machinery: `mqgt_t1_e4_derivation.py` / `mqgt_t3_reverse_search.py`, dps = 80.
Request chain: play lab 4 flagged a near-mirror between the two self-paired
middle towers; Grok chose the exact zeta check; all new weightings were held
until this settled.

## 1. The mirror question — settled: NOT exact

| quantity | S⁷ ce3 | S⁹ ce4 | A + B | rel. residual |
|---|---|---|---|---|
| L = ζ′(0) | +3.496904408895519084275462 | −3.485944242193018072403855 | +0.010960167 | 3.1×10⁻³ |
| D1 = dL/du | +4.650979244807563984055941 | −4.713479244807563984055941 | −0.0625 | 1.3×10⁻² |

The play-table near-cancellation (0.3% / 1.3%) is **not** an exact identity.
Label: coincidence-class structural near-relation between adjacent square
towers (λ_m = m², m ≥ 4 vs m ≥ 5). **No weighting consequence; the hold on
new weightings is discharged with a negative result.**

## 2. What IS exact — a closed form for the entire middle-tower D1 family

The self-paired middle tower on Sⁿ (n odd), p = (n−1)/2, has a2 = 0, so its
u-derivative collapses to a finite combination of Hurwitz values. Numerically
certain at dps = 80 (residuals 1e-64 … 1e-81 = working-precision floor)
across S³, S⁵, S⁷, S⁹, S¹¹, S¹³:

    D1(n) ≡ d/du ζ′_{middle}(0) |_{u=0}  =  (−1)^{x0} · ( π²/3 + H₂(x0 − 1) )

with x0 = (n+1)/2 and H₂(N) = Σ_{m=1..N} 1/m².

| n | x0 | D1 (exact value) | closed form |
|---|---|---|---|
| 3 | 2 | +4.289868133696452872944830… | +(1 + π²/3) |
| 5 | 3 | −4.539868133696452872944830… | −(1 + ¼ + π²/3) |
| 7 | 4 | +4.650979244807563984055941… | +(1 + ¼ + 1/9 + π²/3) |
| 9 | 5 | −4.713479244807563984055941… | −(1 + ¼ + 1/9 + 1/16 + π²/3) |
| 11 | 6 | +4.753479244807563984055941… | +(… + 1/25 + π²/3) |
| 13 | 7 | −4.781257022585341761869867… | −(… + 1/36 + π²/3) |

Consequences, immediate:
- Sign alternation (−1)^{x0} is theorem-grade, not numerology.
- The D1 "mirror miss" between S⁷ and S⁹ is exactly **−1/16**
  (= −1/(x0−1)² step), fully explained by the closed form.
- As n → ∞, D1 → (−1)^{x0}·(π²/3 + π²/6 − 1) = ±(π²/2 − 1): the family is
  bounded and convergent in magnitude.

A proof should follow from the middle-tower Weyl degeneracy polynomials
(constant term c₀ = 2(−1)^{x0+1}, higher even coefficients rational) plus
ζR(2−m, x0) values; the identity is recorded here as numerically verified,
proof object open.

## 3. L pattern (observed, not yet closed form)

L(n) = ζ′(0) of the middle tower alternates with the same sign (−1)^{x0}:
+3.5539603, −3.5155280, +3.4969044, −3.4859442, +3.4787320 for
n = 3, 5, 7, 9, 11, magnitude strictly decreasing (apparent convergence).
Decomposition shows the alternation is driven by the degeneracy polynomial's
constant term c₀ = ±2 acting on ζR′(0, x0) = ln((x0−1)!) − ½ln 2π, while the
higher coefficients contribute large mutually-canceling terms (±10²–10³) —
which is *why* adjacent middle towers nearly mirror without doing so
exactly. Closed form in {ζ(3), ζ(5), …, ln q} exists in principle via
ζ′(−2k); not expanded tonight.

## 4. Bearing on E4 (honest)

The middle towers' u-response is now fully solved in closed form, and
c₃ = −1.56371823031276 is not of the form ±(π²/3 + H₂). This strengthens the
existing exclusion record: the E4 correction is not hidden in the middle
towers' first u-derivative. The α-gap remains where it was — combination
rule open, a4(E) path vacuous, no fitted coincidences admitted.
