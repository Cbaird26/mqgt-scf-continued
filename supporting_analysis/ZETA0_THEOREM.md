# Theorem — ζ(0) pattern across all coexact towers (family extension)

**Status: record-side. Certified in exact rational arithmetic over the full
grid n = 3…21 odd, every p (65 towers), cross-checked against the zeta
machinery at dps = 80 (worst deviation 1.07e-60).** File:
`mqgt_zeta0_theorem.py`. Extends `MIDDLE_TOWER_D1_LEMMA.md` /
`MIDDLE_TOWER_L_THEOREM.md` (2026-09-18).

## Statement

For the coexact p-form tower on Sⁿ (n odd), zero modes excluded (det′):

> **ζ_ce_p(0) = (−1)^{p+1}**, for all p = 0, …, n−1.

Isospectrality-consistent: ce_p ≃ ce_{n−1−p} (B = ⋆d intertwines the
Laplacians) and for n odd, (−1)^{p+1} = (−1)^{n−p+1}, so the pattern extends
over the full range without contradiction.

Companion (zero-mode sensitivity of the scalar tower):
- scalar tower **including** the formal constant-mode position m = (n−1)/2
  (play-lab convention A): ζ(0) = 0 exactly;
- scalar **det′** (constant mode excluded; = ce0, convention B):
  ζ(0) = −1 = (−1)^{0+1} — fitting the family pattern.

## Proof skeleton (general mechanism, certified over the grid)

For any of these towers, with degeneracy polynomial d(m) = Σ c_i mⁱ in
m = k + x0:

    ζ(0) = Σ_i c_i ζR(−i, x0)
         = −c₀/2 − Σ_{q=1}^{x0−1} d(q)                          (*)

(trivial zeros kill all even i ≥ 4; ζ(0) = −1/2 handles i = 0; the head sums
reassemble into values of d). Formula (*) reduces the theorem to exact
polynomial identities in the Weyl dimension formula — verified
coefficient-wise in fractions.Fraction for the whole grid. Middle towers
recover the earlier lemma (d(q) = 0 for q ≤ r, c₀ = −2(−1)^{x0} ⇒
ζ(0) = (−1)^{x0}). A textbook-grade general-r proof needs the same single
Weyl product identity flagged in the D1 lemma.

## Convention discovery (affects the play scorecard — flagged, not silent)

The play labs' p=0 rows used **convention A** (formal inclusion of the
constant mode): L = 4.169289794 / 3.849578692, D1 = −43.925 / −24.598.
The det′ physics convention (**B**, also the t3-reverse-search spec) gives
L = −0.200915319509 / 0.0547377225888, D1 = +0.408333 / +0.339732.

Consequences:
- Lab 5's "scalars don't respond to a dilaton (ζ(0) = 0)" was a
  **zero-mode-convention artifact**: under det′, scalars have ζ(0) = −1 and
  DO respond. σ_dil should be recomputed under B — open recheck item.
- Uniform-baseline σ: convention A = −8.4674, convention B = **−12.677**.
  All play scorecard numbers (C1–C4, parity projections, GKSL, dilaton) are
  convention-A values; a full B-rebuild of labs 1–5 is queued.
- σ_need = −6.21 is convention-independent (it is rel-gap/u₀), so the gate
  itself stands; the computed σ's need the rebuild.

## Certificate output (abridged)

- Claim A: 65/65 towers, ζ(0) = (−1)^{p+1}, exact. S³: {p0:−1, p1:+1} …
  S²¹: {p0:−1 … p10:−1}.
- Claim B: S³…S²¹, A→0 / B→−1, all exact.
- dps=80 machinery cross-check: worst |Δ| = 1.07e-60 over n ≤ 15 grid.
