# EXCLUSION — Door 1: Twisted (Hopf-charge-resolved) towers — CLOSED

**Date:** 2026-09-18 · **Label:** CLOSED (exclusion, not a positive formula)
**Reproduce:** `python3 ../play_notes/play_twisted_towers_lab.py`
(output: `../play_notes/play_twisted_towers_lab_out.txt`)

## Declared principle (pre-computation)

Twisted towers are the geometry's native missing content — Hopf-line-valued
forms on the actual bundle S¹ → S^{2m+1} → CP^m. Compute the charged
coexact spectra for the S⁷-3 and S⁹-2 α towers; any structural shift that
produces c₃ closes the residual without dials.

## Machinery (new, certified)

- SO(2n) Weyl character formula at the diagonal Hopf specialization via
  the confluent-determinant limit; integer charge multiplicities d_q.
- **D-type chirality subtlety discovered in controls:** for λ_n ≠ 0 the
  +det ratio returns the O(2n) average (ch₊ + ch₋)/2 (raw q = ±4
  coefficient exactly 0.5 on [1,1,1,1]); the physical middle-form tower
  carries both chiralities ⇒ ×2. Certified by C1 at every level.
- **Pole regularization for odd-power sector polynomials** (record towers
  are even-only): ζ(0) gains c·a2^j/(2j), ζ′(0) gains
  (c·a2^j/j)(H_{j−1}/2 − ψ(x0)) at 2j − m = 1. Certified against an
  independent Laurent extraction at s = ±10⁻³ (~1e-10, four sectors).

## Controls

C1 charge sums = deg_coexact/deg_scalar at every level, both towers,
k = 0..16 (exact integers). C2/C3 palindrome, nonneg, clean margins.
C4 scalar sectors = SU(m+1) Weyl closed form. C5 spectral certificate
above. A truncated sector-SUM control is void (pole terms cancel only
across all sectors; verified numerically) — not used, not claimed.

## Verdict — CLOSED, negative, structural

The Hopf U(1) acts by **isometry**: charge resolution splits only
degeneracies, never eigenvalues. Every zeta invariant of the twisted
tower sums back over sectors to the identical untwisted value (exact,
certified identity). **c₃ is structurally absent from the charge split.**
Truncated moment probes were tail-dominated and indicative only by design
(σ_M2 = +1.374; never graded).

Charge-resolved spectra exist as exact tables (archived in the output
file) — kept as uniqueness raw material regardless of the verdict.

## Reproduce (one command)

```
python3 play_notes/play_twisted_towers_lab.py
```

Expected: every charge-resolved level sum matches its untwisted target
(archived reference output: `play_notes/play_twisted_towers_lab_out.txt`);
final verdict line: charge-resolved zetas sum exactly to the untwisted
value — c3 structurally absent. Play-side lab promoted to exclusion
with this certificate; run time ~minutes, mpmath dps as set in-file.
