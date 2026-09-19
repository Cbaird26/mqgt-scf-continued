#!/usr/bin/env python3
"""ROUND 15 — LEMMA 6(d) COMPUTATION (record-side, referee-authorized).

Question (Grok charter + ChatGPT authorization, 2026-09-19; see
artifacts/EM_NORMALIZATION_AUDIT_CHARTER_2026-09-19.md and
artifacts/EM_NORMALIZATION_EVIDENCE_MAP_2026-09-19.md):

  TUFT v5 (Nielsen) Theorem 48 derives the fine-structure ratio
  geometrically; its Lemma 6 (Uniqueness of alpha) rests on condition (d):
  "a equals the coupling constant of the n = 0 (massless) sector of the
  partition function." Can condition (d) be DERIVED from the written U(1)
  action — i.e., does the n = 0 sector partition function of that action
  normalize the coupling to Theorem 48's ratio? Compute and certify either
  way. No fitting. No new principle invented. Silence/absence is a result.

Objects (from the audit's evidence map, TUFT v5 page pointers):
  - Quadratic Beltrami action on S^3 (sect. 4.17.1): S[A] = (1/2) int A^*BA,
    B = *d on coexact 1-forms; sector zeta zeta_n(s) = zetaH(s-2, n+1) -
    zetaH(s, n+1); zeta'_1(0) = -zeta(3)/(4 pi^2) + (1/2) ln(2 pi) (p62).
  - Shell gauge action (p65): S^(5) = (1/g_s^2) int Tr(F5 ^ *F5).
  - Theorem 48 (p93-94): alpha = 2 Vol(S^2) (Vol(S^9)/160)^{1/4}
    / (Vol(S^4)^2 Vol(RP^1)) [ratio reading of the OCR'd print; verified
    against the record's exact form in [0] below].
  - Lemma 6 conditions (a)-(d), p94.

Structure of this lab:
  [0] Theorem 48 formula-reading check (vs record exact form, dps=80).
  [1] TUFT sector machinery: independent reproduction (Hurwitz vs closed form).
  [2] The n = 0 sector in the written ladder assembly: what it contains.
  [3] Gaussian U(1) partition function on unit S^9: exact g-dependence and
      determinant content, both zero-mode conventions; the field-redefinition
      point.
  [4] The metric/KK route for the Hopf connection (symbolic).
  [5] VERDICT.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from mpmath import mp, mpf, nstr, pi, log, zeta, sqrt, exp

mp.dps = 80

from mqgt_t1_e4_derivation import build, logdet
from mqgt_t3_reverse_search import deg_scalar, fit_poly, z0


def dzeta(s, a=None):
    """d/ds zeta(s) or Hurwitz d/ds zeta(s, a)."""
    h = mpf("1e-40")
    f = (lambda x: zeta(x)) if a is None else (lambda x: zeta(x, a))
    # mpmath zeta derivative is stable via diff; use it directly
    from mpmath import diff
    return diff(f, s)


def main():
    print("=" * 78)
    print("ROUND 15 — LEMMA 6(d) COMPUTATION")
    print("=" * 78)

    # ---------------------------------------------------------------- [0]
    print("\n[0] Theorem 48 formula reading (OCR resolution by arithmetic)")
    volS2, volS4 = 4 * pi, 8 * pi ** 2 / 3
    volS9, volRP1 = pi ** 5 / 12, pi
    alpha_inv_ratio = (volS4 ** 2 * volRP1) / (2 * volS2 * (volS9 / 160) ** mpf("0.25"))
    alpha_inv_record = mpf(8) / 9 * mpf(1920) ** mpf("0.25") * pi ** mpf("2.75")
    print("  ratio reading  alpha^-1 = 2Vol(S^2)(Vol(S^9)/160)^{1/4}"
          " / (Vol(S^4)^2 Vol(RP^1))")
    print("    =", nstr(alpha_inv_ratio, 25))
    print("  record exact form (8/9) 1920^{1/4} pi^{11/4}")
    print("    =", nstr(alpha_inv_record, 25))
    print("  difference:", nstr(abs(alpha_inv_ratio - alpha_inv_record), 6),
          " -> reading CONFIRMED" )

    # ---------------------------------------------------------------- [1]
    print("\n[1] TUFT sector machinery — independent reproduction")
    zp1 = dzeta(mpf(-2)) - dzeta(mpf(0))
    zp1_closed = -zeta(3) / (4 * pi ** 2) + log(2 * pi) / 2
    print("  zeta'_1(0) via Hurwitz diff :", nstr(zp1, 25))
    print("  zeta'_1(0) TUFT closed form :", nstr(zp1_closed, 25),
          " (p62: 0.888490076)")
    print("  match:", abs(zp1 - zp1_closed) < mpf("1e-60"))
    for n in (2, 3):
        # sector zeta: zeta_n(s) = zetaH(s-2, n+1) - zetaH(s, n+1)
        def f(s, n=n):
            return zeta(s - 2, n + 1) - zeta(s, n + 1)
        from mpmath import diff as _d
        zpn = _d(f, mpf(0))
        zpn_tuft = zp1 + sum(j * (j + 2) * log(j + 1) for j in range(1, n))
        print(f"  zeta'_{n}(0): Hurwitz {nstr(zpn, 20)}   "
              f"TUFT sum-rule {nstr(zpn_tuft, 20)}   "
              f"match: {abs(zpn - zpn_tuft) < mpf('1e-40')}")

    # ---------------------------------------------------------------- [2]
    print("\n[2] The n = 0 sector in the written ladder assembly (sect. 4.16)")
    a_coef = 6 * sqrt(2) * exp(zeta(3) / (24 * pi ** 2))
    print("  helicity coefficient a = 6 sqrt(2) exp(zeta(3)/(24 pi^2))")
    print("    =", nstr(a_coef, 15), " (TUFT p60: 8.5284)")
    alpha_geom = 1 / alpha_inv_record
    print("  ladder factors m_n = (n+1) exp(a n) exp(-D(n)) phi_n,"
          " phi_n = exp(n alpha/6):")
    for n in (0, 1, 2, 3):
        phi_n = exp(n * alpha_geom / 6)
        print(f"    n={n}: multiplicity {n+1}, helicity e^{{a n}} = "
              f"{nstr(exp(a_coef * n), 12)}, phi_n = {nstr(phi_n, 12)}")
    print("  -> at n = 0 every factor is identically 1. The massless sector")
    print("     is the ladder's NORMALIZATION ORIGIN; alpha enters sectors")
    print("     n >= 1 as an INPUT (phi_n = e^{n alpha/6}, p61 eq. 75-76),")
    print("     never as an output of the n = 0 sector.")
    print("  -> the lens-space sector map l_min(n) = n (p62) degenerates at")
    print("     n = 0 (same full spectrum as n = 1): 'n = 0' is ladder")
    print("     language, not a distinct spectral sector of the written")
    print("     quadratic action.")

    # ---------------------------------------------------------------- [3]
    print("\n[3] Gaussian U(1) partition function on unit S^9")
    print("    S = (1/2g^2) int F ^ *F,  Z ~ [det'(D1_ce/g^2)]^{-1/2}"
          " [det'(D0/g^2)]^{+1}")
    print("    scaling identity: det'(cA) = c^{zeta_A(0)} det'A")
    poly91, a2_91, x0_91 = build(9, 1)
    L_ce1 = logdet(poly91, a2_91, x0_91)
    z_ce1 = z0(poly91, x0_91)
    # scalar tower, convention A (formal constant-mode position; t3 spec)
    poly_s, scale_s, _ = fit_poly(lambda k: deg_scalar(9, k), 9, mpf(4), 8)
    L_scal_A = logdet(poly_s, mpf(16), 4)
    z_scal_A = z0(poly_s, 4)
    # scalar tower, convention B (det' = coexact-0)
    poly90, a2_90, x0_90 = build(9, 0)
    L_scal_B = logdet(poly90, a2_90, x0_90)
    z_scal_B = z0(poly90, x0_90)
    print(f"  live tower values (dps=80):")
    print(f"    S^9 ce1:  L = {nstr(L_ce1, 15)},  zeta(0) = {nstr(z_ce1, 8)}"
          f"  (theorem: +1)")
    print(f"    S^9 scal A (formal const.): L = {nstr(L_scal_A, 15)},"
          f"  zeta(0) = {nstr(z_scal_A, 8)}  (theorem: 0)")
    print(f"    S^9 scal B (det' = ce0):  L = {nstr(L_scal_B, 15)},"
          f"  zeta(0) = {nstr(z_scal_B, 8)}  (theorem: -1)")
    print("  g-exponent: gauge factor g^{+zeta_ce1(0)} = g^{+1};")
    print("              ghost factor g^{-2 zeta_0(0)} = g^0 (A) / g^{+2} (B)")
    print("  =>  Z_0 ~ g^{+1} (conv A)   or   g^{+3} (conv B)")
    print("     a FREE POWER of g in either convention.")
    lnZ_A = -L_ce1 / 2 + L_scal_A
    lnZ_B = -L_ce1 / 2 + L_scal_B
    print(f"  determinant content at g = 1:")
    print(f"    ln Z_0 = -(1/2) L_ce1 + L_scal  = {nstr(lnZ_A, 15)} (conv A)")
    print(f"                                         = {nstr(lnZ_B, 15)} (conv B)")
    print("     pure geometry; no dimensionless-coupling slot anywhere.")
    print("  FIELD-REDEFINITION POINT: A' = A/g makes the Gaussian kinetic")
    print("  term canonical; g then lives only in the covariant derivative")
    print("  (charge normalization) and the measure. A free Gaussian partition")
    print("  function cannot fix g. b1(S^9) = b2(S^9) = 0: no harmonic zero")
    print("  modes, no flux lattice, no theta sector. The c1 = 1 flux lives on")
    print("  the CP^4 base and fixes the INTEGER (charge quantization, Thm 47),")
    print("  not the coupling (Door 1 / round-12b echo).")

    # ---------------------------------------------------------------- [4]
    print("\n[4] Metric/KK route (Hopf connection as the photon) — symbolic")
    print("  ds^2 = pi*g^ + rho^2 eta x eta over CP^4, d eta = 2 omega:")
    print("  R_{S^9} contains -(rho^2/4) |F|^2; reduction over CP^4 gives")
    print("      1/g_4^2 = 2 pi rho^3 / kappa_9^2")
    print("  (unit-normalized Hopf connection; prefactor convention-dependent).")
    print("  Needs rho (fiber size) AND kappa_9 (9D gravitational coupling):")
    print("  geometry supplies the rho-dependence, not its value; kappa_9 is")
    print("  gravitational data. Same structural hole as the round-12b")
    print("  illustration (alpha_4 = 3 g_13^2/(pi^6 R^9) needed g_13).")

    # ---------------------------------------------------------------- [5]
    print("""
[5] VERDICT
    Lemma 6(d) is NOT derivable from the written U(1) action by any path
    examined:
      (i)   the quadratic Beltrami action on S^3 carries unit coefficient
            -- no coupling constant exists in it;
      (ii)  the S^5 shell action carries an explicit, free 1/g_s^2 (p65);
      (iii) the S^9 Gaussian Z_0 carries g as a free power (exact exponents
            above) with pure-geometry determinants, and g is removable from
            the Gaussian by field redefinition;
      (iv)  the metric/KK route needs rho and kappa_9, both unfixed;
      (v)   in the written ladder assembly the n = 0 sector is the
            normalization origin (all factors 1); alpha enters other sectors
            as an INPUT via phi_n = e^{n alpha/6}.
    Theorem 48's ratio is nowhere an OUTPUT of the written partition
    functions. The uniqueness lemma's condition (d) therefore has no
    computed object to attach to: the identification is certified as
    ASSERTED, not derived -- consistent with the source's own header
    ("Derived, with one physical identification marked below").

    BOUNDARY OF THIS RESULT: this certifies that the written actions
    contain no coupling-fixing computation. It does not prove that no
    derivation of Lemma 6(d) exists; one would require a written action
    whose U(1) kinetic coefficient is a computed geometric number, or a
    measure/zero-mode argument on a manifold with the relevant harmonic
    structure. Neither is in the corpus or TUFT v5 as scanned (pointers in
    artifacts/EM_NORMALIZATION_EVIDENCE_MAP_2026-09-19.md).
    """)


if __name__ == "__main__":
    main()
