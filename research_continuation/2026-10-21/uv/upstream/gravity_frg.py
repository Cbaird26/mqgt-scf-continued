"""Einstein-Hilbert gravity block in the reconstruction's declared convention.

Declared convention (recorded per FRG_PROJECTION_PROTOCOL_V0_1.md):

- Euclidean signature, d = 4, t = ln(k/k0).
- Linear metric split g = gbar + h; background-covariant gauge fixing;
  Faddeev-Popov ghosts retained in the supertrace.
- Regulator: optimized (Litim) shape R_k(z) = Z_k (k^2 - z) theta(k^2 - z)
  with a TYPE A tensorial structure (Reuter-Saueressig hep-th/0110054).
- Gauge limit alpha -> infinity of Litim, hep-th/0606044 eqs. (6)-(9),
  which is the analytical flow of the regulated Hessian (metric + ghosts)
  decomposed into tensor/vector/scalar modes in that gauge.
- Couplings: gN = G k^2 (dimensionless Newton coupling) and
  lambdaN = lambda_bar k^(-2) (dimensionless cosmological term).

Conversion: Litim's eq. (6) absorbs c_d = (4 pi)^(d/2-1) Gamma(d/2+2)
into g; in d = 4, c_4 = 24 pi.  The equation-level fixed point
(lambda*, g_eq*) = (1/4, 1/64) therefore becomes

    lambdaN* = 1/4,   gN* = (1/64) / c_4 = 1/(1536 pi),

in the reconstruction coordinates gN = G k^2, with eta_N* = -2 and
critical exponents 5/3 +/- i sqrt(167)/3.  This module is the
pure-gravity block; it intentionally excludes matter, R^2 and C^2
contributions.
"""
from __future__ import annotations

from math import pi

from lithium_thresholds import litim_gravity_anomalous_dimension

D = 4.0


def c_d(d: float = D) -> float:
    """The factor c_d absorbed into g in Litim hep-th/0606044."""
    from math import gamma
    return (4.0 * pi) ** (d / 2.0 - 1.0) * gamma(d / 2.0 + 2.0)


def g_eq(g_n: float) -> float:
    """Convert reconstruction gN = G k^2 to the paper's equation-level g."""
    return c_d() * g_n


def g_bound(lam: float) -> float:
    """g_bound(lambda) of Litim eq. (9); the eta_N pole locus."""
    return (1.0 - 2.0 * lam) ** 2 / (2.0 * (D - 2.0))


def eta_n(lam: float, g_n: float) -> float:
    """Anomalous dimension eta_N(lam, gN) in reconstruction coordinates."""
    return litim_gravity_anomalous_dimension(lam, g_eq(g_n), D)


def polynomials(lam: float, g_n: float) -> tuple[float, float]:
    """P1, P2 of Litim eqs. (7)-(8) in reconstruction coordinates (g -> c_d gN)."""
    g = g_eq(g_n)
    p1 = (-16*lam**3 + 4*lam**2*(4 - 10*D*g - 3*D**2*g + D**3*g)
          + 4*lam*(10*D*g + D**2*g - D**3*g - 1)
          + D*(2+D)*(D - 16*g + 8*D*g - 3)*g)
    p2 = 8*(lam**2 - lam - D*g) + 2
    return p1, p2


def beta_lambda_n(lam: float, g_n: float) -> float:
    """beta_lambdaN = d lambdaN / d t in reconstruction coordinates."""
    p1, p2 = polynomials(lam, g_n)
    return p1 / (p2 + 4*(D + 2.0)*g_eq(g_n))


def beta_g_n(lam: float, g_n: float) -> float:
    """beta_gN = d gN / d t in reconstruction coordinates.

    This equals (2 + eta_N) gN by construction (the paper's beta_g is
    (d - 2 + eta) g), so any nonzero fixed point requires eta_N* = -2.
    """
    p2 = polynomials(lam, g_n)[1]
    return (D - 2.0) * g_n * p2 / (p2 + 4*(D + 2.0)*g_eq(g_n))


def beta(lam: float, g_n: float) -> tuple[float, float]:
    """Coupled (beta_lambdaN, beta_gN)."""
    return beta_lambda_n(lam, g_n), beta_g_n(lam, g_n)


def fixed_point() -> tuple[float, float]:
    """The unique non-Gaussian fixed point (lambdaN*, gN*).

    Litim's eq. (6) absorbs c_d into g, so the equation-level coordinate
    is g_eq = c_4 * gN.  The equation-level fixed point is
    (lambda*, g_eq*) = (1/4, 1/64); converting back gives
    gN* = (1/64) / c_4 = 1/(1536 pi).
    """
    return 0.25, 1.0 / (64.0 * c_d())


def fixed_point_equation_level() -> tuple[float, float]:
    """The same point in the paper's equation-level coordinate (c_d absorbed)."""
    return 0.25, 1.0 / 64.0


def fixed_point_paper_coordinates() -> tuple[float, float]:
    """The same point with c_4 reinstated, as printed in Litim eq. (11)."""
    return 0.25, 3.0 * pi / 8.0


def stability_matrix(lam: float, g_n: float, step: float = 1e-6) -> "np.ndarray":
    """Central-difference Jacobian ordered as (lambdaN, gN)."""
    import numpy as np
    point = np.array((lam, g_n), dtype=float)
    matrix = np.empty((2, 2))
    for column in range(2):
        delta = step * max(1.0, abs(point[column]))
        upper, lower = point.copy(), point.copy()
        upper[column] += delta; lower[column] -= delta
        matrix[:, column] = (np.array(beta(*upper)) - np.array(beta(*lower))) / (2*delta)
    return matrix


def critical_exponents(lam: float, g_n: float) -> "np.ndarray":
    """Convention theta = -eig(d beta / d coupling) at the fixed point."""
    import numpy as np
    return -np.linalg.eigvals(stability_matrix(lam, g_n))
