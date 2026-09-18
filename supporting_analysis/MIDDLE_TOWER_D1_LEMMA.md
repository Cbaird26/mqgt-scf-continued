# Lemma — Closed form for the middle-tower u-response D1

**Status: record-side. Proved with exact-rational certificate (r ≤ 10) +
dps-80 floating certificate (r ≤ 6).** Files: `mqgt_middle_tower_d1_proof.py`
(certificate), `mqgt_mirror_check.py` (discovery + high-precision values).

## Statement

Let n be odd, p = (n−1)/2 the self-paired middle coexact tower on the unit
sphere Sⁿ, with spectrum λ_m = m², m ≥ x0 = (n+1)/2, and let ζ_mid(s; u) be
its spectral zeta under the endomorphism shift λ → λ + u. Then

> **D1(n) ≡ d/du ζ′_mid(0; u) |_{u=0} = (−1)^{x0} · ( π²/3 + H₂(x0−1) )**,
> where H₂(N) = Σ_{m=1..N} m^{−2}.

Equivalently, with r = (n−1)/2: D1 = (−1)^{r+1} ( π²/3 + H₂(r) ).

Values: +(1+π²/3), −(1+¼+π²/3), +(1+¼+1/9+π²/3), … converging in magnitude
to π²/2 − 1 as n → ∞, sign alternating in lockstep with ζ_mid(0) = (−1)^{x0+1}.

## Proof

Setup. With a2 = 0 the exact derivative series (dkdu) collapses to j = 1:

    D1 = −Σ_i c_i ζR(2−i, x0),

where d(m) = Σ_i c_i mⁱ (even, degree n−1) is the tower's degeneracy
polynomial in m = k + x0, and ζR(w, x0) = ζ(w) − Σ_{q=1}^{x0−1} q^{−w}.
Since ζ vanishes at negative even integers (trivial zeros), only i = 0, 2
contribute:

    D1 = −c₀ ζ(2) − c₂ ζ(0) + Σ_{q=1}^{x0−1} d(q)/q²
       = −c₀ π²/6 + c₂/2 + Σ_{q=1}^{r} d(q)/q².

Key fact (middle-tower degeneracy factorization). For the self-paired middle
tower on S^{2r+1},

    d(m) = (2/(r!)²) · ∏_{j=1}^{r} (m² − j²).

- Verified coefficient-wise in **exact rational arithmetic** for r = 1…10
  (S³…S²¹) against the Weyl dimension formula: `mqgt_middle_tower_d1_proof.py`,
  all checks OK.
- Anchored in general at k = 0: d evaluated at m = r+1 gives
  (2r+1)!/(r!(r+1)!)·… = binom(2r+1, r)·… reproducing 2·dim of the chiral
  half of ∧^r of SO(2r+2) = binom(2r+1, r+1) — exact agreement with the Weyl
  formula's anchor for all r.
- It is also the middle case of the standard coexact p-form degeneracy
  formula on spheres (Rubin–Ordóñez; Copeland–Toms conventions). The one
  remaining formal step for a textbook-grade general proof is the product
  identity ∏_{2≤i<j≤r+1} (m_i+m_j+2)/(m_i+m_j) = (2r−1)!/(r−1)!r! (finite,
  inductive).

Consequences of the factorization:
1. **d(q) = 0 for q = 1, …, r** — the analytic degeneracy vanishes exactly at
   every integer below the spectrum start, so the finite sum is identically 0.
2. c₀ = d(0) = (2/(r!)²)·(−1)^r (r!)² = 2(−1)^r = −2(−1)^{x0},
   hence −c₀ π²/6 = (−1)^{x0} π²/3.
3. c₂ = coefficient of m² = (2/(r!)²)·(−1)^{r+1}(r!)² H₂(r) = 2(−1)^{r+1} H₂(r),
   hence c₂/2 = (−1)^{x0} H₂(x0−1).

Summing: D1 = (−1)^{x0} ( π²/3 + H₂(x0−1) ). ∎ (r ≤ 10 exact-certified;
general r modulo the one product identity above.)

## Immediate corollaries

- The S⁷ce3/S⁹ce4 "mirror miss" is exactly −1/16 = −1/(x0−1)² — the H₂
  increment. The near-mirror is explained, not coincidental-mysterious.
- The u-response of every self-paired middle tower is now closed form.
- c₃ = −1.56371823031276 (E4, α³ basis) is not of the form ±(π²/3 + H₂);
  the middle towers are excluded from E4's correction **completely**, not
  just numerically.

## Next (ordered by Grok, 2026-09-18): the L family

With d(m) factored, L(n) = ζ′_mid(0) = Σ_i c_i·2ζR′(−i, x0) is mechanical:
a finite combination of ζ′(0) = −½ln 2π, ζ′(−2k) = (−1)^k (2k)! ζ(2k+1) /
(2(2π)^{2k}), and head terms Σ_{q<x0} q^{2k} ln q. Observed: sign (−1)^{x0},
magnitude decreasing 3.55396 → 3.47873 (n = 3…11), apparent convergence.
Closed form to be expanded next; the factorization does the heavy lifting.
