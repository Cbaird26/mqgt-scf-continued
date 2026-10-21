"""Pure-gravity Einstein-Hilbert benchmark from Litim (hep-th/0606044).

This uses the paper's rescaled `g` and alpha -> infinity convention, not the
reconstruction's `gN = G k^2`. It is a validation benchmark only.
"""
from __future__ import annotations

from math import pi
import numpy as np


def polynomials(lam: float, g: float, d: float = 4.0) -> tuple[float, float]:
    p1 = (-16*lam**3 + 4*lam**2*(4 - 10*d*g - 3*d**2*g + d**3*g)
          + 4*lam*(10*d*g + d**2*g - d**3*g - 1)
          + d*(2+d)*(d - 16*g + 8*d*g - 3)*g)
    p2 = 8*(lam**2 - lam - d*g) + 2
    return p1, p2


def beta(lam: float, g: float, d: float = 4.0) -> tuple[float, float]:
    p1, p2 = polynomials(lam, g, d)
    denominator = p2 + 4*(d+2)*g
    return p1/denominator, (d-2)*g*p2/denominator


def eta(lam: float, g: float, d: float = 4.0) -> float:
    g_bound = (1 - 2*lam)**2 / (2*(d-2))
    return (d+2)*g / (g-g_bound)


def d4_fixed_point() -> tuple[float, float]:
    # The flow equations use g/c_d. Litim's printed 3*pi/8 reinstates
    # c_4=24*pi, so the equation-level coordinate is 1/64.
    return 0.25, 1.0/64.0


def d4_fixed_point_with_restored_cd() -> tuple[float, float]:
    """The same point after reinstating c_4=24*pi, as quoted in the paper."""
    return 0.25, 3*pi/8


def stability_matrix(lam: float, g: float, step: float = 1e-6) -> np.ndarray:
    """Central-difference Jacobian ordered as (lambda, g)."""
    point = np.array((lam, g), dtype=float)
    matrix = np.empty((2, 2))
    for column in range(2):
        delta = step * max(1.0, abs(point[column]))
        upper, lower = point.copy(), point.copy()
        upper[column] += delta; lower[column] -= delta
        matrix[:, column] = (np.array(beta(*upper)) - np.array(beta(*lower))) / (2*delta)
    return matrix


def critical_exponents(lam: float, g: float) -> np.ndarray:
    """Convention theta=-eig(d beta/d coupling)."""
    return -np.linalg.eigvals(stability_matrix(lam, g))
