"""Litim/optimized threshold functions for the declared regulator convention.

The reconstruction baseline regulator is the optimized (Litim) form

    R_k(z) = Z_k (k^2 - z) theta(k^2 - z),   R^(0)(z) = (1 - z) theta(1 - z),

with z the relevant background Laplacian eigenvalue.  With the definitions
of Reuter and Saueressig, hep-th/0110054 eq. (2.11),

    Phi^p_n(w)    = 1/Gamma(n) int_0^inf dz z^(n-1)
                    [R^(0)(z) - z R^(0)'(z)] / [z + R^(0)(z) + w]^p,

    Phi_tilde^p_n(w) = 1/Gamma(n) int_0^inf dz z^(n-1)
                    R^(0)(z) / [z + R^(0)(z) + w]^p,

the optimized shape function yields the closed forms

    Phi^p_n(w)         = (1 + w)^(-p) / Gamma(n + 1),
    Phi_tilde^p_n(w)   = (1 + w)^(-p) / Gamma(n + 2),

valid for w > -1.  The recursion relation

    d/dw Phi^p_n(w) = -p Phi^(p+1)_n(w)

holds term by term.  No numerical coefficient in this module is guessed;
every value follows from the defining integrals above.
"""
from __future__ import annotations

from math import gamma

import numpy as np


def _numerator_times_heaviside(z):
    """R^(0)(z) - z R^(0)'(z) for the optimized shape, z >= 0."""
    return np.where(z < 1.0, 1.0, 0.0)


def _regulator_value(z):
    """R^(0)(z) for the optimized shape, z >= 0."""
    return np.where(z < 1.0, 1.0 - z, 0.0)


def Phi(n: int, p: int, w: float) -> float:
    """Closed form of Phi^p_n(w) with the optimized regulator, w > -1."""
    if p < 1:
        raise ValueError("p must be a positive integer")
    if n < 1:
        raise ValueError("n must be a positive integer")
    if w <= -1.0:
        raise ValueError(f"Threshold functions are undefined at w <= -1 (got {w})")
    return (1.0 + w) ** (-p) / gamma(n + 1)


def Phi_tilde(n: int, p: int, w: float) -> float:
    """Closed form of Phi_tilde^p_n(w) with the optimized regulator, w > -1."""
    if p < 1:
        raise ValueError("p must be a positive integer")
    if n < 1:
        raise ValueError("n must be a positive integer")
    if w <= -1.0:
        raise ValueError(f"Threshold functions are undefined at w <= -1 (got {w})")
    return (1.0 + w) ** (-p) / gamma(n + 2)


def Phi_integral(n: int, p: int, w: float, points: int = 2000) -> float:
    """Numerical evaluation of the defining integral for Phi^p_n(w).

    Provided as an independent verification of the closed form; the theta
    factor restricts the integral to z in [0, 1].
    """
    z = np.linspace(0.0, 1.0, points + 1)
    mid = 0.5 * (z[1:] + z[:-1])
    integrand = mid ** (n - 1) * _numerator_times_heaviside(mid) / (1.0 + w) ** p
    return float(np.sum(integrand * (z[1:] - z[:-1])) / gamma(n))


def Phi_tilde_integral(n: int, p: int, w: float, points: int = 2000) -> float:
    """Numerical evaluation of the defining integral for Phi_tilde^p_n(w)."""
    z = np.linspace(0.0, 1.0, points + 1)
    mid = 0.5 * (z[1:] + z[:-1])
    integrand = mid ** (n - 1) * _regulator_value(mid) / (1.0 + w) ** p
    return float(np.sum(integrand * (z[1:] - z[:-1])) / gamma(n))


def Q_n_threshold(n: int, f: str) -> float:
    """Dimensionless Litim integrals Q_n[partial_t P/P] and Q_n[partial_t P/P^2].

    With the optimized regulator, partial_t R_k = 2 k^2 theta(k^2 - z) and the
    modified propagator P = k^2 below the cutoff, so both functionals equal
    2 / Gamma(n + 1) in the dimensionless normalization used here.
    """
    if f == "dP/P":
        return 2.0 / gamma(n + 1)
    if f == "dP/P2":
        return 2.0 / gamma(n + 1)
    raise ValueError(f"Unknown functional {f!r}")


def litim_gravity_anomalous_dimension(lam: float, g_eq: float, d: float = 4.0) -> float:
    """Graviton anomalous dimension of the Litim EH flow, eq. (9) of hep-th/0606044.

    `g_eq` is the equation-level coupling (with c_d absorbed out), i.e. the
    benchmark convention; the reconstruction converts with c_4 = 24 pi.
    """
    g_bound = (1.0 - 2.0 * lam) ** 2 / (2.0 * (d - 2.0))
    return (d + 2.0) * g_eq / (g_eq - g_bound)
