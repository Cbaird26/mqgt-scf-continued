"""Exact one-loop scalar-quartic tensor flow for H + Phi_c + E.

Fields: four real Higgs components h_i, and real singlets phi and e.
Potential:
  V = lambda_H/4 (h_i h_i)^2 + lambda_phi/4 phi^4 + lambda_e/4 e^4
      + p_Hphi/4 (h_i h_i) phi^2 + p_He/4 (h_i h_i) e^2
      + p_phie/4 phi^2 e^2.

Only scalar loops are included. Gauge, Yukawa, gravity, anomalous-dimension,
and dimension-six effects remain separate required inputs.
"""
from __future__ import annotations

from itertools import product
from math import pi
from typing import Sequence

import numpy as np

LOOP = 16.0 * pi**2
H = range(4)
PHI, E = 4, 5
NAMES = ("lambdaH", "lambdaPhi", "lambdaE", "pHPhi", "pHE", "pPhiE")


def _symmetric_assign(tensor: np.ndarray, indices: tuple[int, int, int, int], value: float) -> None:
    from itertools import permutations
    for permutation in set(permutations(indices)):
        tensor[permutation] = value


def quartic_tensor(couplings: Sequence[float]) -> np.ndarray:
    """Build lambda_abcd where V=lambda_abcd field_a field_b field_c field_d/4!."""
    lambda_h, lambda_phi, lambda_e, p_hphi, p_he, p_phie = map(float, couplings)
    tensor = np.zeros((6, 6, 6, 6), dtype=float)
    for i in H:
        _symmetric_assign(tensor, (i, i, i, i), 6.0 * lambda_h)
        for j in H:
            if i != j:
                _symmetric_assign(tensor, (i, i, j, j), 2.0 * lambda_h)
        _symmetric_assign(tensor, (i, i, PHI, PHI), p_hphi)
        _symmetric_assign(tensor, (i, i, E, E), p_he)
    _symmetric_assign(tensor, (PHI, PHI, PHI, PHI), 6.0 * lambda_phi)
    _symmetric_assign(tensor, (E, E, E, E), 6.0 * lambda_e)
    _symmetric_assign(tensor, (PHI, PHI, E, E), p_phie)
    return tensor


def beta_tensor(tensor: np.ndarray) -> np.ndarray:
    """One-loop MS-bar scalar contribution, beta_abcd = sum of 3 contractions."""
    first = np.einsum("abef,efcd->abcd", tensor, tensor)
    second = np.einsum("acef,efbd->abcd", tensor, tensor)
    third = np.einsum("adef,efbc->abcd", tensor, tensor)
    return (first + second + third) / LOOP


def beta_scalar_quartics(couplings: Sequence[float]) -> tuple[float, ...]:
    beta = beta_tensor(quartic_tensor(couplings))
    return (
        beta[0, 0, 0, 0] / 6.0,
        beta[PHI, PHI, PHI, PHI] / 6.0,
        beta[E, E, E, E] / 6.0,
        beta[0, 0, PHI, PHI],
        beta[0, 0, E, E],
        beta[PHI, PHI, E, E],
    )


def potential_is_bounded_sufficiently(couplings: Sequence[float]) -> bool:
    """Conservative sufficient test: nonnegative self and portal quartics."""
    return all(value >= 0.0 for value in couplings)
