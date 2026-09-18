#!/usr/bin/env python3
"""MIRROR IDENTITY CHECK — S^7 ce3 vs S^9 ce4 self-paired middle towers.

RECORD-SIDE. Triggered by play lab 4's structural observation: the two
self-paired middle towers nearly cancel,
    S^7 ce3:  L = +3.496904409,  D1 = +4.651
    S^9 ce4:  L = -3.485944242,  D1 = -4.7135
(magnitudes match to 0.3% / 1.3% with opposite signs, from rounded play
values). Grok 2026-09-18: "Choose (a): exact zeta check on identity.
Hold all new weights until that settles."

Question: are the EXACT high-precision values related by an exact mirror
    L(S^7 ce3) + L(S^9 ce4) = 0,   D1(S^7 ce3) + D1(S^9 ce4) = 0 ?
If exact at dps=80: theorem candidate, dig for the reason.
If not: quantify the closeness and label it (coincidence-class).

Structural backdrop (why a relation is plausible at all):
  - Both towers are PERFECT-SQUARE spectra: lambda_m = m^2, m >= 4 (S^7 ce3)
    resp. m >= 5 (S^9 ce4); a2 = 0 for both (a = (n-1)/2 - p = 0 at middle).
  - Both are self-paired under B = *d (ce_p -> ce_{n-1-p}, p = (n-1)/2), and
    both carry the Weyl-dimension doubling factor 2 (deg_coexact, p = r-1).
  - Their zeta'(0) are finite rational combinations of
    {zeta'(0), zeta'(-2), ..., zeta'(-8)} plus head corrections in ln 2..ln 5
    (different heads: x0 = 4 vs 5). Exact mirror requires a specific
    cancellation among a priori independent transcendentals.

Also scans ALL middle towers S^3 ce1 .. S^11 ce5 (same m^2 family, shifted)
to see whether any mirror is pairwise-specific or a general parity pattern.
This is the explanation probe, not a new weighting.

Machinery: mqgt_t1_e4_derivation.build/logdet/dkdu (exact analytic series,
a2 = 0 collapses the j-series to j = 1 for D1), mqgt_t3_reverse_search.z0.
"""

from mpmath import mp, mpf, nstr, zeta, log

mp.dps = 80

from mqgt_t1_e4_derivation import build, logdet, dkdu
from mqgt_t3_reverse_search import z0, deg_coexact

MIDDLES = [(3, 1), (5, 2), (7, 3), (9, 4), (11, 5)]


def tower(n, p):
    poly, a2, x0 = build(n, p)
    L = logdet(poly, a2, x0)
    D1 = dkdu(poly, a2, x0, 1)
    zz = z0(poly, x0)
    return poly, a2, x0, L, D1, zz


def main():
    print("=" * 78)
    print("MIRROR IDENTITY CHECK — self-paired middle towers (dps=80)")
    print("=" * 78)

    data = {}
    for n, p in MIDDLES:
        poly, a2, x0, L, D1, zz = tower(n, p)
        data[(n, p)] = (poly, a2, x0, L, D1, zz)
        print(f"\nS^{n} ce{p}  (lambda_m = m^2, m >= {x0}; a2 = {nstr(a2,3)})")
        print(f"  zeta(0)  = {nstr(zz, 10)}  (integer check)")
        print(f"  L  = zeta'(0) = {nstr(L, 30)}")
        print(f"  D1 = dL/du    = {nstr(D1, 30)}")
        print(f"  degeneracy poly (coeffs in m = k+{x0}): "
              + ", ".join(f"m^{i}: {nstr(c, 12)}" for i, c in sorted(poly.items())))

    print("\n" + "=" * 78)
    print("[1] THE PAIR: S^7 ce3 vs S^9 ce4")
    print("=" * 78)
    L7, D1_7 = data[(7, 3)][3], data[(7, 3)][4]
    L9, D1_9 = data[(9, 4)][3], data[(9, 4)][4]
    for name, a, b in [("L", L7, L9), ("D1", D1_7, D1_9)]:
        s = a + b
        rel = abs(s) / max(abs(a), abs(b))
        print(f"  {name}: A = {nstr(a, 25)}")
        print(f"       B = {nstr(b, 25)}")
        print(f"       A+B = {nstr(s, 8)}   rel. residual = {nstr(rel, 3)}")
        print(f"       exact mirror? {'YES — theorem candidate' if rel < mpf('1e-50') else 'NO'}")

    print("\n[2] ALL PAIRWISE SUMS L(S^n middle) + L(S^{n+2} middle)")
    for (n1, p1), (n2, p2) in zip(MIDDLES, MIDDLES[1:]):
        a, b = data[(n1, p1)][3], data[(n2, p2)][3]
        rel = abs(a + b) / max(abs(a), abs(b))
        print(f"  S^{n1} ce{p1} + S^{n2} ce{p2}: sum = {nstr(a+b, 8)}   rel = {nstr(rel, 3)}")

    print("\n[3] SIGN/SYMMETRY PATTERN ACROSS MIDDLE TOWERS")
    print("  (looking for alternation or simple ratios — explanation probe)")
    prev = None
    for n, p in MIDDLES:
        L = data[(n, p)][3]
        line = f"  S^{n} ce{p}: L = {nstr(L, 15)}"
        if prev is not None and L != 0:
            line += f"   ratio to prev = {nstr(L / prev, 8)}"
        print(line)
        prev = L

    print("\n[4] DECOMPOSITION: why close (if close)?")
    print("  L = sum_i c_i * 2*zetaR'(-i, x0); with a2=0 no j-tail.")
    for n, p in [(7, 3), (9, 4)]:
        poly, a2, x0 = data[(n, p)][:3]
        terms = []
        for i, c in sorted(poly.items()):
            zr = zeta(-i, derivative=1)
            head = sum(log(mpf(q)) * mpf(q) ** i for q in range(1, int(x0)))
            terms.append((i, c, 2 * c * (zr + head)))
        print(f"  S^{n} ce{p} (x0={x0}):")
        for i, c, t in terms:
            print(f"    c_{i} = {nstr(c, 12):>16s}   contribution = {nstr(t, 15)}")

    print("\n" + "=" * 78)
    print("VERDICT")
    print("=" * 78)
    relL = abs(L7 + L9) / max(abs(L7), abs(L9))
    relD = abs(D1_7 + D1_9) / max(abs(D1_7), abs(D1_9))
    if relL < mpf("1e-50") and relD < mpf("1e-50"):
        print("  EXACT MIRROR at dps=80 — theorem candidate. Next: prove it from")
        print("  the Weyl polynomials + Hurwitz functional equation.")
    else:
        print(f"  NOT exact: rel residuals L: {nstr(relL, 3)}, D1: {nstr(relD, 3)}.")
        print("  Closeness quantified above; label: coincidence-class structural")
        print("  near-relation between square towers m>=4 / m>=5 with adjacent")
        print("  Weyl polynomials. Recorded; no weighting consequence.")


if __name__ == "__main__":
    main()
