"""One-loop, massless two-real-scalar core in MS-bar.

Convention:
    V(phi, e) = lambda_phi/4 * phi**4 + lambda_e/4 * e**4
                + kappa/2 * phi**2 * e**2.

This is an explicitly derived perturbative subsystem, separate from the
unavailable gravity-plus-matter FRG projection.
"""
from __future__ import annotations

from math import pi
from typing import Sequence

LOOP = 16.0 * pi**2


def beta_scalar(couplings: Sequence[float]) -> tuple[float, float, float]:
    """Return (beta_lambda_phi, beta_lambda_e, beta_kappa) at one loop.

    Derived from beta_abcd=(lambda_abef lambda_efcd + permutations)/(16 pi^2)
    with lambda_1111=6 lambda_phi, lambda_2222=6 lambda_e,
    lambda_1122=2 kappa.
    """
    lambda_phi, lambda_e, kappa = map(float, couplings)
    return (
        (18.0 * lambda_phi**2 + 2.0 * kappa**2) / LOOP,
        (18.0 * lambda_e**2 + 2.0 * kappa**2) / LOOP,
        (6.0 * kappa * (lambda_phi + lambda_e) + 8.0 * kappa**2) / LOOP,
    )


def bounded_from_below(couplings: Sequence[float]) -> bool:
    """Co-positivity condition for this potential normalization."""
    lambda_phi, lambda_e, kappa = map(float, couplings)
    return lambda_phi >= 0.0 and lambda_e >= 0.0 and kappa >= -sqrt_product(lambda_phi, lambda_e)


def sqrt_product(left: float, right: float) -> float:
    return (left * right) ** 0.5


def only_real_one_loop_fixed_point(couplings: Sequence[float], tolerance: float = 1e-12) -> bool:
    """Check the proven real fixed point of the isolated one-loop scalar core.

    The first two beta functions are sums of nonnegative squares. Thus both can
    vanish over the reals only when lambda_phi=lambda_e=kappa=0.
    """
    return all(abs(value) <= tolerance for value in couplings)
