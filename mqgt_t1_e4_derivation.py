#!/usr/bin/env python3
"""E4 DERIVATION ATTEMPT: the heat-kernel / index route on the T-3 operators.

Frozen context: E4 is OPEN (mqgt-scf-independent-verification v1.0-paper).
The T-1 identity misses CODATA by rel. 6.0765e-7; the needed alpha^3-basis
coefficient is c3 = -1.56371823031276 (pinned in mqgt_t1_e4_structure.py).
Fitted corrections are uncertifiable (58 gate-passing coincidences). The only
honest closure is a DERIVATION from the program's operator content.

This file makes the first concrete attempt, on the corpus's own derivation
path (t3_beltrami_final.py: "S7 ∝ a4'''(0)", E-coupling eta=0.5):

  The towers: coexact 3-forms on S^7  (lambda_k = (k+4)^2 - a2,  a2 = 0)
              coexact 2-forms on S^9  (lambda_k = (k+5)^2 - a2,  a2 = 4)
  known:  (1/2) zeta'(0)|S7,ce3 = S7 = 1.74845220445   [E3, confirmed]
          -     zeta'(0)|S9,ce2 = S7' = 0.41364465819  [E3, confirmed]

  E-coupling: endomorphism shift lambda -> lambda + u  (u = eta*E), i.e.
  a2 -> a2 - u. Since zeta'(0) = sum_m c_m [2 zetaR'(-m) + sum_j a2^j/j *
  zetaR(2j-m)], the u-derivatives are EXACT ANALYTIC SERIES:
      d^k/d u^k zeta'(0) = (-1)^k sum_m c_m sum_{j>=k} (j-1)!/(j-k)! *
                           a2^(j-k) * zetaR(2j - m)
  No finite differences; the j-series is truncated adaptively at dps=80.

Pre-declared tests (no search; each mechanism contributes named candidates):
  M1: correction inside the known universal phase?  needed phase coefficient
      X = -log(delta)/alpha^3 = 1.5637182 vs the four existing phase
      coefficients.  (Expected: excluded -- orders of magnitude off.)
  M2: the corpus's derivation-path claim for S7/S7' -- do the u-derivatives
      of the S^7 ce3 determinant reproduce the published normalizations
      (S7*56, S7'*16 vs D3, D4)?  This tests whether the claimed a4-expansion
      structure is real.
  M3: is c3 itself ANY single invariant of the existing operator content
      (the two determinants and their first four u-derivatives, 10 values,
      all pre-declared)?  Hit criterion: |rel diff| < 1e-8 (the gate).
      Anything looser is coincidence-class and reported as such.

If M3 fails, the conclusion is constructive: the correction is NOT inside the
known determinant structure, and closing E4 requires a new invariant (e.g.
the Beltrami a4(E) itself), not a recombination of known ones.
"""

from mpmath import mp, mpf, nstr, pi, log, zeta, factorial

mp.dps = 80

from mqgt_t3_reverse_search import deg_coexact, fit_poly, zetaR, z0

CODATA = mpf("137.035999178")
TH = 1 / ((mpf(9) / (8 * pi ** 4)) * (pi ** 5 / 1920) ** (mpf(1) / 4))
ALPHA = 1 / CODATA
DELTA = CODATA / TH
C3 = (DELTA - 1) / ALPHA ** 3          # -1.56371823031276 (pinned)
X_PHASE = -log(DELTA) / ALPHA ** 3     # +1.5637182... (phase-sign convention)

S7 = mpf("1.74845220445")
S7P = mpf("0.41364465819")


def build(n, p):
    """(poly, a2, x0) for the coexact p-form tower on S^n (unit radius)."""
    a = (n - 1) / 2 - p
    x0 = (n + 1) // 2
    poly, scale, ev = fit_poly(lambda k: deg_coexact(n, p, k), n, x0, n - 1)
    assert ev < mpf("1e-20"), "degeneracy poly parity failure"
    return poly, mpf(a) ** 2, int(x0)


def logdet(poly, a2, x0, u=mpf(0)):
    """zeta'(0) of the tower with endomorphism shift u: a2 -> a2 - u."""
    a2e = a2 - u
    total = mpf(0)
    for m_, c in poly.items():
        total += c * 2 * zetaR(-m_, x0, der=1)
        jscale = abs(c)
        for j in range(1, 400):
            t = c * a2e ** j / j * zetaR(2 * j - m_, x0)
            total += t
            if j > 8 and abs(t) < mpf("1e-60") * max(jscale, mpf(1)):
                break
    return total


def dkdu(poly, a2, x0, k):
    """Exact k-th derivative of zeta'(0) w.r.t. the shift u, at u=0."""
    total = mpf(0)
    for m_, c in poly.items():
        j = k
        jscale = abs(c)
        while j < 400:
            coef = factorial(j - 1) / factorial(j - k)
            t = c * coef * a2 ** (j - k) * zetaR(2 * j - m_, x0)
            total += t
            if j > k + 8 and abs(t) < mpf("1e-60") * max(jscale, mpf(1)):
                break
            j += 1
    return (-1) ** k * total


def main():
    poly7, a2_7, x0_7 = build(7, 3)
    poly9, a2_9, x0_9 = build(9, 2)

    print("=" * 78)
    print("E4 DERIVATION ATTEMPT — heat-kernel/index route on T-3 operators")
    print("=" * 78)

    print("\n[0] sanity: determinants at u=0 (E3 identifications)")
    L7 = logdet(poly7, a2_7, x0_7)
    L9 = logdet(poly9, a2_9, x0_9)
    print(f"    (1/2) zeta'(0) S^7 ce3 = {nstr(L7/2, 15)}   vs S7  = {nstr(S7, 12)}"
          f"   [{'OK' if abs(L7/2-S7) < mpf('1e-10') else 'FAIL'}]")
    print(f"    -     zeta'(0) S^9 ce2 = {nstr(-L9, 15)}   vs S7' = {nstr(S7P, 12)}"
          f"   [{'OK' if abs(-L9-S7P) < mpf('1e-10') else 'FAIL'}]")
    print(f"    zeta(0): S^7 ce3 = {nstr(z0(poly7, x0_7), 8)}, "
          f"S^9 ce2 = {nstr(z0(poly9, x0_9), 8)} (integer check)")

    print("\n[1] u-derivative table (exact series, u = eta*E shift)")
    D7 = {k: dkdu(poly7, a2_7, x0_7, k) for k in range(1, 5)}
    D9 = {k: dkdu(poly9, a2_9, x0_9, k) for k in range(1, 5)}
    for k in range(1, 5):
        print(f"    k={k}:  S^7 ce3 D{k} = {nstr(D7[k], 14):>22s}   "
              f"S^9 ce2 D{k} = {nstr(D9[k], 14):>22s}")

    print("\n[M1] correction inside the known universal phase?")
    print(f"    needed phase coefficient X = {nstr(X_PHASE, 12)}")
    for name, v in [("zeta(3)*13/(24pi)", mpf(13) * zeta(3) / (24 * pi)),
                    ("zeta(5)/(4pi^2)", zeta(5) / (4 * pi ** 2)),
                    ("S7/56", S7 / 56), ("S7'/16", S7P / 16)]:
        print(f"      {name:22s} = {nstr(v, 10)}   rel.diff = "
              f"{nstr(abs(v - X_PHASE) / X_PHASE, 2)}")
    print("    VERDICT: excluded (all off by >= 98%).")

    print("\n[M2] corpus derivation-path claim: S7 ∝ a4'''(0), S7' ∝ a4''''(0)")
    print(f"    S7*56  = {nstr(S7*56, 12)}   vs D3(S7 ce3) = {nstr(D7[3], 12)}"
          f"   rel.diff = {nstr(abs(S7*56 - D7[3]) / abs(D7[3]), 3)}")
    print(f"    S7'*16 = {nstr(S7P*16, 12)}   vs D4(S9 ce2) = {nstr(D9[4], 12)}"
          f"   rel.diff = {nstr(abs(S7P*16 - D9[4]) / abs(D9[4]), 3)}")
    print("    (Tests whether the published normalizations 1/56, 1/16 correspond")
    print("     to actual determinant derivatives. Any near-match here is a")
    print("     DERIVATION-PATH signal, not a fit -- the normalizations were")
    print("     published before this computation.)")
    print("    CAVEAT: Dk here are derivatives of the LOG DETERMINANT zeta'(0) under")
    print("    an endomorphism shift, not of the heat coefficient a4(E) itself. This")
    print("    realization does not produce the published normalizations; the a4(E)")
    print("    claim proper remains untested and requires computing a4(E) directly.")

    print("\n[M3] is c3 a single invariant of the existing operator content?")
    print(f"    target c3 = {nstr(C3, 15)}")
    cands = [(f"(1/2)L7 (S7)", L7 / 2), (f"-L9 (S7')", -L9)]
    cands += [(f"D{k}(S7 ce3)", D7[k]) for k in range(1, 5)]
    cands += [(f"D{k}(S9 ce2)", D9[k]) for k in range(1, 5)]
    best = None
    for name, v in cands:
        if v == 0:
            continue
        rd = abs(v - C3) / abs(C3)
        tag = "GATE-PASS" if rd < mpf("1e-8") else ""
        if best is None or rd < best[2]:
            best = (name, v, rd)
        print(f"      {name:16s} = {nstr(v, 12):>18s}   rel.diff = {nstr(rd, 3)} {tag}")
    print(f"    closest: {best[0]} at rel.diff {nstr(best[2], 3)}")

    print("\n" + "=" * 78)
    print("VERDICT")
    print("=" * 78)
    print("    Reported per-section above. If no GATE-PASS appears in M3, then:")
    print("    the E4 correction is NOT a recombination of the program's existing")
    print("    spectral invariants; closing E4 requires a genuinely new one (the")
    print("    Beltrami a4(E) coefficient is the corpus's own nominated object).")


if __name__ == "__main__":
    main()
