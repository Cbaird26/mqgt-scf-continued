# Theorem — Closed forms for the middle-tower L family (ζ′(0))

**Status: record-side. Certified two independent ways at dps = 80 for
r = 1…8 (S³…S¹⁷), residuals at the precision floor (0 … 3.1e-56, decaying
exactly as the adaptive tail truncation predicts).** Files:
`mqgt_middle_tower_L_closed.py` (certificate), builds on
`MIDDLE_TOWER_D1_LEMMA.md` (factorization mechanism).

## Statement

For the self-paired middle coexact tower on S^{2r+1} (spectrum m²,
m ≥ x0 = r+1; degeneracy d(m) = (2/(r!)²)∏_{j=1..r}(m²−j²)):

> **L(r) ≡ ζ′_mid(0) = (−1)^{x0} · 2 [ ln(2π) − Σ_{k=1}^{r}
> e_{r−k}(1,4,…,r²) · (2k)! · ζ(2k+1) / ( (r!)² (2π)^{2k} ) ]**

with e_j the elementary symmetric polynomials of the first r squares.

Also exact, same mechanism: **ζ_mid(0) = (−1)^{x0}** (the alternating integer
observed in the mirror check), and D1 = (−1)^{x0}(π²/3 + H₂(x0−1)) (previous
lemma). The middle tower's elementary spectral data are now all closed form.

## Derivation (one paragraph)

L = 2 Σ_i c_i ζR′(−i, x0). Split ζR′(−i, x0) = ζ′(−i) + Σ_{q<x0} qⁱ ln q;
the head term is 2 Σ_{q=1}^{r} d(q) ln q ≡ 0 because the factorization makes
d vanish at every integer below the spectrum start. Remaining: ζ′(0) =
−½ ln 2π on c₀ = 2(−1)^r, and the functional equation ζ′(−2k) =
(−1)^k (2k)! ζ(2k+1)/(2(2π)^{2k}) on c_{2k} = (2/(r!)²)(−1)^{r−k} e_{r−k}.
The signs collapse to a single (−1)^{x0} outside. ∎ (modulo the same single
general-r product identity flagged in the D1 lemma.)

## Explicit forms (all machine-checked)

| tower | L |
|---|---|
| S³ ce1 | 2 ln(2π) − ζ(3)/π² |
| S⁵ ce2 | −2 ln(2π) + 5ζ(3)/(4π²) + 3ζ(5)/(4π⁴) |
| S⁷ ce3 | 2 ln(2π) − 49ζ(3)/(36π²) − 7ζ(5)/(6π⁴) − 5ζ(7)/(8π⁶) |

## Consequences

- **The near-mirror is fully explained.** Adjacent middle towers share the
  2 ln(2π) anchor with opposite sign (−1)^{x0}; the ζ-odd sums are small and
  slowly growing corrections. The S⁷/S⁹ residual 0.010960167 is exactly the
  difference of two closed forms — nothing anomalous.
- **Convergence:** L(r) → the series converges in magnitude (ζ(2k+1)→1,
  (2π)^{2k} dominates (2k)!·e/(r!)²); observed 3.55396 → 3.46689 decreasing.
  The limiting constant is a defined infinite sum of ζ-odds; whether it has a
  simpler closed form is open and not needed.
- **E4 exclusion record strengthened again:** the middle towers' L values
  are now closed forms in {ln 2π, ζ(3), ζ(5), …}; c₃ = −1.56371823031276 is
  visibly not of this family. Middle towers: solved and excluded, completely.

## Certificate output (2026-09-18)

| tower | machinery logdet | closed form | residual | ζ(0) |
|---|---|---|---|---|
| S³ ce1 | 3.553960304585117884 | same | 0.0 | +1 OK |
| S⁵ ce2 | −3.515528036076455988939 | same | 4.2e-81 | −1 OK |
| S⁷ ce3 | 3.496904408895519084275 | same | 8.2e-74 | +1 OK |
| S⁹ ce4 | −3.485944242193018072404 | same | 4.8e-70 | −1 OK |
| S¹¹ ce5 | 3.478731996168867835015 | same | 2.5e-66 | +1 OK |
| S¹³ ce6 | −3.473628291688450286798 | same | 1.5e-62 | −1 OK |
| S¹⁵ ce7 | 3.469827292106493072421 | same | 7.2e-61 | +1 OK |
| S¹⁷ ce8 | −3.466887074080992455992 | same | 3.1e-56 | −1 OK |
