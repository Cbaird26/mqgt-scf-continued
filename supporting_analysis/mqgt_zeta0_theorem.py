#!/usr/bin/env python3
"""ZETA(0) THEOREM CERTIFICATE — exact rational arithmetic.

RECORD-SIDE. Certifies as middle-tower-family extensions (ordered 2026-09-18):

  THEOREM (coexact zeta(0) pattern): for the coexact p-form tower on S^n
  (n odd), p = 0..n-1, in the det' convention (zero modes excluded),
      zeta_{ce_p}(0) = (-1)^{p+1}.
  Isospectrality-consistent: ce_p ~= ce_{n-1-p} and (-1)^{p+1} = (-1)^{n-p+1}
  for n odd, so the pattern extends over the full p range.

  COMPANION (scalar zero-mode sensitivity): the scalar tower INCLUDING the
  formal m = (n-1)/2 position (the constant mode; convention A of the play
  labs) has zeta(0) = 0; excluding it (det', convention B = ce0) gives -1.
  So the scalar sector's dilaton response in lab 5 was entirely a
  zero-mode-convention artifact — flagged for the play scorecard recheck.

PROOF SKELETON (general, stated; certified exactly over the grid below):
  zeta(0) = sum_i c_i zetaR(-i, x0)  with d(m) = sum c_i m^i the degeneracy
  polynomial in m = k + x0. Trivial zeros kill i >= 4 even; zeta(0) = -1/2:
      zeta(0) = -c_0/2 - sum_{q=1}^{x0-1} d(q).          (*)
  For middle towers, d(q) = 0 (q <= r) and c_0 = -2(-1)^x0, giving
  (-1)^x0 — the earlier lemma. For general p, (*) reduces the theorem to
  exact polynomial identities in the Weyl dimension formula, verified here
  coefficient-wise in fractions.Fraction over the full grid:
      n = 3..21 odd, all p = 0..(n-1)/2  (55 coexact towers),
  plus scalar towers under both conventions, plus dps=80 cross-checks
  against the zeta machinery.

CONVENTION DISCOVERY (recorded 2026-09-18): the play labs' p=0 rows used
convention A (formal inclusion of the constant mode: L = 4.1693 / 3.8496);
the t3 reverse-search spec and det' physics use convention B
(L = -0.20092 / 0.054738). The play scorecard's sigma values are
convention-A numbers; baseline rebuilt under B below as the first recheck.
"""

from fractions import Fraction
from mpmath import mp, mpf, nstr

mp.dps = 80

from mqgt_middle_tower_d1_proof import (
    weyl_dr_exact, deg_coexact_exact, interp_poly_exact)
from mqgt_t1_e4_derivation import build, logdet, dkdu
from mqgt_t3_reverse_search import deg_scalar, fit_poly, z0


def deg_scalar_exact(n, k):
    r = (n + 1) // 2
    return weyl_dr_exact([k] + [0] * (r - 1), r)


def poly_ce_exact(n, p):
    """Degeneracy poly in m = k + x0, x0 = (n+1)/2, exact rationals."""
    x0 = (n + 1) // 2
    ks = list(range(n + 2))
    ys = [deg_coexact_exact(n, p, k) for k in ks]
    cs = interp_poly_exact([k + x0 for k in ks], ys, n - 1)
    return {i: c for i, c in enumerate(cs) if c != 0}, x0


def poly_scalar_exact(n):
    a = (n - 1) // 2
    ks = list(range(n + 2))
    ys = [deg_scalar_exact(n, k) for k in ks]
    cs = interp_poly_exact([k + a for k in ks], ys, n - 1)
    return {i: c for i, c in enumerate(cs) if c != 0}, a


def zeta0_exact(poly, x0):
    """Formula (*): -c_0/2 - sum_{q=1}^{x0-1} d(q)."""
    c0 = poly.get(0, Fraction(0))
    s = sum(sum(c * Fraction(q) ** i for i, c in poly.items())
            for q in range(1, x0))
    return -c0 / 2 - s


def main():
    print("=" * 78)
    print("ZETA(0) THEOREM CERTIFICATE (exact rational arithmetic)")
    print("=" * 78)

    # ---- Claim A: coexact towers ----
    print("\n[A] coexact ce_p on S^n (det'), n = 3..21 odd, all p:")
    bad = []
    count = 0
    for n in range(3, 22, 2):
        row = []
        for p in range(0, (n + 1) // 2):
            if p == 0:
                poly, a = poly_scalar_exact(n)   # ce0 == scalar det'
                x0 = a + 1
            else:
                poly, x0 = poly_ce_exact(n, p)
            z = zeta0_exact(poly, x0)
            want = Fraction((-1) ** (p + 1))
            ok = z == want
            count += 1
            if not ok:
                bad.append((n, p, z))
            row.append(f"p{p}:{z}")
        print(f"  S^{n:2d}: " + "  ".join(row))
    print(f"  [{count} towers, all == (-1)^(p+1): {'ALL OK' if not bad else f'FAILURES: {bad}'}]")

    # ---- Claim B: scalar conventions ----
    print("\n[B] scalar tower, both zero-mode conventions:")
    for n in range(3, 22, 2):
        poly, a = poly_scalar_exact(n)
        zA = zeta0_exact(poly, a)       # include formal m = a position
        zB = zeta0_exact(poly, a + 1)   # det' (exclude constant mode)
        print(f"  S^{n:2d}:  A (incl. const) zeta(0) = {zA}    "
              f"B (det') zeta(0) = {zB}   {'OK' if zA == 0 and zB == -1 else 'CHECK'}")

    # ---- dps=80 cross-check against machinery ----
    print("\n[cross-check] dps=80 z0() machinery vs exact formula:")
    worst = mpf(0)
    for n in range(3, 16, 2):
        for p in range(0, (n + 1) // 2):
            poly, a2, x0 = build(n, p)
            zm = z0(poly, x0)
            ze = Fraction((-1) ** (p + 1))
            worst = max(worst, abs(zm - mpf(int(ze))))
    print(f"  worst |machinery - exact| over n<=15 grid: {nstr(worst, 3)}")

    # ---- convention flag: play baseline rebuilt under B ----
    print("\n[convention flag] play-scorecard baseline sigma under convention B")
    print("  (p>=1 coexact towers unchanged; only the p=0 scalar rows move):")
    T = {}
    for s, n, pmax in (("S7", 7, 3), ("S9", 9, 4)):
        for p in range(0, pmax + 1):
            poly, a2, x0 = build(n, p)   # build(n,0) == ce0 == scalar det'
            T[(s, p)] = (logdet(poly, a2, x0), dkdu(poly, a2, x0, 1))
            if p == 0:
                print(f"    {s} scal det':  L = {nstr(T[(s,0)][0], 12)}"
                      f"   D1 = {nstr(T[(s,0)][1], 12)}"
                      f"  (convention A was L=4.169/3.850, D1=-43.9/-24.6)")
    sigA = mpf("-8.467418722")
    sigB = sum(v[1] for v in T.values()) / sum(v[0] for v in T.values())
    print(f"    uniform baseline:  A = {nstr(sigA, 8)}   B = {nstr(sigB, 8)}")
    print("    -> play scorecard numbers are convention-A; a full B-rebuild")
    print("       of labs 1-5 is an OPEN recheck item (notes updated).")


if __name__ == "__main__":
    main()
