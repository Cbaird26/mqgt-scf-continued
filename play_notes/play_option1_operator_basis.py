#!/usr/bin/env python3
"""PLAY — OPTION 1: the complete linear-response E x (p-form) operator basis
on round S^n (NOT the scientific record).

PRINCIPLE (declared before computation, corpus MATH-01 discipline):
Instead of another weighting, enumerate the COMPLETE basis of linear-in-E,
gauge-consistent, parity-even couplings of the scalar E to a free p-form
sector on a maximally symmetric space, and give each class exactly one
disposition: structurally zero / EFT-unnatural / computed once.

THE BASIS AND ITS DISPOSITIONS (structural arguments pre-registered):

  B1 uniform modulus (dilaton)  e^{gamma E} on the whole operator
     -> computed in lab 5: sigma = +0.797. EXCLUDED numerically.
  B2 non-minimal endomorphism coupling  E * A wedge *(E0 A)
     (E0 = curvature endomorphism of the Hodge/Weitzenboeck operator).
     On round S^n, E0 = -p(n-p) * 1 on each coexact tower -> tower weight
     w_p = p(n-p). SCALARS GET EXACTLY ZERO (scalar endomorphism vanishes
     on any space) -> first convention-INDEPENDENT principle: the zero-mode
     question never arises. THE ONE NEW NUMBER OF OPTION 1.
  B3 Chern-Simons type  E * A wedge dA  (exists only for the middle form:
     p=3 on S7, p=4 on S9). Round S^n has an orientation-reversing
     isometry R with R* (star d) R = -(star d) -> the star-d spectrum is
     +/- symmetric mode by mode -> the linear response sums
     d+ mu+ / lam + d- mu- / lam with d+ = d- , mu = +/- sqrt(lam)
     cancel IDENTICALLY; first nonzero effect is O(E^2).
     EXCLUDED STRUCTURALLY (same class as the mass portal).
  B4 BF / cross-degree mixing  E * A_p wedge *dA_{p-1}
     d maps coexact (p-1) to EXACT p: the mixing leaves the declared
     coexact tower set. Linear response within the set == 0.
     EXCLUDED STRUCTURALLY (same class as the axion).
  B5 higher-derivative uniform  E * A wedge *(Delta^q A),  q >= 1
     response weights become mode-dependent ~ sum d lam^{q-1}:
     q = 1 collapses to the zeta(0) family (= B1, already computed);
     q >= 2 is power-divergent, needs a new counterterm, no technically
     natural window (corpus MATH-01 kill condition). EXCLUDED on
     EFT-naturalness grounds.
  B6 mass portal E^2|A|^2 / axionic E*(topological density)
     quadratic / exactly zero on round S^n. EXCLUDED (prior, lab 5).

So Option 1 produces exactly ONE new number:
    sigma_nm = sum_p p(n-p) D1_p / sum_p p(n-p) L_p   (p >= 1 only).

VERDICT RULES (pre-declared, standing): right sign and |sigma| within
factor 2 of 6.21 -> lead-class (record-side derivation still required);
exact approach to the 1e-8 gate -> graduate; otherwise record and stop.
Controls: tower table must match the archived play values at 5e-8/5e-3.
"""

from mpmath import mp, mpf, nstr

mp.dps = 80

from mqgt_t1_e4_derivation import build, logdet, dkdu

SIGMA_NEED = mpf("-6.21")

ARCHIVE = {
    ("S7", 1): (mpf("0.455557862"), mpf("-0.3208")),
    ("S7", 2): (mpf("-1.075381869"), mpf("+0.2917")),
    ("S7", 3): (mpf("3.496904409"), mpf("+4.651")),
    ("S9", 1): (mpf("0.0787868"), mpf("-0.2655")),
    ("S9", 2): (mpf("-0.4136446582"), mpf("+0.2375")),
    ("S9", 3): (mpf("1.058076924"), mpf("-0.225")),
    ("S9", 4): (mpf("-3.485944242"), mpf("-4.7135")),
}

SET = (("S7", 7, 3), ("S9", 9, 4))


def main():
    print("=" * 80)
    print("PLAY — OPTION 1: complete E x form operator basis; the one new number")
    print("=" * 80)

    print("\n[0] structural exclusions (pre-registered, no computation)")
    print("  B3 Chern-Simons:  +/- symmetric on round S^n (orientation reversal)")
    print("                    -> linear response identically zero. EXCLUDED.")
    print("  B4 BF mixing:     leaves the coexact tower set -> zero within set.")
    print("                    EXCLUDED.")
    print("  B5 higher-deriv:  q=1 collapses to B1; q>=2 EFT-unnatural. EXCLUDED.")
    print("  B6 portal/axion:  quadratic / zero. EXCLUDED (prior).")

    print("\n[1] tower table + weights w_p = p(n-p)  [control vs archive]")
    num = den = mpf(0)
    ok = True
    for s, n, pmax in SET:
        for p in range(1, pmax + 1):
            poly, a2, x0 = build(n, p)
            L = logdet(poly, a2, x0)
            D1 = dkdu(poly, a2, x0, 1)
            w = p * (n - p)
            La, D1a = ARCHIVE[(s, p)]
            m = abs(L - La) < mpf("5e-8") and abs(D1 - D1a) < mpf("5e-3")
            ok &= m
            num += w * D1
            den += w * L
            print(f"  {s} ce{p}:  w = {w:>2}   L = {nstr(L, 14):>16}"
                  f"  D1 = {nstr(D1, 12):>14}   archive {'OK' if m else 'FAIL'}")
    if not ok:
        print("  CONTROL FAILURE — stop.")
        return

    sig = num / den
    print("\n[2] sigma_nm = sum p(n-p) D1 / sum p(n-p) L   (one shot)")
    print(f"    numerator   = {nstr(num, 15)}")
    print(f"    denominator = {nstr(den, 15)}")
    print(f"    sigma_nm    = {nstr(sig, 12)}")
    ratio = sig / SIGMA_NEED
    win = mpf("0.5") <= ratio <= 2 and sig < 0
    print(f"    distance to -6.21: {nstr(abs(sig - SIGMA_NEED), 5)}"
          f"   ratio: {nstr(ratio, 5)}   play-window: {'YES' if win else 'no'}")

    print("\n" + "=" * 80)
    print("VERDICT (pre-declared rules)")
    print("=" * 80)
    if win:
        print(f"  sigma_nm = {nstr(sig, 8)}: lead-class. Record-side derivation of the")
        print("  non-minimal coupling required before any further step.")
    else:
        print(f"  sigma_nm = {nstr(sig, 8)} misses: the non-minimal endomorphism")
        print("  coupling is excluded as stated.")
    print("\n  With B2 disposed, the COMPLETE linear-response operator basis of")
    print("  E x (p-form) on round S^n is exhausted: every class is structurally")
    print("  zero, EFT-unnatural, or numerically excluded. Option 1 is CLOSED.")
    print("  The interior-observer branch now has no open play route to")
    print("  sigma = -6.21 that the declared operator content can express.")


if __name__ == "__main__":
    main()
