"""Constant-background scalar Hessian and Litim-regulated Wetterich trace.

This is the scalar local-potential approximation (LPA) block only. It is an
actual piece of the v0.1 FRG projection, not the full gravity-matter flow.
"""
from __future__ import annotations

from math import pi
from typing import Sequence

import numpy as np

from higgs_two_singlet_core import PHI, E, quartic_tensor


def mass_matrix(background: Sequence[float], masses: Sequence[float], quartics: Sequence[float]) -> np.ndarray:
    """Hessian of V for 4 Higgs real components, Phi_c, E.

    `masses` = (mH2, mPhi2, mE2). Quartic convention matches
    `higgs_two_singlet_core.quartic_tensor`.
    """
    field = np.asarray(background, dtype=float)
    if field.shape != (6,):
        raise ValueError("background must have six real scalar components")
    m_h, m_phi, m_e = map(float, masses)
    quadratic = np.diag((m_h, m_h, m_h, m_h, m_phi, m_e))
    lam = quartic_tensor(quartics)
    return quadratic + 0.5 * np.einsum("abcd,c,d->ab", lam, field, field)


def litim_potential_flow(background: Sequence[float], masses: Sequence[float], quartics: Sequence[float], k: float = 1.0) -> float:
    """Scalar LPA contribution to partial_t U_k in d=4 with optimized regulator.

    Formula: k^4/(32 pi^2) sum_a [1/(1+m_a^2/k^2)].
    It is valid only away from regulator poles.
    """
    eigenvalues = np.linalg.eigvalsh(mass_matrix(background, masses, quartics))
    denominators = 1.0 + eigenvalues / k**2
    if np.any(np.isclose(denominators, 0.0)):
        raise ValueError("Regulator pole encountered in scalar LPA trace")
    return float(k**4 / (32.0 * pi**2) * np.sum(1.0 / denominators))


def _second(fun, axis: int, step: float) -> float:
    zero = np.zeros(3)
    plus, minus = zero.copy(), zero.copy()
    plus[axis], minus[axis] = step, -step
    return (fun(plus) - 2.0*fun(zero) + fun(minus)) / step**2


def _fourth(fun, axis: int, step: float) -> float:
    values = []
    for factor in (-2, -1, 0, 1, 2):
        point = np.zeros(3); point[axis] = factor * step; values.append(fun(point))
    return (values[0] - 4*values[1] + 6*values[2] - 4*values[3] + values[4]) / step**4


def _mixed_second(fun, first: int, second: int, step: float) -> float:
    def second_first_at(value: float) -> float:
        points = []
        for sign in (1, 0, -1):
            point = np.zeros(3); point[first] = sign*step; point[second] = value; points.append(fun(point))
        return (points[0] - 2*points[1] + points[2]) / step**2
    return (second_first_at(step) - 2*second_first_at(0.0) + second_first_at(-step)) / step**2


def project_scalar_potential_flow(masses: Sequence[float], quartics: Sequence[float], k: float = 1.0, step: float = 2e-3) -> dict[str, float]:
    """Project the scalar LPA trace at zero field onto the scalar potential.

    Results are quantum trace contributions only; canonical scaling, anomalous
    dimensions, and all non-scalar traces must be added in the full flow.
    Coordinates are (h radial component, Phi_c, E).
    """
    def flow(point: np.ndarray) -> float:
        background = (point[0], 0.0, 0.0, 0.0, point[1], point[2])
        return litim_potential_flow(background, masses, quartics, k)
    return {
        "mH2": _second(flow, 0, step), "mPhi2": _second(flow, 1, step), "mE2": _second(flow, 2, step),
        "lambdaH": _fourth(flow, 0, step) / 6.0,
        "lambdaPhi": _fourth(flow, 1, step) / 6.0,
        "lambdaE": _fourth(flow, 2, step) / 6.0,
        "pHPhi": _mixed_second(flow, 0, 1, step),
        "pHE": _mixed_second(flow, 0, 2, step),
        "pPhiE": _mixed_second(flow, 1, 2, step),
    }
