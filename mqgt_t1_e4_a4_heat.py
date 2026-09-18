#!/usr/bin/env python3
"""E4 ROUND 2: the a4(E) heat coefficient itself -- analytic evaluation.

Frozen context: E4 OPEN. Round 1 (mqgt_t1_e4_derivation.py) excluded every
existing spectral invariant as the source of c3 = -1.56371823031276. The last
nominated object is the corpus's own derivation path (t3_beltrami_final.py):

    "a4(E) = a4(0) + a4'(0)E + (1/2)a4''(0)E^2 + (1/6)a4'''(0)E^3 + ..."
    "S7  ∝ a4'''(0)  (normalized by 1/56)"
    "S7' ∝ a4''''(0) (normalized by 1/16)"

This file computes a4(E) EXACTLY for the Hodge Laplacian on coexact p-forms
on the unit S^n with the corpus's E-coupling (constant endomorphism shift
E -> E0 + u*I, u = eta*E), using the Gilkey formula quoted in the corpus:

    a4 = (4pi)^(-n/2) (1/360) int tr[ 60 R E + 180 E^2 + 30 Omega^2
         + 5 R^2 - 2 Ric^2 + 2 Riem^2 ]  (derivative terms vanish here)

Bundle data are NOT taken from convention tables -- the Omega_ij matrices of
the Lambda^p bundle are built as explicit integer derivation matrices and
their traces computed exactly (control: p=1 must give tr Omega^2 = -2n(n-1)).

KEY STRUCTURAL FACT this computation exposes: for a Laplace-type operator
with a CONSTANT shift, a4(E0 + u) is a polynomial of degree TWO in u
(terms R*E and E^2 only). Hence a4'''(0) = a4''''(0) = 0 identically, for
every bundle, every curvature, every eta. The corpus's derivation path is
vacuous as stated: nothing can be proportional to a4'''(0) except zero.
The only non-polynomial E-dependence in the sector is the determinant's,
whose derivatives round 1 already computed (no match to S7*56, S7'*16, c3).

Controls: integer arithmetic for all traces; mpmath only for the final print.
"""

from itertools import combinations
from fractions import Fraction as F
import numpy as np


def form_bundle_data(n, p):
    """Exact integer data for the Lambda^p bundle over unit S^n.

    Returns (dim, tr_Omega2, E0) where:
      tr_Omega2 = sum_{i,j} tr(Omega_ij^2)  [Levi-Civita curvature on Lambda^p]
      E0        = Gilkey endomorphism of the Hodge Laplacian on coexact
                  p-forms: Delta_H = -(nabla^2 + E0), E0 = -p(n-p) I.
    """
    dim = len(list(combinations(range(n), p)))
    basis = list(combinations(range(n), p))
    idx = {b: i for i, b in enumerate(basis)}

    def Lij(i, j):
        """so(n) generator on vectors: J_ij e_a = delta_ja e_i - delta_ia e_j,
        extended to Lambda^p as a derivation; integer matrix."""
        M = np.zeros((dim, dim), dtype=object)
        for b, bi in idx.items():
            for r, a in enumerate(b):
                if a == j:
                    tgt, s0 = i, 1
                elif a == i:
                    tgt, s0 = j, -1
                else:
                    continue
                rest = [x for k2, x in enumerate(b) if k2 != r]
                if tgt in rest:
                    continue  # wedge with a repeated index vanishes
                pos = sum(1 for x in rest if x < tgt)
                sign = s0 * (-1) ** (r + pos)
                nb_sorted = tuple(sorted(rest + [tgt]))
                M[idx[nb_sorted], bi] = M[idx[nb_sorted], bi] + sign
        return M

    trO2 = F(0)
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            M = Lij(i, j)
            M2 = M @ M
            trO2 += F(int(sum(M2[k][k] for k in range(dim))))
    E0 = -p * (n - p)
    return dim, trO2, E0


def a4_polynomial(n, p):
    """Exact coefficients of a4(u) = K * (A + B u + C u^2) for the Hodge
    Laplacian on coexact p-forms on unit S^n, shift E -> E0 + u.

    K = (4pi)^(-n/2) Vol(S^n) / 360 is factored out (never affects the
    derivative-degree argument). R = n(n-1), Ric^2 = n(n-1)^2,
    Riem^2 = 2n(n-1) on the unit sphere.
    """
    d, trO2, E0 = form_bundle_data(n, p)
    R = n * (n - 1)
    curv = 5 * R * R - 2 * n * (n - 1) ** 2 + 2 * 2 * n * (n - 1)
    A = F(60 * R * E0 * d) + F(180 * E0 * E0 * d) + F(30) * trO2 + F(curv * d)
    B = F(60 * R * d) + F(360 * E0 * d)
    C = F(180 * d)
    return d, trO2, E0, A, B, C


def main():
    print("=" * 78)
    print("E4 ROUND 2 — a4(E) heat coefficient, exact evaluation")
    print("=" * 78)

    # control: p=1 must give tr Omega^2 = -2 n (n-1)
    for n in (7, 9):
        d, trO2, _ = form_bundle_data(n, 1)
        need = -2 * n * (n - 1)
        print(f"\n[control] S^{n} Lambda^1: tr Omega^2 = {trO2} "
              f"(formula -2n(n-1) = {need}) [{'OK' if trO2 == need else 'FAIL'}]")

    for n, p, label, target, norm in [
            (7, 3, "S^7 ce3 (S7 channel)", "S7 = 1.74845220445", "1/56"),
            (9, 2, "S^9 ce2 (S7' channel)", "S7' = 0.41364465819", "1/16")]:
        d, trO2, E0, A, B, C = a4_polynomial(n, p)
        print(f"\n[{label}]  dim Lambda^{p} = {d}, E0 = {E0}, "
              f"tr Omega^2 = {trO2}")
        print(f"    a4(u) = K * (A + B u + C u^2) with")
        print(f"      A = {A} = {float(A):.6f}")
        print(f"      B = {B} = {float(B):.6f}")
        print(f"      C = {C} = {float(C):.6f}")
        print(f"    a4'''(0)  = 0   (exactly -- a4 is degree 2 in the shift)")
        print(f"    a4''''(0) = 0   (exactly)")
        print(f"    corpus claim: {target} ∝ a4-derivative, norm {norm}")
        print(f"    -> VACUOUS: zero is the only value a4'''/a4'''' can take;")
        print(f"       {target} cannot originate from this object.")

    print("\n" + "=" * 78)
    print("ROUND-2 VERDICT")
    print("=" * 78)
    print("""
    For Laplace-type operators (which include the Hodge/Beltrami sector with
    the corpus's constant endomorphism shift E_p -> E_p + eta*E), the Gilkey
    a4 is polynomial of degree 2 in the shift: the only E-dependent terms in
    the integrand are 60 R E and 180 E^2. Therefore a4'''(0) and a4''''(0)
    vanish identically -- independent of bundle rank, curvature, or eta.

    Consequences:
    1. The corpus derivation path "S7 ∝ a4'''(0), S7' ∝ a4''''(0)" is
       vacuous as stated. S7/S7' are real spectral invariants (E3, confirmed
       to 14 digits as half-determinants of the coexact towers), but they
       do NOT come from a4 E-derivatives. Their actual home is the spectral
       determinant zeta'(0; u), which IS non-polynomial in u -- and whose
       derivatives round 1 computed (D3 = 0.791..., D4 = 0.0651... on S^7),
       matching neither the published normalizations nor c3.
    2. With M1, M2, M3 (round 1) and the a4(E) path (round 2) all excluded,
       no nominated object remains that could produce c3 = -1.56371823031276.

    FINAL E4 STATUS: the T-1 identity alpha^-1 = 137.03608245 is a 7-digit
    approximation (rel. gap 6.0765e-7 to CODATA 2022) with NO known
    structural completion inside the program's current operator content.
    E4 stays on the books as the open problem, now with a complete
    exclusion record: fits (frozen scan), running (structure run), existing
    invariants (round 1), and the heat-coefficient path (round 2).
    """)


if __name__ == "__main__":
    main()
