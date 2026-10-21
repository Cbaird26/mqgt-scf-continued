"""Gravity-matter coupled Einstein-Hilbert system with Litim regulator.

Declared convention (recorded per FRG_PROJECTION_PROTOCOL_V0_1.md):

- Euclidean signature, d dimensions (default 4), t = ln(k/k0).
- Background split g = gbar + sqrt(32 pi G) h; background-covariant gauge
  fixing with alpha = rho = 1 (Dona-Eichhorn-Percacci 1311.2898 eqs. 9-11);
  Faddeev-Popov ghosts retained.
- Regulator of type II for gravitons, Litim shape function
  r(p^2/k^2) = (k^2/p^2 - 1) theta(k^2 - p^2), eq. (19) of 1311.2898.
- Matter: N_S real scalars, N_D Dirac fermions, N_V vectors, all massless
  and minimally coupled; fermions use the type-II cutoff (see 1311.2898).
- Couplings: Lambda_tilde = Lambda k^(-2), G_tilde = G k^(2-d).

This is a different gauge/parametrization than the alpha -> infinity
TYPE A convention of gravity_frg.py.  Both are recorded conventions of the
optimized regulator family; neither is a silently guessed coefficient.
Beta functions and anomalous dimensions below are eqs. (21)-(34) of
arXiv:1311.2898 verbatim.

DISCREPANCY NOTE (ruling, verified against the published LaTeX source
Constraints_on_matter_K.tex of arXiv:1311.2898): the beta functions (21)-(22),
the coefficients a-f of eqs. (23)-(28) and the matter eta formulas are
reproduced verbatim, and with the fixed-point anomalous dimensions of Tables
1/3/5 inserted they vanish at every tabulated fixed point (|beta| ~ 1e-4).
The one-loop anomalous dimensions of the TABLES (eta_h = G~ a(Lambda~) +
matter constants, eta_c = 2*2^{[d/2]} G~ b(Lambda~), and the printed one-loop
eta_S, eta_D, eta_V) reproduce every table entry (fixed points, critical
exponents and all anomalous dimensions) to the printed precision.  The printed
eq. (28) for eta_c (ghost_factor=1) gives |eta_c| ~ 8x smaller than the
tabulated values; at the pure-gravity fixed point the ratio is exactly
eta_c(tab)/[G~ b(Lambda~)] = 8.0008 = 2*2^{[d/2]}, so the source file omits
this factor in eq. (28) (an internal omission: the tables are self-consistent
with beta = 0 at every row, and the tabulated eta_c = -0.806 agrees with the
independent literature value eta_c ~ -0.78 of Eichhorn & Gies, PRD 81, 104026
(2010), whereas the printed equation would give -0.10).  The RG-improved
("full-II") columns are only approximately reproduced (few % in the pure-gravity
case; the SM row drifts further), so the improved system as printed is not
exactly reproducible and full-II entries are used as indicative benchmarks
only.  Default below is the PRINTED convention (ghost_factor=1); pass
ghost_factor=2*2^{[d/2]} for the table convention.
"""
from __future__ import annotations

from math import gamma, pi

import numpy as np

D = 4.0
SPINOR_WEIGHT = 2.0 ** int(D // 2)
PREFACTOR = 32.0 * pi / ((4.0 * pi) ** (D / 2.0) * gamma(D / 2.0))


def _inv(lam: float) -> float:
    return 1.0 / (1.0 - 2.0 * lam)


def a_coeff(lam: float, d: float = D) -> float:
    den = (4.0 * pi) ** (d / 2.0) * gamma(d / 2.0) * d**2 * (d**2 - 4.0) * (3.0 * d - 2.0) * (1.0 - 2.0 * lam) ** 4
    a0 = -4.0 * pi * (d - 2.0) * (-896 + 264*d + 1076*d**2 - 434*d**3 + 21*d**4 + d**5)
    a1 = 16.0 * pi * (d - 2.0) * (-2048 + 2552*d - 318*d**2 - 125*d**3 + 2*d**4 + d**5)
    a2 = -16.0 * pi * (12544 - 25760*d + 16968*d**2 - 4228*d**3 + 354*d**4 - 17*d**5 + d**6)
    a3 = 4096.0 * pi * (d - 2.0) * (-32 + 50*d - 19*d**2 + 2*d**3)
    a4 = -2048.0 * pi * (d - 2.0) * (-32 + 50*d - 19*d**2 + 2*d**3)
    return (a0 + a1*lam + a2*lam**2 + a3*lam**3 + a4*lam**4) / den


def c_coeff(lam: float, d: float = D) -> float:
    den = (4.0 * pi) ** (d / 2.0) * gamma(d / 2.0) * d**2 * (d + 2.0) * (d + 4.0) * (3.0 * d - 2.0) * (1.0 - 2.0 * lam) ** 3
    return 8.0 * pi * (d - 1.0) * (128 + 720*d - 350*d**2 + 29*d**3 + 32*(d - 2.0)*(d + 4.0)*lam) / den


def e_coeff(lam: float, d: float = D) -> float:
    den = (4.0 * pi) ** (d / 2.0) * gamma(d / 2.0) * d**2 * (d + 2.0) * (d + 4.0) * (3.0 * d - 2.0)
    return -128.0 * pi * (32 - 50*d + 23*d**2) / den


def b_coeff(lam: float, d: float = D) -> float:
    den = (4.0 * pi) ** (d / 2.0) * gamma(d / 2.0) * d**2 * (d**2 - 4.0) * (d + 4.0) * (1.0 - 2.0 * lam) ** 2
    return 64.0 * pi * (-8 + 4*d + 18*d**2 - 7*d**3 + 2*(4 - 9*d**2 + 3*d**3)*lam) / den


def d_coeff(lam: float, d: float = D) -> float:
    den = (4.0 * pi) ** (d / 2.0) * gamma(d / 2.0) * d**2 * (d**2 - 4.0) * (d + 4.0) * (1.0 - 2.0 * lam) ** 2
    return -64.0 * pi * (4 - 4*d - 9*d**2 + 4*d**3) / den


def f_coeff(lam: float, d: float = D) -> float:
    den = (4.0 * pi) ** (d / 2.0) * gamma(d / 2.0) * d**2 * (d**2 - 4.0) * (d + 4.0) * (1.0 - 2.0 * lam) ** 2
    return -64.0 * pi * (4 - 9*d**2 + 3*d**3) / den


def eta_system(lam: float, g: float, n_s: float = 0.0, n_d: float = 0.0,
               n_v: float = 0.0, d: float = D, improved: bool = True,
               ghost_factor: float = 1.0) -> tuple[float, ...]:
    """Anomalous dimensions (eta_h, eta_c, eta_S, eta_D, eta_V).

    `improved=True` solves the linear system eq. (48) of 1311.2898 (RG
    improvement, the eta's appear on both sides).  `improved=False` keeps
    the leading one-loop terms only.

    `ghost_factor` multiplies the eta_c source b(Lambda~): 1.0 is the
    printed eq. (28); 2*2^{[d/2]} is the convention used in the paper's
    Tables 1/3/5 (see the module docstring for the discrepancy note).
    """
    inv = _inv(lam)
    s = PREFACTOR * g  # 32 pi G / ((4 pi)^(d/2) Gamma(d/2)) for matter terms

    # Matter contributions to eta_h (eq. 27 of 1311.2898): constant terms.
    mat_h_const = (- n_s * s * (d - 2.0)**3 / (d**2 * (d + 2.0) * (3.0*d - 2.0))
                   + n_d * SPINOR_WEIGHT * (s / 2.0) * 2.0 * (d - 1.0) * (d - 2.0) / (d**3 * (3.0*d - 2.0))
                   - n_v * s * (d - 1.0) * (d - 2.0) * (d**2 - 12.0*d + 8.0) / (d**2 * (d + 2.0) * (3.0*d - 2.0)))

    if not improved:
        eta_h = g * a_coeff(lam, d) + mat_h_const
        eta_c = ghost_factor * g * b_coeff(lam, d)
        eta_s = -s * (2.0/(d + 2.0) * inv**2 + 2.0/(d + 2.0) * inv + (d + 1.0)*(d - 4.0)/(2.0*d) * inv**2)
        eta_d = s * ((d - 1.0)*(d**2 + 9.0*d - 8.0)/(8.0*d*(d - 2.0)*(d + 1.0)) * inv**2
                     + (d - 1.0)**2/(2.0*d*(d + 1.0)*(d - 2.0)) * inv
                     - (d - 1.0)*(2.0*d**2 - 3.0*d - 4.0)/(4.0*d*(d - 2.0)) * inv**2)
        eta_v = -s * ((d - 1.0)*(16.0 + 10.0*d - 9.0*d**2 + d**3)/(2.0*d**2*(d - 2.0)) * inv**2
                      + 4.0*(d - 1.0)*(2.0*d - 5.0)/(d*(d**2 - 4.0)) * inv
                      + 4.0*(d - 1.0)*(2.0*d - 5.0)/(d*(d**2 - 4.0)) * inv**2)
        return eta_h, eta_c, eta_s, eta_d, eta_v

    a, c, e = a_coeff(lam, d), c_coeff(lam, d), e_coeff(lam, d)
    b, dd, f = b_coeff(lam, d), d_coeff(lam, d), f_coeff(lam, d)

    m = np.zeros((5, 5))
    v = np.zeros(5)

    # eta_h row: eqs. (23)-(27): a, c, e carry their own (4 pi)^(d/2) Gamma(d/2)
    # denominators, hence multiply G~ directly (not s).
    v[0] = g * a + mat_h_const
    m[0, 0] = 1.0 - g * c
    m[0, 1] = -g * e
    m[0, 2] = n_s * s * 2.0 * (8.0 - 10.0*d + d**2) / (d**2 * (d + 2.0) * (3.0*d - 2.0) * (d + 4.0))
    m[0, 3] = -n_d * SPINOR_WEIGHT * (s / 2.0) * (d - 1.0) * (d - 2.0)**2 / (d**3 * (3.0*d - 2.0) * (d + 1.0))
    m[0, 4] = -n_v * s * 2.0 * (16.0 - d) * (d - 1.0) * (d - 2.0) / (d**2 * (d + 2.0) * (3.0*d - 2.0) * (d + 4.0))

    v[1] = ghost_factor * g * b
    m[1, 0] = -g * dd
    m[1, 1] = 1.0 - g * f

    v[2] = -s * (2.0/(d + 2.0) * inv**2 + 2.0/(d + 2.0) * inv + (d + 1.0)*(d - 4.0)/(2.0*d) * inv**2)
    m[2, 0] = -s * (2.0/(d + 2.0) * inv**2 / (d + 4.0) + (d + 1.0)*(d - 4.0)/(2.0*d) * inv**2 / (d + 2.0))
    m[2, 2] = 1.0 + s * 2.0/(d + 2.0) * inv / (d + 4.0)

    v[3] = s * ((d - 1.0)*(d**2 + 9.0*d - 8.0)/(8.0*d*(d - 2.0)*(d + 1.0)) * inv**2
                - (d - 1.0)*(2.0*d**2 - 3.0*d - 4.0)/(4.0*d*(d - 2.0)) * inv**2)
    m[3, 0] = -s * ((d - 1.0)*(d**2 + 9.0*d - 8.0)/(8.0*d*(d - 2.0)*(d + 1.0)) * inv**2 / (d + 3.0)
                    - (d - 1.0)*(2.0*d**2 - 3.0*d - 4.0)/(4.0*d*(d - 2.0)) * inv**2 / (d + 2.0))
    m[3, 3] = 1.0 + s * (d - 1.0)**2/(2.0*d*(d + 1.0)*(d - 2.0)) * inv / (d + 2.0)

    v[4] = -s * ((d - 1.0)*(16.0 + 10.0*d - 9.0*d**2 + d**3)/(2.0*d**2*(d - 2.0)) * inv**2
                 + 4.0*(d - 1.0)*(2.0*d - 5.0)/(d*(d**2 - 4.0)) * inv
                 + 4.0*(d - 1.0)*(2.0*d - 5.0)/(d*(d**2 - 4.0)) * inv**2)
    m[4, 0] = -s * ((d - 1.0)*(16.0 + 10.0*d - 9.0*d**2 + d**3)/(2.0*d**2*(d - 2.0)) * inv**2 / (d + 2.0)
                    + 4.0*(d - 1.0)*(2.0*d - 5.0)/(d*(d**2 - 4.0)) * inv**2 / (d + 4.0))
    m[4, 4] = 1.0 + s * 4.0*(d - 1.0)*(2.0*d - 5.0)/(d*(d**2 - 4.0)) * inv / (d + 4.0)

    return tuple(np.linalg.solve(m, v))


def beta_lambda_tilde(lam: float, g: float, n_s: float = 0.0, n_d: float = 0.0,
                      n_v: float = 0.0, d: float = D, improved: bool = True,
                      ghost_factor: float = 1.0) -> float:
    """Beta function of Lambda_tilde, eq. (21) of 1311.2898."""
    eta_h, eta_c, eta_s, eta_d, eta_v = eta_system(lam, g, n_s, n_d, n_v, d, improved, ghost_factor)
    inv = _inv(lam)
    pre = (4.0 * pi) ** (d / 2.0) * gamma(d / 2.0)
    term1 = d*(d + 1.0)*(d + 2.0 - eta_h)*inv - 4.0*d*(d + 2.0 - eta_c)
    term1 += 2.0*n_s*(2.0 + d - eta_s) - 2.0*n_d*SPINOR_WEIGHT*(2.0 + d - eta_d) + 2.0*n_v*(d**2 - 4.0 - d*eta_v)
    term2 = d*(5.0*d - 7.0)*(d - eta_h)*inv + 4.0*(d + 6.0)*(d - eta_c)
    term2 += -2.0*n_s*(d - eta_s) - n_d*SPINOR_WEIGHT*(d - eta_d) + 2.0*n_v*(d*(8.0 - d) - (6.0 - d)*eta_v)
    return (-2.0*lam + 8.0*pi*g*term1/(pre*d*(d + 2.0))
            - 4.0*pi*g*lam*term2/(3.0*d*pre))


def beta_g_tilde(lam: float, g: float, n_s: float = 0.0, n_d: float = 0.0,
                 n_v: float = 0.0, d: float = D, improved: bool = True,
                 ghost_factor: float = 1.0) -> float:
    """Beta function of G_tilde, eq. (22) of 1311.2898."""
    eta_h, eta_c, eta_s, eta_d, eta_v = eta_system(lam, g, n_s, n_d, n_v, d, improved, ghost_factor)
    inv = _inv(lam)
    pre = (4.0 * pi) ** (d / 2.0) * gamma(d / 2.0)
    term2 = d*(5.0*d - 7.0)*(d - eta_h)*inv + 4.0*(d + 6.0)*(d - eta_c)
    term2 += -2.0*n_s*(d - eta_s) - n_d*SPINOR_WEIGHT*(d - eta_d) + 2.0*n_v*(d*(8.0 - d) - (6.0 - d)*eta_v)
    return (d - 2.0)*g - 4.0*pi*g**2*term2/(3.0*d*pre)


def beta(lam: float, g: float, n_s: float = 0.0, n_d: float = 0.0,
         n_v: float = 0.0, d: float = D, improved: bool = True,
         ghost_factor: float = 1.0) -> tuple[float, float]:
    """Coupled (beta_Lambda_tilde, beta_G_tilde)."""
    return (beta_lambda_tilde(lam, g, n_s, n_d, n_v, d, improved, ghost_factor),
            beta_g_tilde(lam, g, n_s, n_d, n_v, d, improved, ghost_factor))


def beta_perturbative(lam: float, g: float, n_s: float = 0.0, n_d: float = 0.0,
                      n_v: float = 0.0) -> tuple[float, float]:
    """Second-order expansion of the d = 4 flow, eqs. (35)-(36) of 1311.2898.

    Used as an analytic cross-check only.
    """
    bg = 2.0*g + g**2/(6.0*pi)*(n_s + 2.0*n_d - 4.0*n_v - 46.0)
    bl = (-2.0*lam + g/(4.0*pi)*(n_s - 4.0*n_d + 2.0*n_v + 2.0)
          + g*lam/(6.0*pi)*(n_s + 2.0*n_d - 4.0*n_v - 16.0))
    return bl, bg


def perturbative_fixed_point(n_s: float = 0.0, n_d: float = 0.0,
                             n_v: float = 0.0) -> tuple[float, float]:
    """Perturbative fixed point, eqs. (37)-(38) of 1311.2898."""
    lam = -0.75*(n_s - 4.0*n_d + 2.0*n_v + 2.0)/(n_s + 2.0*n_d - 4.0*n_v - 31.0)
    g = -12.0*pi/(n_s + 2.0*n_d - 4.0*n_v - 46.0)
    return lam, g


def newton_solve(residual, seed, step: float = 1e-7, tol: float = 1e-12,
                 max_iter: int = 200):
    """Damped Newton solver for a 2-vector residual (no scipy dependency)."""
    point = np.asarray(seed, dtype=float)
    for _ in range(max_iter):
        r = np.asarray(residual(*point), dtype=float)
        if np.max(np.abs(r)) < tol:
            return point
        jac = np.empty((2, 2))
        for column in range(2):
            delta = step * max(1.0, abs(point[column]))
            upper, lower = point.copy(), point.copy()
            upper[column] += delta
            lower[column] -= delta
            jac[:, column] = (np.asarray(residual(*upper), dtype=float)
                              - np.asarray(residual(*lower), dtype=float)) / (2.0*delta)
        try:
            direction = np.linalg.solve(jac, -r)
        except np.linalg.LinAlgError:
            direction = -np.sign(r) * min(0.1, np.max(np.abs(r)))
        point = point + direction
    raise RuntimeError("Newton solver did not converge")


def fixed_point(n_s: float = 0.0, n_d: float = 0.0, n_v: float = 0.0,
                d: float = D, improved: bool = True, ghost_factor: float = 1.0,
                seed=None):
    """Non-Gaussian fixed point (Lambda_tilde*, G_tilde*) for the given matter."""
    default_seed = (-2.0, 1.7) if (n_s + n_d + n_v) > 0 else (0.0, 0.7)
    return newton_solve(lambda lam, g: beta(lam, g, n_s, n_d, n_v, d, improved, ghost_factor),
                        seed if seed is not None else default_seed)


def stability_matrix(lam: float, g: float, n_s: float = 0.0, n_d: float = 0.0,
                     n_v: float = 0.0, d: float = D, improved: bool = True,
                     ghost_factor: float = 1.0, step: float = 1e-6) -> np.ndarray:
    """Central-difference Jacobian ordered as (Lambda_tilde, G_tilde)."""
    point = np.array((lam, g), dtype=float)
    matrix = np.empty((2, 2))
    for column in range(2):
        delta = step * max(1.0, abs(point[column]))
        upper, lower = point.copy(), point.copy()
        upper[column] += delta
        lower[column] -= delta
        matrix[:, column] = (np.asarray(beta(*upper, n_s, n_d, n_v, d, improved, ghost_factor))
                             - np.asarray(beta(*lower, n_s, n_d, n_v, d, improved, ghost_factor))) / (2.0*delta)
    return matrix


def critical_exponents(lam: float, g: float, n_s: float = 0.0, n_d: float = 0.0,
                       n_v: float = 0.0, d: float = D, improved: bool = True,
                       ghost_factor: float = 1.0) -> np.ndarray:
    """Convention theta = -eig(d beta / d coupling) at the fixed point."""
    return -np.linalg.eigvals(stability_matrix(lam, g, n_s, n_d, n_v, d, improved, ghost_factor))


STANDARD_MODEL = dict(n_s=4.0, n_d=45.0/2.0, n_v=12.0)

# Ghost-factor convention used in the tables of arXiv:1311.2898
# (eta_c = 2*2^{[d/2]} * G~ * b(Lambda~) at one loop); see module docstring.
DEP_TABLE_GHOST_FACTOR = 2.0 * SPINOR_WEIGHT
