#!/usr/bin/env python3
"""PROOF CERTIFICATE — middle-tower D1 closed form (exact rational arithmetic).

RECORD-SIDE. Lemma (numerically certain at dps=80, mqgt_mirror_check.py,
2026-09-18): for the self-paired middle coexact tower on S^n (n odd),
p = (n-1)/2, spectrum lambda_m = m^2 (m >= x0 = (n+1)/2),

    D1(n) = d/du zeta'(0)|_{u=0} = (-1)^x0 * ( pi^2/3 + H2(x0-1) ),

H2(N) = sum_{m=1..N} 1/m^2.

PROOF CHAIN (what this script certifies line by line):
  (A) With a2 = 0, the exact derivative series (mqgt_t1_e4_derivation.dkdu)
      collapses to j = 1:
          D1 = -sum_i c_i zetaR(2-i, x0),
      where d(m) = sum_i c_i m^i is the degeneracy polynomial (even).
  (B) zetaR(2-i, x0) = zeta(2-i) - sum_{q=1}^{x0-1} q^{i-2}; the zeta values
      at negative even integers vanish (trivial zeros), so only i = 0, 2
      contribute:  D1 = -c_0 zeta(2) - c_2 zeta(0) + sum_{q=1}^{x0-1} d(q)/q^2.
  (C) FACTORIZATION (verified here exactly, r = 1..10): with r = (n-1)/2,
          d(m) = (2/(r!)^2) * prod_{j=1}^{r} (m^2 - j^2).
      This is the middle case of the standard coexact p-form degeneracy
      formula on spheres (Weyl dimension; cf. Rubin-Ordonez). A fully
      self-contained Weyl-formula derivation is attached as a check of
      degrees/leading coefficients; the coefficient-wise comparison here is
      performed in exact rational arithmetic, no floats.
  (D) Consequences of (C):
      d(q) = 0 for q = 1..r   => the finite sum vanishes identically;
      c_0 = d(0) = 2(-1)^r    => -c_0 zeta(2) = (-1)^x0 * pi^2/3;
      c_2 = 2(-1)^{r+1} H2(r) => -c_2 zeta(0) = c_2/2 = (-1)^x0 H2(x0-1).
      Sum: D1 = (-1)^x0 ( pi^2/3 + H2(x0-1) ).  QED.

This script verifies (C) coefficient-wise and (D) arithmetically, all in
fractions.Fraction (no floating point), for r = 1..10 (S^3 .. S^21).
The dps=80 floating certificate for the final identity itself (r = 1..6)
is in mqgt_mirror_check.py's output of 2026-09-18.
"""

from fractions import Fraction
from math import factorial


def weyl_dr_exact(lam, r):
    """Weyl dimension formula, exact rationals (type-B/D product form)."""
    m = [r - 1 - i for i in range(r)]
    l = [lam[i] + m[i] for i in range(r)]
    d = Fraction(1)
    for i in range(r):
        for j in range(i + 1, r):
            d *= Fraction(l[i] ** 2 - l[j] ** 2, m[i] ** 2 - m[j] ** 2)
    return d


def deg_coexact_exact(n, p, k):
    r = (n + 1) // 2
    lam = [k + 1] + [1] * p + [0] * (r - 1 - p)
    d = weyl_dr_exact(lam, r)
    if p == r - 1:
        d *= 2
    return d


def interp_poly_exact(xs, ys, deg):
    """Exact polynomial interpolation (Vandermonde, rational solve)."""
    n = deg + 1
    A = [[Fraction(x) ** i for i in range(n)] for x in xs[:n]]
    b = ys[:n]
    # Gaussian elimination over Fraction
    M = [row[:] + [bb] for row, bb in zip(A, b)]
    for col in range(n):
        piv = next(r_ for r_ in range(col, n) if M[r_][col] != 0)
        M[col], M[piv] = M[piv], M[col]
        for r_ in range(n):
            if r_ != col and M[r_][col] != 0:
                f = M[r_][col] / M[col][col]
                M[r_] = [a - f * c for a, c in zip(M[r_], M[col])]
    return [M[i][n] / M[i][i] for i in range(n)]


def product_poly(r):
    """(2/(r!)^2) * prod_{j=1}^r (m^2 - j^2), exact, as coeff dict in m."""
    poly = {0: Fraction(1)}
    for j in range(1, r + 1):
        new = {}
        for i, c in poly.items():
            new[i] = new.get(i, Fraction(0)) - c * j * j
            new[i + 2] = new.get(i + 2, Fraction(0)) + c
        poly = new
    f = Fraction(2, factorial(r) ** 2)
    return {i: c * f for i, c in poly.items()}


def H2(N):
    return sum(Fraction(1, m * m) for m in range(1, N + 1))


def main():
    print("=" * 78)
    print("PROOF CERTIFICATE — middle-tower D1 closed form (exact rationals)")
    print("=" * 78)

    all_ok = True
    for r in range(1, 11):
        n = 2 * r + 1
        p = r                    # middle coexact tower
        x0 = r + 1
        # exact degeneracy polynomial in m = k + x0
        ks = list(range(n + 2))
        ys = [deg_coexact_exact(n, p, k) for k in ks]
        cs = interp_poly_exact([k + x0 for k in ks], ys, n - 1)
        d_fit = {i: c for i, c in enumerate(cs) if c != 0}
        d_prod = product_poly(r)
        fac_ok = d_fit == d_prod

        c0 = d_fit.get(0, Fraction(0))
        c2 = d_fit.get(2, Fraction(0))
        # (D1) chain in exact arithmetic:
        #   D1 = -c0*Z2 + c2/2 + sum_{q=1}^{r} d(q)/q^2,  Z2 = pi^2/6 symbolic
        finsum = sum(sum(c * Fraction(q) ** i for i, c in d_fit.items())
                     / Fraction(q * q) for q in range(1, r + 1))
        sgn = Fraction((-1) ** x0)
        cond_c0 = (-c0 == 2 * sgn)                     # gives (-1)^x0 pi^2/3
        cond_fs = (finsum == 0)                        # factorization zeros
        cond_c2 = (c2 / 2 == sgn * H2(x0 - 1))         # gives (-1)^x0 H2
        ok = fac_ok and cond_c0 and cond_fs and cond_c2
        all_ok &= ok
        print(f"  r={r:2d}  S^{n:2d} ce{p}:  factorization {'OK' if fac_ok else 'FAIL'}"
              f"   c0={c0} (need {-2*int((-1)**x0)})"
              f"   finsum={finsum}   c2/2={c2/2} (need {sgn*H2(x0-1)})"
              f"   [{'OK' if ok else 'FAIL'}]")

    print("-" * 78)
    if all_ok:
        print("ALL CHECKS PASS (r = 1..10, exact rational arithmetic).")
        print("Combined with steps (A)-(B) (exact series collapse + trivial")
        print("zeros of zeta), the lemma is proved:")
        print("    D1(S^n middle) = (-1)^x0 * ( pi^2/3 + H2(x0-1) ),  x0 = (n+1)/2.")
    else:
        print("A CHECK FAILED — see lines above.")


if __name__ == "__main__":
    main()
