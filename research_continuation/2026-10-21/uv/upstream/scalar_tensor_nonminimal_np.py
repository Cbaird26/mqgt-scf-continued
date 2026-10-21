"""Narain-Percacci 0911.0386 scalar-tensor nonminimal-coupling block.

Convention label NP-DE-DONDER-TYPEA (recorded, never mixed with other labels
in one solve):

  - Paper: G. Narain, R. Percacci, "On the stability of the asymptotic
    solutions of the Asymptotic Safety program", Class. Quant. Grav.
    27 (2010) 075001, arXiv:0911.0386.
  - d = 4, de-Donder gauge, optimized (Litim-shape) cutoff, single real
    scalar field.  The five-coupling system (lambda_0, xi_0, lambda_2,
    xi_2, lambda_4) with closed-form beta functions is in the paper's
    Appendix A (eqs. A1-A5); the coupling normalization is
    V = k^d sum_n lambda_{2n} phi~^{2n},  F = k^{d-2} sum_n xi_{2n} phi~^{2n},
    with phi~ = phi k^{-(d-2)/2}, so in d = 4 lambda_2 = m^2/k^2 and
    lambda_4 is the dimensionless quartic coefficient of phi^4.
  - eta = partial_t xi_0 / xi_0 = partial_t xi_0~ / xi_0~ + 2.  The system
    is implicit: eta is fixed by the xi_0 flow and partial_t xi_2 appears
    linearly on the right-hand sides of the lambda_2, xi_2 and lambda_4
    flows; both are solved algebraically here.

Verification against the paper (all reproduced by tests):
  - The d = 4 GMFP of the two-coupling system (lambda_0, xi_0):
    (0.00862, 0.02375) with critical exponents 2.143 +- 2.879 i and
    eigenvector (0.3557 +- 0.3776 i, 0.8549), obtained from a numerical
    Jacobian of the beta functions.
  - At the GMFP background with Gaussian matter (lambda_2 = xi_2 =
    lambda_4 = 0) every flow vanishes, so xi_2* = 0 is an exact fixed
    point of the nonminimal coupling.

Recorded discrepancy: the paper's closed-form entries of the stability
matrix M00 (its eqs. for M_{lambda0 lambda0} ... M_{xi0 xi0}) are NOT the
numerical derivatives of the appendix beta functions at the GMFP (e.g.
M_{lambda0 lambda0} differs by exactly +4 and M_{xi0 xi0} by ~ -2.14).
The published critical exponents and eigenvectors are reproduced by the
numerical Jacobian of the closed-form flows, so the physical claims hold;
the M00 closed forms appear to contain transcription errors (the paper
itself notes transcription errors in the precursor paper Perini2).  This
module uses the appendix flows and numerical Jacobians only.

Scaffold wiring (per species, single-scalar block applied to each scalar
independently, matching the DEP treatment of scalars as independent
singlets):  lambda_2 = m_i^2,  xi_2 = xi_i,  lambda_4 = lambda_i/4
(from V = lambda_i/4 (h^2)^2 for the radial field, i.e. the coefficient
of phi^4).  The gravity background is fixed at the GMFP of this
convention, so the xi entries do not mix the NP gauge with the DEP
gravity block.
"""
from __future__ import annotations

from math import pi


def solve_eta(lam0: float, xi0: float, lam2: float, xi2: float) -> float:
    """Anomalous-dimension eta from partial_t xi_0 = (eta - 2) xi_0.

    beta_xi0 = X + eta Y,     eta = beta_xi0/xi0 + 2  ->  eta = (X + 2 xi0)/(xi0 - Y).
    """
    den = xi0 - lam0
    X = (-2.0 * xi0 + (1.0 / (384.0 * pi**2)) *
         (25.0 - 4.0 / (1.0 + 2.0 * lam2) - 24.0 * xi2 / (1.0 + 2.0 * lam2)**2
          + 8.0 * xi0 * (7.0 * xi0 - 2.0 * lam0) / den**2))
    Y = (1.0 / (1152.0 * pi**2)) * (17.0 * xi0**2 + 18.0 * xi0 * lam0
                                    - 15.0 * lam0**2) / den**2
    return (X + 2.0 * xi0) / (xi0 - Y)


def beta_lam0_tilde(lam0: float, xi0: float, lam2: float, eta: float) -> float:
    den = xi0 - lam0
    return (-4.0 * lam0 + (1.0 / (32.0 * pi**2)) *
            (2.0 + 1.0 / (1.0 + 2.0 * lam2) + 6.0 * lam0 / den)
            + (eta / (96.0 * pi**2)) * (5.0 * xi0 - 2.0 * lam0) / den)


def beta_xi0_tilde(lam0: float, xi0: float, lam2: float, xi2: float,
                   eta: float) -> float:
    den = xi0 - lam0
    return (-2.0 * xi0 + (1.0 / (384.0 * pi**2)) *
            (25.0 - 4.0 / (1.0 + 2.0 * lam2)
             - 24.0 * xi2 / (1.0 + 2.0 * lam2)**2
             + 8.0 * xi0 * (7.0 * xi0 - 2.0 * lam0) / den**2)
            + (eta / (1152.0 * pi**2)) *
            (17.0 * xi0**2 + 18.0 * xi0 * lam0 - 15.0 * lam0**2) / den**2)


def beta_xi2_tilde(lam0: float, xi0: float, lam2: float, xi2: float,
                   lam4: float, eta: float | None = None) -> float:
    """partial_t xi_2 with the implicit partial_t xi_2 term solved.

    beta_xi2 = Z + eta W + (partial_t xi2 / xi0) V, solved for
    partial_t xi2 = (Z + eta W) / (1 - V/xi0).
    """
    if eta is None:
        eta = solve_eta(lam0, xi0, lam2, xi2)
    den = xi0 - lam0
    onel2 = 1.0 + 2.0 * lam2
    one2s2 = 1.0 + 2.0 * xi2
    Z = (1.0 / (576.0 * pi**2)) * (
        (onel2 / den) * (9.0 + 39.0 * xi0 / den + 60.0 * xi0**2 / den**2)
        + 3.0 * (3.0 + 32.0 * xi2) / den
        - 6.0 * xi0 * (11.0 + 2.0 * xi2) / den**2
        - 60.0 * xi0**2 * one2s2 / den**3
        + 216.0 * xi2 * one2s2**2 / (onel2**3 * den)
        + 9.0 * (lam0 * (5.0 - 2.0 * xi2) - 2.0 * xi0 * one2s2) * one2s2
        / (onel2 * den**2)
        + 27.0 * one2s2 * (1.0 - 10.0 * xi2 - 16.0 * xi2**2) / (onel2**2 * den)
        + 108.0 * xi0 * xi2 * one2s2**2 / (onel2**2 * den**2)
        + 72.0 * lam4 / onel2**2 * (1.0 + 12.0 * xi2 + 2.0 * lam2) / onel2)
    W = (1.0 / (1152.0 * pi**2)) * (
        (onel2 / den) * (3.0 + 18.0 * xi0 / den + 20.0 * xi0**2 / den**2)
        + 15.0 * xi2 / xi0 - 6.0 * (1.0 + xi2) / den
        - 10.0 * xi0 * (3.0 + 4.0 * xi2) / den**2
        - 20.0 * xi0**2 * one2s2 / den**3
        - 3.0 * (lam0 - xi0 * (5.0 - 4.0 * xi2)) * one2s2 / (onel2 * den**2)
        + 36.0 * xi0 * xi2 * one2s2**2 / (onel2**2 * den**2))
    V = (1.0 / (1152.0 * pi**2)) * (
        -15.0 + 54.0 * xi0 / den + 20.0 * xi0**2 / den**2
        - 6.0 * xi0 * (7.0 + 2.0 * xi2) / (onel2 * den)
        - 144.0 * xi0 * xi2 * one2s2 / (onel2**2 * den))
    return (Z + eta * W) / (1.0 - V / xi0)


def beta_lam2_tilde(lam0: float, xi0: float, lam2: float, xi2: float,
                    lam4: float, eta: float | None = None) -> float:
    """partial_t lambda_2 including the solved partial_t xi_2 term."""
    if eta is None:
        eta = solve_eta(lam0, xi0, lam2, xi2)
    den = xi0 - lam0
    onel2 = 1.0 + 2.0 * lam2
    one2s2 = 1.0 + 2.0 * xi2
    dxi2 = beta_xi2_tilde(lam0, xi0, lam2, xi2, lam4, eta)
    main = (1.0 / (48.0 * pi**2)) * (
        9.0 * lam0 * one2s2 / (2.0 * den**2)
        - 9.0 * (2.0 * lam0 - xi0) * one2s2**2 / (2.0 * onel2 * den**2)
        - 9.0 * one2s2**2 / (2.0 * onel2**2 * den)
        - 18.0 * lam4 / onel2**2)
    eta_part = (eta / (96.0 * pi**2)) * (
        -2.0 * xi2 / xi0 + 3.0 * xi0 * one2s2 / (2.0 * den**2)
        - 3.0 * xi0 * one2s2**2 / (2.0 * onel2 * den**2))
    dxi_part = (dxi2 / xi0) * (1.0 / (96.0 * pi**2)) * (
        2.0 - 3.0 * xi0 / den + 6.0 * xi0 * one2s2 / (onel2 * den))
    return -2.0 * lam2 + main + eta_part + dxi_part


def beta_lam4_tilde(lam0: float, xi0: float, lam2: float, xi2: float,
                    lam4: float, eta: float | None = None) -> float:
    """partial_t lambda_4 including the solved partial_t xi_2 term."""
    if eta is None:
        eta = solve_eta(lam0, xi0, lam2, xi2)
    den = xi0 - lam0
    onel2 = 1.0 + 2.0 * lam2
    one2s2 = 1.0 + 2.0 * xi2
    dxi2 = beta_xi2_tilde(lam0, xi0, lam2, xi2, lam4, eta)
    common = 6.0 * one2s2**2 / onel2**2 - 10.0 * one2s2 / onel2 + 5.0
    main = (1.0 / (48.0 * pi**2)) * (
        (9.0 / (4.0 * den**2)) * (5.0 * onel2 * (1.0 + 4.0 * xi2)
                                  - one2s2 * (21.0 + 62.0 * xi2)
                                  + 33.0 * one2s2**3 / onel2
                                  - one2s2**3 * (23.0 + 24.0 * xi2) / onel2**2
                                  + 6.0 * one2s2**4 / onel2**3)
        + 9.0 * xi0 * (xi2 - lam2)**2 * common / den**3
        - 72.0 * lam2 * lam4 * one2s2 * (1.0 - 4.0 * lam2 + 6.0 * xi2)
        / (den * onel2**3)
        + 9.0 * xi0 * lam4 * common / den**2
        + 216.0 * lam4**2 / onel2**3)
    eta_part = (eta / (96.0 * pi**2)) * (
        2.0 * xi2**2 / xi0**2
        + 3.0 * xi0 * (xi2 - lam2)**2 * common / den**3
        + 3.0 * xi0 * lam4 * common / den**2)
    dxi_part = (dxi2 / xi0) * (1.0 / (96.0 * pi**2)) * (
        -2.0 * xi2 / xi0
        - 3.0 * xi0 * (xi2 - lam2) / den**2
        * (12.0 * one2s2**2 / onel2**2 - 21.0 * one2s2 / onel2 + 10.0)
        - 24.0 * xi0 * lam4 * (1.0 - 4.0 * lam2 + 6.0 * xi2)
        / (onel2**2 * den))
    return main + eta_part + dxi_part


def beta_gmfp_pair(lam0: float, xi0: float, lam2: float = 0.0,
                   xi2: float = 0.0, lam4: float = 0.0) -> tuple[float, float]:
    """The (partial_t lambda_0, partial_t xi_0) pair with eta solved."""
    eta = solve_eta(lam0, xi0, lam2, xi2)
    return (beta_lam0_tilde(lam0, xi0, lam2, eta),
            beta_xi0_tilde(lam0, xi0, lam2, xi2, eta))


GMFP_LAM0_STAR = 0.008620067353898883
GMFP_XI0_STAR = 0.023754680481913166
"""Exact solution of the paper's d = 4 two-coupling GMFP equations, i.e.
24 lambda_0 (16 pi^2 + 1/(lambda_0 - xi_0)) = 19 and
(265 - 2304 pi^2 xi_0) xi_0 + (127 + 2304 pi^2 xi_0) lambda_0
= 160 lambda_0^2/(lambda_0 - xi_0), matching the published rounded values
(lambda_0*, xi_0*) = (0.00862, 0.02375)."""


def beta_xi_matter(lam2: float, xi2: float, lam4: float) -> float:
    """Scaffold entry: partial_t xi_i for one scalar species.

    Evaluated on the NP GMFP gravity background (lambda_0*, xi_0*) with
    eta = 2 (its exact fixed-point value), and the per-species mapping
    lam2 = m_i^2, xi2 = xi_i, lam4 = lambda_i/4.
    """
    return beta_xi2_tilde(GMFP_LAM0_STAR, GMFP_XI0_STAR, lam2, xi2, lam4,
                          eta=2.0)
