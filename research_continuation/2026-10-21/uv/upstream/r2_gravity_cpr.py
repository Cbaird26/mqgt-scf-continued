"""One-loop curvature-squared (R^2) gravity block, Codello-Percacci-Rahmede.

Convention (recorded per FRG_PROJECTION_PROTOCOL_V0_1.md):

- arXiv:0805.2909 (Annals Phys. 324 (2009) 414), the curvature-squared
  truncation section: one-loop approximation, type III generalized optimized
  cutoff R^(n)_k(z) = (a k^n - z) theta(a k^n - z) with a = 1, and the
  Shapiro et al. gauge choice that makes the quadratic action minimal fourth
  order.
- Action ansatz:  S = int sqrt(g) [1/(2 lambda) C^2 + 1/xi R^2 - 1/rho E].
  lambda is the Weyl-squared coupling, xi the R^2 coupling, rho the Euler
  coupling (the 1/tau del^2 R term is a total derivative in d = 4).
- Beta functions, eq. (rsqkj) of the source, verbatim:
      beta_lambda = -(133/10) lambda^2 / (4 pi)^2
      beta_xi     = -(10 lambda^2 - 5 lambda xi + 5 xi^2/36) / (4 pi)^2
      beta_rho    =  (196/45) rho^2 lambda / (4 pi)^2
  With omega = -3 lambda/xi and theta = lambda/rho:
      beta_omega = -(25 + 1098 omega + 200 omega^2) lambda / (60 (4 pi)^2)
      beta_theta =  7 (56 - 171 theta) lambda / (90 (4 pi)^2)
  Fixed points: omega_* in {-5.467, -0.0228} (second root is the UV
  attractive one used in the paper), theta_* = 56/171 ~ 0.3275.  The omega
  conversion is exactly consistent with (beta_lambda, beta_xi) via the chain
  rule (checked algebraically and numerically).
- Newton/cosmological-constant flow including the R^2 couplings (eq. (piero)
  of the source):
      q(omega) = (83 + 70 omega + 8 omega^2)/(18 pi)
      beta_G_tilde      = 2 G - lambda4 G (3 + 26 omega - 40 omega^2)
                          / (12 omega (4 pi)^2) - q(omega) G^2
      beta_Lambda_tilde = -2 L + [lambda4^2 (1 + 20 omega^2)/(256 pi G omega^2)
                          + lambda4 L (1 + 86 omega + 40 omega^2)/(12 omega)]
                          /(4 pi)^2 - lambda4 (1 + 10 omega)/(64 pi^2 omega)
                          + 2 G/pi - q(omega) G L
  (lambda4 denotes the Weyl coupling to avoid confusion with L.)  At
  lambda4 = 0, omega = omega_*:  Lambda_tilde_* = 1/(pi q_*) ~ 0.221,
  G_tilde_* = 2/q_* ~ 1.389, critical exponents 2 and 4.
- PAPER-INTERNAL NOTE (verified against the v5 LaTeX source): beta_omega
  follows exactly from (beta_lambda, beta_xi) by the chain rule with
  omega = -3 lambda/xi.  The printed beta_theta = 7(56 - 171 theta) lambda /
  (90 (4 pi)^2) does NOT follow from beta_rho by the chain rule with
  theta = lambda/rho (the chain rule gives
  -(133/10) lambda (theta + theta_star lambda)/(4 pi)^2); the theta sector is
  decoupled from every other coupling at this order, so the discrepancy does
  not affect any wired coordinate, and theta_star = 56/171 is used as printed.
- Scaffold coordinates a_R2 = 1/xi and a_C2 = 1/(2 lambda4), defined only for
  a_C2 != 0 (the 1/(2 lambda4) parametrization is singular at the Gaussian
  point):
      beta_{a_C2} = 133/(320 pi^2)      (constant, from beta_lambda)
      beta_{a_R2} = (10 x^2 - 5 x + 5/36)/(4 pi)^2,  x = a_R2/(2 a_C2)
- NO-FIXED-POINT RECORD (one-loop block): beta_{a_C2} = 133/(320 pi^2)
  ~ 0.04211 is strictly positive and constant, so the C^2 (Weyl-squared)
  direction runs away and this one-loop truncation has NO fixed point for
  a_C2.  beta_{a_R2} vanishes on the two lines a_R2 = 2 x a_C2 with
  x in {0.0295207, 0.4704793} (the roots of 10 x^2 - 5 x + 5/36 = 0), but
  since a_C2 never stops the (a_R2, a_C2) subsystem has no true fixed
  point either.  This matches the standard one-loop expectation that the
  C^2 coupling is not asymptotically free in this truncation; it is
  recorded as a negative result, not papered over.

All coefficients trace to the equations above; nothing is guessed.
"""
from __future__ import annotations

from math import pi

import numpy as np


def q_omega(omega: float) -> float:
    """q(omega) = (83 + 70 omega + 8 omega^2)/(18 pi), eq. (piero)."""
    return (83.0 + 70.0 * omega + 8.0 * omega**2) / (18.0 * pi)


def omega_fixed_points() -> tuple[float, float]:
    """Roots of beta_omega = 0: (UV-repulsive, UV-attractive)."""
    disc = (1098.0**2 - 4.0 * 200.0 * 25.0) ** 0.5
    return ((-1098.0 - disc) / 400.0, (-1098.0 + disc) / 400.0)


def theta_star() -> float:
    """Fixed point of beta_theta = 0: 56/171 ~ 0.3275."""
    return 56.0 / 171.0


def beta_lambda_rsq(lam: float) -> float:
    """beta of the Weyl coupling lambda, eq. (rsqkj)."""
    return -(133.0 / 10.0) * lam**2 / (4.0 * pi) ** 2


def beta_xi_rsq(lam: float, xi: float) -> float:
    """beta of the R^2 coupling xi, eq. (rsqkj)."""
    return -(10.0 * lam**2 - 5.0 * lam * xi + 5.0 * xi**2 / 36.0) / (4.0 * pi) ** 2


def beta_rho_rsq(lam: float, rho: float) -> float:
    """beta of the Euler coupling rho, eq. (rsqkj)."""
    return (196.0 / 45.0) * rho**2 * lam / (4.0 * pi) ** 2


def beta_omega_rsq(lam: float, omega: float) -> float:
    """beta of omega = -3 lambda/xi, as printed in the paper."""
    return -(25.0 + 1098.0 * omega + 200.0 * omega**2) * lam / (60.0 * (4.0 * pi) ** 2)


def beta_theta_rsq(lam: float, theta: float) -> float:
    """beta of theta = lambda/rho, as printed in the paper."""
    return 7.0 * (56.0 - 171.0 * theta) * lam / (90.0 * (4.0 * pi) ** 2)


def beta_g_tilde_rsq(g: float, lam: float, omega: float) -> float:
    """beta of G_tilde including the R^2 couplings, eq. (piero)."""
    return (2.0 * g - lam * g * (3.0 + 26.0 * omega - 40.0 * omega**2)
            / (12.0 * omega * (4.0 * pi) ** 2) - q_omega(omega) * g**2)


def beta_lambda_tilde_rsq(lam_t: float, g: float, lam: float, omega: float) -> float:
    """beta of Lambda_tilde including the R^2 couplings, eq. (piero)."""
    inner = (lam**2 * (1.0 + 20.0 * omega**2) / (256.0 * pi * g * omega**2)
             + lam * lam_t * (1.0 + 86.0 * omega + 40.0 * omega**2) / (12.0 * omega))
    return (-2.0 * lam_t + inner / (4.0 * pi) ** 2
            - lam * (1.0 + 10.0 * omega) / (64.0 * pi**2 * omega)
            + 2.0 * g / pi - q_omega(omega) * g * lam_t)


def r2_newton_fixed_point() -> tuple[float, float]:
    """(Lambda_tilde*, G_tilde*) at lam = 0, omega = omega_* (one loop)."""
    omega_star = omega_fixed_points()[1]
    q_star = q_omega(omega_star)
    return (1.0 / (pi * q_star), 2.0 / q_star)


def a_r2_beta(a_r2: float, a_c2: float) -> float:
    """beta of the scaffold coordinate a_R2 = 1/xi, defined for a_c2 != 0."""
    if a_c2 == 0.0:
        return np.nan
    x = a_r2 / (2.0 * a_c2)
    return (10.0 * x**2 - 5.0 * x + 5.0 / 36.0) / (4.0 * pi) ** 2


def a_c2_beta() -> float:
    """beta of the scaffold coordinate a_C2 = 1/(2 lambda): 133/(320 pi^2)."""
    return 133.0 / (320.0 * pi**2)
