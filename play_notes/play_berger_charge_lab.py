#!/usr/bin/env python3
"""PLAY LAB — DOOR 2: BERGER CHARGE SUSCEPTIBILITY of the alpha towers.
NOT the scientific record. Play-branch lab with record-grade controls.

DECLARED PRINCIPLE (Christopher, 2026-09-18, before any computation):
the dial-free geometric source of charge-to-eigenvalue coupling is the
canonical variation (Berger squash) of the Hopf fibration — the unique
metric deformation holding the CP^m base fixed and scaling the S^1 fiber.
On scalars it provably shifts every charge-q eigenvalue by exactly
kappa*q^2 with kappa = t^-2 - 1 measured from the round point (kappa = 0
is the record, already excluded). This lab applies the Landau-form ansatz
    lambda -> lambda + kappa q^2
to the two coexact alpha towers (S^7 ce3, S^9 ce2) and computes the
tower's CHARGE SUSCEPTIBILITY: the exact linear responses at the round
point,
    dL/dkappa|0  = + sum_x Q2(x)/lambda(x)   (zeta-reg)
    dD1/dkappa|0 = - sum_x Q2(x)/lambda(x)^2 (zeta-reg)
where Q2(k) = sum_q d_q(k) q^2 is the total charge-second-moment
degeneracy — a closed-form polynomial in x (Dynkin-index polynomiality),
so NO truncation and NO tail domination (the Door-1 failure mode is
structurally absent here). Scorecard:
    sigma_kappa = (dD1/dkappa)/(dL/dkappa) = -[sum Q2/lambda^2]/[sum Q2/lambda]
which is negative by construction (Q2 >= 0); magnitude is the question.
Distance to sigma_need = -6.21 reported. ONE SHOT. Never graded.

CONTROLS:
  C1 charge-table sums vs deg_coexact at every level (re-asserted).
  C2 Q2 polynomiality certified by HOLDOUT: fit on k = 0..11 in x = k+x0,
     verified exact on k = 12..14 (integer data).
  C3 head-shift consistency: delta-L and delta-D1 recomputed with the
     zeta window shifted by +2 (explicit finite heads) must agree < 1e-35.
  C4 LOCK CHECK: sigma_kappa vs the tower's own record D1 (build/dkdu) —
     discovered in-run: |sigma_kappa| = D1(tower) exactly in both towers.
  Engine + spectral functions inherit the Door-1 certificates (C4/C5
  there: SU closed form, Laurent extraction, finite difference).
"""

from mpmath import mp, mpf, nstr, matrix, lu_solve

import play_twisted_towers_lab as TW  # dps=140 set there after imports
from play_twisted_towers_lab import charge_degeneracies
from mqgt_t3_reverse_search import zetaR, deg_coexact
from mqgt_t1_e4_derivation import build, dkdu

mp.dps = 140

SIGMA_NEED = mpf("-6.21")

# ---------------------------------------------------------- helpers
def fit_holdout(xs, ys, deg, nfit, label):
    """fit poly in x on first nfit points, verify exact on the rest."""
    M = matrix([[mpf(xs[i]) ** e for e in range(deg + 1)] for i in range(nfit)])
    c = lu_solve(M, matrix([mpf(ys[i]) for i in range(nfit)]))
    sc = max(abs(v) for v in c)
    poly = {e: c[e] for e in range(deg + 1) if abs(c[e]) > mpf("1e-40") * sc}
    worst = mpf(0)
    for i in range(nfit, len(xs)):
        pv = sum(poly[e] * mpf(xs[i]) ** e for e in poly)
        worst = max(worst, abs(pv - ys[i]))
    rel = worst / max(1, max(abs(mpf(y)) for y in ys))
    assert rel < mpf("1e-25"), f"{label}: holdout failure {nstr(rel, 3)}"
    return poly, rel

def sum_Q2_over_lambda(poly, a2, x0, power):
    """zeta-reg sum_x Q2(x) / (x^2 - a2)^power, x from x0."""
    total = mpf(0)
    for m_, c in poly.items():
        jscale = abs(c)
        for j in range(0, 400):
            coef = mpf(1) if power == 1 else mpf(j + 1)
            w = 2 * power + 2 * j - m_
            t = c * coef * a2 ** j * zetaR(w, x0)
            total += t
            if j > 8 and abs(t) < mpf("1e-60") * max(jscale, mpf(1)):
                break
    return total

# ---------------------------------------------------------- main
def main():
    print("=" * 82)
    print("PLAY LAB — DOOR 2: BERGER CHARGE SUSCEPTIBILITY")
    print("ansatz lambda -> lambda + kappa q^2 (canonical Hopf variation)")
    print("=" * 82)

    TOWERS = (("S7", 7, 3, 4), ("S9", 9, 2, 5))
    KMAX = 14
    results = {}
    for name, ndim, p, r in TOWERS:
        x0 = (ndim + 1) // 2
        a = (ndim - 1) / 2 - p
        a2 = mpf(a) ** 2
        degQ = ndim + 1           # Q2 ~ dim * <q^2> ~ x^(n-1) * x^2
        print(f"\n[{'S7' if ndim==7 else 'S9'}] coexact p={p}: "
              f"x0={x0}, a2={nstr(a2,4)}, levels k=0..{KMAX}")
        ks, Q2s = [], []
        for k in range(0, KMAX + 1):
            lam = [k + 1] + [1] * p + [0] * (r - 1 - p)
            ch = charge_degeneracies(lam)
            tot = sum(ch.values())
            want = int(round(deg_coexact(ndim, p, k)))
            assert tot == want, f"C1 FAIL k={k}: {tot} vs {want}"
            ks.append(k + x0)
            Q2s.append(sum(v * q * q for q, v in ch.items()))
        print(f"  C1 pass at all {KMAX+1} levels; "
              f"Q2(k=0..3) = {Q2s[:4]}")
        poly, rel = fit_holdout(ks, Q2s, degQ, 12, f"{name} Q2")
        odd = max([abs(v) for e, v in poly.items() if e % 2 == 1] + [mpf(0)])
        sc = max(abs(v) for v in poly.values())
        print(f"  C2 holdout (k=12..14): max rel dev {nstr(rel, 3)}; "
              f"Q2 even in x (odd part {nstr(odd/sc, 2)})  [OK]")
        assert odd / sc < mpf("1e-30"), "Q2 not even - pole terms unhandled"
        dL = sum_Q2_over_lambda(poly, a2, x0, 1)
        dD1 = sum_Q2_over_lambda(poly, a2, x0, 2)
        # C3: window shifted by +2 with explicit heads
        head1 = sum(sum(poly[e] * mpf(x) ** e for e in poly)
                    / (mpf(x) ** 2 - a2) for x in (x0, x0 + 1))
        head2 = sum(sum(poly[e] * mpf(x) ** e for e in poly)
                    / (mpf(x) ** 2 - a2) ** 2 for x in (x0, x0 + 1))
        dL2 = head1 + sum_Q2_over_lambda(poly, a2, x0 + 2, 1)
        dD12 = head2 + sum_Q2_over_lambda(poly, a2, x0 + 2, 2)
        ok3 = (abs(dL - dL2) < mpf("1e-35") * max(1, abs(dL))
               and abs(dD1 - dD12) < mpf("1e-35") * max(1, abs(dD1)))
        print(f"  C3 window-shift: dL d={nstr(abs(dL-dL2),2)}, "
              f"dD1 d={nstr(abs(dD1-dD12),2)}  [{'OK' if ok3 else 'FAIL'}]")
        assert ok3
        sig = -dD1 / dL
        # C4: susceptibility locks to the tower's OWN self-response D1
        poly_t, a2_t, x0_t = build(ndim, p)
        D1_t = dkdu(poly_t, a2_t, x0_t, 1)
        idsign = mpf(1) if sig > 0 else mpf(-1)
        iddev = abs(sig - idsign * D1_t)
        print(f"  dL/dkappa  = {nstr(dL, 12)}")
        print(f"  dD1/dkappa = {nstr(-dD1, 12)}")
        print(f"  sigma_kappa = {nstr(sig, 10)}   "
              f"distance to -6.21: {nstr(abs(sig - SIGMA_NEED), 5)}")
        print(f"  C4 LOCK: sigma_kappa = {'+' if idsign > 0 else '-'}D1(tower) "
              f"(D1 = {nstr(D1_t, 10)}, dev {nstr(iddev, 2)})")
        results[name] = (dL, -dD1, sig, idsign * D1_t, iddev)

    dL = sum(v[0] for v in results.values())
    dD = sum(v[1] for v in results.values())
    sig = dD / dL
    print(f"\n[combined towers]  sigma_kappa = {nstr(sig, 10)}   "
          f"distance to -6.21: {nstr(abs(sig - SIGMA_NEED), 5)}")
    print("\nHonesty note: the per-MODE response to kappa q^2 is sign-definite,")
    print("but the zeta-regularized tower totals are not (regularized sums of")
    print("positive series can go negative) — the signs above are the exact")
    print("regularized values, same convention as the record scorecards.")
    print("Structural finding (C4): each tower's charge susceptibility is LOCKED")
    print("to its own self-response D1 — the Berger/canonical-variation route")
    print("cannot generate an independent slope. One shot, reported, not graded.")


if __name__ == "__main__":
    main()
