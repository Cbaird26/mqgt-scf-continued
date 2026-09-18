#!/usr/bin/env python3
"""PLAY — convention-B rebuild of labs 1-5 (NOT the scientific record).

Open recheck item from the zeta(0) certification (2026-09-18): every play
scorecard number so far used convention A for the p=0 tower (scalar tower,
constant mode formally included, zeta(0)=0). Convention B (det' = coexact-0
determinant, zero mode removed, zeta(0)=-1) changes ONLY the two p=0 rows.

This script is NOT a new weighting (the freeze stands). It re-runs the
EXISTING, pre-declared weightings of labs 1-5 with the B rows and reports
how the scorecard moves. Same guardrail: distances to sigma_need=-6.21 are
reported, never graded-into-existence.

Convention A p=0 rows (lab-5 archive): L=4.169289794/3.849578692,
  D1=-43.925/-24.598.
Convention B p=0 rows (zeta0 certification): S7 det' L=-0.200915319509,
  D1=+0.408333333333; S9 det' L=+0.0547377225888, D1=+0.339732142857.

Controls: A-side must reproduce uniform -8.4674, de Rham +37.4, Hodge -8.40,
torsion +0.98, GKSL plateau +1.88, P1/P2/P3 -7.73/-11.39/-8.47, dilaton
+0.797. B-side p=0 rows must match the certification values above.

Notes on each weighting under the swap:
  * torsion (-1)^p*p: p=0 weight is 0 -> convention-INVARIANT (check).
  * GKSL Gamma_0(K): scalar and coexact-0 spectra coincide for k>=1 ->
    weights identical; only the (L,D1) values move.
  * dilaton w=zeta(0): scalar weight 0 (A) -> -1 (B); scalar rows enter.
"""

from mpmath import mp, mpf, nstr

mp.dps = 80

from mqgt_t1_e4_derivation import build, logdet, dkdu
from mqgt_t3_reverse_search import z0, deg_scalar, deg_coexact, fit_poly

SIGMA_NEED = -mpf("6.21")

A_ARCHIVE = {
    ("S7", 0): (mpf("4.169289794"), mpf("-43.925")),
    ("S9", 0): (mpf("3.849578692"), mpf("-24.598")),
}
B_CERT = {
    ("S7", 0): (mpf("-0.200915319509"), mpf("0.408333333333")),
    ("S9", 0): (mpf("0.0547377225888"), mpf("0.339732142857")),
}

SET = (("S7", 7, 3), ("S9", 9, 4))


def build_scalar(n):
    poly, scale, ev = fit_poly(lambda k: deg_scalar(n, k), n, (n - 1) / 2, n - 1)
    return poly, mpf((n - 1) / 2) ** 2, int((n - 1) / 2)


def table(convention):
    """{(s,p): (L, D1, z0)} ; p=0 = scalar (A) or coexact-0 / det' (B)."""
    T = {}
    for s, n, pmax in SET:
        for p in range(0, pmax + 1):
            if p == 0 and convention == "A":
                poly, a2, x0 = build_scalar(n)
            else:
                poly, a2, x0 = build(n, p)
            T[(s, p)] = (logdet(poly, a2, x0), dkdu(poly, a2, x0, 1),
                         z0(poly, int(x0)))
    return T


def sigma(T, wfun):
    num = sum(wfun(s, p) * v[1] for (s, p), v in T.items())
    den = sum(wfun(s, p) * v[0] for (s, p), v in T.items())
    return num / den, num, den


def w_uniform(s, p): return 1
def w_derham(s, p): return (-1) ** p
def w_torsion(s, p): return (-1) ** p * p
def w_P1(s, p): return -1 if p >= 2 else 1
def w_P2(s, p): return -1 if p >= 3 else 1
def w_P3(s, p):
    return -1 if (s == "S7" and p == 3) or (s == "S9" and p == 4) else 1
def w_dilaton(T):
    return lambda s, p: T[(s, p)][2]


def sigma_hodge(T):
    """C3: full Hodge towers ce_p + ce_{p-1}, plain sum (p = 1..pmax)."""
    num = den = mpf(0)
    for s, n, pmax in SET:
        for p in range(1, pmax + 1):
            num += T[(s, p)][1] + T[(s, p - 1)][1]
            den += T[(s, p)][0] + T[(s, p - 1)][0]
    return num / den, num, den


def gamma_wt(n, p, K, convention):
    # p=0: scalar nonzero spectrum == coexact-0 (det') spectrum, verified by
    # build(n,0) reproducing the certification det' L/D1 values exactly.
    # (The standalone helper deg_coexact(n,0,k) is a p>=1 formula and does NOT
    # degenerate to the scalar spectrum -- measured: ce0 gives 35/112/294...
    # where scalar gives 8/35/112... on S7. Use deg_scalar for p=0 in BOTH
    # conventions; the Gamma_0 weights are then convention-independent, which
    # is the physically correct statement: zero-mode removal changes L and D1
    # but not the nonzero mode multiplicities.)
    deg = (lambda k: deg_scalar(n, k)) if p == 0 \
        else (lambda k: deg_coexact(n, p, k))
    return sum(mpf(int(deg(k))) / k for k in range(1, K + 1))


def main():
    print("=" * 80)
    print("PLAY — convention-B rebuild of labs 1-5  (open recheck item)")
    print("=" * 80)

    TA = table("A")
    TB = table("B")

    print("\n[controls] p=0 rows")
    ok = True
    for key in (("S7", 0), ("S9", 0)):
        La, D1a, _ = TA[key]
        Lb, D1b, _ = TB[key]
        ca = abs(La - A_ARCHIVE[key][0]) < mpf("5e-8") and \
             abs(D1a - A_ARCHIVE[key][1]) < mpf("5e-3")
        cb = abs(Lb - B_CERT[key][0]) < mpf("5e-9") and \
             abs(D1b - B_CERT[key][1]) < mpf("5e-9")
        ok &= ca and cb
        print(f"  {key}: A L={nstr(La,12)} D1={nstr(D1a,10)} [{ 'OK' if ca else 'FAIL'}]"
              f"   B L={nstr(Lb,14)} D1={nstr(D1b,12)} [{'OK' if cb else 'FAIL'}]")
    # degeneracy note: standalone deg_coexact(.,0,.) is a p>=1 formula and
    # does not reproduce the scalar spectrum; the correct identity (nonzero
    # scalar spectrum == coexact-0 spectrum) is already proven by build(n,0)
    # matching the det' certification values above.
    print("  p=0 nonzero-mode multiplicities: convention-independent (deg_scalar)")
    # torsion invariance
    sA = sigma(TA, w_torsion)[0]
    sB = sigma(TB, w_torsion)[0]
    print(f"  torsion sigma A={nstr(sA,8)} B={nstr(sB,8)}  invariant: {sA==sB}")
    if not ok:
        print("  CONTROL FAILURE — stop."); return

    rows = [
        ("uniform (C1)",      lambda T: sigma(T, w_uniform)),
        ("de Rham (C2)",      lambda T: sigma(T, w_derham)),
        ("full Hodge (C3)",   sigma_hodge),
        ("torsion (C4)",      lambda T: sigma(T, w_torsion)),
        ("parity P1",         lambda T: sigma(T, w_P1)),
        ("parity P2",         lambda T: sigma(T, w_P2)),
        ("parity P3",         lambda T: sigma(T, w_P3)),
        ("dilaton zeta(0)",   lambda T: sigma(T, w_dilaton(T))),
    ]

    print("\n[scorecard] sigma by weighting, convention A vs B")
    print(f"  {'weighting':<18}{'sigma_A':>12}{'sigma_B':>12}"
          f"{'A dist':>10}{'B dist':>10}")
    out = {}
    for name, fn in rows:
        sigA, _, _ = fn(TA)
        sigB, _, _ = fn(TB)
        out[name] = (sigA, sigB)
        dA = abs(sigA - SIGMA_NEED); dB = abs(sigB - SIGMA_NEED)
        print(f"  {name:<18}{nstr(sigA,8):>12}{nstr(sigB,8):>12}"
              f"{nstr(dA,4):>10}{nstr(dB,4):>10}")

    print("\n[GKSL lab 3] sigma(K) scan, A vs B")
    print(f"  {'K':>6}{'sigma_A(K)':>14}{'sigma_B(K)':>14}")
    for K in (3, 5, 8, 12, 20, 35, 60, 100, 200, 400, 800):
        for conv, T, tag in (("A", TA, None), ("B", TB, None)):
            w = {(s, p): gamma_wt(n, p, K, conv) for s, n, pmax in SET
                 for p in range(0, pmax + 1)}
            sig = sum(w[k] * T[k][1] for k in w) / sum(w[k] * T[k][0] for k in w)
            if conv == "A": sigA = sig
            else: sigB = sig
        print(f"  {K:>6}{nstr(sigA,10):>14}{nstr(sigB,10):>14}")

    print("\n[diagnostics]")
    # uniform family: sigma(t) = (Dce + t Dsc)/(Lce + t Lsc), t = scalar share
    for conv, T in (("A", TA), ("B", TB)):
        Dce = sum(v[1] for (s, p), v in T.items() if p >= 1)
        Lce = sum(v[0] for (s, p), v in T.items() if p >= 1)
        Dsc = sum(v[1] for (s, p), v in T.items() if p == 0)
        Lsc = sum(v[0] for (s, p), v in T.items() if p == 0)
        # solve (Dce + t Dsc) = need (Lce + t Lsc)
        tstar = (SIGMA_NEED * Lce - Dce) / (Dsc - SIGMA_NEED * Lsc)
        inrange = mpf(0) <= tstar <= 1
        print(f"  uniform family conv {conv}: sigma(0)={nstr(Dce/Lce,6)}, "
              f"sigma(1)={nstr((Dce+Dsc)/(Lce+Lsc),6)}, "
              f"t*={nstr(tstar,6)} {'(reachable)' if inrange else '(NOT in [0,1])'}")
    # alternating family under B: does sigma move toward -6.21?
    print(f"  alternating (de Rham) A={nstr(out['de Rham (C2)'][0],6)} "
          f"B={nstr(out['de Rham (C2)'][1],6)}  (target -6.21)")

    print("\n[verdict] pre-declared: report only. Any B-side weighting landing")
    print("  within factor 2 of -6.21 with correct sign upgrades to CANDIDATE-class")
    print("  (still play, gated record-side); none -> the combination-rule")
    print("  exclusion record stands under BOTH conventions.")
    for name, (sa, sb) in out.items():
        ratio = sb / SIGMA_NEED
        win = mpf("0.5") <= ratio <= 2 and sb < 0
        print(f"  {name:<18} B: {'CANDIDATE-window' if win else 'excluded as stated'}")


if __name__ == "__main__":
    main()
