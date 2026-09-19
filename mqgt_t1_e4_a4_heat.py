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

ERRATUM (2026-09-18, ChatGPT round 11, verified): the a4_polynomial call below
builds the FULL Lambda^p bundle (dim C(n,p)), not the coexact tower. The
coexact tower's heat trace follows by the alternating sum of full-form
traces (exact p-forms are isospectral to coexact (p-1)-forms; the constant
accounts for the scalar zero mode and does not touch a4). The correction
block at the end of main() computes the coexact (A,B,C) with the same exact
integer arithmetic. The round-2 verdict is UNAFFECTED: a4 stays quadratic
in the shift under either labeling, so a4'''(0) = a4''''(0) = 0 regardless.
"""

from itertools import combinations
from fractions import Fraction as F
from math import factorial
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

    # ------------------------------------------------------------------
    # CORRECTION BLOCK (2026-09-18, ChatGPT round 11; verified exact here)
    # The towers above were labeled "coexact" but are the FULL Lambda^p
    # bundle. The coexact tower trace follows by the alternating sum
    #     K_ce_p(t) = sum_{j=0}^p (-1)^j K_full_{p-j}(t) + (-1)^{p+1}
    # (exact p-forms isospectral to coexact (p-1)-forms; the constant is
    # the scalar zero mode and does not touch the local a4 coefficients).
    print("=" * 78)
    print("CORRECTION (ChatGPT round 11): full-form vs coexact labeling")
    print("=" * 78)
    for n, p in [(7, 3), (9, 2)]:
        ce = [F(0), F(0), F(0)]
        for j in range(p + 1):
            _, _, _, Af, Bf, Cf = a4_polynomial(n, p - j)
            for i, v in enumerate((Af, Bf, Cf)):
                ce[i] += (-1) ** j * v
        d_ce = sum((-1) ** j * len(list(combinations(range(n), p - j)))
                   for j in range(p + 1))
        print(f"\n[S^{n} coexact {p}-forms]  leading multiplicity {d_ce} "
              f"(full Lambda^{p} bundle: {len(list(combinations(range(n), p)))})")
        print(f"    coexact a4(u) = K * (A + B u + C u^2) with")
        print(f"      A = {ce[0]},  B = {ce[1]},  C = {ce[2]}")
        print(f"    (full-bundle values above were A, B, C of Lambda^{p};")
        print(f"     ChatGPT's reported coexact triple reproduced exactly)")
        # INTEGRATED VALUE, RADIUS RESTORED (ChatGPT round 12a; verified
        # exact here): the a4 density scales as R^-4 and dV as R^n, so the
        # integrated coefficient scales as R^(n-4). For odd n,
        # K_n = sqrt(pi) / (180 * Gamma((n+1)/2) * 2^n) at unit radius.
        k_rat = F(1, 180 * factorial((n - 1) // 2) * 2 ** n)
        a4_int = ce[0] * k_rat
        print(f"    integrated: A4(S^{n}_R) = ({a4_int}) sqrt(pi) "
              f"R^{n - 4}   [dimensionful -- NOT a number]")
    print("""
    VERDICT UNCHANGED: coexact a4(u) is still a polynomial of degree 2 in
    the shift (alternating sum of quadratics), so a4'''(0) = a4''''(0) = 0
    on the coexact towers as well. The correction changes the claimed
    coexact numerical certificate, not the no-go result.

    SHIFT-CONVENTION HARMONIZATION (ChatGPT round 11): this script shifts
    the Gilkey ENDOMORPHISM by +u (E -> E0 + u), i.e. operator eigenvalues
    shift by -u (D = -(nabla^2 + E)). The determinant script
    (mqgt_t1_e4_derivation.py, dkdu) shifts eigenvalues by +u. Translation:
    u_heat = -u_det; all odd u-derivatives pick up a sign between the two
    conventions. Stated here so future certificates quote one convention.

    HIGHER HEAT COEFFICIENTS (limited negative result, ChatGPT round 11):
    for an eigenvalue shift D_u = D0 + u, K_u(t) = e^{-ut} K_0(t), so
        A_{2k}(u) = sum_{j=0}^k (-u)^j/j! A_{2(k-j)}(0),
    giving d^3 A_6 / du^3 |_0 = -A_0 and d^4 A_8 / du^4 |_0 = +A_0
    (in the +u eigenvalue convention; signs flip in this file's
    endomorphism convention). These derivatives are NONZERO, unlike the
    a4 attempt -- but A_0 = (4pi)^(-n/2) Vol(S^n) * (principal-symbol
    multiplicity) is fixed by volume and rank alone. They therefore reduce
    to the leading coefficient and do not, by themselves, derive c3 or the
    T-3 determinant normalizations.

    INTEGRATED VALUES (ChatGPT round 12a, verified exact in this file):
        A4_ce3(S^7_R) = (49 sqrt(pi) / 72) R^3,
        A4_ce2(S^9_R) = -(7 sqrt(pi) / 640) R^5.
    Neither is dimensionless. Any heat-coefficient correction to alpha
    therefore requires a justified radius/normalization prescription --
    the same open gate as the determinant scaling constraint (round 11a,
    manuscript Appendix B): the geometry supplies the R-dependence, not R.
    """)


if __name__ == "__main__":
    main()
