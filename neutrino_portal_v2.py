#!/usr/bin/env python3
"""
neutrino_portal_v2.py — E2 repair applied.

MQGT-SCF neutrino portal with the 3-Yukawa texture, replacing the v1
single-Yukawa spectrum (which was degenerate and contradicted oscillation
data). Two closures are implemented; Variant A is the default (conservative
repair: no printed number changes, only the texture is added).

Inputs (oscillation anchors, NuFIT-scale values used in the errata):
    dm21 = 7.42e-5 eV^2      (solar)
    dm31 = 2.517e-3 eV^2     (atmospheric, normal ordering)
Portal:  m_i = 0.01976 * r_i eV,  r_i = y_nu,i / y_nu,  <E> = 0.1 eV.

Closures:
  A (sum rule preserved):  m1 + m2 + m3 = 59.28 meV fixed,
     solve m1 from  m1 + sqrt(m1^2+dm21) + sqrt(m1^2+dm31) = 59.28 meV.
  B (naturalness capped):  span m3/m1 = S (default 5.8),
     m1 = sqrt(dm31 / (S^2 - 1)); the sum floats to ~0.0720 eV.

Reference values (errata E2, v2 table):
  A: (m1,m2,m3) = (0.481, 8.627, 50.172) meV, span 104x, sum 0.05928 eV
  B: (8.781, 12.301, 50.932) meV, span 5.8x, sum 0.0720 eV
"""
import sys
from math import sqrt

DM21 = 7.42e-5   # eV^2
DM31 = 2.517e-3  # eV^2
SUM_A = 0.05928  # eV (TUFT sum rule / minimal-NO floor)
E_VEV = 0.1      # eV, DETAE monitor switching scale
Y_NU = 0.1976    # v1 fitted Yukawa scale (kept as the texture normalization)


def spectrum_A(sum_ev=SUM_A):
    """Bisection on m1 with the sum rule fixed. Units: meV internally."""
    target = sum_ev * 1e3
    s21, s31 = DM21 * 1e6, DM31 * 1e6  # meV^2
    lo, hi = 1e-9, target / 3.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        f = mid + sqrt(mid * mid + s21) + sqrt(mid * mid + s31)
        if f < target:
            lo = mid
        else:
            hi = mid
    m1 = 0.5 * (lo + hi)
    return m1, sqrt(m1 * m1 + s21), sqrt(m1 * m1 + s31)


def spectrum_B(span=5.8):
    s21, s31 = DM21 * 1e6, DM31 * 1e6
    m1 = sqrt(s31 / (span * span - 1.0))
    return m1, sqrt(m1 * m1 + s21), span * m1


def report(name, m):
    m1, m2, m3 = m
    dm21 = (m2 * m2 - m1 * m1) * 1e-6
    dm31 = (m3 * m3 - m1 * m1) * 1e-6
    total = (m1 + m2 + m3) * 1e-3
    r = [mi / (Y_NU * E_VEV * 1e3) for mi in m]  # r_i = m_i / (y_nu <E>)
    print(f"--- Variant {name} ---")
    print(f"  (m1, m2, m3)      = ({m1:.3f}, {m2:.3f}, {m3:.3f}) meV")
    print(f"  dm21              = {dm21:.5e} eV^2   (target {DM21:.3e})")
    print(f"  dm31              = {dm31:.5e} eV^2   (target {DM31:.4e})")
    print(f"  sum m_nu          = {total:.5f} eV")
    print(f"  Yukawa ratios r_i = ({r[0]:.4f}, {r[1]:.4f}, {r[2]:.4f})")
    print(f"  span r3/r1        = {r[2]/r[0]:.1f}x")
    ok = abs(dm21 - DM21) < 1e-9 and abs(dm31 - DM31) < 1e-8
    print(f"  [{'PASS' if ok else 'FAIL'}] both splittings reproduced")
    return ok


if __name__ == "__main__":
    variant = sys.argv[1].upper() if len(sys.argv) > 1 else "A"
    ok = True
    if variant in ("A", "BOTH"):
        ok &= report("A (sum rule preserved)", spectrum_A())
    if variant in ("B", "BOTH"):
        ok &= report("B (naturalness capped)", spectrum_B())
    if variant not in ("A", "B", "BOTH"):
        print(__doc__)
        sys.exit(2)
    sys.exit(0 if ok else 1)
