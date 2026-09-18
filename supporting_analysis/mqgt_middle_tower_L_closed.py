#!/usr/bin/env python3
"""L-FAMILY CLOSED FORM — middle-tower zeta'(0), exact certificate.

RECORD-SIDE. Continuation of MIDDLE_TOWER_D1_LEMMA.md (2026-09-18), ordered
by Grok: "Proceed to L-family closed forms next (now mechanical)."

DERIVATION (one paragraph):
  L = zeta'_mid(0) = 2 sum_i c_i zetaR'(-i, x0), with d(m) = sum c_i m^i the
  degeneracy polynomial. Splitting zetaR'(-i, x0) = zeta'(-i) +
  sum_{q<x0} q^i ln q gives
      L = 2 sum_i c_i zeta'(-i) + 2 sum_{q=1}^{r} d(q) ln q.
  The factorization d(m) = (2/(r!)^2) prod_{j=1}^r (m^2 - j^2) kills the head
  sum (d(q) = 0 for q <= r). With zeta'(0) = -1/2 ln 2pi and the functional
  equation zeta'(-2k) = (-1)^k (2k)! zeta(2k+1) / (2(2pi)^{2k}), and
  c_{2k} = (2/(r!)^2)(-1)^{r-k} e_{r-k}(1, 4, ..., r^2):

      L(r) = (-1)^{x0} * 2 [ ln(2pi) - sum_{k=1}^{r} e_{r-k} (2k)! zeta(2k+1)
                                / ( (r!)^2 (2pi)^{2k} ) ],   x0 = r+1.

  Same skeleton gives zeta_mid(0) = (-1)^{x0} exactly (trivial zeros +
  d(q) = 0), matching the integer checks in mqgt_mirror_check.py.

This script: computes L both ways (machinery logdet at dps=80 vs closed form
with exact rational coefficients) for r = 1..8 (S^3..S^17), and prints the
explicit small-r forms.
"""

from fractions import Fraction
from math import factorial
from mpmath import mp, mpf, nstr, zeta, log, pi

mp.dps = 80

from mqgt_t1_e4_derivation import build, logdet
from mqgt_t3_reverse_search import z0


def e_sym(j, squares):
    """Elementary symmetric polynomial e_j of the list, exact."""
    poly = [Fraction(1)]
    for s in squares:
        poly.append(Fraction(0))
        for i in range(len(poly) - 1, 0, -1):
            poly[i] += s * poly[i - 1]
    return poly[j]


def L_closed(r):
    """Closed form: exact rational coefficients x mpmath zeta odds."""
    sq = [j * j for j in range(1, r + 1)]
    rf2 = mpf(factorial(r)) ** 2
    x0 = r + 1
    bracket = log(2 * pi)
    for k in range(1, r + 1):
        e = e_sym(r - k, sq)
        coef = (mpf(e.numerator) / mpf(e.denominator)) / rf2
        bracket -= coef * mpf(factorial(2 * k)) * zeta(2 * k + 1) / (2 * pi) ** (2 * k)
    return (-1) ** x0 * 2 * bracket


def main():
    print("=" * 78)
    print("L-FAMILY CLOSED FORM CERTIFICATE (dps=80)")
    print("=" * 78)
    print(f"{'tower':>10s} {'machinery logdet':>28s} {'closed form':>28s} {'residual':>10s}")
    for r in range(1, 9):
        n = 2 * r + 1
        p = r
        poly, a2, x0 = build(n, p)
        Lm = logdet(poly, a2, x0)
        Lc = L_closed(r)
        zz = z0(poly, x0)
        res = abs(Lm - Lc)
        z0ok = abs(zz - (-1) ** x0) < mpf("1e-40")
        print(f"  S^{n:2d} ce{p} {nstr(Lm, 22):>28s} {nstr(Lc, 22):>28s} {nstr(res, 2):>10s}"
              f"   zeta(0)={nstr(zz,3)} {'OK' if z0ok else 'FAIL'}")

    print("-" * 78)
    print("Explicit small-r forms:")
    print("  S^3  ce1:  L =  2 ln(2pi) - zeta(3)/pi^2")
    print("  S^5  ce2:  L = -2 ln(2pi) + 5 zeta(3)/(4 pi^2) + 3 zeta(5)/(4 pi^4)")
    print("  S^7  ce3:  L =  2 ln(2pi) - 49 zeta(3)/(36 pi^2) - 7 zeta(5)/(6 pi^4)"
          " - 5 zeta(7)/(8 pi^6)")
    print("  (coefficients: e_{r-k}(1,4,...,r^2) (2k)! / ((r!)^2 2^{2k-?}) — see note)")


if __name__ == "__main__":
    main()
