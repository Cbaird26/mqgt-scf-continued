"""Sixth-order scalar LPA projections for the H + Phi_c + E system.

Convention (anchored to the verified quartic convention of
`higgs_two_singlet_core`): with invariants x = h^2 = sum h_i^2, y = Phi_c^2,
z = E^2, the potential is
  V = ... + lambda/4 x^2 + p/4 x y + ... + c/8 x^3, c/8 y^3, c/8 z^3,
      c/8 x^2 y, c/8 x^2 z, c/8 x y^2, c/8 x z^2, c/8 y^2 z, c/8 y z^2,
      c/8 x y z,
i.e. every monomial (x^a y^b z^c) with a+b+c = 3 carries a factor 1/8
= 1/2^(a+b+c), the same "2 per invariant factor" rule that fixes the
quartic sector (lambda/4 x^2 and p/4 x y).

The sextic tensor c_abcdef satisfies V = c_abcdef
field_a field_b field_c field_d field_e field_f / 6!, giving the entries
  c_000000 = 90 c_H6,       c_0000PhiPhi = 6 c_H4Phi2, ...
  c_001111 = 18 c_H6 (from 3 h1^4 h2^2),
  c_0011PhiPhi = 2 c_H4Phi2 (from 2 h1^2 h2^2 Phi^2),
  c_001122 = 6 c_H6 (from 6 h1^2 h2^2 h3^2),
  c_00PhiPhiEE = c_H2Phi2E2,
so the O(4) radial projections are
  c_H6 = d6 flow/dh^6 / 90,
  c_H4Phi2 = d4 d2 flow/(dh^4 dphi^2) / 6,
  c_H2Phi2E2 = d2 d2 d2 flow/(dh^2 dphi^2 de^2).

The quantum trace is the same Litim-regulated Wetterich trace as
`scalar_frg_lpa` (k^4/(32 pi^2) sum_a 1/(1 + m_a^2/k^2)), now with the
Hessian of the full sixth-order potential, so the sextic couplings feed
back through their own fourth-field-derivative contribution to the
Hessian.  Only scalar loops are included; canonical scaling, anomalous
dimensions, and all non-scalar traces are separate required inputs.
"""
from __future__ import annotations

from itertools import permutations
from math import pi
from typing import Sequence

import numpy as np

from higgs_two_singlet_core import PHI, E, quartic_tensor

SEXTIC_NAMES = (
    "c_H6", "c_Phi6", "c_E6", "c_H4Phi2", "c_H4E2",
    "c_H2Phi4", "c_H2E4", "c_Phi4E2", "c_Phi2E4", "c_H2Phi2E2",
)


def _symmetric_assign(tensor: np.ndarray, indices: tuple[int, ...], value: float) -> None:
    for permutation in set(permutations(indices)):
        tensor[permutation] = value


def sextic_tensor(couplings: Sequence[float]) -> np.ndarray:
    """Sextic tensor with V = c_abcdef field^6 / 6!."""
    c_h6, c_phi6, c_e6, c_h4phi2, c_h4e2, c_h2phi4, c_h2e4, c_phi4e2, c_phi2e4, c_h2phi2e2 = map(float, couplings)
    tensor = np.zeros((6, 6, 6, 6, 6, 6), dtype=float)
    for i in range(4):
        _symmetric_assign(tensor, (i, i, i, i, i, i), 90.0 * c_h6)
        for j in range(4):
            if i != j:
                _symmetric_assign(tensor, (i, i, i, i, j, j), 18.0 * c_h6)
                _symmetric_assign(tensor, (i, i, j, j, PHI, PHI), 2.0 * c_h4phi2)
                _symmetric_assign(tensor, (i, i, j, j, E, E), 2.0 * c_h4e2)
            for k in range(4):
                if i != j and j != k and i != k:
                    _symmetric_assign(tensor, (i, i, j, j, k, k), 6.0 * c_h6)
    _symmetric_assign(tensor, (PHI, PHI, PHI, PHI, PHI, PHI), 90.0 * c_phi6)
    _symmetric_assign(tensor, (E, E, E, E, E, E), 90.0 * c_e6)
    for i in range(4):
        _symmetric_assign(tensor, (i, i, i, i, PHI, PHI), 6.0 * c_h4phi2)
        _symmetric_assign(tensor, (i, i, i, i, E, E), 6.0 * c_h4e2)
        _symmetric_assign(tensor, (i, i, PHI, PHI, PHI, PHI), 6.0 * c_h2phi4)
        _symmetric_assign(tensor, (i, i, E, E, E, E), 6.0 * c_h2e4)
        _symmetric_assign(tensor, (i, i, PHI, PHI, E, E), c_h2phi2e2)
    _symmetric_assign(tensor, (PHI, PHI, PHI, PHI, E, E), 6.0 * c_phi4e2)
    _symmetric_assign(tensor, (PHI, PHI, E, E, E, E), 6.0 * c_phi2e4)
    return tensor


def mass_matrix_sextic(background: Sequence[float], masses: Sequence[float],
                       quartics: Sequence[float], sextics: Sequence[float]) -> np.ndarray:
    """Hessian of the sixth-order potential at a background."""
    field = np.asarray(background, dtype=float)
    if field.shape != (6,):
        raise ValueError("background must have six real scalar components")
    m_h, m_phi, m_e = map(float, masses)
    quadratic = np.diag((m_h, m_h, m_h, m_h, m_phi, m_e))
    lam = quartic_tensor(quartics)
    cee = sextic_tensor(sextics)
    return (quadratic
            + 0.5 * np.einsum("abcd,c,d->ab", lam, field, field)
            + (1.0 / 24.0) * np.einsum("abcdef,c,d,e,f->ab", cee, field, field, field, field))


def litim_potential_flow_sextic(background: Sequence[float], masses: Sequence[float],
                                quartics: Sequence[float], sextics: Sequence[float],
                                k: float = 1.0) -> float:
    """Scalar LPA contribution to partial_t U_k in d=4 with optimized regulator."""
    eigenvalues = np.linalg.eigvalsh(mass_matrix_sextic(background, masses, quartics, sextics))
    denominators = 1.0 + eigenvalues / k**2
    if np.any(np.isclose(denominators, 0.0)):
        raise ValueError("Regulator pole encountered in scalar LPA trace")
    return float(k**4 / (32.0 * pi**2) * np.sum(1.0 / denominators))


_ORDERS = {
    2: (np.array([1.0, -2.0, 1.0]), np.array([-1.0, 0.0, 1.0])),
    4: (np.array([1.0, -4.0, 6.0, -4.0, 1.0]), np.array([-2.0, -1.0, 0.0, 1.0, 2.0])),
    6: (np.array([1.0, -6.0, 15.0, -20.0, 15.0, -6.0, 1.0]), np.array([-3.0, -2.0, -1.0, 0.0, 1.0, 2.0, 3.0])),
}


def _mixed_derivative(fun, specs: Sequence[tuple[int, int]], step: float) -> float:
    """Mixed central finite difference of total order sum(orders).

    specs = ((axis, order), ...); the stencil is the product of 1D stencils.
    """
    import itertools
    stencils = []
    for axis, order in specs:
        coefficients, offsets = _ORDERS[order]
        stencils.append((axis, coefficients, offsets, order))
    total = 0.0
    for point in itertools.product(*[zip(c, o) for _, c, o, _ in stencils]):
        shift = np.zeros(3)
        weight = 1.0
        for (axis, coeff, offset, order), (c, o) in zip(stencils, point):
            shift[axis] += o * step
            weight *= c / step**order
        total += weight * fun(shift)
    return total


def project_sextic_flow(masses: Sequence[float], quartics: Sequence[float],
                        sextics: Sequence[float], k: float = 1.0,
                        step: float = 5e-2) -> dict[str, float]:
    """Project the sixth-order scalar LPA trace at zero field.

    Coordinates are (h radial component, Phi_c, E).  Results are quantum
    trace contributions only.
    """
    def flow(point: np.ndarray) -> float:
        background = (point[0], 0.0, 0.0, 0.0, point[1], point[2])
        return litim_potential_flow_sextic(background, masses, quartics, sextics, k)

    return {
        "c_H6": _mixed_derivative(flow, [(0, 6)], step) / 90.0,
        "c_Phi6": _mixed_derivative(flow, [(1, 6)], step) / 90.0,
        "c_E6": _mixed_derivative(flow, [(2, 6)], step) / 90.0,
        "c_H4Phi2": _mixed_derivative(flow, [(0, 4), (1, 2)], step) / 6.0,
        "c_H4E2": _mixed_derivative(flow, [(0, 4), (2, 2)], step) / 6.0,
        "c_H2Phi4": _mixed_derivative(flow, [(0, 2), (1, 4)], step) / 6.0,
        "c_H2E4": _mixed_derivative(flow, [(0, 2), (2, 4)], step) / 6.0,
        "c_Phi4E2": _mixed_derivative(flow, [(1, 4), (2, 2)], step) / 6.0,
        "c_Phi2E4": _mixed_derivative(flow, [(1, 2), (2, 4)], step) / 6.0,
        "c_H2Phi2E2": _mixed_derivative(flow, [(0, 2), (1, 2), (2, 2)], step),
    }
