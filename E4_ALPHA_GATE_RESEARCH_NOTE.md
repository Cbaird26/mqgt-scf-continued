# E4 Research Note — Anatomy of the α⁻¹ Gate Residual

**Date:** 2026-09-18 · **Erratum:** E4 (open) · **Frozen record:**
`mqgt-scf-independent-verification` v1.0-paper, §E4
**Reproduce:** `python3 mqgt_t1_e4_structure.py` (80-digit, no candidate search)

## The pinned target

| Quantity | Value |
|---|---|
| Theory α⁻¹ (T-1 identity) | 137.03608244816433744 |
| CODATA 2022 | 137.035999178(21) |
| Absolute gap | 8.327016434×10⁻⁵ |
| Relative gap | 6.07652×10⁻⁷ (gate 1×10⁻⁸: FAIL stands) |
| Needed correction δ−1 | −6.0765137801526242516×10⁻⁷ |
| **Coefficient on α³ basis** | **c₃ = −1.56371823031276** |
| Coefficient on α⁴ basis | c₄ = −214.285690123763 |

Any structural resolution of E4 must produce **c₃ = −1.56371823…** (or the
equivalent on another α-power basis) from the theory's own operator content,
with every factor identifiable *before* comparing to CODATA.

## What this run ruled out

1. **QED-style running.** If the identity yielded a bare α, bridging the gap
   by one-loop vacuum polarization requires ln(q²/m_e²) = 3π·gap = 7.85×10⁻⁴,
   i.e. q ≈ 1.00039·m_e — not a threshold; no physical scale sits there.
   (For scale: running q = 0 → m_Z moves α⁻¹ by ≈ 9.) The residual is not
   running at any natural scale.

2. **The known F3 coincidence, as an identity.** (1 − (π/2)α³) passes the gate
   (residual 2.8×10⁻⁹) but −π/2 = −1.5707963 differs from the needed
   c₃ = −1.5637182 by 4.5×10⁻³ relative — it is excluded outright, before any
   multiplicity argument.

3. **The coincidence class, illustrated.** c₄ = −214.285690 lies within
   1.1×10⁻⁷ of −1500/7; the correction (1 − (1500/7)α⁴) passes the gate with
   residual 6.85×10⁻¹⁴ — and −1500/7 has no derivation from the program. This
   is what one of the 58 pre-declared gate-passers looks like up close.
   **Gate-passing is necessary, not sufficient.**

## Resolution standard (unchanged, now quantified)

A closing derivation must produce the coefficient from a trace anomaly,
heat-kernel coefficient, or index density of the Hopf/Beltrami operator
content already in the theory — the same content that produced
ζ(3)·13/(24π) = 0.20725607285, ζ(5)/(4π²) = 0.0262656868757,
S7/56 = 0.0312223607937, S7′/16 = 0.0258527911369. Any combination of these
(or anything else) found by *fitting* remains coincidence-class per the frozen
13,057-expression scan.

## Status

**E4 remains open.** The target is pinned to 15 digits, the only physically
motivated non-fit hypothesis is excluded numerically, and the resolution
standard is explicit. The next honest step is a heat-kernel/index derivation
of the α³ coefficient from the T-3 operator content — a theory problem, not a
search problem.
